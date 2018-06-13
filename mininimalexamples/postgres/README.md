# Minimal example of Redis

## Use

```
juju deploy ../juju_repository/trusty/redis-proxy
juju deploy redis
juju add-relation redis redis-proxy

```

## Remarks

