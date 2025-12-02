from neo4j import GraphDatabase
from datetime import datetime

class Social_Network_API:
    """
    Social_Network_API class
    social network database in Neo4j

    Attributes
    ----------
    _uri
        url to the Neo4j database
    _driver
        driver of the database
    _session
        session where the database is running
    _allowed_users_types : set[str]
        all allowed Users labels
    _allowed_users_connections_types : set[str]
        all allowed Connections labels

    Methods
    -------
    cleanDatabase(self)
        Delete everything in the database
    createUser(self, type, **kwargs)
        Create user according to the given type and attributes
    createConnection(self, type, userFrom, userTo, **kwargs)
        Create connections between users according to the given type and attributes
    getUserRelatives(self, user) : set[str]
        Get all the relatives of a selected user:Person (only the connections :Family)
    getUserRelativesRelatives(self, user) : set[str]
        Get all the relatives' relatives of a selected user:Person (only the connections :Family)
    createMessage(self, userFrom, userTo, convId, content)
        Create a connection :Message between two users with the given attributes
    getMessageAfterDate(self, user1, user2, convId, date) -> set[str]
        Get all the messages of a conversation send after the given date
    getConversation(self, user1, user2, convId) -> set[str]
        Get all the messages of a conversation 
    """

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
        """
        Delete all elements in the database
        """
        self._session.execute_write(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))
        print("Database cleaned")

    ## Users
    def createUser(self, type, **kwargs):
        """
        Create a new user according to the type given with the given attributes
        Check if the user type is allowed

        Parameters:
        -----------
        type: str
            String with the type of user to create
        kwargs: dict[str, str | dict]
            Dictionnary with all the data linked with the new user
        """
        if type not in self._allowed_users_types:
            print("The user type must be one of these: ", self._allowed_users_types)
        else:
            self._session.execute_write(lambda tx: tx.run(
                f"CREATE (n:User:{type} $props)", props=kwargs
            ))
            print(f"New :User:{type} added named {kwargs["name"]}")
    
    def createConnection(self, type, userFrom, userTo, **kwargs):
        """
        Create a new connection between users according to the type given with the given attributes
        Check if the connection type is allowed

        Parameters:
        -----------
        type: str
            Type of user to create
        userFrom: str
            Name of the user at the start of the connection
        userTo: str
            Name of the user at the end of the connection
        kwargs: dict[str, str | dict]
            Dictionnary with all the data linked with the new user
        """
        if type not in self._allowed_users_connections_types:
            print("The connection type must be one of these: ", self._allowed_users_connections_types)
        else:
            self._session.execute_write(lambda tx: tx.run(
                f"MATCH (n:User {{name: '{userFrom}'}}), (m:User {{name: '{userTo}'}}) CREATE (n)-[:{type} $props]->(m)", props=kwargs
            ))
            print(f"New connection :{type} added between {userFrom} and {userTo}")
    
    def getUserRelatives(self, user) -> set[str]:
        """
        Login to a session in redis according to the username
        Create a token with a lifetime of 1 month
        Return the privilege of the user and the token

        Parameters:
        -----------
        user: str
            String with the name of the user

        Return:
        -------
        ['No relatives"] if the user doesn't have relatives
        Or a dictionary with the names of all the user's relatives
        """
        result = self._session.execute_write(
            lambda tx: tx.run(
                f"match (n:User:Person {{name: $name}})-[:Family]->(m:User:Person) return m", name=user
        ).data())
        if result:
            users = [record["m"]["name"] for record in result]
            print(f"Relatives of {user}: ", users)
            return users
        else:
            print(f"No relatives found for {user}")
            return ["No relatives"]

    def getUserRelativesRelatives(self, user) -> set[str]:
        """
        Login to a session in redis according to the username
        Create a token with a lifetime of 1 month
        Return the privilege of the user and the token

        Parameters:
        -----------
        username: str
            String with the username of the session we want to login
        password: str
            String with the password of the session we want to login

        Return:
        -------
        -1 if the connection data are not good
        Or a dictionary with the privilege and the token of the user
        """
        result = self._session.execute_write(
            lambda tx: tx.run(
                f"match (n:User:Person {{name: $name}})-[:Family]->(m:User:Person)-[:Family]->(o:User:Person) return o", name=user
        ).data())
        if result:
            users = [record["o"]["name"] for record in result]
            print(f"Relatives' relatives of {user}: ", users)
            return users
        else:
            print(f"No relatives' relatives found for {user}")
            return ["No relatives' relatives"]

    ## Messages
    def createMessage(self, userFrom, userTo, convId, content):
        """
        Login to a session in redis according to the username
        Create a token with a lifetime of 1 month
        Return the privilege of the user and the token

        Parameters:
        -----------
        username: str
            String with the username of the session we want to login
        password: str
            String with the password of the session we want to login

        Return:
        -------
        -1 if the connection data are not good
        Or a dictionary with the privilege and the token of the user
        """
        result1 = self._session.execute_write(
            lambda tx: tx.run(
                f"match (n:User:Person)-[c:Message]->(m:User:Person) where c.convId = $convId and ((n.name = $name1 and m.name = $name2) or (m.name = $name1 and n.name = $name2)) return c", 
                name1=userFrom, name2=userTo, convId=convId
        ).data())
        seqNb = len(result1) + 1
        self._session.execute_write(lambda tx: tx.run(
            f"MATCH (n:User {{name: '{userFrom}'}}), (m:User {{name: '{userTo}'}}) CREATE (n)-[:Message $props]->(m)", props={"convId":convId, "content":content, "date":datetime.now(), "seqNb": seqNb}
        ))
        print(f"New :Message added between {userFrom} and {userTo}")

    def getMessageAfterDate(self, user1, user2, convId, date) -> set[str]:
        """
        Login to a session in redis according to the username
        Create a token with a lifetime of 1 month
        Return the privilege of the user and the token

        Parameters:
        -----------
        username: str
            String with the username of the session we want to login
        password: str
            String with the password of the session we want to login

        Return:
        -------
        -1 if the connection data are not good
        Or a dictionary with the privilege and the token of the user
        """
        results = self._session.execute_write(
            lambda tx: [
                record["c"]._properties
                for record in tx.run(
                f"match (n:User:Person)-[c:Message {{convId: $convId}}]->(m:User:Person) where c.date > $date and ((n.name = $name1 and m.name = $name2) or (m.name = $name1 and n.name = $name2)) return c", 
                name1=user1, convId=convId, name2=user2, date=date
        )]) 
        results.sort(key=lambda x: x['seqNb'])
        print(f"Conversion n°{convId} between {user1} and {user2} after {date}:")
        resultsFinal = []
        for result in results:
            resultsFinal.append(f"{result['seqNb']}: {result['content']}")
            print(f"{result['seqNb']}: {result['content']}")
        if resultsFinal:
            return resultsFinal
        else:
            return ["No conversation"]

    def getConversation(self, user1, user2, convId) -> set[str]:
        """
        Login to a session in redis according to the username
        Create a token with a lifetime of 1 month
        Return the privilege of the user and the token

        Parameters:
        -----------
        username: str
            String with the username of the session we want to login
        password: str
            String with the password of the session we want to login

        Return:
        -------
        -1 if the connection data are not good
        Or a dictionary with the privilege and the token of the user
        """
        results = self._session.execute_write(
            lambda tx: [
                record["c"]._properties
                for record in tx.run(
                f"match (n:User:Person)-[c:Message {{convId: $convId}}]->(m:User:Person) where ((n.name = $name1 and m.name = $name2) or (m.name = $name1 and n.name = $name2)) return c", 
                name1=user1, convId=convId, name2=user2
        )]) 
        results.sort(key=lambda x: x['seqNb'])
        print(f"Conversion n°{convId} between {user1} and {user2}:")
        resultsFinal = []
        for result in results:
            resultsFinal.append(f"{result['seqNb']}: {result['content']}")
            print(f"{result['seqNb']}: {result['content']}")
        if resultsFinal:
            return resultsFinal
        else:
            return ["No conversation"]
        
 
        
