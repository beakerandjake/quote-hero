#! /bin/bash
set -euo pipefail

# The github repo: https://github.com/first20hours/google-10000-english
# provides a great wordlist we can use, it's the most common english words so it's likely that 
# there will be overlap with wikiquote.  
words_file_url=https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt
words_file_name=words.txt

# download the words file
wget "$words_file_url" -O "$words_file_name" || rm -f "$words_file_name"

# if the download failed, use the words file that ships with the os as a backup.
if [ ! -f "$words_file_name" ]; then
    echo "Failed to download words file! Using os words file as backup."
    ln -sf /usr/share/dict/words "$words_file_name"
fi