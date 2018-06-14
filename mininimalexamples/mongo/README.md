# Minimal example of Mongo

## Use

```
juju deploy mongo
juju deploy ../juju_repository/trusty/mongo-proxy
juju add-relation mongo mongo-proxy
```

## Remarks

Only host + port available
