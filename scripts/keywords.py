import rake
import jsonl

with jsonl.open('../clustering/cluster_pairings.jsonl') as f:
    clusters = f.read()
with jsonl.open('../dataset_files/train.jsonl.gz', gzip=True) as ds:
    articles = ds.read()

cluster_id = 11271
archives = clusters[int(cluster_id)]
article_text = ""
for article in articles:
    if article['archive'] == next(iter(archives.values())):
        article_text = article['text']

rake_object = rake.Rake()
keywords = rake_object.run(article_text)

print(keywords)
