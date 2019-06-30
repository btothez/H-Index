# Introduction

This is a simple app, built on the tornado framework which can access an ElasticSearch. Over a collection of documents, the app returns the authors in order of their H-Index.

When accessed in the following way:

```bash
curl "http://localhost:9999/?limit=1000&subject=brain%cancer"
```

The app returns the following JSON:
```json
[
    {
        "author": "Marina Hansen",
        "doc_count": 56,
        "h_index": 18
    },
    {
        "author": "Marilyn Mccarty",
        "doc_count": 55,
        "h_index": 18
    },
    {
        "author": "Melvin Livingston",
        "doc_count": 55,
        "h_index": 18
    }
]
```



## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
