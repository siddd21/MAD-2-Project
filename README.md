# MAD-2 Project (Music-App v2)

It is a multi-user app. Used for streaming music/reading lyrics. User can play, read lyrics, rate songs, create playlists. This application was developed for the MAD-2 project (Jan-2024 term).

## Requirements

- Project zip file
- Windows OS with WSL
- Python: 3.10
- Browser: Chrome/Brave/Firefox
- Terminal: WSL
- Npm or Yarn
- `redis-server` installtion

  ```bash
  # install redis
  $ sudo install redis-server
  ```

- MailHog installtion

  ```bash
  # install go
  $ sudo apt install golang-go

  # install mailhog
  $ go install github.com/mailhog/MailHog@latest
  ```

## Run Locally

Clone the project OR download the zip file

```bash
  git clone https://link-to-project
```

The project requires 6 terminals

- Terminal-1 (Backend)

  - Go to the project backend

    ```bash
    $ cd Project/backend
    ```

  - Create and activate virtual environment

    ```bash
    $ python3 -m venv .env
    $ source .env/bin/activate
    ```

  - Install dependencies

    ```bash
    $ pip install -r requirements.txt
    ```

  - Start the backend server
    ```bash
    $ python3 main.py
    ```

- Terminal-2 (Frontend)

  - Go to the project frontend

    ```bash
    $ cd Project/frontend
    ```

  - Install dependencies

    ```bash
    $ npm install
    ```

  - Start the frontend server
    ```bash
    $ npm run serve
    ```

- Terminal-3 (Redis)

  - Start the redis-server

    ```bash
    # stop if redis is already running
    $ sudo systemctl stop redis

    # start redis-server
    $ redis-server
    ```

- Terminal-4 (MailHog)

  - Start MailHog server

    ```bash
        $ ~/go/bin/MailHog
    ```

- Terminal-5 (Celery-worker)

  - Go to the project backend

    ```bash
    $ cd Project/backend
    ```

  - Start celery-worker
    ```bash
    $ celery -A main:celery_app worker -l INFO
    ```

- Terminal-6 (Celery-Beat)

  - Go to the project backend

    ```bash
    $ cd Project/backend
    ```

  - Start celery-beat
    ```bash
    $ celery -A main:celery_app beat -l INFO
    ```

Open your browser and navigate to http://localhost:8080
