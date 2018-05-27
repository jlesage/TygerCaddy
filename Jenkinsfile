pipeline {
  agent none
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