import pymongo as pm

class Mongo:
    def __init__(self):
        client = pm.MongoClient("mongodb+srv://admin:admin@newssummary.xjugy.azure.mongodb.net/NewsSumm?retryWrites=true&w=majority")
        db = client['News']
        print(db)
        collection = db['NewsSumm']
        print(collection)

    def inserInDB(self, collection, title, url, who, summary):
        new_insert = {"title": title,
                    "url": url,
                    "who": who,
                    "summary": summary}
        check = collection.insert_one(new_insert)
        print(check.inserted_id)
        
    def findAllDB(self, collection, country):
        query = {"country": country}
        results = collection.find(query)
        #returns a list of the results
        return results

    def deleteAllDB(self, collection):
        #delete all db right before update
        collection.delete_many({})
    

    
