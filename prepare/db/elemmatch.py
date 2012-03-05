a = { "foo" : [
    {
        "shape":"square",
        "color":"red",
        "thick":True
        },
    {
        "shape":"circle",
        "color":"red",
        "thick":True
        }
    ] }


b = { "foo" : [
    {
        "shape":"square",
        "color": "red",
        "thick": True
        },
    {
        "shape": "square",
        "color": "purple",
        "thick": False
        }
    ] 
}

import pymongo
print a, b
db = pymongo.Connection("127.0.0.1", 27017).app
db.test.em.save(a)
db.test.em.save(b)

