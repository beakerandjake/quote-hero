FROM python:3.12.3

WORKDIR /api

# Create the words.txt file
RUN apt-get update && apt-get install wget
COPY load_words_file.sh .
RUN chmod +x load_words_file.sh
RUN ./load_words_file.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY random_word.py .

CMD [ "python", "random_word.py" ]