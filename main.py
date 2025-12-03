from social_network_api import Social_Network_API
from datetime import datetime, timedelta

username = "neo4j"
password = "neo4j123"

newAPI = Social_Network_API(username, password)

newAPI.cleanDatabase()

user = {"name":"Emilie", "email":"dubiefe@gmail.com", "age":20}
user2 = {"name":"Damien", "email":"dubiefe@gmail.com", "age":25}
user3 = {"name":"Thomas", "email":"dubiefe@gmail.com", "age":25}
ed = {"name":"IUT2", "email":"iut2@gmail.com"}
company = {"name":"Evenbright", "email":"evenbright@gmail.com"}
company2 = {"name":"Google", "email":"evenbright@gmail.com"}

newAPI.createUser("Test", **user)
newAPI.createUser("Person", **user)
newAPI.createUser("Person", **user2)
newAPI.createUser("Person", **user3)
newAPI.createUser("Educational_Center", **ed)
newAPI.createUser("Company", **company)
newAPI.createUser("Company", **company2)

connection1 = {"endDate":2025, "startDate":2023}
connection2 = {"startDate":2022}

newAPI.createConnection("Test", "Emilie", "Damien")
newAPI.createConnection("Family", "Emilie", "Damien")
newAPI.createConnection("Family", "Damien", "Thomas")
newAPI.createConnection("Studied", "Damien", "IUT2", **connection1)
newAPI.createConnection("Working", "Emilie", "Evenbright", **connection2)
newAPI.createConnection("Working", "Damien", "Evenbright", **connection2)
newAPI.createConnection("Working", "Thomas", "Google", **connection2)

result = newAPI.getUserRelatives("Emilie")
result2 = newAPI.getUserRelativesRelatives("Emilie")

newAPI.createMessage("Emilie", "Damien", "2", "Hello!")
newAPI.createMessage("Emilie", "Damien", "3", "Hello!")
newAPI.createMessage("Emilie", "Damien", "2", "How are you?")
newAPI.createMessage("Damien", "Emilie", "2", "Hi!")
newAPI.createMessage("Damien", "Emilie", "2", "Fine and you?")
newAPI.createMessage("Emilie", "Damien", "2", "Perfect, see you tomorrow!")

result = newAPI.getMessageAfterDate("Emilie", "Damien", "2", datetime.now() - timedelta(milliseconds=100))
result2 = newAPI.getConversation("Emilie", "Damien", "2")
 
newAPI.createPublication("Emilie", "Test", "Yeah, it is working", ["Thomas", "Damien"])

newAPI.getMentionnedCollegues("Emilie")

