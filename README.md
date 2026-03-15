# ACEest Fitness & Gym - DevOps CI/CD Project

## Project Overview
Flask web application for fitness/gym management, containerized using Docker and deployed via Jenkins.
CI is implemented using GitHub Actions (lint, docker build, pytest inside container).

## Tech Stack
- Python + Flask
- Pytest
- Docker
- Jenkins
- GitHub Actions

## Local Setup (Run Without Docker)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py