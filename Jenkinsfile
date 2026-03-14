pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t aceest-fitness-app .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker rm -f aceest-fitness || true'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 3000:5000 --name aceest-fitness aceest-fitness-app'
            }
        }
