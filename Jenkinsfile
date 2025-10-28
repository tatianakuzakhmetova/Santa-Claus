pipeline {
  agent any
  stages {
    stage('Build') {
      parallel {
        stage('Build') {
          steps {
            echo 'Hello from Jenkins'
          }
        }

        stage('shell') {
          steps {
            sh 'sh \'echo Hello from Shell\''
          }
        }

        stage('python-shell') {
          steps {
            sh 'sh \'python3 -c "print(\\"Hello from Python\\")"\''
          }
        }

      }
    }

  }
}