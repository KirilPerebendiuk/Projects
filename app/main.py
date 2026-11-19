from fastapi import FastAPI

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
