import json

with open('../watson_results/results.json', mode='r') as fp:
    obj = json.load(fp)
fp.close()
entities = obj['entities']
for entity in entities:
    if int(entity['count']) > 2:
        print(entity['text']," : " ,entity['count'])
