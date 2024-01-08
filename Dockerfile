FROM python:3.10

WORKDIR /home

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "__main__.py"]
