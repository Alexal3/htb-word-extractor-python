import click
import requests
import re
import os.path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_html_of(url):
    resp = requests.get(url)

    if resp.status_code != 200:
        print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)

    return resp.content.decode()

def count_occurrences_in(word_list, min_length):
    word_count = {}

    for word in word_list:
        if len(word) < min_length:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            current_count = word_count.get(word)
            word_count[word] = current_count + 1
    return word_count

def get_all_words_from(start_url, max_depth):
    visited = set()
    queue = [(start_url, 0)]
    raw_text = ''

    while queue:
        url, depth = queue.pop(0)
 
        if (url not in visited) and (depth <= max_depth) and (urlparse(start_url).netloc == urlparse(url).netloc):
            html = get_html_of(url)
            visited.add(url)
            soup = BeautifulSoup(html, 'html.parser')
            raw_text = raw_text + '\n' + soup.get_text()

            if depth < max_depth:
                for link in soup.find_all('a', href=True):
                    absolute_link = urljoin(url, link['href'])
                    if absolute_link not in visited:
                        queue.append((absolute_link, depth + 1))

    return re.findall(r'\w+', raw_text)

def get_top_10_words_from(all_words, min_length):
    for word in all_words:
        word = word.lower()

    occurrences = count_occurrences_in(all_words, min_length)
    sorted_top_words = sorted(occurrences.items(), key=lambda item: item[1], reverse=True)
    return sorted_top_words[:10]

def generate_passwords_from_words(words):
    passwords = []
    symbols = ['!', '@', '#', '$', '%', '&', '*', '(', ')', '_', '+', '-', '=', '?']

    for word in words:
        passwords.append(word[0].lower())
        passwords.append(word[0].capitalize())
        passwords.append(word[0].upper())

    for word in words:
        for number in range(0, 2101):
            passwords.append(word[0].lower() + str(number))
            passwords.append(word[0].capitalize() + str(number))
            passwords.append(word[0].upper() + str(number))

    for word in words:
        for symbol in symbols:
            passwords.append(word[0].lower() + symbol)
            passwords.append(word[0].capitalize() + symbol)
            passwords.append(word[0].upper() + symbol)

    for word in words:
        for number in range(0, 2101):
            for symbol in symbols:
                passwords.append(word[0].lower() + str(number) + symbol)
                passwords.append(word[0].capitalize() + str(number) + symbol)
                passwords.append(word[0].upper() + str(number) + symbol)

    return passwords

def print_passwords_to(file, passwords):
    if not os.path.isfile(file):
        with open(file, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(passwords))
    else:
        print(f'File {file} already exists. Exiting...')
        exit(1)

def print_top_10_words(top_10_words):
    print('\nTop 10 words are:\n')

    for i in range(min(10, len(top_10_words))):
        print(top_10_words[i][0])

    print()

@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.')
@click.option('--file', '-f', default='output.txt', prompt='Output file', help='File to print the passwords to (default: ./output.txt).')
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit).')
@click.option('--depth', '-d', default=0, help='Crawl depth of the script (default: 0).')
def main(url, file, length, depth):
    words = get_all_words_from(url, depth)
    top_10_words = get_top_10_words_from(words, length)
    passwords = generate_passwords_from_words(top_10_words)

    print_top_10_words(top_10_words)
    print_passwords_to(file, passwords)

if __name__ == '__main__':
    main()
