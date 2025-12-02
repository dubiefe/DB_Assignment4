from neo4j import GraphDatabase

class Social_Network_API:

    _uri = "neo4j://localhost:7687"
    _driver = None
    _session = None
    _allowed_users_types = ["Person", "Company", "Educational_Center"]
    _allowed_users_connections_types = ["Family", "Work", "Friendship", "Academic", "Studied", "Studying", "Worked", "Working"]

    def __init__(self, username, password):
        """
        Initialize the connection with neo4j
        """
        self._driver = GraphDatabase.driver(self._uri, auth=(username, password))
        self._session = self._driver.session()

    def cleanDatabase(self):
        self._session.execute_write(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))
        print("Database cleaned")

    ## Users
    def createUser(self, type, **kwargs):
        if type not in self._allowed_users_types:
            print("The user type must be one of these: ", self._allowed_users_types)
        else:
            self._session.execute_write(lambda tx: tx.run(
                f"CREATE (n:User:{type} $props)", props=kwargs
            ))
            print(f"New :User:{type} added named {kwargs["name"]}")
    
    def createConnection(self, type, userFrom, userTo, **kwargs):
        if type not in self._allowed_users_connections_types:
            print("The connection type must be one of these: ", self._allowed_users_connections_types)
        else:
            self._session.execute_write(lambda tx: tx.run(
                f"MATCH (n:User {{name: '{userFrom}'}}), (m:User {{name: '{userTo}'}}) CREATE (n)-[:{type} $props]->(m)", props=kwargs
            ))
            print(f"New connection :{type} added between {userFrom} and {userTo}")
    
    def getUserRelatives(self, user):
        result = self._session.execute_write(
            lambda tx: tx.run(
                f"match (n:User:Person {{name: $name}})-[:Family]->(m:User:Person) return m", name=user
        ).data())
        if result:
            users = [record["m"]["name"] for record in result]
            print(f"Relatives of {user}: ", users)
        else:
            print(f"No realtives found for {user}")

    def getUserRelativesRelatives(self, user):
        result = self._session.execute_write(
            lambda tx: tx.run(
                f"match (n:User:Person {{name: $name}})-[:Family]->(m:User:Person)-[:Family]->(o:User:Person) return o", name=user
        ).data())
        if result:
            users = [record["o"]["name"] for record in result]
            print(f"Relatives' relatives of {user}: ", users)
        else:
            print(f"No realtives' relatives found for {user}")
        
 
        
