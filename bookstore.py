__author__ = 'GP60'

#imports are here
from function import *  #defined functions
import flask

#database connects
graph = neo4j_connect()
db = mongo_connect()

#main front-end serer manipulation starts here