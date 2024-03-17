# MongoDB Username: wjy8023tvxq
# Password: TWUENGkvWGjFiFWq

from flask_pymongo import PyMongo


def get_db(app):
    # MongoDB configuration
    CONNECTION_STRING = "mongodb+srv://wjy8023tvxq:TWUENGkvWGjFiFWq@playground.mcdxani.mongodb.net/HistoUI"
    app.config["MONGO_URI"] = CONNECTION_STRING
    mongo = PyMongo(app)
    return mongo.db

def insert_feedback(db, feedback_data):
    feedback_collection = db.feedback
    feedback_collection.insert_one(feedback_data)

def get_feedback_all(db):
    feedback_collection = db.feedback

    # fetch data from the feedback collection
    feedback_data = feedback_collection.find({})
    feedback_list = list(feedback_data)

    # convert the object id to string
    for feedback in feedback_list:
        feedback["_id"] = str(feedback["_id"])

    return feedback_list

def get_feedback_by_query(db, feedback_query):
    feedback_collection = db.feedback
    feedback_data = feedback_collection.find(feedback_query)
    feedback_list = list(feedback_data)

    # convert the object id to string
    for feedback in feedback_list:
        feedback["_id"] = str(feedback["_id"])

    return feedback_list

def get_feedback_by_field(db, query, projection):
    feedback_collection = db.feedback
    feedback_data = feedback_collection.find(query, projection)
    feedback_list = list(feedback_data)
    return feedback_list