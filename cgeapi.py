import socket
import a2s
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVER_IP = "169.150.249.133"
SERVER_PORT = 22913

@app.get("/serverinfo")
def get_server_info():
    try:
        socket.setdefaulttimeout(3)  # Prevent long hangs (3 seconds max)
        info = a2s.info((SERVER_IP, SERVER_PORT))

        # ✅ Fix #2 — Check for password protection before querying players
        if getattr(info, "password_protected", False):
            return JSONResponse(content={
                "server_name": info.server_name,
                "map": info.map_name,
                "players": info.player_count,
                "max_players": info.max_players,
                "game_folder": info.folder,
                "game": info.game,
                "version": info.version,
                "password_protected": True,
                "players_list": "Hidden (server is password protected)"
            })

        # If not password protected, continue to get player info
        players = a2s.players((SERVER_IP, SERVER_PORT))

        return JSONResponse(content={
            "server_name": info.server_name,
            "map": info.map_name,
            "players": info.player_count,
            "max_players": info.max_players,
            "game_folder": info.folder,
            "game": info.game,
            "version": info.version,
            "password_protected": False,
            "players_list": [{"name": p.name, "score": p.score, "duration": p.duration} for p in players]
        })

    except (socket.timeout, TimeoutError):
        # Handle servers that don't respond (password protected or offline)
        return JSONResponse(content={
            "error": "Server did not respond. It may be password protected or offline."
        }, status_code=504)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
