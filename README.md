## Accompanist — a self-hosted karaoke system with AI

<div style="text-align: center">
    <img width="200px" src="./imgs/logo.png">
</div>

<div style="text-align: center">
    <img width="500px" src="./imgs/screenshot.png">
</div>


(not yet released)

## Development notes

This project uses `ruff` for formatting and linting. For VS Code, just install
the "Ruff" extension and reload the editor.

### General

```
cp .env.sample .env
docker-compose up -d --build
mkdir storage-volume
```

Install nvidia-container-runtime to use GPU inside Docker containters:

```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Frontend

```
cd frontend
nvm install 20
nvm use 20
npm install -g @vue/cli
npm install
npm run serve
```

### TODOs

#### Necessary todos

- Print traceback of errors
- Run `alembic upgrade head` at launching

#### Possible todos

- [All the "TODO"s in the code]
- Publish docker image(s) to Docker Hub
- Frontend localization
- Add Telegram bot wrapper for the backend
- Add mypy (+ CI)
