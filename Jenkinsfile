pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t aceest-fitness-app .'
            }
        }

        stage('Run Unit Tests (container)') {
            steps {
                sh 'docker run --rm -w /app -e PYTHONPATH=/app aceest-fitness-app python -m pytest -q'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker rm -f aceest-fitness || true'
            }
        }

        stage('Run Docker Container') {
            steps {
                // host 3000 -> container 5000 (gunicorn binds 5000)
                sh 'docker run -d -p 3000:5000 --name aceest-fitness aceest-fitness-app'
            }
        }
    }
}