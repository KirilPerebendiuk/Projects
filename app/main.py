from fastapi import FastAPI

from app.db.connection import get_connection
from app.schemas import TaskCreate

app = FastAPI(
    title="DevOps Task Platform",
    description="A task management API built for DevOps practice",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "DevOps Task Platform API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/tasks")
def get_tasks():
    with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, description, status, created_at "
                "FROM tasks ORDER BY id"
            )
            rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "created_at": row[4],
        }
        for row in rows
    ]


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, description)
                VALUES (%s, %s)
                RETURNING id, title, description, status, created_at
                """,
                (task.title, task.description),
            )
            row = cur.fetchone()

    return {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "status": row[3],
        "created_at": row[4],
    }
