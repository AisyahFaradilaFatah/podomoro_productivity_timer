"""
Memproses user input dan generate responses
"""

import random
from config import RESPONSES

# LOCAL ASSISTANT (Rule-Based)
class LocalAssistant:
    def __init__(self):
        """Inisialisasi assistant"""
        self.responses = RESPONSES
    
    def get_response(self, command: str, **kwargs) -> str:
        """
        Generate response berdasarkan command
        Args:
            command (str): Tipe command (start, check_time, pause, dll)
            **kwargs: Parameter untuk format string (duration, percentage, dll)
        Returns:
            str: Response message yang random dari template
        """
        if command not in self.responses:
            return self._default_response()
        
        # Get random response dari template
        response_template = random.choice(self.responses[command])
        
        # Format dengan parameter
        try:
            return response_template.format(**kwargs)
        except KeyError:
            return response_template
    
    def _default_response(self) -> str:
        """Default response jika command tidak dikenali"""
        return "Maaf, perintah tidak dimengerti. Ketik 'help' untuk bantuan."
    
    def parse_command(self, user_input: str) -> dict:
        """
        Parse user input ke command yang dimengerti
        Args:
            user_input (str): Raw input dari user
        Returns:
            dict: {type: command_type, duration: duration (jika ada)}
        """
        lower_input = user_input.lower().strip()
        
        # Start timer
        if any(word in lower_input for word in ["mulai", "start", "begin", "run", "timer"]):
            # Extract duration
            duration = self._extract_number(user_input, default=25)
            return {"type": "start", "duration": min(duration, 120), "raw": user_input}
        
        # Check time
        elif any(word in lower_input for word in ["berapa", "sisa", "time", "remaining", "progress"]):
            return {"type": "check_time", "raw": user_input}
        
        # Pause
        elif any(word in lower_input for word in ["pause", "jeda", "istirahat"]):
            return {"type": "pause", "raw": user_input}
        
        # Resume
        elif any(word in lower_input for word in ["resume", "lanjut", "continue", "go"]):
            return {"type": "resume", "raw": user_input}
        
        # Stop
        elif any(word in lower_input for word in ["stop", "henti", "berhenti", "halt"]):
            return {"type": "stop", "raw": user_input}
        
        # Motivation
        elif any(word in lower_input for word in ["motivasi", "motivation", "semangat", "inspire"]):
            return {"type": "motivation", "raw": user_input}
        
        # Statistics
        elif any(word in lower_input for word in ["stats", "statistik", "statistik", "progress", "summary"]):
            return {"type": "stats", "raw": user_input}
        
        # Help
        elif any(word in lower_input for word in ["help", "bantuan", "?"]):
            return {"type": "help", "raw": user_input}
        
        else:
            return {"type": "unknown", "raw": user_input}
    
    @staticmethod
    def _extract_number(text: str, default: int = 25) -> int:
        """
        Extract number dari text
        Args:
            text (str): Text untuk extract
            default (int): Default jika tidak ada number
        Returns:
            int: Number yang diekstract
        """
        import re
        numbers = re.findall(r'\d+', text)
        if numbers:
            return int(numbers[0])
        return default

# MOTIVATIONAL QUOTES
QUOTES = [
    "💡 Mendedikasikan fokus penuh selama 25 menit tanpa gangguan ternyata mampu menghasilkan kualitas kerja yang luar biasa dan jauh lebih baik dari yang kamu bayangkan! 🌟",
    "🎯 Kuncinya adalah mengerjakan satu tugas dalam satu waktu. Jangan biarkan konsentrasimu terpecah, curahkan seluruh energimu sekarang karena kamu pasti mampu menyelesaikannya! 💪",
    "✨ Jangan remehkan langkah kecil, karena setiap sesi yang tuntas adalah satu langkah nyata yang membawamu semakin dekat menuju pencapaian tujuan besarmu. Tetap semangat! 🚀",
    "🔥Produktivitas sejati bukanlah tindakan sekali waktu, melainkan kebiasaan yang dibangun hari demi hari. Tetaplah konsisten, karena hasil tidak akan mengkhianati usaha! 📈",
    "🌟 Mengambil jeda bukan berarti berhenti, karena istirahat yang berkualitas adalah bahan bakar vital bagi produktivitas untuk menjaga energimu tetap prima. Keseimbangan itu kuncinya! ⚖️"
]

def get_motivation_quote() -> str:
    """Dapatkan motivational quote random"""
    return random.choice(QUOTES)

# FACTORY
def create_assistant() -> LocalAssistant:
    """Create local assistant instance"""
    return LocalAssistant()
