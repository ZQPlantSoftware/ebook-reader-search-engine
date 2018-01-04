# -*- coding: UTF-8 -*-

from whoosh.index import create_in
import whoosh.index as index
from whoosh.fields import Schema, TEXT, ID
from whoosh.query import Term
from ChineseTokenizer import ChineseAnalyzer
from bs4 import BeautifulSoup
from whoosh.qparser import QueryParser
from baseengine import BaseEngine
import os
import re
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class WhooshEngine(BaseEngine):
    # analyzer = RegexAnalyzer(ur"([\u4e00-\u9fa5])|(\w+(\.?\w+)*)")
    analyzer = ChineseAnalyzer()
    # whoosh
    schema = Schema(
        title=TEXT(stored=True),
        path=TEXT(stored=True),
        href=ID(stored=True),
        bid=ID(stored=True),
        cfiBase=TEXT(stored=True),
        spinePos=TEXT(stored=True),
        content=TEXT(stored=True, analyzer=analyzer))

    def open(self):
        try:
            self.ix = index.open_dir(self.databasePath)

        except Exception, e:
            print "openning database {} failed".format(self.databaseName)

    def create(self):

        try:
            if not os.path.exists(self.databasePath):
                os.mkdir(self.databasePath)

                print "openning database {} to create".format(self.databaseName)
                self.ix = index.create_in(self.databasePath, self.schema)
            else:
              print "openning database {} to create".format(self.databaseName)
              self.ix = index.open_dir(self.databasePath, self.schema)
        except Exception, e:
            print 'here??', e

        self.writer = self.ix.writer()

    def add(self, bid='', path='', href='', title='', cfiBase='', spinePos=''):
        text = self.__get_text(path)
        self.writer.add_document(bid=unicode(bid.decode('utf-8')), title=unicode(title.decode('utf-8')), path=unicode(path), href=unicode(href), cfiBase=unicode(cfiBase), spinePos=unicode(spinePos), content=unicode(text))
        print "Indexed: " + bid + '|' + title + ' | ' + path + ' | ' + href + ' | ' + str(spinePos)

    def finished(self):
        self.writer.commit()

    def query(self, q, bid, limit=None):
        with self.ix.searcher() as searcher:
            results = []
            parsedQuery = QueryParser("content", schema=self.ix.schema).parse(q)

            allow_q = Term("bid", bid)

            hits = searcher.search(parsedQuery, filter=allow_q, limit=limit)

            for hit in hits:
                item = {}
                item['bid'] = hit["bid"].encode("utf-8")
                item['title'] = hit["title"].encode("utf-8")
                item['href'] = hit["href"].encode("utf-8")
                item['path'] = hit["path"].encode("utf-8")
                item['title'] = hit["title"].encode("utf-8")
                item['cfiBase'] = hit["cfiBase"].encode("utf-8")
                item['spinePos'] = hit["spinePos"].encode("utf-8")
                results.append(item)

            return results

    def __get_text(self, filename):
        # html = urllib.urlopen('http://www.nytimes.com/2009/12/21/us/21storm.html').read()
        html = open(filename, "r")
        soup = BeautifulSoup(html)
        texts = soup.findAll(text=True)

        def visible(element):
                if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                        return False
                elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                        return False
                return True

        visible_texts = filter(visible, texts)

        contents = ' '.join([s for s in visible_texts])

        return contents.strip() #.encode('utf-8')
