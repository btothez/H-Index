#!/usr/bin/env python

from elasticsearch import Elasticsearch
import numpy as np
import random
es=Elasticsearch([{'host':'localhost','port':9200}])
names = [
    'Marco Cain',
    'Reynaldo Barry',
    'Marina Hansen',
    'David Raymond',
    'Camron Simmons',
    'Melvin Livingston',
    'Alicia Shah',
    'Penelope Carter',
    'Marilyn Mccarty',
]

topics = [
    'brain cancer',
    'lower back pain',
    'liver failure'
]

words = [
    'formularist',
    'catechu',
    'ornithophilous',
    'Lyrurus',
    'hamstring',
    'coling',
    'wove',
    'bromphenol',
    'hydrogenase',
    'festinately',
    'marcescence',
    'bierbalk',
    'inexpedience',
    'macrophotograph',
    'overrigidity',
    'jarry',
    'unsoaped',
    'hemihedron',
    'acrologism',
    'thermophilic',
    'flitting',
    'immune',
    'somnambulize',
    'grateful',
    'rudge',
    'mould',
    'bezoar',
    'massa',
    'palaeoniscid',
    'prillion',
    'overcritical',
    'glyceryl',
    'unregarded',
    'additively',
    'nonelective',
    'lighter',
    'Maniva',
    'brimfully',
    'unendurability',
    'ruralness',
    'pronation',
    'witherweight',
    'pyroscopy',
    'careful',
    'heed',
    'brachistochronous',
    'associate',
    'Yankeefy',
    'xylenol',
]



for ind in range(500):
    doc = {
        "title": words[ind % len(words)],
        "abstract": topics[ind % len(topics)],
        "author": names[ind % len(names) ],
        "citation_count": random.randint(1, 25)
    }
    print(doc)
    es.index(index='research',doc_type='paper',id=ind,body=doc)


es.search(index='research',body={
    "query": {
        'bool':{
            'must':[{
                    'match':{
                        'author':'Monica Hull',
                    }
                }, {
                    'match':{
                        'abstract':'brain cancer',
                    }
            }]
        }
    },
})
