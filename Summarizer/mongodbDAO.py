import pymongo as pm

class Mongo:
    def __init__(self):
        getClient = self.GetClient()
        self.client = pm.MongoClient(getClient)
        getDB = self.GetDB()
        self.db = self.client[getDB]
        getCollection = self.GetCollection()
        self.collection = self.db[getCollection]

    def GetClient(self):
        return "mongodb+srv://admin:admin@newssummary.xjugy.azure.mongodb.net/NewsSumm?retryWrites=true&w=majority"
    
    def GetDB(self):
        return "News"

    def GetCollection(self):
        return 'NewsSumm'

    def GetSession(self):
        return self.collection

    def InserInDB(self, country, title, url, whoWhenWhere, summary, tone):
        collection = self.GetSession()
        newInsert = {
                    "country": country,
                    "title": title,
                    "url": url,
                    "who/when/where": whoWhenWhere,
                    "summary": summary,
                    "tone: ": tone}
        collection.insert_one(newInsert)
        
    def FindAllDB(self, country):
        collection = self.GetSession()
        results = collection.find({"country": country})
        #returns a list of the results
        return results

    def DeleteAllDB(self):
        collection = self.GetSession()
        #delete all db right before update
        collection.delete_many({})

    def CloseConnection(self):
        self.client.close()
    

    
