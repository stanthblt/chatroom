import asyncio
import re
import uuid
from os import environ

MAX_USERS = environ.get("MAX_USERS")
MAX_USERS = int(MAX_USERS) if MAX_USERS is not None else 20

LISTENING_PORT = environ.get("CHAT_PORT")
LISTENING_PORT = int(LISTENING_PORT) if LISTENING_PORT is not None else 14447

host = '0.0.0.0'
port = LISTENING_PORT
max_users = MAX_USERS

# Structure pour gérer les clients
CLIENTS = {}

# Fonction pour générer un nouveau client
async def generateNewClient(writer, reader, username, addr, userid):
    CLIENTS[userid] = {'writer': writer, 'reader': reader, 'username': username, 'addr': addr}
    print(CLIENTS[userid])

# Fonction pour gérer l'entrée dans la salle de chat
async def joinEvent(userid):
    for id in CLIENTS:
        writer = CLIENTS[id]['writer']
        servermessage = f"{CLIENTS[userid]['username']} a rejoint la chatroom".encode("utf-8")
        writer.write(servermessage)
    return

# Fonction pour gérer la sortie de la salle de chat
async def leaveEvent(userid):
    for id in CLIENTS:
        writer = CLIENTS[id]['writer']
        if CLIENTS[id]['username'] == '':
            CLIENTS[id]['username'] = CLIENTS[userid]['writer']
        servermessage = f"{CLIENTS[id]['username']} a quitté la chatroom".encode("utf-8")
        writer.write(servermessage)
    return

# Fonction pour envoyer un message à tous les utilisateurs
async def sendAll(message, userid):
    for id in CLIENTS:
        writer = CLIENTS[id]['writer']
        if id == userid:
            servermessage = f"{CLIENTS[userid]['username']} : {message}".encode("utf-8")
        else:
            servermessage = f"Vous avez dit : {message}".encode("utf-8")
        writer.write(servermessage)
    return

# Fonction principale pour gérer les paquets entrants
async def handle_packet(reader, writer):
    if len(CLIENTS) > max_users:
        print("Too Many users in the room!")
        return

    userid = uuid.uuid4()
    addr = writer.get_extra_info('peername')

    # Gestion du pseudo
    while True:
        data = await reader.read(100)
        message = data.decode('utf-8')
        if not data:
            await asyncio.sleep(0.05)
        if re.match(r'^[a-z0-9_-]{3,15}$', message):
            await generateNewClient(writer, reader, message, addr, userid)
            await joinEvent(userid)
            break

    # Gestion des messages
    while True:
        data = await reader.read(100)
        message = data.decode('utf-8')
        if not data:
            await asyncio.sleep(0.05)
        print(f"Message received from {addr[0]!r}:{addr[1]!r} :{message!r}")
        if data == b'':  # Gestion de la déconnexion
            await leaveEvent(userid)
            writer.close()
            await writer.wait_closed()
            return
        else:
            await sendAll(message, userid)

        await writer.drain()

async def main():
    server = await asyncio.start_server(handle_packet, host, port)

    addr = server.sockets[0].getsockname()
    print(f"Serveur en écoute sur {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
