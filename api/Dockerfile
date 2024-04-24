# download or create the words.txt file as a build layer.
FROM alpine:3.14 as get_words
WORKDIR /words
RUN apk add --no-cache wget bash
COPY bin .
RUN chmod +x load_words_file.sh
RUN ./load_words_file.sh

# main layer runs the api
FROM python:3.12.3
WORKDIR /api

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=get_words /words/words.txt data/
COPY src src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--root-path", "/api"]