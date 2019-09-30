pipeline {
  environment {
    TEST_HOST = "root@172.30.0.102"
  }

  agent any
  stages {
    stage('check docker') {
      steps {
        sh "docker --version"
        sh "docker-compose --version"
        sh "docker -H ssh://${TEST_HOST} version"
        sh "docker-compose -H ssh://${TEST_HOST} version"
      }
    }

    stage('hello') {
      steps {
        sh "pwd"
        sh "ls"
      }
    }

  }
}