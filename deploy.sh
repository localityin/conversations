#!/bin/bash

# Define the profile name
PROFILE="inference_services"

# Step 1: Bring down containers for the specified profile
echo "🛑 Stopping and removing all containers with profile '${PROFILE}'..."
docker-compose --profile $PROFILE down

# Step 2: Remove unused Docker images, networks, and volumes (optional)
echo "🧹 Removing dangling images, unused volumes, and networks..."
docker system prune -f

# Step 3: Build and start containers with the specified profile
echo "🚀 Building and starting containers with profile '${PROFILE}'..."
docker-compose --profile $PROFILE up --build -d

# Completion message
echo "✅ Deployment complete! 🚢"