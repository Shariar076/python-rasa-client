import asyncio

import socketio
from fastapi import Response

sio_client = socketio.AsyncClient()

@sio_client.event
async def connect():
    print('I\'m connected as', sio_client.sid)
    # join_room request: the client chooses a room
    await sio_client.emit('session_request', {'session_id': sio_client.sid})


@sio_client.event
async def session_confirm(room_id):
    """Server informs which room this client has joined"""
    print("Joined room:", room_id)


@sio_client.event
async def disconnect():
    print('I\'m disconnected')


@sio_client.event
async def bot_uttered(data):
    print('reply: ', data['text'])
    # next message
    message = input("message: ")
    if message=='exit':
        await sio_client.disconnect()
    else:
        data = {"session_id": sio_client.sid, "message": message}
        await sio_client.emit('user_uttered', data)    
    


async def main():
    await sio_client.connect(url='http://0.0.0.0:8000', socketio_path='/chatbot/socket.io')
    # await sio_client.connect(url='http://0.0.0.0:5005', socketio_path='socket.io', transports=['websocket'])

    message = "Hello" # 1st message
    data = {"session_id": sio_client.sid, "message": message}
    await sio_client.emit('user_uttered', data)

    # event = await sio_client.on("bot_uttered")
    # print(event)
    # print(f'received event: "{event[0]}" with arguments {event[1:]}')

    await sio_client.wait()



asyncio.run(main())


"""
Exception occurred while handling uri: 'ws://0.0.0.0:5005/socket.io/?transport=websocket&EIO=4&t=1698045340.2737615'
Traceback (most recent call last):
  File "/home/himel/Documents/ChatBot/venv_rasa_305/lib/python3.8/site-packages/sanic/app.py", line 782, in handle_request
    raise ServerError(
sanic.exceptions.ServerError: Invalid response type None (need HTTPResponse)

this is a known issue:
https://github.com/miguelgrinberg/python-engineio/issues/221
https://github.com/sanic-org/sanic/issues/2105
https://github.com/sanic-org/sanic/issues/2572
"""