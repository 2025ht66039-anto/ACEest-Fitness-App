\# ACEest Fitness \& Gym – DevOps CI/CD Project



\## Project Overview

ACEest Fitness \& Gym is a Python \*\*Flask\*\* web application that demonstrates an industry-style \*\*DevOps CI/CD pipeline\*\*.



For Assignment 2, the main CI implementation is done using \*\*Jenkins + Pytest + SonarQube\*\*:

\- Code checkout from GitHub

\- Python virtual environment setup

\- Dependency installation from `requirements.txt`

\- Automated unit testing using \*\*Pytest\*\* (JUnit + Coverage XML reports)

\- Static code analysis using \*\*SonarQube\*\* (Quality Gate)



The application is containerized using \*\*Docker\*\*, and Kubernetes manifests are provided for deployment.



\---



\## Tech Stack

\- Python 3 + Flask

\- Pytest + pytest-cov

\- Jenkins (CI pipeline)

\- SonarQube (code quality analysis)

\- Docker

\- Kubernetes / Minikube (deployment manifests)



\---



\## Repository Structure (High Level)

\- `ACEest\_Fitness.py` → Flask application entry

\- `templates/` → HTML templates

\- `tests/` → Pytest unit tests

\- `Jenkinsfile` → Jenkins CI pipeline

\- `sonar-project.properties` → SonarQube project configuration

\- `Dockerfile` → Application container build file

\- `docker-compose.yml` (if available) → local orchestration (optional)

\- `k8s/` → Kubernetes YAML manifests (deployment/service strategies)

\- `jenkins/` → Jenkins Docker image build files (custom Jenkins image)



\---



\## Local Setup (Run Without Docker)



\### Prerequisites

\- Python installed (3.11+ recommended)

\- pip installed



\### Steps

```bash

python -m venv venv

\# Linux/Mac:

source venv/bin/activate

\# Windows (PowerShell):

\# .\\venv\\Scripts\\Activate.ps1



pip install -r requirements.txt

python ACEest\_Fitness.py

