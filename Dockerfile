FROM python:3.11
WORKDIR /AnimalsBotDiscord
COPY requirements.txt /AnimalsBotDiscord/
RUN pip install -r requirements.txt
COPY . /AnimalsBotDiscord
CMD python main.py