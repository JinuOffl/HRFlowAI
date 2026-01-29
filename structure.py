import os

structure = [
    "backend/api/v1",
    "backend/core",
    "backend/models",
    "backend/services",
    "backend/utils",
    "frontend/templates",
    "frontend/static/css",
    "frontend/static/js",
    "tests",
    "docs",
    "configs"
]

files = [
    "backend/main.py",
    "backend/core/config.py",
    "backend/models/db.py",
    "backend/services/nl2sql.py",
    "backend/services/analysis.py",
    "backend/services/summarization.py",
    "backend/utils/helpers.py",
    "frontend/app.py",
    "frontend/templates/index.html",
    ".env",
    "run.bat"
]

for folder in structure:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, 'w') as f:
        pass

print("Project structure created successfully.")