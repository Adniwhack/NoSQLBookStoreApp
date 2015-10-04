__author__ = 'GP60'

import pymongo
from pymongo import MongoClient
from random import randint
from datetime import *
import time
from py2neo import Node, Relationship
from py2neo import Graph
from operator import itemgetter

# neo4j Data retrieval done in x.properties[<property name>]

def mongo_connect():
    try:
        conn = pymongo.MongoClient()
        print("Connected Successfully!")
        client = MongoClient('localhost', 27017)

        db = client.bookstore
        return db
    except (pymongo.errors.ConnectionFailure, e):
        print("Could not connect to MongoDB: %s" % e)


def neo4j_connect():
    graph = Graph("http://localhost:7474/db/data/")
    return graph


def create_customer(Customer_ID, Customer_Name, graph):
    query = "CREATE (n: Customer {id : '" + str(Customer_ID) + "', name : '" + Customer_Name + "'}) return n;"
    # print(query)
    customer = graph.cypher.stream(query)
    return customer


def create_book(Book_ID, Book_Name, Book_Category, graph):
    query1 = "CREATE (N: Book {Book_id : '" + str(Book_ID) + "', Book_name : '" + Book_Name + "' }) return N"

    x = get_category(Book_Category,graph)
    if x == None:

        queryi = "Create (N : Category {category_name : '"+Book_Category+"'}) Return N"
        graph.cypher.execute(queryi)
    query2 = "MATCH (N:Book {Book_id : '" + str(Book_ID) + "'}), (M: Category {category_name : '" + Book_Category + "'}) CREATE (N)-[:belongs_to]->(M)"
    graph.cypher.execute(query1)



    graph.cypher.execute(query2)


def get_book(Book_ID, graph):#Mongo
    query = "MATCH (N:Book {Book_id : '" + str(Book_ID) + "'}) return N"
    result = graph.cypher.stream(query)
    listx= []
    for i in result:
        listx.append(i[0])
    if listx == []:
        return None
    return listx[0]

def get_category(Category, graph):
    query = "MATCH(n:Category{category_name : '"+Category+"'}) return n"
    result = graph.cypher.stream(query)
    listx= []
    for i in result:
        listx.append(i[0])
    if listx == []:
        return None
    return listx[0].properties


def get_customer(Customer_ID, graph):#Mongo
    query = "MATCH (N:Customer {id : '" + str(Customer_ID) + "'}) return N"
    result = graph.cypher.stream(query)

    listx= []
    for i in result:
        listx.append(i[0])
    if listx == []:
        return None
    return listx[0].properties

def customer_buy_book(Customer_ID, Book_ID, quantity, cost, date, graph): #date must be in datetime format

    date = int(time.mktime(date.timetuple()))
    query = "match (n:Customer{id:'"+str(Customer_ID)+"'}), (m:Book{Book_id: '"+str(Book_ID)+"' }) create (n)-[:Buy {quantity: "+str(quantity)+", cost : "+str(cost)+", date : "+str(date)+"}]->(m) "
    print(query)
    result = graph.cypher.execute(query)
    return result


def get_invoice_details():
    return False


def get_recommended(Customer_ID,date,  graph): #date must be in datetime format

    date = int(time.mktime(date.timetuple()))

    query = "match (n:Customer{id:'" + str(Customer_ID) + "'})-[buy]->(x : Book),(x)-->(cat:Category),(cat)<--(book: Book) where "+str(date)+" - buy.date < 2505600 and "+str(date)+" - buy.date > 0 return distinct book"
    print(query)
    result = graph.cypher.stream(query)
    retlist = []
    for i in result:
        retlist.append(i[0].properties)
    return retlist


def get_total_income(time_init,  graph,time_end=datetime(1970, 1,1)):#date must be in datetime format

    time_init = int(time.mktime(time_init.timetuple()))
    #time_end = int(time.mktime(time_end.timetuple()))
    query = "match(n:Customer)-[b]->() where b.date < "+str(time_init)+"  and "+str(time_init)+" - b.date  <  2505600   return n.name,sum(b.cost), sum(b.quantity)"
    print(query)
    result = graph.cypher.stream(query)
    retlist = []
    for i in result:
        retlist.append([i[0], i[1], i[2]])
    sorted(retlist, key=itemgetter(2))
    return retlist


