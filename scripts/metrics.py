import random
import sys

from newsroom import jsonl
from newsroom.analyze import Fragments

with jsonl.open("Orlando.jsonl", gzip = False) as train_file:
    train = train_file.read()

# Compute stats on random training example:
article_str = sys.argv[2]
article_list = article_str.split()
summary_num = int(sys.argv[1])
for article in article_list:
    summary = train[summary_num]['summary']
    text = train[int(article)]['text']
    fragments = Fragments(summary, text)

    # Print paper metrics:
    print('For summary '+str(summary_num)+', article '+str(article))
    print("Coverage:",    fragments.coverage())
    print("Density:",     fragments.density())
    print("Compression:", fragments.compression())

    # Extractive fragments oracle:

    print("List of extractive fragments:")
    print(fragments.strings())
