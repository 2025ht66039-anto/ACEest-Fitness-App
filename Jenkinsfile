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
                    docker run --rm \
                      -v "$WORKSPACE":/app \
                      -w /app \
                      python:3.11-slim \
                      sh -c "
                        python -m pip install --upgrade pip &&
                        pip install -r requirements.txt pytest pytest-cov &&
                        pytest -v --cov=. --cov-report=xml --junitxml=test-results.xml
                      "
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            docker run --rm \
                              -e SONAR_HOST_URL="$SONAR_HOST_URL" \
                              -e SONAR_TOKEN="$SONAR_TOKEN" \
                              -v "$WORKSPACE":/usr/src \
                              -w /usr/src \
                              sonarsource/sonar-scanner-cli:latest \
                              -Dsonar.projectKey=aceest-fitness-app \
                              -Dsonar.projectName="ACEest Fitness App" \
                              -Dsonar.sources=. \
                              -Dsonar.tests=tests \
                              -Dsonar.exclusions=venv/**,__pycache__/**,.pytest_cache/**,.git/**,k8s/**,versions/**,docker-compose/**,templates/** \
                              -Dsonar.python.coverage.reportPaths=coverage.xml
                        '''
                    }
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
                        sh '''
                            kubectl apply -f k8s/rolling/
                            kubectl set image deployment/aceest-fitness aceest-fitness=$IMAGE_NAME:$IMAGE_TAG
                            kubectl rollout status deployment/aceest-fitness
                        '''
                    } else if (params.DEPLOY_STRATEGY == 'blue-green') {
                        sh '''
                            kubectl apply -f k8s/blue-green/blue-deployment.yaml
                            kubectl apply -f k8s/blue-green/service.yaml
                            kubectl apply -f k8s/blue-green/green-deployment.yaml
                            kubectl rollout status deployment/aceest-blue
                            kubectl rollout status deployment/aceest-green
                        '''
                    } else if (params.DEPLOY_STRATEGY == 'canary') {
                        sh '''
                            kubectl apply -f k8s/canary/stable-deployment.yaml
                            kubectl apply -f k8s/canary/stable-service.yaml
                            kubectl apply -f k8s/canary/ingress-stable.yaml
                            kubectl apply -f k8s/canary/canary-deployment.yaml
                            kubectl apply -f k8s/canary/canary-service.yaml
                            kubectl apply -f k8s/canary/ingress-canary.yaml
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-results.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'coverage.xml, test-results.xml'
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