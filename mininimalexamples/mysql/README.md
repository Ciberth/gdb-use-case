# Minimal example of Mysql

## Use

```
juju deploy mysql
juju deploy mysql-proxy
juju add-relation mysql:db mysql-proxy:mysql-shared
juju add-relation mysql:db-admin mysql-proxy:mysql-root
```

## Remarks

- Same for mariadb (normally, not tested)
- So this is a bit an odd thing. There are three interfaces (mysql, mysql-shared, mysql-root). Imo they should all become one. The mysql interface should have an option to request a database with at least a databasename (and maybe a username) and an optional parameter should indicate if the user should be an admin. Another possibility is the feature to give a list of hosts where the user is allowed to operate on/from.