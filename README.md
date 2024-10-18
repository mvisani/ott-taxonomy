# OTT-Taxonomy
This repository contains the code to download the OTT taxonomy with different versions.

## Installation
Clone this repository and activate your environment. You can then run : 
```bash
pip install .
```

## Usage
To download all the files of all the versions of the taxonomy, you can run the following command:
```bash
python examples/download_ott_taxonomy.py all
```

You can also do : 
```python
from ott_taxonomy import Dataset
ott = Dataset.load("ott3.6")
full_graph = ott.to_networkx()
subgraph = ott.generate_subgraph_from_id(770311)

# if you want to keep the subspecies:
subgraph = ott.generate_subgraph_from_id(770311, drop_subspecies=False)
```

Or get the dataframe : 
```python
from ott_taxonomy import Dataset
ott = Dataset.load("ott3.6")
df = ott.get_taxonomy()
```