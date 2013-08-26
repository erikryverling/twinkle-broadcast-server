#!/bin/bash
SCRIPT_DIR=$(dirname $(readlink -f "$BASH_SOURCE"))

cd $SCRIPT_DIR/../twinkle-broadcast-server
python broadcastserver.py "$@"
