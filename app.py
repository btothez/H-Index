#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json

from elasticsearch import Elasticsearch


from tornado.options import define, options

define("port", default=9999, help="run on the given port", type=int)

es=Elasticsearch([{'host':'localhost','port':9200}])

class ESWrapper:
    def __init__(self):
        # Connect to the elastic cluster
        self.es=Elasticsearch([{'host':'localhost','port':9200}])


class MainHandler(tornado.web.RequestHandler):
    def query_h_index(self, subject, limit):
        reduce_script = """
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
        """

        query_dict = {
            "match_phrase": {
                "abstract": subject
            },
        }
        terms_dict = {
            "field": "author.keyword",
            "size": limit,
        }
        sort_dict = {
            "bucket_sort": {
                "sort": [{"h_index.value": {"order": "desc"}}]
            }
        }

        response = es.search(index='research',body={
            "query" : query_dict,

            "aggs": {
                "grouped_authors": {
                    "terms": terms_dict,
                    "aggs": {
                        "h_index": {
                            "scripted_metric": {
                                "init_script" : "state.transactions = []",
                                "map_script": "state.transactions.add(doc['citation_count'].value)",
                                "combine_script": "return state.transactions",
                                "reduce_script": reduce_script
                            },
                        },
                        "h_index_sort": sort_dict,
                    }
                },
            }
        })

        if type(response) == dict and 'aggregations' in response:
           return list(map(self.transform, response['aggregations']['grouped_authors']['buckets']))
        return {'status': 'error'}

    def transform(self, obj):
        return {
            'author': obj['key'],
            'doc_count': obj['doc_count'],
            'h_index': obj['h_index']['value']
        }

    def get(self):
        limit=self.get_argument("limit", 30, True)
        subject=self.get_argument("subject", "brain cancer", True)
        response = self.query_h_index(subject, limit)
        self.write(json.dumps(response))


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([(r"/", MainHandler)])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    print("serving on localhost:9999...")
    main()