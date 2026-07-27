# 🌐 Claude Proxy

> A lightweight proxy that allows Claude Code to work with AI providers that are not officially supported.

---

## ✨ Features

- 🚀 Lightweight and fast
- 🔗 Redirect Claude Code requests
- 🤖 Compatible with multiple AI providers
- 🔓 Fully open source
- 🛡️ Safe and transparent
- ⚙️ Easy configuration
- 📦 Portable executable
- 💻 Windows support

---

# 📖 What is Claude Proxy?

Claude Proxy is a lightweight application that acts as a bridge between **Claude Code** and AI providers that are not officially supported by Claude Code.

Instead of communicating directly with Anthropic's API, Claude Code sends its requests to Claude Proxy. Claude Proxy then forwards those requests to the AI provider you have configured.

This allows Claude Code to work with many different AI providers while keeping the user experience almost identical.

The goal of this project is to make Claude Code more flexible without requiring official support for every provider.

---

# 🔒 Is Claude Proxy Safe?

**Yes.**

Claude Proxy is completely **open source**.

Every line of code used by the application is available inside this repository, meaning anyone can inspect exactly how it works.

Some antivirus programs or VirusTotal may report the executable as a **Trojan**.

This **does not necessarily mean the application is malicious**.

Applications packaged with Python, especially those that create local proxy services or intercept HTTP requests, are commonly flagged by heuristic detection engines.

These reports are often **false positives**.

Claude Proxy **does not**:

- ❌ Install malware
- ❌ Install spyware
- ❌ Create backdoors
- ❌ Mine cryptocurrency
- ❌ Collect personal information
- ❌ Upload your files
- ❌ Remotely control your computer

If you are concerned about security, we strongly encourage you to inspect the source code yourself.

The application's main logic is located in:

```text
claude_proxy.py
```

Since the project is open source, you are free to build the executable yourself.

---

# 📥 Installation

## Step 1 — Download

Go to the **Releases** page.

Download the latest version of:

```text
Claude Proxy.exe
```

Run the executable.

No installation is required.

---

## Step 2 — Configure Claude Proxy

When the application opens, complete the required fields.

Typically these include:

- 🔑 API Key
- 🌐 Provider
- 🤖 Model
- ⚙️ Custom settings (if required)

After entering the information, click:

> ▶ Run

If everything is configured correctly, the application will display that the proxy server is running.

Leave Claude Proxy running while using Claude Code.

---

# ⚙️ Configure Claude Code

Claude Code must be configured to communicate with Claude Proxy.

## Locate the configuration folder

Open **File Explorer**.

Navigate to:

```text
This PC
```

Open your Windows drive.

Usually:

```text
C:\
```

Open:

```text
Users
```

Open your Windows account folder.

Example:

```text
C:\Users\John
```

Open:

```text
.claude
```

Locate:

```text
settings.json
```

Open the file using Notepad.

---

## Replace the configuration

If you have previously configured Claude Code, remove the old configuration from:

```text
settings.json
```

If this is a fresh Claude Code installation, you usually don't need to remove anything.

Return to this repository.

At the top of the repository you'll find a section named:

```text
Config
```

Copy the entire configuration.

Paste it into:

```text
settings.json
```

Press:

```text
Ctrl + S
```

to save the file.

---

# 🚀 Launch Claude Code

Open Command Prompt.

Run:

```bash
claude
```

Claude Code will start.

Choose your preferred interface.

Press **Enter** again to continue.

---

# 🔗 Connect to Claude Proxy

During the initial setup, Claude Code may ask:

```text
Use sk-cms?
```

Select:

✅ **Yes**

Do **not** select **No**.

Claude Code will then connect to Claude Proxy.

---

# 🛠 Troubleshooting

If Claude Code doesn't work immediately:

Run:

```text
/model
```

Use the **Up** and **Down** arrow keys to select the same model configured inside Claude Proxy.

Press **Enter**.

After that, try sending:

```text
hi
```

If Claude responds normally without errors, your installation is complete.

---

# ❓ Frequently Asked Questions

## VirusTotal says Claude Proxy is a Trojan

This is usually a **false positive**.

The executable may trigger heuristic detections because it creates a local proxy service.

If you are unsure, inspect the source code and build the executable yourself.

---

## Claude Code cannot connect

Make sure:

- Claude Proxy is running.
- Your API key is correct.
- Your provider configuration is correct.
- The selected model matches the proxy configuration.
- The correct Config has been copied into `settings.json`.

---

## Claude Code returns model errors

Run:

```text
/model
```

Then choose the same model configured in Claude Proxy.

---

## Nothing happens after starting Claude

Restart Claude Code.

Restart Claude Proxy.

Verify that your firewall or antivirus is not blocking localhost connections.

---

# 📂 Project Structure

```text
.
├── claude_proxy.py
├── config/
├── releases/
├── README.md
└── LICENSE
```

---

# ❤️ Support

If you have any questions, suggestions, or need assistance, feel free to contact us.

**Telegram**

> @Nulltestfun1

---

# ⭐ Support the Project

If Claude Proxy helps you, please consider giving this repository a **Star**.

It helps more people discover the project and motivates future development.

Thank you for using Claude Proxy ❤️
