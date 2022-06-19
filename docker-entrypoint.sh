#!/bin/bash

set -e

if [ $MIGRATIONS == 'true' ] ; then
    echo "Alembic migrations..."
    alembic upgrade heads
fi

exec "$@"
