"""
Konfigurasi global untuk Pomodoro Timer
"""

# Pomodoro Constants
POMODORO_DURATION = 25  # minutes
SHORT_BREAK = 5         # minutes
LONG_BREAK = 15         # minutes
SESSIONS_UNTIL_LONG_BREAK = 4

# Terminal Colors & Styling
class Colors:
    """ANSI Color codes untuk terminal"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Background colors
    BG_GREEN = '\033[102m'
    BG_BLACK = '\033[100m'

# AI Responses (Simple Rule-Based)
RESPONSES = {
    "start": [
        "✅  Pomodoro dimulai! Fokus penuh untuk {duration} menit. Kamu bisa! 💪",
        "🎯  Timer {duration} menit sudah berjalan. Mari kita fokus! 🚀",
        "⏱️  {duration} menit dimulai. Saatnya produktif! 🔥"
    ],
    
    "check_time": [
        "⏱️  Sisa: {formatted} ({percentage}%)",
        "📊  Progress: {formatted} | {progress_bar}",
        "⏳  Tinggal {formatted} lagi. Tetap fokus! 💪"
    ],
    
    "pause": [
        "⏸️  Timer di-pause. Istirahat sebentar? ☕",
        "⏸️  Paused. Ambil napas dalam... 🧘",
        "⏸️  Timer ter-pause. Santai dulu! 😌"
    ],
    
    "resume": [
        "▶️  Timer dilanjutkan. Mari fokus lagi! 🎯",
        "▶️  Ayo kita lanjut! Jangan menyerah! 💪",
        "▶️  Lanjut lagi. Semangat! 🚀"
    ],
    
    "stop": [
        "⏹️  Timer dihentikan. Selesai {duration} menit. Bagus! 👏",
        "⏹️  Timer stop. Kamu sudah produktif selama {duration} menit! 🎉",
        "⏹️  Sesi berakhir. Kamu sudah produktif! ✨"
    ],
    
    "stats": [
        "📊  Statistik Anda:\n   Total: {total_sessions} sessions\n   Waktu: {total_minutes} menit ({total_hours}j)\n   Impresif! 🔥",
        "📈  Performa Harian:\n   Sessions: {total_sessions}\n   Total: {total_minutes} menit\n   Keep it up! 💪",
        "🏆  Ringkasan:\n   {total_sessions} sesi selesai\n   {total_minutes} menit produktif\n   Excellent work! 👍"
    ],
    
    "error_no_timer": [
        "❌  Tidak ada timer yang sedang berjalan.",
        "⚠️  Timer belum dimulai.",
        "😅  Belum ada sesi aktif."
    ],
    
    "error_timer_running": [
        "⚠️  Timer masih berjalan! Gunakan 'stop' untuk menghentikan.",
        "🏃  Timer sudah jalan. Fokus! 💪",
        "⏱️  Sesi masih berlangsung."
    ]
}

# UI Messages
WELCOME_MESSAGE = f"""\n{Colors.BG_GREEN}{Colors.BOLD}{'':^60}{Colors.RESET}
{Colors.BG_GREEN}{Colors.BOLD}{'POMODORO PRODUCTIVITY TIMER':^60}{Colors.RESET}
{Colors.BG_GREEN}{Colors.BOLD}{'Local Edition (No API)':^60}{Colors.RESET}
{Colors.BG_GREEN}{Colors.BOLD}{'':^60}{Colors.RESET}"""

AVAILABLE_COMMANDS = f"""{Colors.MAGENTA}📌 Perintah yang bisa diberikan:{Colors.RESET}
  • 'Mulai pomodoro 25 menit' atau 'start 25' - Mulai timer
  • 'Berapa sisa?' atau 'time' - Cek sisa waktu
  • 'Pause' - Pause timer
  • 'Resume' - Lanjut timer
  • 'Stop' - Hentikan timer
  • 'Motivasi' - Minta motivasi
  • 'Stats' - Lihat statistik
  • 'Help' - Bantuan
  • 'Exit' - Keluar\n"""
