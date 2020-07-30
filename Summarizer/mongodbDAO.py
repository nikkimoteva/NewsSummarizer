import pymongo as pm

class Mongo:
    def __init__(self):
        getClient = self.get_client()
        self.client = pm.MongoClient(getClient)
        getDB = self.get_db()
        self.db = self.client[getDB]
        getCollection = self.get_collection()
        self.collection = self.db[getCollection]

    def get_client(self):
        return "mongodb+srv://admin:admin@newssummary.xjugy.azure.mongodb.net/NewsSumm?retryWrites=true&w=majority"
    
    def get_db(self):
        return "News"

    def get_collection(self):
        return 'NewsSumm'

    def getSession(self):
        return self.collection

    def inserInDB(self, title, url, who, summary):
        collection = self.getSession()
        new_insert = {"title": title,
                    "url": url,
                    "who": who,
                    "summary": summary}
        check = collection.insert_one(new_insert)
        print(check.inserted_id)
        
    def findAllDB(self, collection, country):
        collection = self.getSession()
        query = {"country": country}
        results = collection.find(query)
        #returns a list of the results
        return results

    def deleteAllDB(self):
        collection = self.getSession()
        #delete all db right before update
        collection.delete_many({})

    def closeConnection(self):
        self.client.close()
    

    
