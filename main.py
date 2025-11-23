import sys
from config import Colors
from utils import (
    clear_terminal,
    print_welcome,
    print_user_input,
    print_response,
    print_goodbye,
    print_error,
    handle_interrupt
)
from tools import start_pomodoro, get_remaining_time, stop_pomodoro, pause_pomodoro, resume_pomodoro, get_session_statistics
from assistant import create_assistant

# MAIN APPLICATION
class PomodoroApp:
    """Main application controller (No API)"""
    
    def __init__(self):
        """Inisialisasi aplikasi"""
        self.assistant = create_assistant()
        self.running = True
    
    def run(self) -> None:
        """Main application loop"""
        clear_terminal()
        print_welcome()
        
        while self.running:
            try:
                # Get user input
                user_input = print_user_input("")
                
                # Check exit command
                if user_input.lower() in ["exit", "q", "quit", "keluar"]:
                    self.running = False
                    print_goodbye()
                    break
                
                # Skip empty input
                if not user_input.strip():
                    continue
                
                # Parse command
                command_info = self.assistant.parse_command(user_input)
                command_type = command_info["type"]
                
                # Handle command
                self.handle_command(command_type, command_info)
            
            except KeyboardInterrupt:
                handle_interrupt()
            except Exception as e:
                print_error(f"Error: {str(e)}")
    
    def handle_command(self, command_type: str, command_info: dict) -> None:
        """
        Handle specific command
        Args:
            command_type (str): Type of command
            command_info (dict): Command information
        """
        if command_type == "start":
            duration = command_info.get("duration", 25)
            result = start_pomodoro(duration)
            response = self.assistant.get_response("start", duration=duration)
            print_response(response)
        
        elif command_type == "check_time":
            result = get_remaining_time()
            if result["status"] == "idle":
                print_response("⏳ Tidak ada timer yang berjalan. Ketik 'start 25' untuk mulai!")
            else:
                response = self.assistant.get_response(
                    "check_time",
                    formatted=result["formatted"],
                    percentage=result["percentage"],
                    progress_bar=result["progress_bar"]
                )
                print_response(response)
        
        elif command_type == "pause":
            result = pause_pomodoro()
            if result["status"] == "error":
                print_response(result["message"])
            else:
                response = self.assistant.get_response("pause")
                print_response(response)
        
        elif command_type == "resume":
            result = resume_pomodoro()
            if result["status"] == "error":
                print_response(result["message"])
            else:
                response = self.assistant.get_response("resume")
                print_response(response)
        
        elif command_type == "stop":
            result = stop_pomodoro()
            if result["status"] == "error":
                print_response(result["message"])
            else:
                duration = result.get("time_completed", 0)
                response = self.assistant.get_response("stop", duration=duration)
                print_response(response)
        
        elif command_type == "motivation":
            from assistant import get_motivation_quote
            quote = get_motivation_quote()
            print_response(f"{quote}")
        
        elif command_type == "stats":
            result = get_session_statistics()
            if result["status"] == "no_data":
                print_response("📊 Belum ada session. Mulai sekarang dengan 'start 25'!")
            else:
                response = self.assistant.get_response(
                    "stats",
                    total_sessions=result["total_sessions"],
                    total_minutes=result["total_minutes"],
                    total_hours=result["total_hours"]
                )
                print_response(response)
        
        elif command_type == "help":
            self.show_help()
        
        else:
            print_response("❓ Perintah tidak dikenali. Ketik 'help' untuk bantuan.")
    
    def show_help(self) -> None:
        """Show help message"""
        help_text = f"""
{Colors.CYAN}{Colors.BOLD}📖 BANTUAN - Perintah Tersedia:{Colors.RESET}

{Colors.GREEN}Mulai Timer:{Colors.RESET}
  • 'Mulai pomodoro 25' atau 'start 25' - Timer 25 menit
  • 'Mulai 30' - Timer 30 menit (sesuai kebutuhan)
  • 'Mulai' - Timer default 25 menit

{Colors.GREEN}Cek Waktu:{Colors.RESET}
  • 'Berapa sisa?' atau 'time' - Lihat sisa waktu
  • 'Progress' - Lihat progress bar

{Colors.GREEN}Kontrol Timer:{Colors.RESET}
  • 'Pause' atau 'jeda' - Jeda sebentar
  • 'Resume' atau 'lanjut' - Lanjutkan timer
  • 'Stop' atau 'henti' - Hentikan & reset

{Colors.GREEN}Info:{Colors.RESET}
  • 'Stats' atau 'statistik' - Lihat statistik
  • 'Motivasi' - Dapatkan motivasi
  • 'Help' atau '?' - Tampilkan bantuan ini
  • 'Exit' atau 'quit' - Keluar aplikasi

{Colors.YELLOW}Tips:{Colors.RESET}
  • Gunakan Pomodoro 25 menit untuk hasil optimal
  • Istirahat 5 menit setelah setiap session
  • Konsisten adalah kunci kesuksesan! 💪

{Colors.MAGENTA}Contoh session:{Colors.RESET}
  1. 'Mulai 25' → Start 25 menit timer
  2. 'Berapa sisa?' → Cek sisa waktu (berkali-kali)
  3. 'Pause' → Jeda jika perlu
  4. 'Resume' → Lanjut fokus
  5. 'Stats' → Lihat progress harian
"""
        print(help_text)
    
    def shutdown(self) -> None:
        """Cleanup dan shutdown"""
        self.running = False
        print_goodbye()

# ENTRY POINT
def main():
    """Main entry point"""
    try:
        app = PomodoroApp()
        app.run()
    except Exception as e:
        print_error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
