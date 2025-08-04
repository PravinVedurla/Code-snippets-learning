"""
DOCKER COMPREHENSIVE GUIDE FOR INTERVIEW PREPARATION
=================================================

This guide contains detailed examples and explanations of Docker concepts
commonly asked in technical interviews. Each section includes:
- Core concepts explanation
- Code examples with detailed comments
- Best practices and common pitfalls
- Interview tips and frequently asked questions
"""

# =============================================================================
# 1. DOCKER BASICS
# =============================================================================

"""
Docker Basics - Core Concepts
----------------------------
Docker is a platform for developing, shipping, and running applications in containers.
Key features: isolation, portability, efficiency, and version control.

Common Interview Questions:
- What is Docker and how is it different from VMs?
- Explain Docker architecture
- What are containers and images?
- How do you create and manage Docker containers?
"""

# Basic Dockerfile Example
"""
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
"""

# Common Docker Commands
"""
# Build an image
docker build -t myapp .

# Run a container
docker run -d -p 8080:80 myapp

# List containers
docker ps

# Stop container
docker stop <container_id>

# Remove container
docker rm <container_id>

# List images
docker images

# Remove image
docker rmi <image_id>
"""

# =============================================================================
# 2. DOCKER NETWORKING
# =============================================================================

"""
Docker Networking
----------------
Docker provides several networking options to enable container communication.
Understanding networking is crucial for microservices architecture.

Common Interview Questions:
- What are Docker network types?
- How do containers communicate?
- Explain Docker network drivers
- How to isolate container networks?
"""

# Network Types
"""
1. Bridge Network (Default)
   - Isolated network on host
   - Containers can communicate
   - Port mapping for external access

2. Host Network
   - Container shares host's network
   - No network isolation
   - Better performance

3. None Network
   - No networking
   - Complete network isolation

4. Overlay Network
   - Multi-host networking
   - Used in Docker Swarm
"""

# Network Commands
"""
# Create network
docker network create mynetwork

# List networks
docker network ls

# Connect container to network
docker network connect mynetwork container1

# Inspect network
docker network inspect mynetwork

# Run container with network
docker run --network=mynetwork myapp
"""

# =============================================================================
# 3. DOCKER VOLUMES
# =============================================================================

"""
Docker Volumes
-------------
Volumes provide persistent storage for containers and enable data sharing.
Essential for stateful applications and databases.

Common Interview Questions:
- What are Docker volumes?
- Types of Docker volumes?
- How to share data between containers?
- Best practices for volume management?
"""

# Volume Types
"""
1. Named Volumes
   - Managed by Docker
   - Persistent across container lifecycle
   - Easy to backup and share

2. Bind Mounts
   - Maps host directory to container
   - Direct access to host filesystem
   - Good for development

3. tmpfs Mounts
   - Stored in host memory
   - Temporary storage
   - Secure sensitive information
"""

# Volume Commands
"""
# Create volume
docker volume create myvolume

# List volumes
docker volume ls

# Inspect volume
docker volume inspect myvolume

# Run container with volume
docker run -v myvolume:/data myapp

# Bind mount
docker run -v /host/path:/container/path myapp
"""

# =============================================================================
# 4. DOCKER COMPOSE
# =============================================================================

"""
Docker Compose
-------------
Tool for defining and running multi-container applications.
Uses YAML file to configure application services.

Common Interview Questions:
- What is Docker Compose?
- Benefits of using Docker Compose?
- How to define services in docker-compose.yml?
- Compose vs Dockerfile?
"""

# Docker Compose Example
"""
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    environment:
      FLASK_ENV: development
  redis:
    image: "redis:alpine"
  db:
    image: "postgres:13"
    environment:
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypassword
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
"""

# Compose Commands
"""
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Scale service
docker-compose up -d --scale web=3

# List containers
docker-compose ps
"""

# =============================================================================
# 5. DOCKER SECURITY
# =============================================================================

"""
Docker Security
--------------
Security is crucial for containerized applications.
Multiple layers of security from container to host.

Common Interview Questions:
- How to secure Docker containers?
- What are Docker security best practices?
- How to handle sensitive data?
- Container isolation techniques?
"""

# Security Best Practices
"""
1. Image Security
   - Use official images
   - Scan for vulnerabilities
   - Keep base images updated

2. Container Security
   - Run as non-root user
   - Limit container capabilities
   - Use read-only root filesystem

3. Runtime Security
   - Resource limits
   - Network segmentation
   - Regular security audits

4. Host Security
   - Secure Docker daemon
   - Update Docker regularly
   - Monitor container activities
"""

# Security Commands
"""
# Run container as non-root
docker run --user 1000:1000 myapp

# Set memory limit
docker run --memory=512m myapp

# Read-only root filesystem
docker run --read-only myapp

# Security scan
docker scan myimage
"""

# =============================================================================
# 6. DOCKER OPTIMIZATION
# =============================================================================

"""
Docker Optimization
------------------
Optimizing Docker images and containers for better performance.
Reduce size, improve build time, and enhance efficiency.

Common Interview Questions:
- How to optimize Docker images?
- Multi-stage builds explanation?
- Caching in Docker builds?
- Performance tuning techniques?
"""

# Multi-stage Build Example
"""
# Build stage
FROM node:14 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""

# Optimization Techniques
"""
1. Layer Optimization
   - Combine RUN commands
   - Use .dockerignore
   - Clean up in same layer

2. Base Image Selection
   - Use slim/alpine variants
   - Official images preferred
   - Minimal required packages

3. Build Cache
   - Order instructions properly
   - Copy dependencies first
   - Use build arguments wisely

4. Resource Management
   - Set resource limits
   - Monitor container stats
   - Regular cleanup
"""

# =============================================================================
# INTERVIEW TIPS AND BEST PRACTICES
# =============================================================================

"""
INTERVIEW TIPS AND COMMON QUESTIONS
=================================

1. Docker Basics:
   - Understand container vs VM differences
   - Know Docker architecture components
   - Explain image layers and caching
   - Dockerfile instructions and best practices

2. Networking:
   - Different network types and use cases
   - Container communication patterns
   - Network security and isolation
   - Docker DNS and service discovery

3. Storage:
   - Volume types and when to use each
   - Persistent data management
   - Backup and restore strategies
   - Storage drivers and performance

4. Docker Compose:
   - Multi-container application deployment
   - Service definition and configuration
   - Environment variables and secrets
   - Scaling and load balancing

5. Security:
   - Container isolation
   - Image security scanning
   - Runtime security
   - Access control and authentication

6. Performance:
   - Image optimization
   - Build optimization
   - Resource management
   - Monitoring and logging

7. Common Pitfalls:
   - Not using .dockerignore
   - Improper layer caching
   - Running as root
   - Ignoring security best practices

8. Best Practices:
   - Use official images
   - Implement health checks
   - Regular security updates
   - Proper logging and monitoring
"""

# =============================================================================
# PRACTICAL EXAMPLES
# =============================================================================

"""
Here are some practical examples commonly asked in interviews:

1. Basic Web Application
-----------------------
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]

2. Multi-stage Build
-------------------
# Dockerfile
FROM node:14 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

3. Docker Compose Stack
----------------------
version: '3'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/dbname
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

4. Secure Container
------------------
# Dockerfile
FROM python:3.9-slim
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser
CMD ["python", "app.py"]
"""

if __name__ == "__main__":
    print("Docker Interview Preparation Guide")
    print("This file contains examples and interview tips for Docker concepts")
