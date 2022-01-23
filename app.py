from flask import Flask, url_for, redirect, render_template, abort, request, flash, jsonify
from flask_restful import Api

from flask_caching import Cache
from flask_cors import CORS, cross_origin
from flask_executor import Executor


server = Flask(__name__)

server.config['SECRET_KEY'] = b'C\x1a!\xa2Q\xbd\xf5\xfdDx\xd0\x8e\x0c\x16\x04\x82'


api = Api(server)
executor = Executor(server)
cache = Cache(server, config={'CACHE_TYPE': 'simple'})

server.config['CORS_HEADERS'] = 'Content-Type'

server.app_context().push()


# ---------------------nft------------------------------------
from apis.nfts import NftOrderbook
api.add_resource(NftOrderbook, '/nft-orderbook', '/nft-orderbook')

# ---------------------nft------------------------------------
from apis.collection import Collection
api.add_resource(Collection, '/collection', '/collection')

