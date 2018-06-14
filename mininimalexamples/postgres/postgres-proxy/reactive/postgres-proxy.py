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
def ready():
    host.service_reload('apache2')
    status_set('active', 'apache ready - gdb not concrete')

# Postgres requests 

@when('pgsql.connected')
@when_not('webapp.pgsql.configured')
def request_postgresql_db():
    pgsql_endpoint = endpoint_from_flag('pgsql.connected')
    pgsql_endpoint.set_database("postgresproxydb")
    status_set('maintenance', 'Requesting pgsql db')


@when('pgsql.master.available')
@when_not('webapp.pgsql.configured')
def render_pgsql_config():   
    pgsql_endpoint = endpoint_from_flag('pgsql.master.available')
    
    render('postgres-config.j2', '/var/www/postgres-proxy/postgres-config.html', {
        'db_master': pgsql_endpoint.master,
        'db_pass': pgsql_endpoint.master['password'],
        'db_dbname': pgsql_endpoint.master['dbname'],
        'db_host': pgsql_endpoint.master['host'],
        'db_user': pgsql_endpoint.master['user'],
        'db_port': pgsql_endpoint.master['port'],
    })

    host.service_reload('apache2')
    set_flag('webapp.pgsql.configured')
    status_set('active', 'Apache/Proxy ready!')
