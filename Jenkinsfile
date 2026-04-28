pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = "aceest-fitness-app"
        SONAR_PROJECT_NAME = "ACEest Fitness App"
        SONAR_HOST_URL = "http://10.35.6.106:9000"
    }

    stages {

        stage('Checkout') {
            steps {
                deleteDir()
                git branch: 'main', url: 'https://github.com/2025ht66039-anto/ACEest-Fitness-App.git'
            }
        }

        stage('Create Virtualenv and Install Dependencies') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pytest -v --cov=. --cov-report=xml --junitxml=test-results.xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            docker run --rm \
                            --volumes-from jenkins \
                            -w /var/jenkins_home/workspace/ACEestFitnessApp \
                            sonarsource/sonar-scanner-cli:latest \
                            -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                            -Dsonar.projectName="$SONAR_PROJECT_NAME" \
                            -Dsonar.projectBaseDir=/var/jenkins_home/workspace/ACEestFitnessApp \
                            -Dsonar.sources=. \
                            -Dsonar.tests=tests \
                            -Dsonar.exclusions=tests/**,.venv/**,__pycache__/**,.pytest_cache/**,.git/**,k8s/**,versions/**,docker-compose/**,templates/**,*.db \
                            -Dsonar.test.inclusions=tests/** \
                            -Dsonar.coverage.exclusions=tests/** \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            script {
                if (fileExists('test-results.xml')) {
                    junit 'test-results.xml'
                }
            }
            archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
            deleteDir()
        }

        success {
            echo '✅ Pipeline completed successfully'
        }

        failure {
            echo '❌ Pipeline failed'
        }
    }
}