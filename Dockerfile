FROM continuumio/miniconda3

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src/main.py /app/main.py
COPY ./src /app/src

ENTRYPOINT ["python", "main.py"]