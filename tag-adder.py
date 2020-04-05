import json
import argparse
import configparser
""" updates a json with tags provided from another json
"""
ALL_ENTRIES = dict()

## Read path to unlabelled papers and model from config
config = configparser.RawConfigParser()
config.read('config.cfg')

unlabelled_path =  config.get('Data', 'unlabelled')
model_path =  config.get('Model', 'model')
predictions_path = config.get('Data', 'predictions')
kumu_path = config.get('Data', 'outKumu')

def main():
    parser = argparse.ArgumentParser(description='Update file1 tags to file2')
    parser.add_argument('--in', dest='infile', default='outKumu256.json', help='input json')
    parser.add_argument('--out', dest='outfile', default='crypto-semantics-data.json', help='output json')
 
    args = parser.parse_args()

    new_papers = None
    with open(args.infile, "r") as ku:
        new_papers = json.load(ku)
    new_papers = new_papers['elements']

    for paper in new_papers:
        ALL_ENTRIES[paper['id']] = paper

    old_papers = None
    with open(args.outfile, "r") as ku:
        old_papers = json.load(ku)
    old_papers = old_papers['elements']

    for paper in old_papers:
#        import ipdb; ipdb.set_trace()
        if paper['id'] in ALL_ENTRIES:
            updated_entry = ALL_ENTRIES[paper['id']]
            if 'tags' in updated_entry:
                paper['tags'] = updated_entry['tags']

    old_papers = {'elements': old_papers}

    with open(args.outfile, "w", encoding='utf-8') as ku:
        json.dump(old_papers, ku, indent=2,ensure_ascii=False)

main()
