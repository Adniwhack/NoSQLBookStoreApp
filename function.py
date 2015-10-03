__author__ = 'GP60'

import pymongo
from pymongo import MongoClient
from random import randint
from datetime import date
from py2neo import Node, Relationship
from py2neo import Graph


def mongo_connect():
    try:
        conn = pymongo.MongoClient()
        print("Connected Successfully!")
        client = MongoClient('localhost', 27017)

        db = client.bookstore
        return db
    except (pymongo.errors.ConnectionFailure, e):
        print ("Could not connect to MongoDB: %s" % e )


def neo4j_connect():

    graph = Graph("http://localhost:7474/db/data/")
    return graph


def create_customer(Customer_ID, Customer_Name , graph):
    query = "CREATE (n: Customer {id : '" + str(Customer_ID) + "', name : '" + Customer_Name + "'}) return n;"
    print(query)
    customer = graph.cypher.execute(query)
    return customer

def create_book(Book_ID, Book_Name, Book_Author, Book_Category, Book_CategoryID, graph):
    query = ""