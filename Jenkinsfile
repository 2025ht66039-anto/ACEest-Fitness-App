pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
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
                    withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            docker run --rm \
                              --volumes-from jenkins \
                              -w /var/jenkins_home/workspace/ACEestFitnessApp \
                              sonarsource/sonar-scanner-cli:latest \
                              -Dsonar.projectKey=aceest-fitness-app \
                              -Dsonar.projectName="ACEest Fitness App" \
                              -Dsonar.projectBaseDir=/var/jenkins_home/workspace/ACEestFitnessApp \
                              -Dsonar.sources=ACEest_Fitness.py \
                              -Dsonar.tests=tests \
                              -Dsonar.exclusions=venv/**,__pycache__/**,.pytest_cache/**,.git/**,k8s/**,versions/**,docker-compose/**,templates/**,*.db \
                              -Dsonar.coverage.exclusions=tests/** \
                              -Dsonar.python.coverage.reportPaths=coverage.xml \
                              -Dsonar.host.url="$SONAR_HOST_URL" \
                              -Dsonar.login="$SONAR_TOKEN"
                        '''
                    }
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
            deleteDir()
        }
    }
}