import json_lines
import numpy as np
import fragments
events = []
eventsFull = []
fileName = input("Enter name of the file in events: ")
with open('events/'+fileName+'.jsonl', 'rb') as f: # opening file in binary(rb) mode
    for item in json_lines.reader(f):
        events.append(item)
with open('events/'+fileName+'F.jsonl', 'rb') as f: # opening file in binary(rb) mode
    for item in json_lines.reader(f):
        eventsFull.append(item)
density = np.ndarray(shape = (len(events), len(eventsFull)))
coverage = np.ndarray(shape = (len(events), len(eventsFull)))
compression = np.ndarray(shape = (len(events), len(eventsFull)))
for article, aEvent in enumerate(events, start = 0):
    for summary, sEvent in enumerate(eventsFull, start = 0):
        fragment = fragments.Fragments(sEvent['summary'], aEvent['text'])
        density[article, summary] = fragment.density()
        coverage[article, summary] = fragment.coverage()
        compression[article, summary] = fragment.compression()
np.savetxt("events/data/"+fileName+"GBDensity.csv", density, delimiter=",")
np.savetxt("events/data/"+fileName+"GBCoverage.csv", coverage, delimiter=",")
np.savetxt("events/data/"+fileName+"GBCompression.csv", compression, delimiter=",")
