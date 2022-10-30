import pymongo

#connecting with mongodb
client = pymongo.MongoClient("mongodb+srv://ajay96:1234@cluster0.7phm1vl.mongodb.net/?retryWrites=true&w=majority")
db = client.TelephoneDirectory
details = db.teldetails


#insert_one
data = {"name" : "Jacob", "phoneNum" : 8136794125, "place" : "Banglore"}
details.insert_one(data) 


#Inserting multiple data
data1 = [
    {"name" : "Ajay", "phoneNum" : 8138023676, "place" : "Kochi"},
    {"name" : "Veerendra", "phoneNum" : 9765123875, "place" : "Kolkata"},
    {"name" : "Jobin", "phoneNum" : 7234098616, "place" : "Kolkata"},
    {"name" : "Matt", "phoneNum" : 9734721888, "place" : "Banglore"},
    {"name" : "Jason", "phoneNum" : 7620987661, "place" : "Banglore"},
    {"name" : "Jeniffer", "phoneNum" : 9078561234, "place" : "Manglore"},
    {"name" : "Dewin", "phoneNum" : 7856124598, "place" : "Guwahati"},
    {"name" : "Rishika", "phoneNum" : 9456127836, "place" : "Kochi"}
]

details.insert_many(data1)


#printing the data updated
for x in details.find():
  print(x)


#finding the data in which place startswith letter "M"
for x in details.find({"place":{"$regex":"^M"}}):
  print(x)


#update_one
dat = {"name":"Radhika"}
new_val = {"$set":{"phoneNum": 8138092654}}
query = details.update_one(dat, new_val)
for x in details.find():
  print(x)


#update_many
dat = {"place":"Mysore"}
new_val = {"$set":{"place": "Coimbatore"}}
query = details.update_many(dat, new_val)
for x in details.find({},{"_id":0}):
  print(x)


#delete_one
query = {"phoneNum" : 8134670916}
details.delete_one(query)
for x in details.find():
  print(x)


#delete_many
query = {"place" : "Banglore"}
details.delete_many(query)
for x in details.find():
  print(x)
