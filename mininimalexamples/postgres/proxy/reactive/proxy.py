#!/usr/bin/python

import pwd
import os
from subprocess import call
from charmhelpers.core import host, hookenv
from charmhelpers.core.hookenv import log, status_set, config
from charmhelpers.core.templating import render
from charms.reactive import when, when_not, set_flag, clear_flag, when_file_changed, endpoint_from_flag
from charms.reactive import Endpoint

# Redis requests 

@when('redis.available')
@when_not('webapp.redis.configured')
def write_redis_configs():
    status_set('maintenance', 'Rendering redis details')

    redis_ep = endpoint_from_flag('redis.available')
    redis_db = redis_ep.redis_data()[0]

    # Available: redis_db['host'], redis_db['uri'], redis_db['port'], redis_db['password']

    render('redis-config.j2', '/var/www/proxy/redis-config.html', {
        'host': redis_db['host'],
        'uri': redis_db['uri'],
        'port': redis_db['port'],
        'password': redis_db['password'],
    })

    host.service_reload('apache2')
    set_state('webapp.redis.configured')
    status_set('active', 'Apache/Proxy ready!')
