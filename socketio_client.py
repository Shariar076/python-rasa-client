import asyncio

import socketio

sio_client = socketio.AsyncClient()
token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJWVjhKZ25mOFBWeVM1S05qSXdSLXB3T19LbTNnZ0wtUzM4dGg1ZkFUa3ZNIn0.eyJleHAiOjE2OTg1ODY0MzIsImlhdCI6MTY5ODU4NjEzMiwiYXV0aF90aW1lIjoxNjk4NTg1ODEzLCJqdGkiOiI1ODY0MDI4NC01MmQ0LTRkN2MtYjk0MC0xN2Y3NjkzMmQ1YWYiLCJpc3MiOiJodHRwczovL2FpLmNlbGxvc2NvcGUubmV0L2tleWNsb2FrL3JlYWxtcy9jZWxsb3Njb3BlX2FpIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjI5YmY1ZWZjLTUwY2YtNGE4Ni1iZDFjLTRmODBlOGU5Y2E4MyIsInR5cCI6IkJlYXJlciIsImF6cCI6IndlYmpzX2NsaWVudCIsIm5vbmNlIjoiN2JlMzI3MzktNmVlYy00NDBkLTkzMmQtMmY2NmI5YjdkN2Y5Iiwic2Vzc2lvbl9zdGF0ZSI6IjJiMzIwNzY3LTAwMTMtNDJmNi05Yjc5LTExM2NlNTMwMGY4YiIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9haS5jZWxsb3Njb3BlLm5ldCIsImh0dHA6Ly9sb2NhbGhvc3Q6MzAwMCJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1jZWxsb3Njb3BlX2FpIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiIyYjMyMDc2Ny0wMDEzLTQyZjYtOWI3OS0xMTNjZTUzMDBmOGIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IlNoYXJpYXIgS2FiaXIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzaGFyaWFyLmthYmlyQGNlbGxvc2NvLnBlIiwiZ2l2ZW5fbmFtZSI6IlNoYXJpYXIiLCJtb2JpbGVfbnVtYmVyIjoiMDE4MzIwNTU2NTYiLCJmYW1pbHlfbmFtZSI6IkthYmlyIiwiZW1haWwiOiJzaGFyaWFyLmthYmlyQGNlbGxvc2NvLnBlIn0.pbRdcwkK_FjXHefW7hOLt-AZpw3yG_nBzhkD1ww8ucxBpL6BEXwmyuYrdkorF8pCSxLl_dP7x1JfhmBtUX1H57IVBQScTWL3-y21nhPY4hY5VxhEJpBJCjxARbNvkYmw0uMohjF4lg_XHbgkIenhFr-rm4p-zZ_AxNnmUHKj06XPQEzsruepwX5zt5L00EzuKwZI3wLIepsiB_cSemuDKcArJAHPxFgSA2o8lCTIaqx34QZMxbbilK1Ltx0bXjcUmdWlNdR5kdRB15XNHjRH7tNYFU7R9RRHyZGMKYQcNQGOT1eBqZH5bVtEGWv4aN4v_XR5b1fIFTKFnEDzQW1frg'
room = '01832055656'
@sio_client.event
async def connect():
    print('I\'m connected as', sio_client.sid)
    # join_room request: the client chooses a room
    await sio_client.emit('session_request', {'session_id': sio_client.sid})


@sio_client.event
async def session_confirm(room_id):
    """Server informs which room this client has joined"""
    print("Joined room:", room_id)
    # assert room==room_id


@sio_client.event
async def disconnect():
    print('I\'m disconnected')


@sio_client.event
async def bot_uttered(data):
    print('reply: ', data)
    # next message
    message = input("message: ")
    if message=='exit':
        await sio_client.disconnect()
    else:
        # data = {"session_id": sio_client.sid, "message": message}
        data = {"session_id": room, "message": message}
        await sio_client.emit('user_uttered', data)    
    


async def main():
    await sio_client.connect(url='https://ai.celloscope.net', socketio_path='/chatbot/socket.io', auth={'token': token})
    # await sio_client.connect(url='http://172.16.6.3:5005', socketio_path='socket.io', transports=['websocket'])
    message = "কারেন্ট একাউন্ট ব্যালেন্স" # 1st message
    data = {"session_id": room, "message": message}
    await sio_client.emit('user_uttered', data)

    # event = await sio_client.on("bot_uttered")
    # print(event)
    # print(f'received event: "{event[0]}" with arguments {event[1:]}')

    await sio_client.wait()



asyncio.run(main())


"""
NGINX proxy:
location /chatbot/socket.io/ {
                # rewrite ^/chatbot/(.*)$ /$1 break;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_pass http://172.16.6.105:8000;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection $connection_upgrade;
}

                
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
