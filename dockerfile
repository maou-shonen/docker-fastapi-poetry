ARG TAG

FROM tiangolo/uvicorn-gunicorn-fastapi:$TAG

RUN wget -qO - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && ln -s $HOME/.poetry/bin/poetry /usr/sbin/ \
    && poetry config virtualenvs.create false

