# HOWTO add/remove papers

## The easy way

Fill in an GitHub issue with the paper and some associated tags you think
are right for it, as in [here](https://github.com/rdragos/kumuScripts/issues/1#issuecomment-610406754).


## The hard way

Suppose you want to add the paper called "Practical Covertly Secure MPC for Dishonest Majority - Or: Breaking the SPDZ Limits"

As the current pipeline
stands, if you want to add a paper you need to follow the next steps:

1. Find its semantic scholar id (s2id), for example:
<https://www.semanticscholar.org/paper/Practical-Covertly-Secure-MPC-for-Dishonest-Or%3A-the-Damg%C3%A5rd-Keller/e69e44f837662fdc5c49a7ba40666ba7bd5980c0>

The **s2id** of a paper consist in the entire digest before the end of the link, i.e.: `e69e44f837662fdc5c49a7ba40666ba7bd5980c0`

2. Look for the json information corresponding to the **s2id** in `crypto-semantics-data.json`, eg:
```javascript
...
    {
      "label": "DKL+12",
      "abstract": "SPDZ (pronounced “Speedz”) is the nickname of the MPC protocol of Damgard et al. from Crypto 2012. In this paper we both resolve a number of open problems with SPDZ; and present several theoretical and practical improvements to the protocol. In detail, we start by designing and implementing a covertly secure key generation protocol for obtaining a BGV public key and a shared associated secret key. We then construct both a covertly and actively secure preprocessing phase, both of which compare favourably with previous work in terms of efficiency and provable security.",
      "id": "e69e44f837662fdc5c49a7ba40666ba7bd5980c0",
      "venue": "ESORICS",
      "s2Url": "https://semanticscholar.org/paper/e69e44f837662fdc5c49a7ba40666ba7bd5980c0",
      "authors": [
        "Ivan Damgård",
        "Marcel Keller",
        "Enrique Larraia",
        "Valerio Pastro",
        "Peter Scholl",
        "Nigel P. Smart"
      ],
      "title": "Practical Covertly Secure MPC for Dishonest Majority - Or: Breaking the SPDZ Limits",
      "year": 2012
    },
 ...
```

Check if the **s2id** is in `tagged_output.json`. If it is and you actually want to delete the entry
from the Kumu map then set the flag `isMPC: 0`.

If the **s2id** is not in `tagged_output.json` then add this entry at the end of of `tagged_output.json`.
with the corresponding `isMPC` flag:
```javascript

    {
      "label": "DKL+12",
      "abstract": "SPDZ (pronounced “Speedz”) is the nickname of the MPC protocol of Damgard et al. from Crypto 2012. In this paper we both resolve a number of open problems with SPDZ; and present several theoretical and practical improvements to the protocol. In detail, we start by designing and implementing a covertly secure key generation protocol for obtaining a BGV public key and a shared associated secret key. We then construct both a covertly and actively secure preprocessing phase, both of which compare favourably with previous work in terms of efficiency and provable security.",
      "id": "e69e44f837662fdc5c49a7ba40666ba7bd5980c0",
      "venue": "ESORICS",
      "s2Url": "https://semanticscholar.org/paper/e69e44f837662fdc5c49a7ba40666ba7bd5980c0",
      "authors": [
        "Ivan Damgård",
        "Marcel Keller",
        "Enrique Larraia",
        "Valerio Pastro",
        "Peter Scholl",
        "Nigel P. Smart"
      ],
      "title": "Practical Covertly Secure MPC for Dishonest Majority - Or: Breaking the SPDZ Limits",
      "year": 2012,
      "isMPC": 1
    }
```
 
Once this is done please submit a pull request and I will make sure to re-run a script that adds automatically
the connections in the visual map.

# Instructions for developers:

To get a list of COED papers take the following steps:

1. Fetch semanticscholar local database of cryptography papers
and output the result into a json by running:

```
python kumucollector.py --output 0
```
This will output a big file as `kumu_output.json'

2. Train a model using the some partially labelled data by running
```
python trainer.py
```
3. After having the ML model now run obtain the new COED paper classification
using 
```
python predictor.py
```
This should output a json called ``predicted_output.json`.

4. If you want to restrict the graph to, say, 128 citations execute:
```
python kumucollector.py --output 2 --limit 128

```

The last command will use `predicted_output.json` together with the connections
from `kumu_output` and will output the kumu graph in `outKumu128.json`.

In order to avoid losing the tag information we recommend running

```
python tag-adder.py --in crypto-semantics-data.json --out predicted_output.json
```

after a re-run of `python kumucollector.py --output 0`

# Modifying some semantic-scholar entries

Perhaps there is some wrong information about a paper such as author names, conference name,
year appeareance, etc. Add it to corrections.json with the fields you wish to correct
along with its semantic scholar id. Then re-run `python kumucollector.py --output 0`
    

## FAQ

**Question:** Why is not paper X in there?

**Answer:** Most likely because it's indexed wrong by semantic scholar. The way we built this database was by
selecting for papers which appeared in CRYPTO, EUROCRYPT, CCS, etc. Sometimes semantic scholar does
parses the venues incorrectly, or even author names, sometimes it has duplications of the same paper
so the number of citations might be slightly different than what you see on Google Scholar.

##
**Q:** Where can I see this marvellous map?

**A:** You can find it on Kumu [here](https://kumu.io/DragosRotaru/coed-map#coed-256).

##
**Q:** Are there any other cryptography maps?

**A:** Yes, a very more detailed map on FHE literature made by Ilia Iliashenko.
[Check it out here](https://kumu.io/iliailia/fhe-graph#academic-papers).


## Thanks

We would like to thank Peter Sebastian Nordholt for posting the scripts used in https://guutboy.github.io/ 
on GitHub.
We would also like to thank the COSIC group for their helpful feedback on initial version of the map.



