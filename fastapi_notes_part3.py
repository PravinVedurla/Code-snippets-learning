"""
FASTAPI COMPREHENSIVE GUIDE - PART 3
====================================

This file completes the FastAPI interview preparation guide with:
- Deployment (Uvicorn, Docker, Kubernetes)
- Testing with TestClient
- Background Tasks
- Performance Optimization (async, caching, DB queries, load balancing)
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import uvicorn
import pytest
from unittest.mock import Mock, patch
import asyncio
import time
import redis
from functools import lru_cache
import os
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy import text
from fastapi_notes.database import AsyncSessionLocal
from fastapi_notes.security import create_access_token
from email.mime.text import MIMEText
import smtplib

# =============================================================================
# 7. DEPLOYMENT (UVICORN, DOCKER, KUBERNETES)
# =============================================================================

"""
Deployment Strategies
--------------------
FastAPI applications can be deployed using various methods:
- Uvicorn for development and simple deployments
- Docker for containerized deployments
- Kubernetes for orchestrated deployments

Interview Questions:
- How to deploy a FastAPI application?
- Explain the difference between development and production servers
- How to configure Uvicorn for production?
- What are the benefits of containerization?
- How to handle environment variables in production?
- How to implement health checks?
"""

# Uvicorn configuration
def run_development_server():
    """
    Development server configuration
    Interview Tip: Use uvicorn.run() for development, gunicorn for production
    """
    uvicorn.run(
        "fastapi_notes:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        workers=1     # Multiple workers for production
    )

# Production configuration example
"""
Production deployment with Gunicorn:
gunicorn fastapi_notes:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
"""

# Environment configuration
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Environment configuration using Pydantic
    Interview Tip: Use Pydantic Settings for type-safe configuration
    """
    app_name: str = "FastAPI Interview Prep"
    debug: bool = False
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your-secret-key"
    redis_url: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Health check endpoint
def health_check():
    """
    Health check endpoint for load balancers
    Interview Tip: Always implement health checks for production
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": "production" if not settings.debug else "development"
    }

# Dockerfile example (commented out as it's not Python code)
"""
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run the application
CMD ["uvicorn", "fastapi_notes:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# Docker Compose example (commented out as it's not Python code)
"""
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=dbname
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web

volumes:
  postgres_data:
"""

# Kubernetes deployment example (commented out as it's not Python code)
"""
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
      - name: fastapi-app
        image: fastapi-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        livenessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
"""

# =============================================================================
# 8. TESTING WITH TESTCLIENT
# =============================================================================

"""
Testing with TestClient
-----------------------
FastAPI provides TestClient for testing applications without running a server.
It's built on top of requests and allows for comprehensive API testing.

Interview Questions:
- How to test FastAPI applications?
- What is TestClient and how does it work?
- How to test authentication in FastAPI?
- Explain unit testing vs integration testing
- How to mock dependencies in tests?
- How to test file uploads?
"""

# Create test client
def create_test_client():
    """
    Create test client for FastAPI application
    Interview Tip: TestClient simulates HTTP requests without running a server
    """
    from fastapi import FastAPI
    app = FastAPI()
    
    # Add some test endpoints
    @app.get("/")
    def read_root():
        return {"Hello": "World"}
    
    @app.get("/users/{user_id}")
    def read_user(user_id: int):
        return {"user_id": user_id}
    
    return TestClient(app)

client = create_test_client()

# Basic test examples
def test_read_main():
    """
    Basic endpoint test
    Interview Tip: Always test both success and error cases
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_user():
    """
    Test path parameters
    """
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["user_id"] == 1

def test_get_user_invalid():
    """
    Test error handling
    """
    response = client.get("/users/-1")
    assert response.status_code == 422  # Validation error

# Testing with authentication
def test_protected_route_without_auth():
    """
    Test protected route without authentication
    """
    # This would test a protected endpoint
    # response = client.get("/users/me/")
    # assert response.status_code == 401
    pass

def test_protected_route_with_auth():
    """
    Test protected route with authentication
    Interview Tip: Mock authentication for testing
    """
    # Create a mock token
    # token = create_access_token(data={"sub": "johndoe"})
    # headers = {"Authorization": f"Bearer {token}"}
    # response = client.get("/users/me/", headers=headers)
    # assert response.status_code == 200
    pass

# Testing file uploads
def test_upload_file():
    """
    Test file upload endpoint
    """
    test_file_content = b"test file content"
    files = {"file": ("test.txt", test_file_content, "text/plain")}
    
    # response = client.post("/upload-file/", files=files)
    # assert response.status_code == 200
    # assert response.json()["filename"] == "test.txt"
    pass

# Testing with mocked dependencies
@patch('fastapi_notes.get_database')
def test_db_items(mock_get_db):
    """
    Test with mocked database dependency
    Interview Tip: Use unittest.mock for dependency injection testing
    """
    # Mock database response
    mock_db = Mock()
    mock_db.get_items.return_value = [{"id": 1, "name": "Test Item"}]
    mock_get_db.return_value = mock_db
    
    # response = client.get("/db-items/")
    # assert response.status_code == 200
    # assert response.json() == [{"id": 1, "name": "Test Item"}]
    pass

# Pytest fixtures example
@pytest.fixture
def test_client():
    """
    Pytest fixture for test client
    Interview Tip: Use fixtures for common test setup
    """
    return create_test_client()

@pytest.fixture
def auth_headers():
    """
    Fixture for authentication headers
    """
    # token = create_access_token(data={"sub": "johndoe"})
    # return {"Authorization": f"Bearer {token}"}
    return {"Authorization": "Bearer test-token"}

def test_with_fixtures(test_client, auth_headers):
    """
    Test using fixtures
    """
    # response = test_client.get("/users/me/", headers=auth_headers)
    # assert response.status_code == 200
    pass

# Integration test example
def test_full_user_workflow():
    """
    Integration test for complete user workflow
    Interview Tip: Test complete workflows, not just individual endpoints
    """
    # 1. Create user
    # user_data = {"username": "testuser", "email": "test@example.com"}
    # response = client.post("/users/", json=user_data)
    # assert response.status_code == 201
    # user_id = response.json()["id"]
    
    # 2. Get user
    # response = client.get(f"/users/{user_id}")
    # assert response.status_code == 200
    # assert response.json()["username"] == "testuser"
    
    # 3. Update user
    # update_data = {"email": "updated@example.com"}
    # response = client.put(f"/users/{user_id}", json=update_data)
    # assert response.status_code == 200
    
    # 4. Delete user
    # response = client.delete(f"/users/{user_id}")
    # assert response.status_code == 204
    pass

# =============================================================================
# 9. BACKGROUND TASKS
# =============================================================================

"""
Background Tasks in FastAPI
---------------------------
FastAPI provides BackgroundTasks for running operations after response is sent.
Useful for: email sending, file processing, database cleanup, etc.

Interview Questions:
- What are background tasks and when to use them?
- How do background tasks work in FastAPI?
- Difference between background tasks and async tasks?
- How to handle background task failures?
- How to implement task queues?
"""

# Background task functions
def send_email_background(email: str, message: str):
    """
    Background task for sending emails
    Interview Tip: Background tasks run after response is sent
    """
    # Simulate email sending
    print(f"Sending email to {email}: {message}")
    # In real app, use proper email service
    # smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    # smtp_server.starttls()
    # smtp_server.login('your_email@gmail.com', 'your_password')
    # msg = MIMEText(message)
    # msg['Subject'] = 'Notification'
    # msg['From'] = 'your_email@gmail.com'
    # msg['To'] = email
    # smtp_server.send_message(msg)

def process_file_background(filename: str):
    """
    Background task for file processing
    """
    print(f"Processing file: {filename}")
    # Simulate file processing
    time.sleep(5)
    print(f"File {filename} processed successfully")

def cleanup_database_background():
    """
    Background task for database cleanup
    """
    print("Cleaning up database...")
    # Simulate database cleanup
    time.sleep(2)
    print("Database cleanup completed")

# Endpoints with background tasks
def send_notification(
    email: str,
    message: str,
    background_tasks: BackgroundTasks
):
    """
    Send notification with background email task
    Interview Tip: Background tasks don't block the response
    """
    background_tasks.add_task(send_email_background, email, message)
    return {"message": "Notification will be sent in background"}

def upload_and_process(
    file: bytes,
    filename: str,
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Upload file and process it in background
    """
    # Save file immediately
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    file_path = upload_dir / filename
    
    with open(file_path, "wb") as buffer:
        buffer.write(file)
    
    # Add background processing task
    background_tasks.add_task(process_file_background, filename)
    
    return {
        "message": "File uploaded and processing started",
        "filename": filename
    }

def register_user(
    user_data: dict,
    background_tasks: BackgroundTasks
):
    """
    User registration with multiple background tasks
    Interview Tip: You can add multiple background tasks
    """
    # Create user (simulated)
    new_user = {
        "id": 1,
        "username": user_data["username"],
        "email": user_data["email"],
        "is_active": True,
        "created_at": datetime.now()
    }
    
    # Add multiple background tasks
    background_tasks.add_task(
        send_email_background,
        user_data["email"],
        f"Welcome {user_data['username']}!"
    )
    background_tasks.add_task(cleanup_database_background)
    
    return {
        "message": "User registered successfully",
        "user": new_user,
        "background_tasks": ["welcome_email", "db_cleanup"]
    }

# Background task with error handling
def risky_background_task():
    """
    Background task that might fail
    Interview Tip: Always handle exceptions in background tasks
    """
    try:
        # Simulate risky operation
        import random
        if random.random() < 0.5:
            raise Exception("Random failure")
        print("Background task completed successfully")
    except Exception as e:
        print(f"Background task failed: {e}")
        # In real app, log to monitoring service

def risky_operation(background_tasks: BackgroundTasks):
    """
    Endpoint with error-prone background task
    """
    background_tasks.add_task(risky_background_task)
    return {"message": "Risky operation started in background"}

# =============================================================================
# 10. PERFORMANCE OPTIMIZATION
# =============================================================================

"""
Performance Optimization in FastAPI
-----------------------------------
FastAPI applications can be optimized for:
- Database query optimization
- Caching strategies
- Async operations
- Load balancing
- Connection pooling

Interview Questions:
- How to optimize FastAPI application performance?
- What caching strategies can you implement?
- How to optimize database queries?
- Explain connection pooling
- How to implement load balancing?
- How to monitor performance?
"""

# Redis cache setup
redis_client = redis.Redis.from_url(settings.redis_url)

# Caching utilities
def get_cache_key(prefix: str, **kwargs) -> str:
    """
    Generate cache key
    Interview Tip: Use consistent cache key patterns
    """
    key_parts = [prefix]
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}:{v}")
    return ":".join(key_parts)

async def get_cached_data(key: str, ttl: int = 300):
    """
    Get data from cache
    """
    try:
        data = redis_client.get(key)
        return data.decode() if data else None
    except Exception as e:
        print(f"Cache error: {e}")
        return None

async def set_cached_data(key: str, data: str, ttl: int = 300):
    """
    Set data in cache
    """
    try:
        redis_client.setex(key, ttl, data)
    except Exception as e:
        print(f"Cache error: {e}")

# LRU Cache example
@lru_cache(maxsize=128)
def expensive_calculation(n: int) -> int:
    """
    Expensive calculation with LRU cache
    Interview Tip: Use @lru_cache for function-level caching
    """
    # Simulate expensive calculation
    time.sleep(1)
    return n * n

# Database query optimization
async def get_user_optimized(user_id: int):
    """
    Optimized database query with connection pooling
    Interview Tip: Use connection pooling for database efficiency
    """
    # Simulate database query
    # async with AsyncSessionLocal() as session:
    #     # Use proper indexing and limit results
    #     query = text("""
    #         SELECT id, username, email, created_at 
    #         FROM users 
    #         WHERE id = :user_id 
    #         LIMIT 1
    #     """)
    #     result = await session.execute(query, {"user_id": user_id})
    #     return result.fetchone()
    
    # Mock response
    return {"id": user_id, "username": f"user_{user_id}", "email": f"user{user_id}@example.com"}

# Cached endpoint example
def get_cached_user(user_id: int):
    """
    Endpoint with Redis caching
    Interview Tip: Cache frequently accessed data
    """
    cache_key = get_cache_key("user", user_id=user_id)
    
    # Try to get from cache first
    cached_data = asyncio.run(get_cached_data(cache_key))
    if cached_data:
        return {"data": cached_data, "source": "cache"}
    
    # If not in cache, get from database
    user_data = asyncio.run(get_user_optimized(user_id))
    if user_data:
        # Cache the result
        asyncio.run(set_cached_data(cache_key, str(user_data)))
        return {"data": user_data, "source": "database"}
    
    raise HTTPException(status_code=404, detail="User not found")

# Async batch processing
async def process_items_batch(items: List[dict]):
    """
    Batch processing for better performance
    Interview Tip: Process items in batches to reduce overhead
    """
    # Process items concurrently
    tasks = [process_single_item(item) for item in items]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

async def process_single_item(item: dict):
    """
    Process single item (simulated)
    """
    await asyncio.sleep(0.1)  # Simulate processing time
    return {"processed": item, "status": "success"}

def process_batch_endpoint(items: List[dict]):
    """
    Batch processing endpoint
    """
    results = asyncio.run(process_items_batch(items))
    return {"processed_items": len(results), "results": results}

# Performance monitoring
def performance_middleware(request, call_next):
    """
    Middleware for performance monitoring
    Interview Tip: Monitor response times in production
    """
    start_time = time.time()
    response = call_next(request)
    process_time = time.time() - start_time
    
    # Add custom header with processing time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log slow requests
    if process_time > 1.0:
        print(f"Slow request: {request.url} took {process_time:.2f}s")
    
    return response

# Connection pooling example
def get_database_stats():
    """
    Endpoint demonstrating connection pooling
    Interview Tip: Monitor connection pool usage
    """
    # Simulate pool statistics
    return {
        "pool_size": 20,
        "checked_in": 15,
        "checked_out": 5,
        "overflow": 0
    }

# Load balancing considerations
"""
Load Balancing Strategies:
1. Multiple FastAPI instances behind a load balancer
2. Use health check endpoints
3. Implement sticky sessions if needed
4. Use Redis for session storage
5. Implement circuit breakers
"""

# Rate limiting example
def rate_limit_middleware(request, call_next):
    """
    Simple rate limiting middleware
    Interview Tip: Implement rate limiting for API protection
    """
    # In real implementation, check rate limits
    # client_ip = request.client.host
    # if is_rate_limited(client_ip):
    #     return JSONResponse(
    #         status_code=429,
    #         content={"detail": "Rate limit exceeded"}
    #     )
    
    return call_next(request)

# =============================================================================
# INTERVIEW TIPS AND COMMON QUESTIONS - PART 3
# =============================================================================

"""
INTERVIEW TIPS AND COMMON QUESTIONS - PART 3
============================================

1. Deployment:
   - Use Gunicorn for production
   - Containerize with Docker
   - Use environment variables
   - Implement health checks
   - Use reverse proxy (nginx)
   - Implement proper logging

2. Testing:
   - Test both success and error cases
   - Mock external dependencies
   - Use TestClient for API testing
   - Implement integration tests
   - Test authentication flows
   - Use fixtures for common setup

3. Background Tasks:
   - Use for non-critical operations
   - Handle exceptions properly
   - Implement retry mechanisms
   - Monitor task execution
   - Use task queues for complex workflows

4. Performance Optimization:
   - Use async/await for I/O operations
   - Implement caching strategies
   - Optimize database queries
   - Use connection pooling
   - Monitor performance metrics
   - Implement load balancing

5. Common Pitfalls:
   - Not handling exceptions in background tasks
   - Not implementing proper caching
   - Not optimizing database queries
   - Not monitoring performance
   - Not implementing health checks
   - Not using environment variables

6. Production Considerations:
   - Security best practices
   - Monitoring and logging
   - Error handling
   - Performance optimization
   - Scalability planning
   - Backup strategies

7. Advanced Topics:
   - WebSocket support
   - GraphQL integration
   - Microservices architecture
   - Event-driven architecture
   - Message queues
   - Distributed caching

8. Interview Preparation:
   - Understand async/await concepts
   - Know dependency injection patterns
   - Be familiar with testing strategies
   - Understand deployment options
   - Know performance optimization techniques
   - Be aware of security best practices
"""

if __name__ == "__main__":
    print("FastAPI Part 3 - Deployment, Testing, Background Tasks, and Performance")
    print("This file contains examples and interview tips for advanced FastAPI concepts") 