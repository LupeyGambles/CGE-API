# cgeapi.py
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import valve.source.a2s

app = FastAPI()

# Enable CORS so GitHub Pages can fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your site if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVER_IP = "169.150.249.133"
SERVER_PORT = 22913

@app.get("/serverinfo")
def get_server_info():
    try:
        with valve.source.a2s.ServerQuerier((SERVER_IP, SERVER_PORT)) as server:
            info = server.info()
            players = server.players()

            server_data = {
                "server_name": info.values.get('server_name'),
                "map": info.values.get('map'),
                "players": info.values.get('player_count'),
                "max_players": info.values.get('max_players'),
                "game_folder": info.values.get('folder'),
                "game": info.values.get('game'),
                "version": info.values.get('version'),
                "players_list": []
            }

            if players.values['player_count'] > 0:
                for p in players.values['players']:
                    server_data["players_list"].append({
                        "name": p['name'],
                        "score": p['score'],
                        "duration": p['duration']
                    })

            return JSONResponse(content=server_data)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
