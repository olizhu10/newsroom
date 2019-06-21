from jsonl import openJsonl
import json

def main():
    jsonName = "Mandela.json"
    jsonlFile = openJsonl("Mandela.jsonl")
    with open(jsonName, 'r') as file:
        lines = json.load(file)
        jsonlFile.write(lines)

if __name__ == '__main__':
    main()
