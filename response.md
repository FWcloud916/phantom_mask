# Response
  Current contest as an example. Feel free to edit/remove it.

## Required
python >= 3.10.6
poetry
PostgreSQL

Or

Docker
Docker-compose


### RUN Project
1. `cp .env.example .env` and edit environments
2. `poetry install`
3. `uvicorn main:app --reload`

Or Use Docker
`docker-compose up -d --build`


### API Document
  After service up, link to `http://localhost:8000/docs`

### Import Data Commands
#### With Python
  `python -m app.commands.import import-pharmacy-data -f 'data/pharmacies.json'`
  `python -m app.commands.import import-user-data -f 'data/users.json'`
#### With docker compose and makefile
  `make build-local` -> setup docker
  `make import-data` -> import data from ./data/*json

## Bonus
### Dockerized
  check my dockerfile [here](./Dockerfile)

