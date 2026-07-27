# 🌐 Claude Proxy

<div align="right">

[🇻🇳 Tiếng Việt](#-claude-proxy) | [🇺🇸 English](#-claude-proxy-english) | [🇨🇳 简体中文](#-claude-proxy-中文)

</div>

---

# 🇻🇳 Claude Proxy

## 📖 Claude Proxy là gì?

Claude Proxy là một công cụ giúp **chuyển hướng (Proxy)** các yêu cầu từ **Claude Code** đến nhà cung cấp AI mà bạn đang sử dụng nhưng **Claude Code chưa hỗ trợ trực tiếp**.

Điều này cho phép bạn sử dụng nhiều nhà cung cấp AI khác nhau ngay trong Claude Code mà không cần chờ hỗ trợ chính thức.

---

## 🔒 Claude Proxy có an toàn không?

**Có.**

Toàn bộ mã nguồn của Claude Proxy đều được công khai trong repository này, vì vậy bạn hoàn toàn có thể tự kiểm tra chương trình hoạt động như thế nào.

Một số phần mềm diệt virus hoặc VirusTotal có thể cảnh báo tệp `.exe` là **Trojan**. Đây **không đồng nghĩa** với việc phần mềm chứa mã độc.

Điều này thường xảy ra với các chương trình được đóng gói bằng Python hoặc có hành vi mở kết nối mạng.

> ⚠️ Chúng tôi **không thêm bất kỳ mã độc, cửa hậu (Backdoor), phần mềm gián điệp (Spyware) hay bất kỳ phương thức nào nhằm truy cập trái phép vào máy tính của bạn.**

Nếu bạn không tin tưởng, hãy kiểm tra trực tiếp mã nguồn.

Đặc biệt là tệp:

```text
claude_proxy.py
```

Bạn có thể tự đọc toàn bộ mã nguồn để xác minh.

---

# 📥 Bước 1 - Tải Claude Proxy

Truy cập mục **Releases** của repository.

Tải phiên bản mới nhất.

Sau khi tải xong hãy mở:

```text
Claude Proxy.exe
```

---

# ⚙️ Bước 2 - Cấu hình Proxy

Sau khi mở chương trình:

✅ Nhập API Key

✅ Chọn nhà cung cấp AI

✅ Chọn Model

✅ Nhập các thông tin cần thiết

Sau đó nhấn:

▶ **Run**

Nếu chương trình hiện trạng thái Running nghĩa là Proxy đã hoạt động.

---

# 📝 Bước 3 - Cấu hình Claude Code

## 1️⃣ Mở thư mục cấu hình

Mở **File Explorer**

↓

This PC

↓

Ổ cài Windows

Thông thường là:

```text
C:\
```

↓

Mở thư mục:

```text
Users
```

↓

Mở thư mục tài khoản Windows của bạn.

Ví dụ:

```text
C:\Users\fanfan
```

↓

Mở tiếp:

```text
.claude
```

↓

Bạn sẽ thấy:

```text
settings.json
```

Mở bằng **Notepad**.

---

## 2️⃣ Chỉnh sửa settings.json

Nếu bạn đã từng dùng Claude Code trước đây:

🗑 Xóa toàn bộ nội dung cũ trong `settings.json`.

Nếu bạn vừa mới cài Claude Code bằng PowerShell hoặc CMD thì thường không cần xóa.

Quay lại repository.

Ở đầu trang sẽ có mục:

```text
Config
```

Sao chép **toàn bộ nội dung** trong Config.

Dán vào:

```text
settings.json
```

Sau đó nhấn:

```text
Ctrl + S
```

để lưu.

---

# 🚀 Bước 4 - Chạy Claude Code

Nhấn:

```text
Win + R
```

Nhập:

```text
cmd
```

Nhấn **Enter**

Sau đó nhập:

```bash
claude
```

Nhấn **Enter**

Claude Code sẽ mở.

Tiếp tục chọn giao diện bạn muốn sử dụng.

Sau đó nhấn **Enter** thêm một lần nữa để mở Claude trong thư mục hiện tại.

---

# 🔗 Bước 5 - Kết nối Proxy

Nếu Claude Code hỏi:

```text
Use sk-cms?
```

✅ Chọn dòng trên (Yes)

❌ Không chọn No

Sau khi xác nhận, Claude Code sẽ kết nối tới Claude Proxy.

---

# 🛠 Nếu chưa hoạt động

Trong Claude Code nhập:

```text
/model
```

Dùng:

⬆

⬇

để chọn đúng model mà bạn đang cấu hình trong Claude Proxy.

Nhấn:

```text
Enter
```

Sau đó thử nhập:

```text
hi
```

Nếu Claude trả lời bình thường và không báo lỗi thì bạn đã cài đặt thành công.

🎉 Chúc mừng!

---

# ❓ Câu hỏi thường gặp

## VirusTotal báo Trojan?

Đây có thể chỉ là **False Positive**.

Nếu bạn lo ngại, hãy tự kiểm tra mã nguồn trước khi sử dụng.

---

## Claude Code không kết nối được?

Kiểm tra:

- Proxy đã Running chưa.
- API Key đúng chưa.
- Model đã chọn đúng chưa.
- `settings.json` đã dán đúng Config chưa.

---

## Proxy bị lỗi?

Hãy mở lại Proxy và kiểm tra thông báo lỗi trong cửa sổ chương trình.

---

# 📞 Liên hệ

Nếu có bất kỳ thắc mắc hoặc cần hỗ trợ, vui lòng liên hệ Telegram:

**👤 @Nulltestfun1**

---

---

# 🇺🇸 Claude Proxy English

> Click **🇻🇳 Tiếng Việt** above for Vietnamese.

## What is Claude Proxy?

Claude Proxy redirects Claude Code requests to AI providers that Claude Code doesn't support natively.

It lets you use different AI providers through Claude Code without waiting for official support.

## Is it safe?

✅ Yes.

The source code is completely open-source and available in this repository.

Some antivirus software or VirusTotal may flag the executable as a Trojan because it is packaged with Python or performs network communication. This is often a **False Positive**.

You can inspect the source code yourself, especially:

```text
claude_proxy.py
```

## Quick Start

1. Download the latest version from **Releases**.
2. Open **Claude Proxy.exe**.
3. Configure your API Key, Provider and Model.
4. Click **Run**.
5. Copy the repository's **Config** into:

```text
C:\Users\<YourUser>\.claude\settings.json
```

6. Save the file.
7. Open CMD.

```bash
claude
```

8. If prompted:

```
Use sk-cms?
```

Choose **Yes**.

If necessary, run:

```text
/model
```

Select the correct model.

You're done.

---

## Contact

Telegram:

**@Nulltestfun1**

---

# 🇨🇳 Claude Proxy 中文

> 点击上方 **🇨🇳 中文** 可快速查看。

## Claude Proxy 是什么？

Claude Proxy 是一个代理工具，可以将 Claude Code 的请求转发到 Claude Code 尚未原生支持的 AI 服务提供商。

## 是否安全？

✅ 是的。

本项目完全开源，您可以查看所有源代码。

部分杀毒软件或 VirusTotal 可能会误报 Trojan（木马），这通常属于 **误报（False Positive）**。

您可以直接查看：

```text
claude_proxy.py
```

确认程序的全部实现。

## 快速开始

1. 在 **Releases** 下载最新版本。
2. 打开 **Claude Proxy.exe**。
3. 配置 API Key、Provider 和 Model。
4. 点击 **Run**。
5. 将仓库中的 **Config** 复制到：

```text
C:\Users\<用户名>\.claude\settings.json
```

6. 保存文件。
7. 打开 CMD。

```bash
claude
```

8. 如果提示：

```
Use sk-cms?
```

请选择 **Yes**。

如果需要：

```text
/model
```

选择正确的模型即可。

🎉 配置完成！

---

## 联系方式

Telegram：

**@Nulltestfun1**
