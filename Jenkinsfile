pipeline {
    agent any

    parameters {
        choice(
            name: 'DEPLOY_STRATEGY',
            choices: ['rolling', 'blue-green', 'canary'],
            description: 'Choose deployment strategy'
        )
    }

    environment {
        IMAGE_NAME = "2025ht66039/aceest-fitness-app"
        IMAGE_TAG  = "v${BUILD_NUMBER}"
        K8S_NAMESPACE = "default"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest -v --cov=. --cov-report=xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=aceest-fitness-app \
                          -Dsonar.sources=. \
                          -Dsonar.tests=tests \
                          -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    if (params.DEPLOY_STRATEGY == 'rolling') {
                        sh """
                            kubectl apply -f k8s/rolling/
                            kubectl set image deployment/aceest-fitness aceest-fitness=${IMAGE_NAME}:${IMAGE_TAG}
                            kubectl rollout status deployment/aceest-fitness
                        """
                    }

                    if (params.DEPLOY_STRATEGY == 'blue-green') {
                        sh """
                            kubectl apply -f k8s/blue-green/blue-deployment.yaml
                            kubectl apply -f k8s/blue-green/service.yaml
                            kubectl apply -f k8s/blue-green/green-deployment.yaml
                            kubectl rollout status deployment/aceest-green
                            kubectl patch service aceest-bg-service -p '{"spec":{"selector":{"app":"aceest-fitness","track":"green"}}}'
                        """
                    }

                    if (params.DEPLOY_STRATEGY == 'canary') {
                        sh """
                            kubectl apply -f k8s/canary/stable-deployment.yaml
                            kubectl apply -f k8s/canary/stable-service.yaml
                            kubectl apply -f k8s/canary/ingress-stable.yaml
                            kubectl apply -f k8s/canary/canary-deployment.yaml
                            kubectl apply -f k8s/canary/canary-service.yaml
                            kubectl apply -f k8s/canary/ingress-canary.yaml
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
        success {
            echo 'Build successful'
        }
        failure {
            echo 'Build failed'
        }
    }
}