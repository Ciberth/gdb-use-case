# Minimal example of Redis

## Use

```
juju deploy ../juju_repository/trusty/redis-proxy
juju deploy redis
juju add-relation redis redis-proxy

```

## Remarks

Host and uri return None when using interface, port returns 6397. Not working properly!
