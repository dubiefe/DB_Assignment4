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
     -- Users --
    createUser(self, type, **kwargs)
        Create user according to the given type and attributes
    createConnection(self, type, userFrom, userTo, **kwargs)
        Create connections between users according to the given type and attributes
    getUserRelatives(self, user) : set[str]
        Get all the relatives of a selected user:Person (only the connections :Family)
    getUserRelativesRelatives(self, user) : set[str]
        Get all the relatives' relatives of a selected user:Person (only the connections :Family)
     -- Messages --
    createMessage(self, userFrom, userTo, convId, content)
        Create a connection :Message between two users with the given attributes
    getMessageAfterDate(self, user1, user2, convId, date) -> set[str]
        Get all the messages of a conversation send after the given date
    getConversation(self, user1, user2, convId) -> set[str]
        Get all the messages of a conversation 
     -- Publications --
    createPublication(self, user, title, body, mentions)
        Create a publication and all the connections linked to it
    getMentionnedCollegues(self, user) -> set[str]
        Get all the collegues mentionned in publication by the given user
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
        ## Check if the user type is allowed
        if type not in self._allowed_users_types:
            print("The user type must be one of these: ", self._allowed_users_types)
        ## Create the new user
        else:
            self._session.execute_write(lambda tx: tx.run(
                f"CREATE (n:User:{type} $props)", 
                props=kwargs
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
        ## Check if the connection type is allowed
        if type not in self._allowed_users_connections_types:
            print("The connection type must be one of these: ", self._allowed_users_connections_types)
        ## Create the new connection
        else:
            self._session.execute_write(lambda tx: tx.run(
                f"MATCH (n:User {{name: '{userFrom}'}}), (m:User {{name: '{userTo}'}}) CREATE (n)-[:{type} $props]->(m)", 
                props=kwargs
            ))
            print(f"New connection :{type} added between {userFrom} and {userTo}")
    
    def getUserRelatives(self, user) -> set[str]:
        """
        Get the name of the user:Person connected to the user with a :Family connection

        Parameters:
        -----------
        user: str
            String with the name of the user

        Return:
        -------
        ['No relatives"] if the user doesn't have relatives
        Or a dictionary with the names of all the user's relatives
        """
        ## Fetch the user's relatives
        user_relatives = self._session.execute_write(
            lambda tx: tx.run(
                f"match (n:User:Person {{name: $name}})-[:Family]->(m:User:Person) return m", 
                name=user
        ).data())
        ## Check the result
        if user_relatives:
            users = [record["m"]["name"] for record in user_relatives]
            print(f"Relatives of {user}: ", users)
            return users
        else:
            print(f"No relatives found for {user}")
            return ["No relatives"]

    def getUserRelativesRelatives(self, user) -> set[str]:
        """
        Get the name of the user:Person connected to another user:Person with a :Family connection and who also is connected to the user with a :Family connection

        Parameters:
        -----------
        user: str
            String with the name of the user

        Return:
        -------
        ['No relatives' relatives"] if the user doesn't have relatives' relatives
        Or a dictionary with the names of all the user's relatives' relatives
        """
        ## Fetch the user's relatives' relatives
        user_relatives_relatives = self._session.execute_write(
            lambda tx: tx.run(
                f"match (n:User:Person {{name: $name}})-[:Family]->(m:User:Person)-[:Family]->(o:User:Person) return o", name=user
        ).data())
        ## Check the result
        if user_relatives_relatives:
            users = [record["o"]["name"] for record in user_relatives_relatives]
            print(f"Relatives' relatives of {user}: ", users)
            return users
        else:
            print(f"No relatives' relatives found for {user}")
            return ["No relatives' relatives"]

    ## Messages
    def createMessage(self, userFrom, userTo, convId, content):
        """
        Create a :Message connection between userFrom and userTo
        The :Message has an attribute convId, content and seqNb
        The last one is determined by all the messages in the same conversation already whared between the two users

        Parameters:
        -----------
        userFrom: str
            String with the name of the user who is sending the message
        userTo: str
            String with the name of the user who is receiving the message
        convId: str
            String with the id of the conversation where the message belongs
        content: str
            String with the content of the message send
        """
        ## Look for all the previous messages in the conversation
        messages_send = self._session.execute_write(
            lambda tx: tx.run(
                f"match (n:User:Person)-[c:Message]->(m:User:Person) where c.convId = $convId and ((n.name = $name1 and m.name = $name2) or (m.name = $name1 and n.name = $name2)) return c", 
                name1=userFrom, name2=userTo, convId=convId
        ).data())
        ## Calculate the sequence number based on the number of already send messages
        seqNb = len(messages_send) + 1
        ## Create the new message
        self._session.execute_write(lambda tx: tx.run(
            f"MATCH (n:User {{name: '{userFrom}'}}), (m:User {{name: '{userTo}'}}) CREATE (n)-[:Message $props]->(m)", 
            props={"convId":convId, "content":content, "date":datetime.now(), "seqNb": seqNb}
        ))
        print(f"New :Message added between {userFrom} and {userTo}")

    def getMessageAfterDate(self, user1, user2, convId, date) -> set[str]:
        """
        Get the messages between two users with the given convId after the given date

        Parameters:
        -----------
        user1: str
            String with the name of one of the user involved in the conversation
        user2: str
            String with the name of the other user involved in the conversation
        convId: str
            String with the id of the conversation
        date: Date
            Date with the minimum date for the messages

        Return:
        -------
        ["No conversation"] if no messages are found
        Or a dictionary with all the messages send in the conversation after the date
        """
        ## Fetch the messages after the date
        messages_after_date = self._session.execute_write(
            lambda tx: [
                record["c"]._properties
                for record in tx.run(
                f"match (n:User:Person)-[c:Message {{convId: $convId}}]->(m:User:Person) where c.date > $date and ((n.name = $name1 and m.name = $name2) or (m.name = $name1 and n.name = $name2)) return c", 
                name1=user1, convId=convId, name2=user2, date=date
        )]) 
        ## Sort the messages by the sequence number
        messages_after_date.sort(key=lambda x: x['seqNb'])
        print(f"Conversion n°{convId} between {user1} and {user2} after {date}:")
        ## Deal with the messages' data
        messages_after_date_final = []
        for result in messages_after_date:
            ## Store it in a dictionnary for return
            messages_after_date_final.append(f"{result['seqNb']}: {result['content']}")
            ## Print it
            print(f"{result['seqNb']}: {result['content']}")
        if messages_after_date_final:
            return messages_after_date_final
        else:
            return ["No conversation"]

    def getConversation(self, user1, user2, convId) -> set[str]:
        """
        Get all the messages between two users with the given convId

        Parameters:
        -----------
        user1: str
            String with the name of one of the user involved in the conversation
        user2: str
            String with the name of the other user involved in the conversation
        convId: str
            String with the id of the conversation

        Return:
        -------
        ["No conversation"] if no messages are found
        Or a dictionary with all the messages send in the conversation
        """
        ## Fetch all the messages
        messages = self._session.execute_write(
            lambda tx: [
                record["c"]._properties
                for record in tx.run(
                f"match (n:User:Person)-[c:Message {{convId: $convId}}]->(m:User:Person) where ((n.name = $name1 and m.name = $name2) or (m.name = $name1 and n.name = $name2)) return c", 
                name1=user1, convId=convId, name2=user2
        )]) 
        ## Sort the messages by the sequence number
        messages.sort(key=lambda x: x['seqNb'])
        print(f"Conversion n°{convId} between {user1} and {user2}:")
        ## Deal with the messages' data
        messages_final = []
        for result in messages:
            ## Store it in a dictionnary for return
            messages_final.append(f"{result['seqNb']}: {result['content']}")
            ## Print it
            print(f"{result['seqNb']}: {result['content']}")
        if messages_final:
            return messages_final
        else:
            return ["No conversation"]
        
    ## Publications
    def createPublication(self, user, title, body, mentions):
        """
        Create a publication with the given title, body and mentions
        Create :Published connection between the user and the publication
        Create :Mentioned connections between the publication and all the users in the mentions

        Parameters:
        -----------
        user: str
            String with the name of the user who made the publication
        title: str
            String with the title of the publication
        body: str
            String with the body of the publication
        mentions: set[str]
            Set of Strings with the names of the users mentioned in the publication
        """
        ## Create publication and link with author
        self._session.execute_write(lambda tx: tx.run(
            f"match (n:User:Person {{name: $name}}) create (n)-[:Published]->(m:Publication $props)",
            name=user, props={"title":title, "body":body, "mentions":mentions}
        ))
        print(f"New :Publication created titled '{title}' and published by {user}")
        ## Create connections :Mentioned between publication and user in mentions
        for mention in mentions:
            self._session.execute_write(lambda tx: tx.run(
                f"match (n:User:Person {{name: $name}}), (p:Publication {{title: $title}}) create (p)-[:Mentionned]->(n)",
                name=mention, title=title
            ))
            print(f"New :Mentionned created between :Publication titled '{title}' and published by {user}, and {mention}") 

    def getMentionnedCollegues(self, user) -> set[str]:
        """
        Get all user's collegues mentionned in one of their publication

        Parameters:
        -----------
        user: str
            String with the name of the user

        Return:
        -------
        ["No mentionned collegues"] if no collegues are found
        Or a dictionary with all the collegues' names mentionned in a publication
        """
        ## Get collegues mentionned in a publication of the user
        collegues = self._session.execute_write(lambda tx: tx.run(
            f"match (:User:Person {{name: $name}})-[:Working]->(c:User:Company) ,(:User:Person {{name: $name}})-[:Published]->(:Publication)-[:Mentionned]->(m:User:Person)-[:Working]->(:User:Company {{name: c.name}}) return m",
            name=user
        ).data())
        ## Deal with the collegues' data
        collegues_final = []
        for collegue in collegues:
            ## Store the collegue's name
            collegues_final.append(collegue['m']['name'])
        ## Display and return the result
        if collegues_final:
            print(f"Mentionned collegues of {user}: ", collegues_final)
            return collegues_final
        else:
            print(f"No mentionned collegues found for {user}")
            return ["No mentionned collegues"]

            



        
 
        
