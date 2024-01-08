#!/bin/sh

# Wait for Elasticsearch to be up and running
/wait-for-it.sh elasticsearch:9200 --timeout=60 --strict -- echo "Elasticsearch is up"

# Bootstrap the database
bootstrap --config /schema.json

# Run pgsync in daemon mode
pgsync --config /schema.json --daemon
