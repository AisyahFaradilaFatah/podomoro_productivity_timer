"""
Custom tools/functions untuk Pomodoro Timer
Backend logic untuk timer management
"""

import threading
import time
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Any

# Global Timer State
timer_state = {
    "active": False,
    "start_time": None,
    "duration": 0,
    "paused_time": None,
    "total_paused": 0,
    "sessions_completed": 0,
    "total_focus_time": 0,  # dalam detik
}

session_history = []

# POMODORO TOOLS
def start_pomodoro(duration_minutes: int) -> Dict[str, Any]:
    """
    Mulai Pomodoro timer dengan durasi tertentu
    Args:
        duration_minutes (int): Durasi dalam menit (default: 25)
    Returns:
        Dict dengan status dan metadata
    """
    if timer_state["active"]:
        remaining = get_remaining_time()["remaining"]
        return {
            "status": "error",
            "message": f"⚠️ Timer sudah berjalan! Sisa: {remaining} detik"
        }
    
    timer_state["active"] = True
    timer_state["start_time"] = datetime.now()
    timer_state["duration"] = duration_minutes * 60
    timer_state["total_paused"] = 0
    
    # Start background thread untuk countdown
    threading.Thread(target=_timer_countdown, daemon=True).start()
    
    return {
        "status": "success",
        "message": f"✅ Pomodoro dimulai! Durasi: {duration_minutes} menit",
        "start_time": timer_state["start_time"].isoformat(),
        "duration_seconds": timer_state["duration"]
    }

def get_remaining_time() -> Dict[str, Any]:
    """
    Dapatkan sisa waktu timer yang sedang berjalan
    Returns:
        Dict dengan status, remaining time, dan progress bar
    """
    if not timer_state["active"]:
        return {
            "status": "idle",
            "message": "⏳ Tidak ada timer yang berjalan",
            "remaining": 0
        }
    
    elapsed = (datetime.now() - timer_state["start_time"]).total_seconds() - timer_state["total_paused"]
    remaining = timer_state["duration"] - elapsed
    
    if remaining <= 0:
        timer_state["active"] = False
        return {
            "status": "completed",
            "message": "🎉 Timer selesai! Waktu untuk istirahat!",
            "remaining": 0
        }
    
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    percentage = int((elapsed / timer_state["duration"]) * 100)
    
    # Generate progress bar
    bar_length = 20
    filled = int(bar_length * percentage / 100)
    progress_bar = "█" * filled + "░" * (bar_length - filled)
    
    return {
        "status": "running",
        "remaining": int(remaining),
        "formatted": f"{minutes:02d}:{seconds:02d}",
        "percentage": percentage,
        "progress_bar": f"[{progress_bar}] {percentage}%",
        "message": f"⏱️ Sisa: {minutes:02d}:{seconds:02d}"
    }

def stop_pomodoro() -> Dict[str, Any]:
    """
    Hentikan dan reset timer
    Returns:
        Dict dengan status dan waktu yang sudah dikerjakan
    """
    if not timer_state["active"]:
        return {
            "status": "error",
            "message": "❌ Tidak ada timer yang sedang berjalan"
        }
    
    elapsed = (datetime.now() - timer_state["start_time"]).total_seconds() - timer_state["total_paused"]
    minutes_completed = int(elapsed // 60)
    
    timer_state["active"] = False
    timer_state["start_time"] = None
    timer_state["duration"] = 0
    
    # Save to history
    session_history.append({
        "timestamp": datetime.now().isoformat(),
        "duration_requested": timer_state["duration"] // 60,
        "duration_completed": minutes_completed,
        "status": "stopped"
    })
    
    return {
        "status": "stopped",
        "message": f"⏹️ Timer dihentikan. Selesai {minutes_completed} menit.",
        "time_completed": minutes_completed
    }

def pause_pomodoro() -> Dict[str, Any]:
    """
    Pause timer yang sedang berjalan
    Returns:
        Dict dengan status dan remaining time
    """
    if not timer_state["active"]:
        return {
            "status": "error",
            "message": "❌ Tidak ada timer yang sedang berjalan"
        }
    
    if timer_state["paused_time"] is not None:
        return {
            "status": "error",
            "message": "⏸️ Timer sudah di-pause. Gunakan 'resume' untuk melanjutkan."
        }
    
    timer_state["paused_time"] = datetime.now()
    return {
        "status": "paused",
        "message": "⏸️ Timer di-pause",
        "remaining": get_remaining_time()["remaining"]
    }

def resume_pomodoro() -> Dict[str, Any]:
    """
    Resume timer yang di-pause
    Returns:
        Dict dengan status dan remaining time
    """
    if not timer_state["active"]:
        return {
            "status": "error",
            "message": "❌ Tidak ada timer yang sedang berjalan"
        }
    
    if timer_state["paused_time"] is None:
        return {
            "status": "error",
            "message": "❌ Timer tidak sedang di-pause"
        }
    
    pause_duration = (datetime.now() - timer_state["paused_time"]).total_seconds()
    timer_state["total_paused"] += pause_duration
    timer_state["paused_time"] = None
    
    return {
        "status": "resumed",
        "message": "▶️ Timer dilanjutkan",
        "remaining": get_remaining_time()["remaining"]
    }

def get_session_statistics() -> Dict[str, Any]:
    """
    Dapatkan statistik session history
    Returns:
        Dict dengan statistics
    """
    if not session_history:
        return {
            "status": "no_data",
            "message": "📊 Belum ada session yang tercatat"
        }
    
    total_completed = sum(s["duration_completed"] for s in session_history)
    total_sessions = len(session_history)
    
    return {
        "status": "success",
        "total_sessions": total_sessions,
        "total_minutes": total_completed,
        "total_hours": round(total_completed / 60, 2),
        "message": f"📊 Total: {total_sessions} sessions, {total_completed} menit ({round(total_completed / 60, 2)} jam)",
        "history": session_history
    }

# BACKGROUND UTILITIES
def _timer_countdown():
    """
    Background thread untuk countdown dan notifikasi
    Berjalan di thread terpisah agar tidak blocking
    """
    while timer_state["active"]:
        time.sleep(0.5)
        remaining = get_remaining_time()["remaining"]
        
        if remaining <= 0:
            timer_state["active"] = False
            _beep_notification()
            timer_state["sessions_completed"] += 1
            break
        
        # Beep di 5 detik terakhir
        if 0 < remaining <= 5:
            _beep_notification()

def _beep_notification():
    """
    Terminal bell notification (beep)
    """
    sys.stdout.write('\a')
    sys.stdout.flush()

# TOOL DEFINITION
def get_tool_definitions() -> list:
    """
    Definisikan tools dalam format OpenAI
    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "start_pomodoro",
            "description": "Mulai Pomodoro timer dengan durasi tertentu (dalam menit). Default 25 menit untuk fokus, 5 menit untuk istirahat.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Durasi Pomodoro dalam menit (default: 25)"
                    }
                },
                "required": ["duration_minutes"]
            }
        },
        {
            "name": "get_remaining_time",
            "description": "Cek sisa waktu pada Pomodoro yang sedang berjalan dengan progress bar",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "stop_pomodoro",
            "description": "Hentikan Pomodoro timer dan reset",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "pause_pomodoro",
            "description": "Pause Pomodoro timer sementara",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "resume_pomodoro",
            "description": "Resume Pomodoro timer yang di-pause",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_session_statistics",
            "description": "Dapatkan statistik semua session yang sudah dikerjakan",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        }
    ]

def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> str:
    """
    Execute tool call dan return JSON result
    Args:
        tool_name (str): Nama tool yang dipanggil
        tool_input (Dict): Parameter tool
    
    Returns:
        JSON string dengan hasil tool
    """
    tool_mapping = {
        "start_pomodoro": start_pomodoro,
        "get_remaining_time": get_remaining_time,
        "stop_pomodoro": stop_pomodoro,
        "pause_pomodoro": pause_pomodoro,
        "resume_pomodoro": resume_pomodoro,
        "get_session_statistics": get_session_statistics,
    }
    
    if tool_name not in tool_mapping:
        return json.dumps({"error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)
    
    try:
        result = tool_mapping[tool_name](**tool_input)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
