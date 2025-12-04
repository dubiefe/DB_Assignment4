from social_network_api import Social_Network_API
from datetime import datetime, timedelta

username = "neo4j"
password = "neo4j123"

newAPI = Social_Network_API(username, password)

newAPI.cleanDatabase()

user = {"name":"Emilie", "email":"dubiefe@gmail.com", "age":20}
user2 = {"name":"Damien", "email":"dubiefe@gmail.com", "age":25}
user3 = {"name":"Thomas", "email":"dubiefe@gmail.com", "age":25}
user4 = {"name":"Claire", "email":"dubiefe@gmail.com", "age":20}
user5 = {"name":"David", "email":"dubiefe@gmail.com", "age":25}
user6 = {"name":"Cleo", "email":"dubiefe@gmail.com", "age":25}
user7 = {"name":"Romane", "email":"dubiefe@gmail.com", "age":20}
user8 = {"name":"Lucile", "email":"dubiefe@gmail.com", "age":25}
user9 = {"name":"Itziar", "email":"dubiefe@gmail.com", "age":25}
user10 = {"name":"Irel", "email":"dubiefe@gmail.com", "age":20}
ed = {"name":"IUT2", "email":"iut2@gmail.com"}
company = {"name":"Evenbright", "email":"evenbright@gmail.com"}
company2 = {"name":"Google", "email":"evenbright@gmail.com"}

newAPI.createUser("Test", **user)
newAPI.createUser("Person", **user)
newAPI.createUser("Person", **user2)
newAPI.createUser("Person", **user3)
newAPI.createUser("Person", **user4)
newAPI.createUser("Person", **user5)
newAPI.createUser("Person", **user6)
newAPI.createUser("Person", **user7)
newAPI.createUser("Person", **user8)
newAPI.createUser("Person", **user9)
newAPI.createUser("Person", **user10)
newAPI.createUser("Educational_Center", **ed)
newAPI.createUser("Company", **company)
newAPI.createUser("Company", **company2)

connection1 = {"endDate":2025, "startDate":2023}
connection2 = {"startDate":2022}

connections_to_create = [
    ("Test", "Emilie", "Damien"),
    ("Family", "Emilie", "Damien"),
    ("Work", "Emilie", "Damien"),
    ("Family", "Damien", "Thomas"),
    ("Family", "Claire", "Thomas"),
    ("Family", "David", "Emilie"),
    ("Friendship", "Emilie", "Romane"),
    ("Friendship", "Irel", "Lucile"),
    ("Work", "David", "Claire"),
    ("Academic", "Damien", "Romane"),
    ("Academic", "Damien", "Irel"),
    ("Academic", "Emilie", "Itziar"),
    ("Work", "Damien", "Itziar"),
    ("Work", "Cleo", "Claire"),
    ("Friendship", "Thomas", "Romane"),
    ("Family", "Claire", "David"),
    ("Work", "Emilie", "Claire"),
    ("Friendship", "Itziar", "Lucile"),
    ("Academic", "Romane", "Cleo"),
    ("Work", "Damien", "Claire"),
    ("Family", "Itziar", "Thomas"),
    ("Friendship", "David", "Romane"),
    ("Family", "Irel", "Itziar"),
    ("Academic", "Emilie", "Lucile"),
    ("Work", "Romane", "Claire"),
    ("Family", "Cleo", "David"),
    ("Friendship", "Thomas", "Irel"),
    ("Work", "Emilie", "Lucile"),
]

for relation_type, user1, user2 in connections_to_create:
    newAPI.createConnection(relation_type, user1, user2)

newAPI.createConnection("Studied", "Damien", "IUT2", **connection1)
newAPI.createConnection("Working", "Emilie", "Evenbright", **connection2)
newAPI.createConnection("Working", "Damien", "Evenbright", **connection2)
newAPI.createConnection("Working", "Thomas", "Google", **connection2)

result = newAPI.getUserRelatives("Emilie")
result2 = newAPI.getUserRelativesRelatives("Emilie")

#newAPI.createMessage("Emilie", "Damien", "2", "Hello!")
#newAPI.createMessage("Emilie", "Damien", "3", "Hello!")
#newAPI.createMessage("Emilie", "Damien", "2", "How are you?")
#newAPI.createMessage("Damien", "Emilie", "2", "Hi!")
#newAPI.createMessage("Damien", "Emilie", "2", "Fine and you?")
#newAPI.createMessage("Emilie", "Damien", "2", "Perfect, see you tomorrow!")

#result = newAPI.getMessageAfterDate("Emilie", "Damien", "2", datetime.now() - timedelta(milliseconds=100))
#result2 = newAPI.getConversation("Emilie", "Damien", "2")
 
#newAPI.createPublication("Emilie", "Test", "Yeah, it is working", ["Thomas", "Damien"])

#newAPI.getMentionnedCollegues("Emilie")

newAPI.getConnectionsHops('Emilie', "Irel", 3)

