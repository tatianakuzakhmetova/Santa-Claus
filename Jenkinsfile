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
            sh 'sh \'echo "Hello from Shell"\''
          }
        }

        stage('python-shell') {
          steps {
            sh '/bin/sh -c "which python3"'
          }
        }

      }
    }

  }
}