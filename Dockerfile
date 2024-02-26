FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt
RUN pip install --upgrade pip

COPY . /code/

CMD ["python", "main.py"]