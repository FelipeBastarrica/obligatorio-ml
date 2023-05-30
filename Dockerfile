FROM python:3.9.6
WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD scrapy crawl gallito -s LOG_FILE=./scrapy_gallito.log