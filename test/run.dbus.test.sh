#!/bin/bash

SERVICE_SCRIPT=dbus-motion-service.py
CLIENT_SCRIPT=dbus-motion-client.py

./$SERVICE_SCRIPT &
DBUS_PID=$!
echo "DBUS PID: $DBUS_PID"
./$CLIENT_SCRIPT
kill $DBUS_PID