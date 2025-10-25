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
    socket.setdefaulttimeout(5)

    try:
        info = a2s.info((SERVER_IP, SERVER_PORT))
        map_name = getattr(info, "map_name", "Unknown")
        server_name = getattr(info, "server_name", "Unknown")
        player_count = getattr(info, "player_count", "Unknown")
        max_players = getattr(info, "max_players", "Unknown")
        game = getattr(info, "game", "Unknown")
        version = getattr(info, "version", "Unknown")
        password_protected = getattr(info, "password_protected", False)

        # Try fetching players
        try:
            players = a2s.players((SERVER_IP, SERVER_PORT))
            if not players:
                players_list = [{"name": "Unknown", "score": 0, "duration": 0}]
            else:
                players_list = [{"name": p.name or "Unknown", "score": p.score, "duration": p.duration} for p in players]
        except Exception:
            players_list = [{"name": "Unknown", "score": 0, "duration": 0}]

        return JSONResponse(content={
            "server_name": server_name,
            "map": map_name,
            "players": player_count,
            "max_players": max_players,
            "game": game,
            "version": version,
            "password_protected": password_protected,
            "players_list": players_list
        })

    except Exception:
        # If info query fails entirely, return Unknowns
        return JSONResponse(content={
            "server_name": "Unknown",
            "map": "Unknown",
            "players": "Unknown",
            "max_players": "Unknown",
            "game": "Unknown",
            "version": "Unknown",
            "password_protected": False,
            "players_list": [{"name": "Unknown", "score": 0, "duration": 0}]
        }, status_code=504)
