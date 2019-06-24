import jsonl
import numpy as np
import fragments
events = []
fileName = input("Enter name of the file in events: ")
with jsonl.open('../jsonl_files/'+fileName+'.jsonl') as f:
    for item in f:
        events.append(item)
density = np.ndarray(shape = (len(events), len(events)))
coverage = np.ndarray(shape = (len(events), len(events)))
compression = np.ndarray(shape = (len(events), len(events)))
for article, aEvent in enumerate(events, start = 0):
    for summary, sEvent in enumerate(events, start = 0):
        fragment = fragments.Fragments(sEvent['summary'], aEvent['text'])
        density[article, summary] = fragment.density()
        coverage[article, summary] = fragment.coverage()
        compression[article, summary] = fragment.compression()
np.savetxt("events/data/"+fileName+"Density.csv", density, delimiter=",")
np.savetxt("events/data/"+fileName+"Coverage.csv", coverage, delimiter=",")
np.savetxt("events/data/"+fileName+"Compression.csv", compression, delimiter=",")
