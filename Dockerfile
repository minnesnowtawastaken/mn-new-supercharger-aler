FROM python:3.9

WORKDIR /src

RUN apt-get -y update
RUN apt-get -y install git

RUN git clone https://github.com/minnesnowtawastaken/mn-new-supercharger-alert.git

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r mn-new-supercharger-alert/requirements.txt

WORKDIR /src/mn-new-supercharger-alert

CMD ["python", "main.py"]
