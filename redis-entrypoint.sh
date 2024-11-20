#!/bin/bash

# Ensure the directory for redis.conf exists
mkdir -p /usr/local/etc/redis

# Generate redis.conf with dynamic username and password
cat <<EOF > /usr/local/etc/redis/redis.conf
# Default user settings
user default off

# Custom user settings
user $REDIS_USER on >$REDIS_PASSWORD ~* +@all

# Bind to all network interfaces (optional)
bind 0.0.0.0

# Port to listen on
port 6379
EOF

# Start Redis with the generated configuration
exec redis-server /usr/local/etc/redis/redis.conf