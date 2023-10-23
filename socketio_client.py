import asyncio

import socketio
from fastapi import Response

sio_client = socketio.AsyncClient()


@sio_client.event
async def connect():
    print('I\'m connected as', sio_client.sid)
    await sio_client.emit('session_request', {'session_id': sio_client.sid})


@sio_client.event
async def session_confirm(room_id):
    print("Joined room:", room_id)


@sio_client.event
async def bot_uttered(data):
    print('reply: ', data['text'])
    # next message
    message = input("message: ")
    data = {"session_id": sio_client.sid, "message": message}
    await sio_client.emit('user_uttered', data)


@sio_client.event
async def disconnect():
    print('I\'m disconnected')


async def main():
    # await sio_client.connect(url='http://0.0.0.0:8000', socketio_path='/chatbot/socket.io')
    await sio_client.connect(url='http://0.0.0.0:5005', socketio_path='socket.io')

    # await sio_client.send('chat', {'message': "message"})
    # await sio_client.emit('chat', data)

    # event = await bot_uttered(data)
    # print(f'received event: "{event[0]}" with arguments {event[1:]}')
    message = "Hello" # 1st message
    data = {"session_id": sio_client.sid, "message": message}
    await sio_client.emit('user_uttered', data)
    # event = await sio_client.on("bot_uttered")
    # print(event)
    await sio_client.wait()
    # event = await sio_client.event("bot_uttered")
    # print(f'received event: "{event[0]}" with arguments {event[1:]}')

    await sio_client.disconnect()


asyncio.run(main())
