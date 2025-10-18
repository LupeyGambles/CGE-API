# cgeapi.py

import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from steam import source
import asyncio

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

# Helper function to query server (blocking call wrapped for asyncio)
def query_server(ip, port):
    try:
        server = source.a2s.ServerQuerier((ip, port))
        info = server.get_info()
        players = server.get_players()
        server.close()

        server_data = {
            "server_name": info.get('server_name'),
            "map": info.get('map'),
            "players": info.get('player_count'),
            "max_players": info.get('max_players'),
            "game_folder": info.get('folder'),
            "game": info.get('game'),
            "version": info.get('version'),
            "players_list": []
        }

        for p in players.get('players', []):
            server_data["players_list"].append({
                "name": p['name'],
                "score": p['score'],
                "duration": p['duration']
            })

        return server_data
    except Exception as e:
        return {"error": str(e)}

@app.get("/serverinfo")
async def get_server_info():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, query_server, SERVER_IP, SERVER_PORT)
    return JSONResponse(content=result)
