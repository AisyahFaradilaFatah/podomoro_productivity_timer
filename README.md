# Pomodoro Productivity Timer

**Fast • Simple • Offline • No API Needed**
Aplikasi terminal Pomodoro AI-Agent yang menggunakan local logic untuk instant response (< 1ms). Tidak memerlukan internet, API key, atau setup kompleks.

---

## ✨ Fitur Utama

### ⏱️ Timer Pomodoro
- Start timer dengan durasi custom (1-120 menit)
- Pause/Resume kapan saja
- Stop dan reset
- Automatic beep saat timer selesai
- **Non-blocking background thread** - UI tetap responsif

### 🤖 Local AI
- Natural language command parsing
- Random response templates untuk variety
- Instant response (< 1ms)
- Motivational quotes random
- **Tanpa API call** - semua lokal

### 📊 Session Tracking
- Tracking semua session
- Hitung total waktu & session count
- Display statistics
- Session history in-memory

### 🎨 Beautiful Terminal UI
- Colored output (GREEN/CYAN/RED)
- Emoji integration
- Progress bar visualization
- Clean formatting
- Error handling graceful

---

## 💬 Usage

### Basic Commands

```bash
# Start timer
Mulai pomodoro 25 menit
start 30
mulai 20

# Check remaining time
Berapa sisa?
time
progress

# Control timer
Pause
Resume
Stop

# View statistics
Stats
Statistik

# Get motivation
Motivasi
Motivation

# Help
Help
?

# Exit
Exit
Quit
```

### Flow Diagram

```
User Input
    ↓
assistant.parse_command()
├─ Extract command type (start, pause, stop, etc)
└─ Extract parameters (duration, etc)
    ↓
main.handle_command()
├─ Execute tool (tools.py)
└─ Get response template
    ↓
assistant.get_response()
├─ Select random template
└─ Format with parameters
    ↓
utils.print_response()
└─ Display to user (INSTANT! < 1ms)
    ↓
Loop continues...
```

## 🛠️ Customization

### Edit Response Templates

```python
# config.py - RESPONSES dictionary

RESPONSES = {
    "start": [
        "Your custom message 1 {duration}",
        "Your custom message 2 {duration}",
        "Your custom message 3"
    ],
    "check_time": [
        "Your time message {formatted}",
    ]
}
```

### Add Motivational Quotes

```python
# assistant.py - QUOTES list

QUOTES = [
    "Your custom quote 1",
    "Your custom quote 2",
    "Your custom quote 3",
]
```

### Add New Commands

```python
# assistant.py - parse_command()

elif any(word in lower_input for word in ["your_keyword"]):
    return {"type": "your_command"}

# main.py - handle_command()

elif command_type == "your_command":
    # Your custom logic here
    pass
```

---
