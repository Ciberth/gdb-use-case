# Minimal example of Postgres

## Use

```
juju deploy ../juju_repository/trusty/postgres-proxy
juju deploy postgresql
juju deploy pgbouncer
juju add-relation pgbouncer postgresql
juju add-relation postgresql postgres-proxy

```

## Remarks

- Pgbouncer needed other remote charm can't access, only postgres-proxy can access due to host auth (pg_hba.conf). A config on postgresql allows to edit this but impossible in an automated way so pgbouncer is still needed.

