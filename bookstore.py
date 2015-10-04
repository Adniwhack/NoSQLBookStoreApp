__author__ = 'GP60'

#imports are here
from function import *  #defined functions
import flask

#database connects
graph = neo4j_connect()
db = mongo_connect()


print(get_recommended(60, datetime(2014, 10,22), graph))


#main front-end serer manipulation starts here