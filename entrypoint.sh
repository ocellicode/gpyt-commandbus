#!/bin/bash
set -euo pipefail

if [ -v MIGRATE ]; then
    alembic upgrade head
fi

exec waitress-serve gpyt_commandbus.injection.injector:app
