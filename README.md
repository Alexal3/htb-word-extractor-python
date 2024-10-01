# htb-word-extractor-python
This repository is a solution to a task from the "Introduction to Python 3" module on the HTB Academy.

The task was as follows:

>- Add a --output / -o argument that lets us define an output file to print to instead of the console (something like with open('path.txt', 'w') as wr: and wr.write(word)).
>- Add common password mutations to the output, e.g., Capitalized, lowercase, UPPERCASE, and with various bits appended like the current and recent years, random numbers or symbols, e.g., 2019, 1!, 2!, 3!, 01, 123. Summer2021! and similar variations are depressingly frequent passwords.
>- Add a --depth / -d argument specifying the crawl depth of the script. This implies the ability to grab not only words but also URLs on the webpage(s), check if they are within scope (e.g., domain), and add them to a list of pages to crawl next.
>- The program currently crashes if a minimum length of 10 or higher is specified. Try to figure out why and fix it (hint: check out that last for-loop).

The original script can be found in this [commit](https://github.com/Alexal3/htb-word-extractor-python/commit/bf45c328c579e3046403686702d917bc1ac197e3).
