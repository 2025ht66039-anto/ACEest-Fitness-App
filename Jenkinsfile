stages {
    stage('Checkout') {
        steps {
            checkout scm
        }
    }

    stage('Run Unit Tests') {
        steps {
            sh '''
                python3 --version
                python3 -m pip install --upgrade pip
                pip3 install -r requirements.txt pytest pytest-cov
                pytest -v --cov=. --cov-report=xml --junitxml=test-results.xml
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
}