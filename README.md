# E-Book Reader

This is a nice e-book reader base on `epub.js` `React` support both PC and mobile.

The whole reader system with 3 part, React front end application, JAVA backend services with mysql database and a python search engine.

1. [Reader Frontend Page](https://github.com/ZQPlantSoftware/epub-reader) React base front end application

2. [Java Reader Backend Services](https://github.com/ZQPlantSoftware/epub-reader-services) We use Spring Boot and MySQL

3. [Reader Search Engine](https://github.com/ZQPlantSoftware/ebook-reader-search-engine) Python whoosh

** It's a e-book reader only for EPUB now, we may support other format of ebook later **

## Search Engine Part

This search engine base on python search framework [whoosh](https://whoosh.readthedocs.io/en/latest/)

To use this (assumes a Python 2.7 environment with pip and virtualenv)

```
$ virtualenv venv

$ source venv/bin/activate

$ pip install -r requirements.txt
```

Add an unzipped epub to the source directory, say /your_epub/ then run

`$ python indexer.py --i your_epub`

Finally run the search api

`$ python search.py`

Flask should run on localhost:5000/ and you can query the server with the /search route and the parameter q, like:

localhost:5000/search?q=test

## License

MIT
