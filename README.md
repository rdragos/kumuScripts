# HOWTO add/remove papers

As the current pipeline stands, if you want to add/remove a paper you need to follow the next steps:

1. Find its semantic scholar id, for example: <https://www.semanticscholar.org/paper/Fully-Homomorphic-Encryption-with-Relatively-Small-Smart-Vercauteren/e2957cbe949d4e76764bec20291a66de89393174>

The id for this paper is `e2957cbe949d4e76764bec20291a66de89393174`

2. Look for its json information in `crypto-semantics-data.json, eg:
```javascript
...
    {
      "label": "SmartVercauteren09",
      "abstract": "We present a fully homomorphic encryption scheme which has both relatively small key and ciphertext size. Our construction follows that of Gentry by producing a fully homomorphic scheme from a “somewhat” homomorphic scheme. For the somewhat homomorphic scheme the public and private keys consist of two large integers (one of which is shared by both the public and private key) and the ciphertext consists of one large integer. As such, our scheme has smaller message expansion and key size than Gentry’s original scheme. In addition, our proposal allows efficient fully homomorphic encryption over any field of characteristic two.",
      "id": "e2957cbe949d4e76764bec20291a66de89393174",
      "venue": "Public Key Cryptography",
      "s2Url": "https://semanticscholar.org/paper/e2957cbe949d4e76764bec20291a66de89393174",
      "authors": [
        "Nigel P. Smart",
        "Frederik Vercauteren"
      ],
      "title": "Fully Homomorphic Encryption with Relatively Small Key and Ciphertext Sizes",
      "year": 2009,
      "tags": [
        "fhe",
        "public-key cryptography"
      ]
    }
...
```

and look for it in `tagged_output.json` to check whether there is such an entry and check the flag `isMPC`
to be set up accordingly (0 to remove paper in the kumu map, 1 to add paper in the map).

If there is no such entry, then make sure to add it at the end of `tagged_output.json`, with the corresponding flag, eg:
```javascript
    {
      "label": "SmartVercauteren09",
      "abstract": "We present a fully homomorphic encryption scheme which has both relatively small key and ciphertext size. Our construction follows that of Gentry by producing a fully homomorphic scheme from a “somewhat” homomorphic scheme. For the somewhat homomorphic scheme the public and private keys consist of two large integers (one of which is shared by both the public and private key) and the ciphertext consists of one large integer. As such, our scheme has smaller message expansion and key size than Gentry’s original scheme. In addition, our proposal allows efficient fully homomorphic encryption over any field of characteristic two.",
      "id": "e2957cbe949d4e76764bec20291a66de89393174",
      "venue": "Public Key Cryptography",
      "s2Url": "https://semanticscholar.org/paper/e2957cbe949d4e76764bec20291a66de89393174",
      "authors": [
        "Nigel P. Smart",
        "Frederik Vercauteren"
      ],
      "title": "Fully Homomorphic Encryption with Relatively Small Key and Ciphertext Sizes",
      "year": 2009,
      "isMPC": 1,
      "tags": [
        "fhe",
        "public-key cryptography"
      ]
    }
```
 
Once this is done please submit a pull request and I'll make sure to re-run a script that adds automatically
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
python tag-adder.py --in crypto-semantics-data.json --out kumu_output.json
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

**Question:** Where can I see this marvellous map?

**Answer:** [Here it is](https://kumu.io/DragosRotaru/coed-map#coed-256)

**Question:** Are there any other cryptography maps?

**Answer:** Yes, a very more detailed map on FHE literature made by Ilia Iliashenko.
[Check it out here](https://kumu.io/iliailia/fhe-graph#academic-papers)


## Thanks

We would like to thank Peter Sebastian Nordholt for posting the scripts used in https://guutboy.github.io/ 
on GitHub.



