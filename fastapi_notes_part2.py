"""
FASTAPI COMPREHENSIVE GUIDE - PART 2
====================================

This file continues the FastAPI interview preparation guide with:
- Data Validation with Pydantic
- File Handling with UploadFile
- Authentication and Security (OAuth2, JWT)
- Additional examples and best practices
"""

from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, EmailStr, field_validator
from datetime import datetime, timedelta
from enum import Enum
from passlib.context import CryptContext
from jose import JWTError, jwt
import uvicorn
import shutil
import os
from pathlib import Path

# =============================================================================
# 4. DATA VALIDATION WITH PYDANTIC
# =============================================================================

"""
Data Validation with Pydantic
-----------------------------
Pydantic provides data validation using Python type annotations.
FastAPI uses Pydantic for request/response models and automatic validation.

Interview Questions:
- What is Pydantic and how does FastAPI use it?
- Explain Pydantic models vs regular Python classes
- How to handle validation errors?
- What are Pydantic validators?
- How to create custom validators?
"""

# Basic Pydantic model
class User(BaseModel):
    """
    Basic Pydantic model with validation
    Interview Tip: Pydantic automatically validates data types and constraints
    """
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=120)  # greater than or equal, less than or equal
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    
    @field_validator('username')
    def username_must_be_valid(cls, v):
        """
        Custom validator for username
        Interview Tip: Validators run after type conversion
        """
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
    
    class Config:
        # Example configuration
        schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "age": 25,
                "is_active": True
            }
        }

# Enum for status
class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

# Nested models
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class UserProfile(BaseModel):
    """
    Nested Pydantic model example
    Interview Tip: Use nested models for complex data structures
    """
    user: User
    address: Address
    status: UserStatus = UserStatus.ACTIVE

# Request/Response models
class UserCreate(BaseModel):
    """
    Model for creating users (request body)
    Interview Tip: Separate request and response models for better API design
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=120)

class UserResponse(BaseModel):
    """
    Model for user responses (response body)
    Interview Tip: response_model ensures response validation and documentation
    """
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

# Optional fields and default values
class Item(BaseModel):
    """
    Model with optional fields and defaults
    Interview Tip: Use Optional for nullable fields, defaults for required fields
    """
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)  # greater than 0
    tags: List[str] = []
    metadata: Dict[str, Any] = {}

# Advanced validation example
class Product(BaseModel):
    """
    Advanced Pydantic model with complex validation
    Interview Tip: Show understanding of complex validation scenarios
    """
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    category: str = Field(..., regex=r'^[A-Za-z\s]+$')  # Only letters and spaces
    stock: int = Field(..., ge=0)
    
    @field_validator('price')
    def price_must_be_reasonable(cls, v):
        """Custom validator for price"""
        if v > 10000:
            raise ValueError('Price too high')
        return round(v, 2)
    
    @field_validator('name')
    def name_must_be_title_case(cls, v):
        """Convert name to title case"""
        return v.title()
    
    @property
    def is_in_stock(self) -> bool:
        """Computed property"""
        return self.stock > 0

# =============================================================================
# 5. FILE HANDLING WITH UPLOADFILE
# =============================================================================

"""
File Handling with UploadFile
-----------------------------
FastAPI provides UploadFile for handling file uploads efficiently.
It's built on top of Python-multipart and supports async operations.

Interview Questions:
- How does FastAPI handle file uploads?
- What's the difference between UploadFile and bytes?
- How to handle multiple file uploads?
- How to validate file types and sizes?
- How to process files asynchronously?
"""

# Single file upload
def upload_single_file(file: UploadFile = File(...)):
    """
    Basic file upload endpoint
    Interview Tip: UploadFile provides metadata like filename, content_type
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed"
        )
    
    # Create upload directory
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    # Save file
    file_path = upload_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size
    }

# Multiple file uploads
def upload_multiple_files(files: List[UploadFile] = File(...)):
    """
    Multiple file upload example
    Interview Tip: Use List[UploadFile] for multiple files
    """
    results = []
    for file in files:
        # Validate file size (e.g., max 5MB)
        if file.size > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File {file.filename} is too large"
            )
        
        # Save file
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        results.append({
            "filename": file.filename,
            "size": file.size
        })
    
    return {"uploaded_files": results}

# File upload with form data
def upload_with_form(
    file: UploadFile = File(...),
    description: str = Form(...)
):
    """
    File upload with additional form data
    Interview Tip: Use Form() for form fields, File() for files
    """
    return {
        "filename": file.filename,
        "description": description,
        "content_type": file.content_type
    }

# File download
def download_file(filename: str):
    """
    File download endpoint
    Interview Tip: Use FileResponse for efficient file serving
    """
    file_path = Path("uploads") / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

# Async file processing
async def process_file_async(file: UploadFile = File(...)):
    """
    Async file processing example
    Interview Tip: UploadFile.file is a SpooledTemporaryFile
    """
    # Read file content asynchronously
    content = await file.read()
    
    # Process content (e.g., parse CSV, analyze text)
    lines = content.decode().split('\n')
    word_count = len(content.split())
    
    return {
        "filename": file.filename,
        "lines": len(lines),
        "word_count": word_count,
        "size": len(content)
    }

# =============================================================================
# 6. AUTHENTICATION AND SECURITY
# =============================================================================

"""
Authentication and Security in FastAPI
--------------------------------------
FastAPI provides built-in security utilities for OAuth2, JWT, and other
authentication methods. Security is handled through dependencies.

Interview Questions:
- How to implement JWT authentication in FastAPI?
- Explain OAuth2 with Password flow
- How to handle password hashing?
- What are security best practices?
- How to implement role-based access control?
- How to handle token refresh?
"""

# Security configuration
SECRET_KEY = "your-secret-key-here"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model for authentication
class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str
    disabled: bool = False
    role: str = "user"

# Simulated user database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "john@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
        "role": "admin"
    },
    "jane": {
        "username": "jane",
        "email": "jane@example.com",
        "hashed_password": pwd_context.hash("password"),
        "disabled": False,
        "role": "user"
    }
}

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    Interview Tip: Always hash passwords, never store plain text
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password
    Interview Tip: Use bcrypt for password hashing
    """
    return pwd_context.hash(password)

def get_user(username: str):
    """
    Get user from database
    Interview Tip: In real apps, use proper database queries
    """
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(username: str, password: str):
    """
    Authenticate user with username and password
    Interview Tip: Always use secure authentication methods
    """
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# JWT token utilities
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create JWT access token
    Interview Tip: Always set expiration time for tokens
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """
    Create refresh token
    Interview Tip: Refresh tokens should have longer expiration
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verify JWT token
    Interview Tip: Handle JWTError exceptions properly
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

# Authentication dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get current user from JWT token
    Interview Tip: This is a common pattern for protected routes
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    
    user = get_user(username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    """
    Get current active user
    Interview Tip: Use this for additional user state validation
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Role-based access control
def require_role(required_role: str):
    """
    Dependency for role-based access control
    Interview Tip: This pattern is commonly used for authorization
    """
    def role_checker(current_user: UserInDB = Depends(get_current_active_user)):
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

# Authentication endpoints
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 password flow login endpoint
    Interview Tip: This is the standard OAuth2 password flow
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def refresh_access_token(refresh_token: str):
    """
    Refresh access token endpoint
    Interview Tip: Implement token refresh for better UX
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if username is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user = get_user(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

# Protected routes
def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Protected route example
    Interview Tip: Use dependencies for authentication
    """
    return current_user

def admin_only_route(current_user: UserInDB = Depends(require_role("admin"))):
    """
    Admin-only route example
    Interview Tip: Implement proper authorization checks
    """
    return {"message": "Admin access granted", "user": current_user}

# Security best practices
def security_headers():
    """
    Add security headers middleware
    Interview Tip: Always implement security headers in production
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
    }

# =============================================================================
# INTERVIEW TIPS AND COMMON QUESTIONS
# =============================================================================

"""
INTERVIEW TIPS AND COMMON QUESTIONS - PART 2
============================================

1. Pydantic Validation:
   - Always validate input data
   - Use custom validators for complex logic
   - Separate request/response models
   - Handle validation errors gracefully

2. File Handling:
   - Validate file types and sizes
   - Use async operations for large files
   - Implement proper error handling
   - Consider security implications

3. Authentication:
   - Use JWT for stateless authentication
   - Implement token refresh
   - Hash passwords with bcrypt
   - Use role-based access control
   - Validate tokens properly

4. Security Best Practices:
   - Use HTTPS in production
   - Implement rate limiting
   - Add security headers
   - Validate all inputs
   - Use environment variables for secrets
   - Implement proper error handling

5. Common Pitfalls:
   - Not handling file upload errors
   - Not validating file types
   - Not implementing proper authentication
   - Not using secure password hashing
   - Not handling JWT errors properly

6. Performance Considerations:
   - Use async file operations
   - Implement file size limits
   - Use streaming for large files
   - Cache authentication results
   - Optimize database queries

7. Testing Authentication:
   - Test with valid/invalid tokens
   - Test role-based access
   - Test token expiration
   - Test refresh tokens
   - Mock external services

8. Production Deployment:
   - Use proper secret management
   - Implement logging
   - Monitor authentication failures
   - Use secure file storage
   - Implement backup strategies
"""

if __name__ == "__main__":
    print("FastAPI Part 2 - Data Validation, File Handling, and Authentication")
    print("This file contains examples and interview tips for FastAPI concepts") 