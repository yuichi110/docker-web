pipeline {
  environment {
    TEST_HOST = "root@172.30.0.102"
  }

  agent any
  stages {
    stage('check env') {
      steps {
        sh "docker --version"
        sh "docker-compose --version"
        sh "docker -H ssh://${TEST_HOST} version"
        sh "docker-compose -H ssh://${TEST_HOST} version"
      }
    }

    stage('build/test') {
      steps {
        sh "docker-compose -H ssh://${TEST_HOST} up -d"
      }
    }

    stage('cleanup') {
      steps {
        sh "docker-compose -H ssh://${TEST_HOST} stop"
        sh "docker -H ssh://${TEST_HOST} container prune -f"
      }
    }
  }
}