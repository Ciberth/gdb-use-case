#!/usr/bin/python

import pwd
import os
from subprocess import call
from charmhelpers.core import host, hookenv
from charmhelpers.core.hookenv import log, status_set, config
from charmhelpers.core.templating import render
from charms.reactive import when, when_not, set_flag, clear_flag, when_file_changed, endpoint_from_flag
from charms.reactive import Endpoint

# Apache

@when('apache.available')
def finishing_up_setting_up_sites():
    host.service_reload('apache2')
    set_flag('apache.start')

@when('apache.start')
@when_not('webapp.mysql.configured')
def ready():
    host.service_reload('apache2')
    status_set('active', 'apache ready/waiting relation')

# Mysql requests (2 phases)

## 1. Request a db through mysql-shared interface
## 2. Requast a root user through mysql-root interface

### 1.

@when('mysql-shared.connected')
@when_not('webapp.mysqlshared.configured')
def request_mysql_db():
    log('--- IN REQUEST SHARED')
    mysql_endpoint = endpoint_from_flag('mysql-shared.connected')
    mysql_endpoint.configure('proxy_mysql_db2', 'proxy_mysql_user2', prefix="proxy")
    status_set('maintenance', 'Requesting mysql db')


@when('mysql-shared.available')
@when_not('webapp.mysql.configured')
def render_mysql_config():   
    mysql_endpoint = endpoint_from_flag('mysql-shared.available')
    
    render('mysql-config.j2', '/var/www/mysql-proxy/mysql-config.html', {
        'db_pass': mysql_endpoint.password("proxy"),
        'db_dbname': mysql_endpoint.database("proxy"),
        'db_host': mysql_endpoint.db_host(),
        'hostname': mysql_endpoint.hostname("proxy"),
        'db_user': mysql_endpoint.username("proxy"), # note no port :/
    })
    log('--- NA RENDER SHARED')

    host.service_reload('apache2')
    set_flag('webapp.mysqlshared.configured')
    status_set('active', 'mysql shared done!')

### 2. 

@when('mysql-root.connected')
@when_not('webapp.mysqlroot.configured')
def request_mysql_root_user():
    status_set('maintenance', 'Requesting mysql root user')

@when('mysql-root.available')
@when_not('webapp.mysqlroot.configured')
def render_mysql_root_config():
    mysqlroot_endpoint = endpoint_from_flag('mysql-root.available')

    render('mysql-config.j2', '/var/www/mysql-proxy/mysql-root-config.html', {
        'db_pass': mysqlroot_endpoint.password(),
        'db_dbname': mysqlroot_endpoint.database(),
        'db_host': mysqlroot_endpoint.host(),
        'db_user': mysqlroot_endpoint.user(),
        'db_port': mysqlroot_endpoint.port(),
    })

    log('--- NA RENDER ROOT')
    host.service_reload('apache2')
    set_flag('webapp.mysqlroot.configured')
    status_set('active', 'mysql-root done!')
    

@when('webapp.mysqlshared.configured', 'webapp.mysqlroot.configured')
def set_flag_mysql_is_done():
    host.service_reload('apache2')
    log('--- BEIDE FLAGS AND SET 1 FLAG')
    set_flag('webapp.mysql.configured')
