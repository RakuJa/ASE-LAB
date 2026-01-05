FROM python:3.12-slim
WORKDIR /src
ENV FLASK_APP=src/app.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run", "--host=0.0.0.0"]