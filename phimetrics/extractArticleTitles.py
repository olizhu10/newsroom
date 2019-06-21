import json_lines
from itertools import islice
import jsonlines
fileName = input("Enter name of the file in events: ")
with open ('events/'+fileName+'.txt','r') as f :
    names = [name.rstrip() for name in f]
with jsonlines.open('events/'+fileName+'.jsonl', mode = 'w') as writer:
    with open('data/train-stats.jsonl', 'rb') as f: # opening file in binary(rb) mode
       for item in json_lines.reader(f):
           for name in names:
                if(item['archive']==name):
                    writer.write(item)
       f.close()
    writer.close()
