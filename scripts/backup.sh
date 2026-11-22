#!/bin/bash
set -euo pipefail
umask 077

if [ "$(hostname)" != "viikko1-webservu" ]; then
    echo "ERROR: Wrong server"
    exit 1
fi

STAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG="/home/ubuntu/week4-backup.log"

if rsync -a \
    -e "ssh -i /home/ubuntu/.ssh/week4_backup_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes" \
    /var/www/html/ \
    "week4backup@192.168.1.148:/srv/backups/server-a/$STAMP/" \
    >> "$LOG" 2>&1
then
    echo "$(date -Is) SUCCESS: $STAMP" >> "$LOG"
else
    echo "$(date -Is) FAILED: $STAMP" >> "$LOG"
    exit 1
fi
