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

# Mongo request <-- only host port for now as mongo creates when needed

@when('mongodb.connected')
def request_mongodb():
    mongodb_ep = endpoint_from_flag('mongodb.connected')
    mongodb_connection = mongodb_ep.connection_string()

    render('mongo-config.j2', '/var/www/mongo-proxy/mongo-config.html', {
        'db_host': mongodb_connection.split(':')[0],
        'db_port': mongodb_connection.split(':')[1],
    })