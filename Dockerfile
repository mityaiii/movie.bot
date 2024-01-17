FROM python:3.10

WORKDIR /home

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN /home/venv/bin/pip install --upgrade pip setuptools
RUN /home/venv/bin/pip install -r requirements.txt

COPY . .

CMD ["/home/venv/bin/python", "main.py"]
