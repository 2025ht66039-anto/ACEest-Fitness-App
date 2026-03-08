stage('Run Docker Container') {
  steps {
    sh '''
      docker rm -f aceest-fitness-app || true
      docker run -d --name aceest-fitness-app -p 3000:3000 aceest-fitness-app
    '''
  }
}