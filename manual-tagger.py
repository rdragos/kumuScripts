import json
from os import path
import numpy as np
import sys
import configparser

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

prev_state = set()

discovered_items = dict()

config = configparser.RawConfigParser()
config.read('config.cfg')

def load_prev_state():
    with open(config.get('Data', 'labelled')) as json_file:
        prev_list = json.load(json_file)
        discovered_items['elements'] = prev_list['elements']
        for item in prev_list['elements']:
            prev_state.add(item['s2Url'])
 
if path.isfile(config.get('Data', 'labelled')):
    load_prev_state()
   
def main():

    def tag(item):
        print(bcolors.OKBLUE + item['title'] + bcolors.ENDC)
        print()
        print(bcolors.OKBLUE + str(item['authors']) + bcolors.ENDC)
        print()
        print(bcolors.OKBLUE + item['abstract'] + bcolors.ENDC)

        choice = input("""
                Do you consider it an MPC paper?

                1: Yes
                0: No
                """)
        if choice == "0":
            return 0
        elif choice == "1":
            return 1
        else:
            sys.exit

    def save_state(items):
        with open(config.get('Data', 'labelled'), "w", encoding='utf-8') as ku:
            json.dump(items, ku, indent=2,ensure_ascii=False)


    option_file = None
    if sys.argv[1] == 'tag':
        # just show to console output random papers
        # and then tag randomly
        option_file = config.get('Data', 'unlabelled')
    elif sys.argv[1] == 'improve':
        # try to refine the already classified mpc/coed papers
        option_file = config.get('Data', 'predictions')

    data = None
    with open(file_name) as json_file:
        data = json.load(json_file)

    data = [p for p in data['elements']]

    permutation = np.random.permutation(len(data))
    if sys.argv[1] == 'improve':
        permutation = sorted(permutation, key=lambda item: data[item]['pred']>0, reverse=True)

    global discovered_items

    for i in range(len(data)):
        index = permutation[i]
        if data[index]['s2Url'] in prev_state:
            # paper encountered in some previous tagging procedure
            continue
        if data[index]['pred'] is True:
            continue
        item = data[index]
        item['isMPC'] = tag(item)
        discovered_items['elements'].append(item)
        save_state(discovered_items)

if __name__=="__main__":
    main()
#import ipdb; ipdb.set_trace()
