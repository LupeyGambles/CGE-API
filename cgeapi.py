import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import a2s

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVER_IP = "169.150.249.133"
SERVER_PORT = 22912

@app.get("/serverinfo")
def get_server_info():
    try:
        info = a2s.info((SERVER_IP, SERVER_PORT))
        players = a2s.players((SERVER_IP, SERVER_PORT))

        server_data = {
            "server_name": info.server_name,
            "map": info.map_name,
            "players": info.player_count,
            "max_players": info.max_players,
            "game_folder": info.folder,
            "game": info.game,
            "version": info.version,
            "players_list": [{"name": p.name, "score": p.score, "duration": p.duration} for p in players]
        }
        return JSONResponse(content=server_data)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
