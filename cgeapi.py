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
    socket.setdefaulttimeout(5)  # Give server more time for slow maps

    try:
        info = a2s.info((SERVER_IP, SERVER_PORT))

        # If map info is missing, return "unknown"
        map_name = getattr(info, "map_name", "unknown")

        # Handle password-protected servers
        if getattr(info, "password_protected", False):
            return JSONResponse(content={
                "server_name": getattr(info, "server_name", "cge7-193?"),
                "map": map_name,
                "players": getattr(info, "player_count", 0),
                "max_players": getattr(info, "max_players", 0),
                "game": getattr(info, "game", "unknown"),
                "version": getattr(info, "version", "unknown"),
                "password_protected": True,
                "players_list": "Hidden (server is password protected)"
            })

        # Query players safely
        try:
            players = a2s.players((SERVER_IP, SERVER_PORT))
            players_list = [{"name": p.name, "score": p.score, "duration": p.duration} for p in players]
        except (socket.timeout, TimeoutError, a2s.BrokenMessageError):
            # If player query fails, return empty list instead of breaking
            players_list = []

        return JSONResponse(content={
            "server_name": getattr(info, "server_name", "cge7-193?"),
            "map": map_name,
            "players": getattr(info, "player_count", 0),
            "max_players": getattr(info, "max_players", 0),
            "game": getattr(info, "game", "unknown"),
            "version": getattr(info, "version", "unknown"),
            "password_protected": False,
            "players_list": players_list
        })

    except (socket.timeout, TimeoutError, a2s.BrokenMessageError):
        # If server fails completely, return default unknowns
        return JSONResponse(content={
            "server_name": "cge7-193?",
            "map": "unknown",
            "players": 0,
            "max_players": 0,
            "game": "unknown",
            "version": "unknown",
            "password_protected": False,
            "players_list": []
        }, status_code=504)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
