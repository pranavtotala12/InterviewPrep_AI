from fastapi import FastAPI

app = FastAPI(
    title="InterviewPrep AI",
    description="AI-powered interview preparation assistant",
    version="1.0.0"
)

@app.get("/")
def home():

    return {
        "message": "Welcome to InterviewPrep AI",
        "status": "Application is running"
    }