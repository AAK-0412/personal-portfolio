
from contextlib import asynccontextmanager
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

from backend.database import create_tables, get_connection
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Personal Portfolio API",
    description="Backend API for my personal portfolio website",
    version="1.0.0",
    lifespan=lifespan,
)
app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# Request model for contact form submissions.
class ContactMessage(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    subject: str | None = Field(default=None, max_length=150)
    message: str = Field(min_length=10, max_length=5000)


@app.get("/")
def home():
    return {"message": "Personal Portfolio API is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/projects")
def get_projects():
    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT id, title, description, technologies,
                   github_url, demo_url, status
            FROM projects
            ORDER BY id
        """).fetchall()

        return [dict(row) for row in rows]

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve projects.",
        )

    finally:
        connection.close()


@app.post("/contact", status_code=201)
@limiter.limit("5/minute")
def submit_contact(request: Request, message: ContactMessage):
    name = message.name.strip()
    email = str(message.email).strip()
    subject = (message.subject or "").strip()
    content = message.message.strip()

    if len(name) < 2:
        raise HTTPException(
            status_code=422,
            detail="Name must contain at least two characters.",
        )

    if len(content) < 10:
        raise HTTPException(
            status_code=422,
            detail="Message must contain at least ten characters.",
        )

    # Prevent empty subjects from being stored as empty strings.
    subject = subject or None

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO contact_messages (name, email, subject, message)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, subject, content),
        )

        connection.commit()

        return {
            "message": "Your message has been received successfully.",
            "id": cursor.lastrowid,
        }

    except Exception:
        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to save your message. Please try again later.",
        )

    finally:
        connection.close()
