pipeline {
  agent {
    docker {
      image 'python:3.5.1'
    }

  }
  stages {
    stage('Initialise') {
      steps {
        sh 'python --version'
      }
    }
    stage('Change Directory') {
      steps {
        sh '''cd /apps/TygerCaddy/TygerCaddy
pyhton3 manage.py migrate'''
      }
    }
  }
}