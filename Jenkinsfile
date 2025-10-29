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
            sh '/bin/sh -c "echo Hello, Blue Ocean! && date"'
          }
        }

      }
    }

  }
}