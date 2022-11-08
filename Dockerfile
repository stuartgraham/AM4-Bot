FROM selenium/standalone-chrome

USER root
RUN apt update && apt install python3-distutils -y

RUN apt install python3-pip -y
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

RUN mkdir -p /app
WORKDIR /app
COPY main.py /app

ENTRYPOINT python3 main.py