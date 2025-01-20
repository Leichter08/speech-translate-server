import asyncio
from typing import Any, Dict, Optional, Set

import websockets

from speech_translate.utils.audio.record import record_server_session

recording_params = {}
active_connections = set()

def set_recording_params(**params):
    global recording_params
    recording_params = params
    
async def handle_connection(websocket):
    client_address = websocket.remote_address
    print(f"Client connected from {client_address}")

    try:
        active_connections.add(websocket)

        async for message in websocket:
            if not message:
                continue
            
            # Process the received message
            # print(f"Received message: {message}")
            # You can call existing functions to process the message
            # For example, start a recording session
            # await bc.mw.rec(message)

            await record_server_session(
                lang_source=recording_params.get('lang_source'),
                lang_target=recording_params.get('lang_target'),
                engine=recording_params.get('engine'),
                model_name_tc=recording_params.get('model_name_tc'),
                device=recording_params.get('device'),
                is_tc=recording_params.get('is_tc'),
                is_tl=recording_params.get('is_tl'),
                speaker=recording_params.get('speaker'),
                websocket_input=message
            )

    except websockets.exceptions.ConnectionClosed:
        print(f"Client {client_address} disconnected")
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        active_connections.remove(websocket)
        await websocket.close()
        

async def start_websocket_server():
    async with websockets.serve(handle_connection, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(start_websocket_server())