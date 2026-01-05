FROM python:3.12-slim

COPY app.py 1234/app.py
COPY requirements.txt 1234/requirements.txt

WORKDIR /1234

RUN pip install -r requirements.txt

EXPOSE 5008

CMD ["flask", "run", "--host=0.0.0.0", "--port=5008"]