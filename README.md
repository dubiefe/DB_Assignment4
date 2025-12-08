# Advanced Databases - Assignment 4

College project for Advanced Databases at U-TAD

Authors:

- Emilie Dubief
- Itziar Morales Rodríguez

Toolset:

- Python (3.12)
- Neo4j

## Project structure

- The function for the API are in the file social_network_api
- To test these function, launch the file main.py

```
project_root/
|-- main.py
|-- README.md
|-- social_network_api.py
```

## Project definition

### Database schema

To build the API for the social network, we defined the following database schema.
Each part will be detailed afterward.

![Complete database](./database_images/2_complete_database.png)
*Complete database schema*

#### Users Person

The social network will be constitute of different types of users, the first one is :User:Person.
This type represents the users of the social network with the following attributes:

![Node Person](./database_images/1_nodes_person.png)

These users can have connections with other :User:Person.
These connections are represented bellow:

![Connection Users](./database_images/3_user.png)

The connection message is a bit differente from the other because it has attributes:
  - convId -> The id of the conversation where the message belongs
  - seqNb  -> The sequance number of the message, for the order of the message in the conversation
  - date   -> The date when the message was send
  - from   -> The name of the user who send the message

#### Users Educational_Center

This type of user represent the education centers of the social network, they have the following attributes.

![Node Educational_Center](./database_images/1_nodes_ed.png)

These users can only have connections with other :User:Person.
These connections are represented bellow:

![Connection Educational_Center](./database_images/5_ed.png)

These connections all have date attributes defining when the :User:Person spent in the educational center.

#### Users Company

This type of user represent the companies of the social network, they have the following attributes.

![Node Company](./database_images/1_nodes_company.png)

These users can only have connections only with other :User:Person.
These connections are represented bellow:

![Connection Company](./database_images/6_company.png)

These connections all have date attributes defining when the :User:Person spent in the company.

#### Publication

Finally, :User:Person can make :Publication in the social network, they have the following attributes:

![Node Publication](./database_images/1_nodes_publication.png)

:Publication can only have connections with other :User:Person.
These connections are represented bellow:

![Connection Publication](./database_images/4_publication.png)

The connection :Mentionned must be between a :Publication and the :User:Person mentionned in the attributes <mentions>.
The connection :Published must be between the :User:Person who made the publication and the :Publication.

### Social Network API



## Issues & Exceptions

