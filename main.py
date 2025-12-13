from social_network_api import Social_Network_API
from datetime import datetime, timedelta

username = "neo4j"
password = "neo4j123"

newAPI = Social_Network_API(username, password)

newAPI.cleanDatabase()

print("")
print("-------------------- Social Network API Test --------------------")

print("")
print("---------- I - User Test ----------")

print("")
print("----- A - User Creation -----")
print("")

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

print("")
print("----- B - Connection between Users Creation -----")
print("")

# Between Persons
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

connection1 = {"endDate":2025, "startDate":2023}
connection2 = {"startDate":2022}

# Between Person and Company or Eductaional centers
newAPI.createConnection("Studied", "Damien", "IUT2", **connection1)
newAPI.createConnection("Working", "Emilie", "Evenbright", **connection2)
newAPI.createConnection("Working", "Damien", "Evenbright", **connection2)
newAPI.createConnection("Working", "Thomas", "Google", **connection2)

print("")
print("----- C - Get users' relatives -----")
print("")

user = "Emilie"
resultRelatives = newAPI.getUserRelatives(user)
print("Relatives of Emilie: ", resultRelatives)

print("")
print("----- C - Get users' relatives' relatives -----")
print("")

user = "Emilie"
resultRelativesRelatives = newAPI.getUserRelativesRelatives(user)
print("Relatives' relatives of Emilie: ", resultRelativesRelatives)

print("")
print("---------- II - Messages Test ----------")

print("")
print("----- A - Create messages -----")
print("")

newAPI.createMessage("Emilie", "Damien", "2", "Hello!")
newAPI.createMessage("Emilie", "Damien", "3", "Hello!")
newAPI.createMessage("Emilie", "Damien", "2", "How are you?")
newAPI.createMessage("Damien", "Emilie", "2", "Hi!")
newAPI.createMessage("Damien", "Emilie", "2", "Fine and you?")
newAPI.createMessage("Emilie", "Damien", "2", "Perfect, see you tomorrow!")

newAPI.createMessage("Damien", "Irel", "4", "Hello!")
newAPI.createMessage("Irel", "Damien", "4", "Hello!")

newAPI.createMessage("Damien", "Itziar", "5", "Hello!")
newAPI.createMessage("Itziar", "Damien", "5", "Hello!")

newAPI.createMessage("Itziar", "Irel", "6", "Hello!")
newAPI.createMessage("Irel", "Itziar", "6", "Hello!")

newAPI.createMessage("Emilie", "Itziar", "7", "Hello!")


print("")
print("----- B - Get messages before date -----")
print("")

messagesBeforeDate = newAPI.getMessageAfterDate("Emilie", "Damien", "2", datetime.now() - timedelta(milliseconds=100))
print(f"Conversion n°2 between Emilie and Damien after {datetime.now() - timedelta(milliseconds=100)}:") 
for message in messagesBeforeDate:
    print(message)

print("")
print("----- C - Get all messages in one conversation -----")
print("")

messages = newAPI.getConversation("Emilie", "Damien", "2")
print(f"Conversion n°2 between Emilie and Damien:") 
for message in messages:
    print(message)

print("")
print("---------- III - Publications Test ----------")

print("")
print("----- A - Create Publication -----")
print("")

newAPI.createPublication("Emilie", "Hello World", "This is a new publication", ["Thomas", "Damien"])

print("")
print("----- B - Get mentionned collegues in Publication -----")
print("")

mentionnedCollegues = newAPI.getMentionnedCollegues("Emilie")
print("Mentionned collegues in Emilie's publication: ", mentionnedCollegues)

print("")
print("---------- IV - Connections Test ----------")

print("")
print("----- A - Connection Hops -----")
print("")

user = 'Emilie'
user2 = 'Irel'
nb_hops = 3
connectionsHops = newAPI.getConnectionsHops(user, user2, nb_hops)
print(f"All connections of maximum {nb_hops} hops between {user} and {user2}: ")
for connection in connectionsHops:
    print(connection)

nb_msgs = 1
connectionsWithMessages = newAPI.getConnectionsWithMessages(user, user2, nb_msgs)
print(f"All connections of minimum {nb_msgs} messages between {user} and {user2}: ")
for connection in connectionsWithMessages:
    print(connection)

# Close Neo4j driver and session
newAPI.close()
