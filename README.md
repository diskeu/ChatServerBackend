# ChatServerBackend

A lightweight Python chat server backend built for real server deployment. Based on the custom HTTP server framework from [Chat_Server](https://github.com/diskeu/Chat_Server) and extended with MySQL persistence and structured logging for production use.

## Features

- Custom Python HTTP server (no heavy frameworks)
- MySQL-backed message and user storage
- CSV-based request/access logging
- Environment-driven configuration via `.env`
- Designed to run on a real Linux server (e.g. via `systemd` or `screen`)

## Requirements

- Python 3.10+
- MySQL / MariaDB server running and accessible
- Python packages (install via pip):

```
pip install -r requirements.txt
```

> If there is no `requirements.txt` yet, you will need at minimum: `mysql-connector-python` and `python-dotenv`.

## Project Structure

```
ChatServerBackend/
├── src/                        # Server source code
├── Configurations/
│   └── mysql.conf              # MySQL connection config (not committed)
├── Logs/
│   └── base_log.csv            # Access / base log file (not committed)
├── .env                        # Environment variable file (not committed)
├── .gitignore
└── README.md
```

## Configuration

Three files must be created manually before running the server. They are excluded from version control via `.gitignore`.

### 1. `Configurations/mysql.conf`

Create the directory and file:

```bash
mkdir -p Configurations
```

```ini
[DEFAULT]
host = localhost
port = 3306

[root]
user = your_mysql_username
password = your_mysql_password
```

Replace `your_mysql_username` and `your_mysql_password` with your actual MySQL credentials.

### 2. `Logs/base_log.csv`

Create the log directory and an empty log file:

```bash
mkdir -p Logs
touch Logs/base_log.csv
```

### 3. `.env`

Create a `.env` file in the project root:

```env
MYSQL_CONFIG_FILE=./Configurations/mysql.conf
MYSQL_USER_NAME=root
BASE_LOGFILE=Logs/base_log.csv
```

Adjust `MYSQL_USER_NAME` to match the section name in your `mysql.conf` if you use a different database user.

## Running the Server

From the project root:

```bash
python src/main.py
```

> The exact entry point filename may vary — check the `src/` directory for the main server file.

### Running persistently with `screen`

```bash
screen -S chatserver
python src/main.py
# Detach with Ctrl+A, then D
```

## Security Notes

- Restrict MySQL user permissions to only the database this server needs.
- If exposing the server to the internet, consider placing it behind a reverse proxy (nginx or Caddy) and using TLS.

## Related Projects

- [Chat_Server](https://github.com/diskeu/Chat_Server) — Original chat server prototype with custom HTTP framework
- [Media-System](https://github.com/diskeu/Media-System) — Media handling component used in this backend
