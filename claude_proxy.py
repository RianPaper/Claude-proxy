#Code by: Null Testfun1
import json
import sys
import threading
import time
import uuid
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import tkinter as tk
from tkinter import ttk, scrolledtext

# ---------------------------------------------------------------------------
# Hide the console window on Windows (works when double-clicking a .py file
# that was launched with python.exe instead of pythonw.exe, or when frozen
# with PyInstaller in --console mode). No effect on macOS/Linux.
# ---------------------------------------------------------------------------
if sys.platform.startswith("win"):
    try:
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Config shared between the GUI thread and the server thread
# ---------------------------------------------------------------------------
CONFIG = {
    "base_url": "",       # base url e.g. https://api.mistral.ai/v1
    "api_key": "",
    "model": "",           # model name e.g. mistral-large-latest
}
LOG_CALLBACK = None  # assigned by the GUI to print logs


def log(msg: str):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line)
    if LOG_CALLBACK:
        LOG_CALLBACK(line)


# ---------------------------------------------------------------------------
# Translate request: Anthropic messages format -> OpenAI chat/completions format
# ---------------------------------------------------------------------------
def anthropic_to_openai_request(body: dict) -> dict:
    messages = []

    system = body.get("system")
    if system:
        if isinstance(system, list):
            system_text = "\n".join(
                b.get("text", "") for b in system if isinstance(b, dict)
            )
        else:
            system_text = str(system)
        if system_text.strip():
            messages.append({"role": "system", "content": system_text})

    for m in body.get("messages", []):
        role = m.get("role", "user")
        content = m.get("content", "")
        if isinstance(content, str):
            messages.append({"role": role, "content": content})
        elif isinstance(content, list):
            # merge text blocks together; skip other block types (image, tool_use, etc.)
            text_parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
            messages.append({"role": role, "content": "\n".join(text_parts)})

    openai_body = {
        "model": CONFIG["model"] or body.get("model", ""),
        "messages": messages,
        "max_tokens": body.get("max_tokens", 1024),
        "stream": bool(body.get("stream", False)),
    }
    if "temperature" in body:
        openai_body["temperature"] = body["temperature"]
    return openai_body


# ---------------------------------------------------------------------------
# Translate response: OpenAI format -> Anthropic Messages format (non-stream)
# ---------------------------------------------------------------------------
def openai_to_anthropic_response(openai_resp: dict) -> dict:
    choice = (openai_resp.get("choices") or [{}])[0]
    message = choice.get("message", {})
    text = message.get("content", "") or ""
    usage = openai_resp.get("usage", {})

    return {
        "id": openai_resp.get("id", f"msg_{uuid.uuid4().hex[:24]}"),
        "type": "message",
        "role": "assistant",
        "model": openai_resp.get("model", CONFIG["model"]),
        "content": [{"type": "text", "text": text}],
        "stop_reason": "end_turn"
        if choice.get("finish_reason") in (None, "stop")
        else choice.get("finish_reason"),
        "stop_sequence": None,
        "usage": {
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
        },
    }


# ---------------------------------------------------------------------------
# SSE helpers for streaming
# ---------------------------------------------------------------------------
def sse_event(event_type: str, data: dict) -> bytes:
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n".encode("utf-8")


class ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # disable the noisy default http.server log, use our own log() instead

    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if not self.path.startswith("/v1/messages"):
            self._send_json(404, {"error": "not found"})
            return

        if not CONFIG["base_url"]:
            self._send_json(
                500, {"error": "Proxy is not configured with a Base URL yet. Open the GUI and enter the config."}
            )
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            anthropic_body = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid json body"})
            return

        is_stream = bool(anthropic_body.get("stream", False))
        openai_body = anthropic_to_openai_request(anthropic_body)

        target_url = CONFIG["base_url"].rstrip("/") + "/chat/completions"
        req = urllib.request.Request(
            target_url,
            data=json.dumps(openai_body).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {CONFIG['api_key']}",
            },
        )

        log(f"→ Forwarding to {target_url} (model={openai_body.get('model')}, stream={is_stream})")

        try:
            upstream = urllib.request.urlopen(req, timeout=120)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            log(f"✗ Upstream error {e.code}: {err_body[:300]}")
            self._send_json(e.code, {"error": err_body})
            return
        except urllib.error.URLError as e:
            log(f"✗ Could not connect to upstream: {e}")
            self._send_json(502, {"error": str(e)})
            return

        if not is_stream:
            data = json.loads(upstream.read().decode("utf-8"))
            anthropic_resp = openai_to_anthropic_response(data)
            log("✓ Response returned (non-stream)")
            self._send_json(200, anthropic_resp)
            return

        # ---- Streaming: read SSE from upstream (OpenAI format), re-emit as
        # ---- Anthropic SSE format ----
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        msg_id = f"msg_{uuid.uuid4().hex[:24]}"
        self.wfile.write(sse_event("message_start", {
            "type": "message_start",
            "message": {
                "id": msg_id, "type": "message", "role": "assistant",
                "model": CONFIG["model"], "content": [],
                "stop_reason": None, "stop_sequence": None,
                "usage": {"input_tokens": 0, "output_tokens": 0},
            },
        }))
        self.wfile.write(sse_event("content_block_start", {
            "type": "content_block_start", "index": 0,
            "content_block": {"type": "text", "text": ""},
        }))
        self.wfile.flush()

        try:
            for raw_line in upstream:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line or not line.startswith("data:"):
                    continue
                payload = line[len("data:"):].strip()
                if payload == "[DONE]":
                    break
                try:
                    chunk = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                delta = (chunk.get("choices") or [{}])[0].get("delta", {})
                piece = delta.get("content")
                if piece:
                    self.wfile.write(sse_event("content_block_delta", {
                        "type": "content_block_delta", "index": 0,
                        "delta": {"type": "text_delta", "text": piece},
                    }))
                    self.wfile.flush()
        except Exception as e:
            log(f"✗ Error while reading stream: {e}")

        self.wfile.write(sse_event("content_block_stop", {
            "type": "content_block_stop", "index": 0,
        }))
        self.wfile.write(sse_event("message_delta", {
            "type": "message_delta",
            "delta": {"stop_reason": "end_turn", "stop_sequence": None},
            "usage": {"output_tokens": 0},
        }))
        self.wfile.write(sse_event("message_stop", {"type": "message_stop"}))
        self.wfile.flush()
        log("✓ Response completed (stream)")


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------
class ProxyApp:
    def __init__(self, root):
        self.root = root
        root.title("Claude Code Proxy")
        root.geometry("640x480")

        frm = ttk.Frame(root, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Provider Base URL (e.g. https://api.mistral.ai/v1)").pack(anchor="w")
        self.base_url_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.base_url_var, width=70).pack(fill="x", pady=(0, 8))

        ttk.Label(frm, text="Provider API Key").pack(anchor="w")
        self.api_key_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.api_key_var, width=70, show="*").pack(fill="x", pady=(0, 8))

        ttk.Label(frm, text="Model name (e.g. mistral-large-latest)").pack(anchor="w")
        self.model_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.model_var, width=70).pack(fill="x", pady=(0, 8))

        ttk.Label(frm, text="Local port (default 5555)").pack(anchor="w")
        self.port_var = tk.StringVar(value="5555")
        ttk.Entry(frm, textvariable=self.port_var, width=20).pack(fill="x", pady=(0, 8))

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill="x", pady=8)
        self.start_btn = ttk.Button(btn_frame, text="Start Proxy", command=self.start)
        self.start_btn.pack(side="left", padx=(0, 8))
        self.stop_btn = ttk.Button(btn_frame, text="Stop Proxy", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left")

        self.status_var = tk.StringVar(value="Stopped")
        ttk.Label(frm, textvariable=self.status_var, foreground="gray").pack(anchor="w", pady=(0, 8))

        ttk.Label(frm, text="Log:").pack(anchor="w")
        self.log_box = scrolledtext.ScrolledText(frm, height=14, state="disabled")
        self.log_box.pack(fill="both", expand=True)

        self.server = None
        self.server_thread = None

        global LOG_CALLBACK
        LOG_CALLBACK = self._append_log

    def _append_log(self, line: str):
        def _do():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", line + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        self.root.after(0, _do)

    def start(self):
        base_url = self.base_url_var.get().strip()
        api_key = self.api_key_var.get().strip()
        model = self.model_var.get().strip()
        port_str = self.port_var.get().strip()

        if not base_url or not model:
            log("✗ Base URL and Model are required before starting.")
            return
        try:
            port = int(port_str)
        except ValueError:
            log("✗ Invalid port.")
            return

        CONFIG["base_url"] = base_url
        CONFIG["api_key"] = api_key
        CONFIG["model"] = model

        try:
            self.server = ThreadingHTTPServer(("localhost", port), ProxyHandler)
        except OSError as e:
            log(f"✗ Could not open port {port}: {e}")
            return

        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

        self.status_var.set(f"Running at http://localhost:{port}")
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        log(f"✓ Proxy started at http://localhost:{port} -> {base_url} (model={model})")

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        self.status_var.set("Stopped")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        log("■ Proxy stopped")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProxyApp(root)
    root.mainloop()
