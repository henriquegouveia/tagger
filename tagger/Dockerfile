FROM python:latest

WORKDIR /usr/src/app

COPY . ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U spacy
RUN python -m spacy download nl_core_news_sm

COPY . .

EXPOSE  5000
ENTRYPOINT ["python"]

CMD ["tagger.py" ]
