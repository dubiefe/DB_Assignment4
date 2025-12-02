from social_network_api import Social_Network_API

username = "neo4j"
password = "neo4j123"

newAPI = Social_Network_API(username, password)

newAPI.cleanDatabase()

user = {"name":"Emilie", "email":"dubiefe@gmail.com", "age":20}
user2 = {"name":"Damien", "email":"dubiefe@gmail.com", "age":25}
user3 = {"name":"Thomas", "email":"dubiefe@gmail.com", "age":25}
ed = {"name":"IUT2", "email":"iut2@gmail.com"}
company = {"name":"Evenbright", "email":"evenbright@gmail.com"}

newAPI.createUser("Test", **user)
newAPI.createUser("Person", **user)
newAPI.createUser("Person", **user2)
newAPI.createUser("Person", **user3)
newAPI.createUser("Educational_Center", **ed)
newAPI.createUser("Company", **company)

connection1 = {"endDate":2025, "startDate":2023}
connection2 = {"startDate":2022}

newAPI.createConnection("Test", "Emilie", "Damien")
newAPI.createConnection("Family", "Emilie", "Damien")
newAPI.createConnection("Family", "Damien", "Thomas")
newAPI.createConnection("Studied", "Damien", "IUT2", **connection1)
newAPI.createConnection("Working", "Emilie", "Evenbright", **connection2)

newAPI.getUserRelatives("Emilie")
newAPI.getUserRelativesRelatives("Emilie")





