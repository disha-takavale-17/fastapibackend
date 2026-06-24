from fastapi import FastAPI
from app.routes import book_routes, user_routes, login_routes
from fastapi.middleware.cors import CORSMiddleware

from app import auth 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include user routes
app.include_router(user_routes.router)
app.include_router(book_routes.router)
app.include_router(login_routes.router)

