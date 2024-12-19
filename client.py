import asyncio
import re
import sys

host = 'localhost'  
port = 14447

async def receive(reader, writer):
    while True:
        data = await reader.read(1024)
        if data:
            print(data.decode())
        else:
            await asyncio.sleep(0.05)

async def clientinput(reader, writer):
    while True:
        # Utilisation de run_in_executor pour faire de l'input non-bloquant
        clientmessage = await asyncio.get_event_loop().run_in_executor(None, input, "Que veux-tu envoyer au serveur ? ")
        msg = clientmessage.encode("utf-8")
        writer.write(msg)
        await writer.drain()

async def main():
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except socket.error as msg:
        print(f"Erreur de connexion avec le serveur : {msg}")
        sys.exit(1)

    print(f"Connecté avec succès au serveur {host} sur le port {port}")

    # Demande du pseudo de l'utilisateur
    while True:
        print("Veuillez choisir un pseudo:")
        username = input()
        if re.match(r'^[a-z0-9_-]{3,15}$', username):
            break
        else:
            print("Pseudo invalide, veuillez choisir un pseudo de 3 à 15 caractères") 

    msg = username.encode("utf-8")
    writer.write(msg)
    await writer.drain()

    # Démarrage des deux tâches : recevoir et envoyer des messages
    tasks = [receive(reader, writer), clientinput(reader, writer)]
    await asyncio.gather(*tasks)

asyncio.run(main())
