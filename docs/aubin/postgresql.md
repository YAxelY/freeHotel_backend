## login in the database

not recommended to use PGPASSWORD yet it's fast for testing purpose

    PGPASSWORD=securepass123 psql -h localhost -U hotel_user -d hotel_db

## Useful psql Commands (Run from inside psql)
Command	What it does

Command | What it does
\dt | List tables
\d tableName | Show table structure
\l | List databases
\c dbName | Connect to a DB
\du | List users/roles
\q | Quit psql