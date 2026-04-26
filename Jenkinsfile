pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 --version
                    python3 -m pip install --user --upgrade pip
                    python3 -m pip install --user -r requirements.txt pytest pytest-cov
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    python3 -m pytest -v --cov=. --cov-report=xml --junitxml=test-results.xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        docker run --rm \
                          -e SONAR_HOST_URL="$SONAR_HOST_URL" \
                          -e SONAR_TOKEN="$SONAR_AUTH_TOKEN" \
                          -v "$WORKSPACE:/usr/src" \
                          -w /usr/src \
                          sonarsource/sonar-scanner-cli:latest \
                          -Dsonar.host.url="$SONAR_HOST_URL" \
                          -Dsonar.login="$SONAR_AUTH_TOKEN"
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                if (fileExists('test-results.xml')) {
                    junit 'test-results.xml'
                } else {
                    echo 'No test-results.xml found, skipping junit publish.'
                }
            }
            archiveArtifacts artifacts: 'coverage.xml,test-results.xml', allowEmptyArchive: true
        }
    }
}