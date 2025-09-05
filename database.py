from pymongo import MongoClient
from bson.objectid import ObjectId

class DataBase:
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017/")
        db = client['new_database']
        self.collection = db.get_collection('mail_storage')  

    def insertOne(self, sender, reciever, cc, subject, date, body, category, auto_reply, urgency):
        id = self.collection.insert_one({'sender': sender, 
                                         'reciever':reciever, 
                                         'Cc': cc, 
                                         'subject':subject, 
                                         'date':date, 
                                         'body':body, 
                                         'category':category, 
                                         'auto_reply':auto_reply,
                                         'urgency':urgency,
                                         'status':'unread'}).inserted_id
        return id
    
    def fetchAll(self):
        cursor = self.collection.find()
        mails = []
        for mail in cursor:
            mails.append(mail)
        return mails

    def get_email_by_id(self, email_id):
        try:
            mail = self.collection.find_one({'_id': ObjectId(email_id)})
            return mail
        except Exception:
            return None



