import json
import argparse
import configparser
""" Compresses all json files into a single one and draws connections between them.

    It has two uses:
        1) Simply fetches all the 

"""
FAILS = 0
ALL_ENTRIES = dict()

## Read path to unlabelled papers and model from config
config = configparser.RawConfigParser()
config.read('config.cfg')
unlabelled_path =  config.get('Data', 'unlabelled')
model_path =  config.get('Model', 'model')
predictions_path = config.get('Data', 'predictions')
kumu_path = config.get('Data', 'outKumu')
semantics_pattern = config.get('Semantics', 'filePattern')

def fetch_data():
    def inner_fetch(name):
        sem_dir = config.get('Semantics', 'pathToData')
        entries = []
        f = open(sem_dir + name, 'r')
        for line in f.readlines():
            tmp = json.loads(line)
            if 'year' in tmp.keys():
                entries.append(tmp)
            else:
                global FAILS
                FAILS += 1
        return entries

    def gen_name(digits, index):
        return semantics_pattern + digits + str(index)

    all_entries = []
    for i in range(10):
        all_entries += inner_fetch(gen_name('-00', i))

    for i in range(10,100):
        all_entries += inner_fetch(gen_name('-0', i))

    for i in range(100,181):
        all_entries += inner_fetch(gen_name('-', i))

    all_entries += inner_fetch('s2-corpus-additions')

    return all_entries

complete_entries = fetch_data()

complete_entries = sorted(complete_entries, key=lambda k: k['year'])
for item in complete_entries:
    ALL_ENTRIES[item['id']] = item

# abbreviate entries
abbreviated_entries = list()
for paper in complete_entries:
    short_authors = [author['name'].split(' ')[-1] for author in paper['authors']]
    if len(short_authors) > 2:
        abbrv = [short_authors[i][0] for i in range(3)] + list("+")
        short_authors = abbrv
        
    complete_authors = [author['name'] for author in paper['authors']]
    short_year = str(paper['year'])[2:]

    abbreviated_entries.append({
            "label": "".join(author for author in short_authors) + short_year,
            "abstract": paper['paperAbstract'],
            "id": paper['id'],
            "venue": paper['venue'],
            "s2Url": paper['s2Url'],
            "authors": complete_authors,
            "title": paper['title'],
            "year": paper['year'],
    })

abbreviated_entries_by_id = dict()
for paper in abbreviated_entries:
    abbreviated_entries_by_id[paper['id']] = paper

def add_corections():
    corrections = None
    with open("corrections.json", "r") as dataFile:
          corrections = json.load(dataFile)
    for paper in corrections:
        paper_id = paper['id']
        for field in paper.keys():
            abbreviated_entries_by_id[paper_id][field] = paper[field]

add_corections()
abbreviated_entries = list()
for key in abbreviated_entries_by_id.keys():
    paper = abbreviated_entries_by_id[key]
    abbreviated_entries.append(paper)

def output_all():
    return ({'elements': abbreviated_entries},unlabelled_path)

def output_allplus():
    pass

def output_sparse(limit):
    # this outputs all papers that have at least limit citation and draws the graph between them
    # also makes sense to run this function after identified the coed_papers
    coed_papers = None
    with open(predictions_path) as json_file:
        coed_papers = json.load(json_file)

    # get rid of annoying kumu format
    coed_papers = [p for p in coed_papers['elements'] if p['pred']]
    coed_papers = list(filter(lambda p: len(ALL_ENTRIES[p['id']]['inCitations']) >= limit, coed_papers))

    # put every coed paper id into a set to find them easily
    coed_paper_ids = set()
    for paper in coed_papers:
        coed_paper_ids.add(paper['id'])

    connections = list()
    NUM_CONNECTIONS = 0
    NUM_SKIPPED = 0
    for paper in coed_papers:
        paper_id = paper['id']
        paper['numInCitations'] = len(ALL_ENTRIES[paper_id]['inCitations'])
        paper.pop('pred', None)
        # outcitations are references inside paper
        # incitations are papers which cite the paper
        out_citations = ALL_ENTRIES[paper_id]['outCitations']
        for citation in out_citations:
            # only add a connection if it's between two COED papers
            if citation in coed_paper_ids:
                connections.append({
                        "id": NUM_CONNECTIONS,
                        "from": citation,
                        "to": paper_id,
                        "direction": "directed"
                })
                NUM_CONNECTIONS += 1
            else:
                NUM_SKIPPED += 1

    print("Total papers: ", len(coed_papers))
    print("Total connections: ", NUM_CONNECTIONS)
    print("Total skipped: ", NUM_SKIPPED)

    # now compress venues to avoid duplicates such as CCS, CCS '04, etc

    venues = list()
    f = open('venues.txt', 'r')
    for line in f.readlines():
        venues.append(json.loads(line))
        
    from difflib import SequenceMatcher

    for paper in coed_papers:
        best_venue = {'venue': paper['venue']}
        best_score = 0

        for venue in venues:
            for possible_name in venue['names']:
                match_score = SequenceMatcher(None, possible_name, paper['venue']).ratio()
                if match_score > best_score and match_score > 0.5:
                    best_score = match_score
                    best_venue = venue

        paper['venue'] = best_venue['venue']


    global kumu_path
    kumu_path += "outKumu" + str(limit) + ".json"
    return (dict({"elements": coed_papers, "connections": connections}), kumu_path)

def main():
    parser = argparse.ArgumentParser(description='Process output type')
    parser.add_argument('--output', dest='output_type', type=int,
                        default=0, help='all/all+/sparse')
    parser.add_argument('--limit', dest='limit', type=int,
                        default=0, help='limit citations to')

 
    args = parser.parse_args()
    print(args.output_type)

    toWrite = None
    papers = None

    if args.output_type == 0:
        papers, toWrite = output_all()
    elif args.output_type == 1:
        papers = output_allplus()
    elif args.output_type == 2:
        papers, toWrite = output_sparse(args.limit)
        
    with open(toWrite, "w", encoding='utf-8') as ku:
        json.dump(papers, ku, indent=2,ensure_ascii=False)


if __name__=="__main__":
    main()

