# Introduction

This is a simple app, built on the tornado framework which can access an ElasticSearch. Over a collection of documents, the app returns the authors in order of their H-Index.

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

First make sure elasticsearch is running locally on port 9200. In an environment with a elasticsearch and tornado installed via pip, first run the following script:


```bash
./data_factory.py
```

This inserts hundreds of documents into storage which can then be queried and aggregated, used to compute an h-index score, and finally sorted by this score.

Next, run the server locally by running:

```bash
./app.py
```

## The code


