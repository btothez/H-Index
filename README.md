# Introduction

This is a simple app built on the Tornado framework, which can access an Elasticsearch instance. Looking at a collection of research papers, the app can return the highest ranked authors in order of their H-Index.

When accessed in the following way:

```bash
curl "http://localhost:9999/?limit=20&subject=brain%20cancer"
```

The app returns the following JSON:
```json
[
    {
        "author": "Marco Cain",
        "doc_count": 56,
        "h_index": 18
    },
    {
        "author": "Alicia Shah",
        "doc_count": 55,
        "h_index": 17
    },
    {
        "author": "David Raymond",
        "doc_count": 56,
        "h_index": 16
    }
]
```


## Setup

First make sure Elasticsearch is running locally on port 9200. In an environment with a Elasticsearch and Tornado installed via pip, first run the following script:


```bash
./data_factory.py
```

This inserts hundreds of documents into storage which can then be queried and aggregated, used to compute an h-index score, and finally sorted by this score.

Next, run the server locally by running:

```bash
./app.py
```

## The code
The Elasticsearch query is very straightforward, it simply uses the url parameter 'subject' ("brain cancer" by default) to retrieve documents with this phrase in their abstract. The aggregation engine then groups all these documents by their author.

The next step is to create a metric on each of these buckets (the collection of documents by the author) called h-index. This was done using script metric feature of Elastic Search. The most relevant part of this script, the "reduce script," was written in the native ES scripting language called "Painless"
```javascript
    def citationCounts = [];
    for (state in states) {
        for (el in state) {
            citationCounts.add(el);
        }
    }
    citationCounts.sort((x,y) -> (int)y - (int)x);
    def h_index = 0;
    int index = 1;
    for (cnt in citationCounts) {
        if (index <= cnt) {
            h_index = index;
        } else {
            break;
        }
        index+=1;
    }
    return h_index;
```

To break this down, the states value comes in as an array of arrays (from different shards on the ES instance), and needs to be accumulated into one Array. From there, the values (citation counts of the documents) are sorted in descending order. As the script iterates through the descending citation_counts, the final index at which the index is less than or equal to the citation count is returned as the value of h_index.
