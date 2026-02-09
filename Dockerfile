FROM python:latest

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

WORKDIR /app

COPY LICENSE /app/LICENSE
COPY data/ /app/data/
COPY src/ /app/src/
COPY static/ /app/static/
COPY templates/ /app/templates
COPY train_game.py /app/train_game.py

EXPOSE 8080

ENTRYPOINT [ "python", "train_game.py" ]
