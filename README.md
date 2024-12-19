# Chatroom avec Docker

## Construction avec le Dockerfile :

**Exécutez la commande suivante dans le répertoire où se trouve le Dockerfile :**

```bash
docker build . -t chatroom
```

## Pour démarrer le conteneur, pensez à exposer les ports en utilisant la commande suivante :

```bash
docker run -p 14447:14447 chatroom
```

## Pour spécifier vos propres ports, utilisez cette commande :

```bash
docker run -e CHAT_PORT=14447 -p 14447:14447 chatroom
```

---

# Utilisation de Docker Compose

**Exécutez la commande suivante dans le répertoire contenant le fichier `docker-compose.yml` :**

```bash
docker compose up
```