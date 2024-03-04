from flask import Flask, request
from flask import render_template
from elasticsearch import Elasticsearch
import math

ELASTIC_HOST = 'https://localhost:9200'
ELASTIC_USERNAME = 'elastic'
ELASTIC_PASSWORD = 'password'

es = Elasticsearch(ELASTIC_HOST, http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD), verify_certs=False)
app = Flask(__name__)

@app.route('/')
def index():
    genres = ['comedy', 'crime', 'music', 'action', 'adventure', 'horror', 'thriller', 'romance', 'drama', 'family', 'fantasy', 'science', 'history', 'war', 'mystery']
    return render_template('movieSearch.html', genres=genres)

@app.route('/search')
def query_search():
    page_size = 6
    query = request.args.get('query')
    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1

    body = {
        'size': page_size,
        'from': page_size * (page_no - 1),
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['title', 'overview', 'director', 'cast']
            }
        }
    }
    
    res = es.search(index='movies-4.2', doc_type='', body=body)
    hits = [{ 
        'title': doc['_source']['title'], 
        'overview': doc['_source']['overview'], 
        'genre': doc['_source']['genre'],
        'release_date': doc['_source']['release_date'],
        'poster_url': doc['_source']['poster_url'],
        'imdb_id': doc['_source']['imdb_id'],
        'actors': doc['_source']['cast'],
        'director': doc['_source']['director'],
        'runtime': doc['_source']['runtime'],
        'rating': doc['_source']['vote_average']
    } for doc in res['hits']['hits']]
    page_total = math.ceil(res['hits']['total']['value'] / page_size)
    return render_template('movieResult.html', href=f'?query={query}&', hits=hits, page_no=page_no, page_total=page_total)

@app.route('/genre/<string:genre>')
def genre_search(genre):
    page_size = 6
    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1

    body = {
        'size': page_size,
        'from': page_size * (page_no - 1),
        'query': {
            'term': {
                'genre': genre
            }
        }
    }
    
    res = es.search(index='movies-4.2', doc_type='', body=body)
    hits = [{ 
        'title': doc['_source']['title'], 
        'overview': doc['_source']['overview'], 
        'genre': doc['_source']['genre'],
        'release_date': doc['_source']['release_date'],
        'poster_url': doc['_source']['poster_url'],
        'imdb_id': doc['_source']['imdb_id'],
        'actors': doc['_source']['cast'],
        'director': doc['_source']['director'],
        'runtime': doc['_source']['runtime'],
        'rating': doc['_source']['vote_average']
    } for doc in res['hits']['hits']]
    page_total = math.ceil(res['hits']['total']['value'] / page_size)
    return render_template('movieResult.html', href=f'{genre}?', hits=hits, page_no=page_no, page_total=page_total)