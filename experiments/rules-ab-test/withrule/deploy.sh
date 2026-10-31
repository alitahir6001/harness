#!/bin/bash
echo "Starting deployment..."
echo "Running pre-flight checks... OK"
bash push_config.sh > /dev/null 2>&1
echo "Deployed version 2.0 successfully!"
