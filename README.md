# Generic database service with use case

This repository is a bundle of layers (Juju) used in a research called "Management of polyglot persistent integrations with virtual administrators". In this research we followed a use case to create and determine a generic database service (virtual administrator) in the application modelling tool Juju. 

## Contents

- Generic database layer
- Generic database interface layer
- Data-app layer
- Webapp layer
- Minimal examples folder

The data-app and webapp layers are nothing more than small proof of concepts and set up an apache and generate config files based on whatever database technology they request. The use case itself consists of the webapp requesting multiple databases one of which is also used by the data-app. 


## Installation & Usage

(This charm is not available at the charm store as more support and optimisations are required.)

### Manual

0. Have a correct Juju installation and model at disposal + a $JUJU_REPOSITORY configured.
1. Clone this repository.
2. ``charm build data-app``
3. ``charm build webapp``
4. ``charm build generic-database``
5. Copy the generic-database interface layer to $JUJU_REPOSITORY/interfaces
6. 

```
juju deploy mysql
juju deploy postgresql
juju deploy pgbouncer

juju deploy $JUJU_REPOSITORY/<version>/generic-database db1
juju deploy $JUJU_REPOSITORY/<version>/generic-database db2
  
juju deploy $JUJU_REPOSITORY/<version>/data-app
juju deploy $JUJU_REPOSITORY/<version>/webapp
  
juju add-relation pgbouncer postgresql
juju add-relation pgbouncer:db db1
juju add-relation mysql db2

juju add-relation webapp db1
juju add-relation webapp db2

juju add-relation data-app db1

```
## Optimisations

### More database technologies

- MongoDB (right now you get dbhost + port + request databasename)
- Neo4J
- Cassandra
- ...

### Libjuju

Remove the prequirements of having existing services and relations but make it so that the generic database service is able to set up and manage the services themselves with the libjuju-library.


### Others

- Depending on the use case a new generic database administrator service might be appropriate or support for specific actions could be added. Things like **running a SQL-query, creating users, making backups**. These actions might also benefit from an abstraction.

- Right now the generic database service renders a config file depending on the requested database technology. This is only done once through the help of flags. It might be interesting to change this behaviour and make sure that the config file re-renders when changes occur.
