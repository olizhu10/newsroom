from jsonl import openJsonl
import json

def main():
    jsonName = "../clustering/sample_clusters.json"
    jsonlFile = openJsonl("sample_clusters.jsonl")
    with open(jsonName, 'r') as file:
        lines = json.load(file)
        jsonlFile.write(lines)

if __name__ == '__main__':
    main()
