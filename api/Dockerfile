FROM python:3.12.3

WORKDIR /api

# download the words.txt file
RUN apt-get update && apt-get install wget
COPY bin .
RUN chmod +x load_words_file.sh
RUN ./load_words_file.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]