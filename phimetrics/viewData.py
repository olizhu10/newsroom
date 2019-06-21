import json_lines
from itertools import islice

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))
eventlist = []
with open('data/train-stats.jsonl', 'rb') as f: # opening file in binary(rb) mode
   for item in json_lines.reader(f):
        if (item['date']>"20080909000000" and item['date']<"20080915000000" and "Collider" in item['title']):
            print(item['summary'])
            print(item['archive'])
            eventlist.append(item)
print(len(eventlist))
"""Boston Marathon, if (item['date']>"20130415000000" and item['date']<"20130420000000" and "Marathon" in item['title']):"""
"""Hurricane Sandy, if (item['date']>"20121022000000" and item['date']<"20121110000000" and "Sandy" in item['title']):"""
"""LHC, if (item['date']>"20080909000000" and item['date']<"20080915000000" and "Collider" in item['title']):"""
