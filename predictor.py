from sklearn.externals import joblib
import json
import sys
import configparser
"""Adds mpc predictions to eprint papers.

This script loads the unlabelled eprint papers and finds all papers that does not have
an mpc prediction yet. It then loads a a pre-trained classifier and uses it
to add predictions to all papers found in the first step. The result is written back to
the file of unlabelled papers"""

def combi_predictions(unpredicted, model_path):
    abs_clf = joblib.load(model_path + "abs")
    tit_clf = joblib.load(model_path + "tit")
    aut_clf = joblib.load(model_path + "aut")
    combi_clf = joblib.load(model_path + "combi")
    tit_predictions = tit_clf.predict([p['title'] for p in unpredicted]);
    abs_predictions = abs_clf.predict([p['abstract'] for p in unpredicted]);
    aut_predictions = aut_clf.predict([" ".join(p['authors']) for p in unpredicted]);
    combi_features = []
    for i in range(0, len(unpredicted)):
        feature = [float(abs_predictions[i]), float(tit_predictions[i]), float(aut_predictions[i])]
        combi_features.append(feature)
    return combi_clf.predict(combi_features)

## Read path to unlabelled papers and model from config
config = configparser.RawConfigParser()
config.read('config.cfg')
unlabelled_path =  config.get('Data', 'unlabelled')
model_path =  config.get('Model', 'model')
predictions_path = config.get('Data', 'predictions')
labelled_path = config.get('Data', 'labelled')

with open(unlabelled_path) as dataFile:
  papers = json.load(dataFile)['elements']

with open(labelled_path) as dataFile:
  labelled_papers = json.load(dataFile)['elements']

already_labeled = dict()
for item in labelled_papers:
  already_labeled[item['id']] = item['isMPC']


unpredicted = [p for p in papers if p['id'] not in already_labeled.keys()]
mpc_count = 0
coed_papers = list()
if len(unpredicted) > 0:
    predicted = combi_predictions(unpredicted, model_path)
    for i in range(0, len(unpredicted)):
        paper = unpredicted[i]
        # small hack, only works for MPC
        if int(paper['year']) <= 1978:
            paper['pred'] = False
            continue
        if predicted[i] == 1:
            mpc_count += 1
            paper['pred'] = True
        else:
            paper['pred'] = False

manually_labeled = [p for p in papers if p['id'] in already_labeled.keys()]
for paper in manually_labeled:
    paper['pred'] = (already_labeled[paper['id']] == 1)
    
allpapers = unpredicted + manually_labeled
# careful here      
papers = dict({'elements': allpapers})
with open(predictions_path, 'w') as dataFile:
    json.dump(papers, dataFile, separators=(',', ':'), indent=2, sort_keys=True)
print(str(mpc_count))

