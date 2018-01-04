# -*- coding: UTF-8 -*-
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from flask import Flask
from flask import request
import json

from epubsearch import EpubIndexer
from epubsearch import crossdomain
from epubsearch import EpubParser

app = Flask(__name__)
indexSearch = EpubIndexer("whoosh")


@app.route("/")
def home():
    return "try /search?q=whale"


@app.route("/search", methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def search():
    query = request.args.get('q')
    bid = request.args.get('bid')

    if not query or not bid:
        return json.dumps({"msg": "attr is miss", "code": "404"})

    results = indexSearch.search(query, bid=bid)
    results["code"] = "200"
    results["msg"] = "success"
    return json.dumps(results)


@app.route("/index_book", methods=['GET', 'POST'])
@crossdomain(origin='*')
def index_book():
    path = request.args.get('path')
    bid = request.args.get('bid')

    if not path or not bid:
        return json.dumps({"msg": "attr is miss"})

    epub = EpubParser(path)
    index = EpubIndexer('whoosh')
    index.load(epub, bid)

    return json.dumps({ "msg": "success" })

if __name__ == "__main__":
    app.run(debug=True)
