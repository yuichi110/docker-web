pipeline {
  environment {
    TEST_HOST = "root@172.30.0.102"
  }

  agent any
  stages {
    stage('check docker environment') {
      steps {
        sh "docker --version"
        sh "docker-compose --version"
        sh "docker -H ssh://${TEST_HOST} version"
        sh "docker-compose -H ssh://${TEST_HOST} version"
      }
    }

    stage('build and test at test host') {
      steps {
        sh "docker-compose -H ssh://${TEST_HOST} up -d"
      }
    }

    stage('cleanup at test host') {
      steps {
        sh "docker-compose -H ssh://${TEST_HOST} stop"
      }
    }
  }
}