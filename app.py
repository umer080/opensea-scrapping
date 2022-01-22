from flask import Flask, url_for, redirect, render_template, abort, request, flash, jsonify
from flask_restful import Api

from flask_caching import Cache
from flask_cors import CORS, cross_origin

from celery import Celery

server = Flask(__name__,
               static_url_path='',
               static_folder='./static',
               template_folder='./templates')

server.config['SECRET_KEY'] = b'C\x1a!\xa2Q\xbd\xf5\xfdDx\xd0\x8e\x0c\x16\x04\x82'


api = Api(server)

cache = Cache(server, config={'CACHE_TYPE': 'simple'})

server.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(server, resources={r"/*": {"origins": "*"}})

server.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
server.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(server.name, broker=server.config['CELERY_BROKER_URL'])
celery.conf.update(server.config)


server.app_context().push()


# ---------------------nft------------------------------------
from apis.nfts import NftOrderbook
api.add_resource(NftOrderbook, '/nft-orderbook', '/nft-orderbook')

# ---------------------nft------------------------------------
from apis.collection import Collection
api.add_resource(Collection, '/collection', '/collection')

# ---------------------activity------------------------------------
from apis.activities import Open
api.add_resource(Open, '/activities', '/activities')
