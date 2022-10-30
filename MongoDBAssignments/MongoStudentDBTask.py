------------Question 1------------
data = db.studdet
for x in db.studdet.aggregate([
    {"$addFields": {
    "Totalmarks":{"$sum": "$scores.score"}}},
 { "$sort": { "Totalmarks": -1 }},
  { "$limit" : 1},
{ "$project": {
    "_id": 0,
    "name": 1
    }
 }
]):
  print (x)
  

-------------Question 2--------------
db.collection.aggregate([
  {
    "$unwind": "$scores"
  },
  {
    "$match": {
      "scores.type": "exam",
      
    }
  },
  {
    "$group": {
      "_id": "null",
      students: {
        "$push": "$$ROOT"
      },
      avg: {
        "$avg": "$scores.score"
      }
    }
  },
  {
    $project: {
      _id: 0,
      students: {
        $filter: {
          input: "$students",
          cond: {
            $and: [
              {
                $lt: [
                  "$$this.scores.score",
                  "$avg"
                ]
              },
              {
                $gt: [
                  "$$this.scores.score",
                  40
                ]
              }
            ]
          }
        }
      }
    }
  }
])