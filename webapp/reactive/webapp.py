#!/usr/bin/python

import pwd
import os
from subprocess import call
from charmhelpers.core import host
from charmhelpers.core.hookenv import log, status_set, config
from charmhelpers.core.templating import render
from charms.reactive import when, when_not, set_flag, clear_flag, when_file_changed, endpoint_from_flag
from charms.reactive import Endpoint

###########################################################################
#                                                                         #
# Installation of apache + waiting for generic-database (provider) charm  #
#                                                                         #
###########################################################################

@when('apache.available')
def finishing_up_setting_up_sites():
    host.service_reload('apache2')
    set_flag('apache.start')


@when('apache.start')
@when_not('postgresdb.configured', 'mysqldb.configured', 'mongodb.configured')
def waiting_for_db():
    host.service_reload('apache2')
    status_set('maintenance', 'Waiting for at least 1 generic database relation')

@when_not('postgresdb.configured')
def waiting_for_db1():
    status_set('maintenance', 'Waiting for gdb (postgres) relation')

@when_not('mysqldb.configured')
def waiting_for_db2():
    status_set('maintenance', 'Waiting for gdb (mysql) relation')

@when_not('mongodb.configured')
def waiting_for_db3():
    status_set('maintenance', 'Waiting for gdb (mongo) relation')

########################################################################
#                                                                      #
# Request of database technology to generic-database (provider charm)  #
#                                                                      #
########################################################################


@when('endpoint.postgresqlgdb.joined')
@when_not('postgresdb.configured')
def request_postgresql_db():
    endpoint = endpoint_from_flag('endpoint.postgresqlgdb.joined')
    endpoint.request('postgresql', 'dbitems99')
    status_set('maintenance', 'Requesting postgresql gdb')

@when('endpoint.mysqlgdb.joined')
@when_not('mysqldb.configured')
def request_mysql_db():
    endpoint = endpoint_from_flag('endpoint.mysqlgdb.joined')
    endpoint.request('mysql', 'dbusers99')
    status_set('maintenance', 'Requesting mysql gdb')

@when('endpoint.mongogdb.joined')
@when_not('mongodb.configured')
def request_mongo_db():
    endpoint = endpoint_from_flag('endpoint.mongogdb.joined')
    endpoint.request('mongodb', 'dbmongo99')
    status_set('maintenance', 'Requesting mongo gdb')


##################################################
#                                                #
# Request successful, get data and render config # 
#                                                #
##################################################


@when('endpoint.postgresqlgdb.available')
@when_not('postgresdb.configured')
def pgsql_render_config():
    
    pgsql = endpoint_from_flag('endpoint.postgresqlgdb.available')

    render('db-config.j2', '/var/www/webapp/postgresql-config.html', {
        'gdb_host' : pgsql.host(),
        'gdb_port' : pgsql.port(),
        'gdb_dbname' : pgsql.databasename(),
        'gdb_user' : pgsql.user(),
        'gdb_password' : pgsql.password(),
    })
    status_set('maintenance', 'Rendering config file')
    set_flag('postgresdb.configured')
    set_flag('restart-app')

@when('endpoint.mysqlgdb.available')
@when_not('mysqldb.configured')
def mysql_render_config():
    
    mysql = endpoint_from_flag('endpoint.mysqlgdb.available')

    render('db-config.j2', '/var/www/webapp/mysql-config.html', {
        'gdb_host' : mysql.host(),
        'gdb_port' : mysql.port(),
        'gdb_dbname' : mysql.databasename(),
        'gdb_user' : mysql.user(),
        'gdb_password' : mysql.password(),
    })
    status_set('maintenance', 'Rendering config file')
    set_flag('mysqldb.configured')
    set_flag('restart-app')

@when('endpoint.mongogdb.available')
@when_not('mongodb.configured')
def mongo_render_config():
    
    mongo = endpoint_from_flag('endpoint.mongogdb.available')

    render('db-config.j2', '/var/www/webapp/mongo-config.html', {
        'gdb_host' : mongo.host(),
        'gdb_port' : mongo.port(),
    })
    status_set('maintenance', 'Rendering config file')
    set_flag('mongodb.configured')
    set_flag('restart-app')

@when('restart-app')
def restart_app():
    host.service_reload('apache2')
    clear_flag('restart-app')
    status_set('active', 'Apache restarted')

@when('postgresdb.configured','mysqldb.configured','mongodb.configured')
def all_flags_set():
    status_set('active', 'Webapp configured!')
    set_flag('webapp.configured')
    

