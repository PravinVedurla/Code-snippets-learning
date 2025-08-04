"""
FASTAPI COMPREHENSIVE GUIDE FOR INTERVIEW PREPARATION
====================================================

This file contains detailed examples and explanations of FastAPI concepts
commonly asked in technical interviews. Each section includes:
- Core concepts explanation
- Code examples with detailed comments
- Best practices and common pitfalls
- Interview tips and frequently asked questions
"""

# =============================================================================
# 1. FASTAPI BASICS
# =============================================================================

"""
FastAPI Basics - Core Concepts
------------------------------
FastAPI is a modern, fast web framework for building APIs with Python 3.7+.
Key features: automatic API documentation, type hints, async support, validation.

Common Interview Questions:
- What is FastAPI and why choose it over Flask/Django?
- Explain FastAPI's automatic documentation feature
- How does FastAPI handle type hints?
- What are the main advantages of FastAPI?
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import uvicorn

# Basic FastAPI application setup
app = FastAPI(
    title="Interview Prep API",
    description="Comprehensive FastAPI examples for interview preparation",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc documentation
)

# CORS middleware for handling cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic route with path parameters
@app.get("/")
async def root():
    """
    Root endpoint - demonstrates basic async function
    Interview Tip: Always mention that FastAPI supports both sync and async functions
    """
    return {"message": "FastAPI Interview Prep"}

# Path parameters with type hints
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """
    Path parameter example with automatic type conversion and validation
    FastAPI automatically converts string to int and validates the type
    """
    if user_id < 1:
        raise HTTPException(status_code=400, detail="User ID must be positive")
    return {"user_id": user_id, "name": f"User {user_id}"}

# Query parameters
@app.get("/search/")
async def search_items(
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    """
    Query parameters with defaults and optional values
    Interview Tip: Explain how FastAPI automatically generates OpenAPI schema
    """
    return {
        "query": q,
        "skip": skip,
        "limit": limit,
        "results": f"Searching for {q} with pagination"
    }

# =============================================================================
# 2. ASYNCHRONOUS PROGRAMMING
# =============================================================================

"""
Asynchronous Programming in FastAPI
-----------------------------------
FastAPI is built on top of Starlette and supports async/await patterns.
This enables high concurrency and better performance for I/O-bound operations.

Interview Questions:
- What is the difference between sync and async functions in FastAPI?
- When should you use async vs sync?
- How does FastAPI handle concurrent requests?
- Explain the event loop in FastAPI
"""

import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

# Async function example
@app.get("/async-example")
async def async_example():
    """
    Demonstrates async/await pattern
    This function can handle multiple concurrent requests efficiently
    """
    # Simulate async I/O operation (database query, API call, etc.)
    await asyncio.sleep(1)
    return {"message": "Async operation completed"}

# Sync function example (use when you have CPU-bound operations)
@app.get("/sync-example")
def sync_example():
    """
    Sync function - use for CPU-bound operations
    Interview Tip: FastAPI runs sync functions in a thread pool
    """
    time.sleep(1)  # Blocking operation
    return {"message": "Sync operation completed"}

# Async with external API calls
@app.get("/fetch-data")
async def fetch_external_data():
    """
    Demonstrates async HTTP requests using aiohttp
    Shows how to handle multiple concurrent external API calls
    """
    async with aiohttp.ClientSession() as session:
        # Fetch multiple URLs concurrently
        urls = [
            "https://jsonplaceholder.typicode.com/posts/1",
            "https://jsonplaceholder.typicode.com/posts/2",
            "https://jsonplaceholder.typicode.com/posts/3"
        ]
        
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        
        results = []
        for response in responses:
            data = await response.json()
            results.append(data)
        
        return {"results": results}

# CPU-bound operation with ThreadPoolExecutor
@app.get("/cpu-intensive")
async def cpu_intensive_task():
    """
    Demonstrates handling CPU-bound operations in async context
    Interview Tip: Use ThreadPoolExecutor for CPU-bound tasks in async functions
    """
    def heavy_computation():
        # Simulate CPU-intensive work
        result = 0
        for i in range(1000000):
            result += i
        return result
    
    # Run CPU-bound task in thread pool
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, heavy_computation)
    
    return {"result": result}

# =============================================================================
# 3. DEPENDENCY INJECTION
# =============================================================================

"""
Dependency Injection in FastAPI
-------------------------------
FastAPI's dependency injection system allows you to:
- Share common logic between routes
- Manage database connections
- Handle authentication
- Implement caching
- Manage configuration

Interview Questions:
- What is dependency injection and why use it?
- How does FastAPI's dependency injection work?
- Explain the difference between function and class dependencies
- How to create reusable dependencies?
"""

from fastapi import Depends, Header
from typing import Optional

# Simple dependency
def get_common_params(
    skip: int = 0,
    limit: int = 100
):
    """
    Simple dependency that provides common query parameters
    Can be reused across multiple endpoints
    """
    return {"skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(get_common_params)):
    """
    Uses dependency injection for common parameters
    Interview Tip: Dependencies are evaluated for each request
    """
    return commons

# Dependency with database connection simulation
class Database:
    def __init__(self):
        self.connection = "database_connection"
    
    def get_items(self):
        return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

def get_database():
    """
    Dependency that provides database connection
    Interview Tip: This pattern is commonly used for database sessions
    """
    db = Database()
    try:
        yield db
    finally:
        # Cleanup code here
        pass

@app.get("/db-items/")
async def read_db_items(db: Database = Depends(get_database)):
    """
    Uses database dependency
    Interview Tip: Dependencies can be classes or functions
    """
    return db.get_items()

# Authentication dependency
def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Authentication dependency example
    Interview Tip: This is a common pattern for JWT token validation
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # In real app, validate JWT token here
    user = {"id": 1, "username": "john_doe"}
    return user

@app.get("/protected/")
async def protected_route(current_user: dict = Depends(get_current_user)):
    """
    Protected route using authentication dependency
    """
    return {"message": "This is protected", "user": current_user}

# Nested dependencies
def get_query_token(token: str):
    return token

def get_query_or_cookie_token(
    token: str = Depends(get_query_token),
    last_token: Optional[str] = None
):
    if token:
        return token
    return last_token

@app.get("/nested-deps/")
async def read_query(token: str = Depends(get_query_or_cookie_token)):
    """
    Demonstrates nested dependencies
    """
    return {"token": token}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
