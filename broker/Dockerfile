FROM python:3.9-slim

COPY . ./app
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 9998/udp
EXPOSE 9999
EXPOSE 5001

CMD ["python", "broker.py"]