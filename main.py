"""
Project 103 - FastAPI Application
Entry point for the web application.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Project 103")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Homepage with red background (as requested)."""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Project 103</title>
            <style>
                body {
                    background-color: red;
                    color: white;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    text-align: center;
                }
                h1 {
                    font-size: 3em;
                    margin-bottom: 0.5em;
                }
                p {
                    font-size: 1.2em;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to Project 103</h1>
                <p>Homepage with red background</p>
            </div>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "project": "103"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
