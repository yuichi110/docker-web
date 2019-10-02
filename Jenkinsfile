pipeline {
  environment {
    TEST_HOST = "root@172.30.0.102"
  }

  agent any
  stages {
    stage('env') {
      steps {
        sh "echo 'Jenkins Build Number: ${BUILD_NUMBER}'"
        sh "echo 'BUILD_NUMBER=${BUILD_NUMBER}' > .env"
        sh "cat .env"
        sh "docker --version"
        sh "docker-compose --version"
        sh "docker -H ssh://${TEST_HOST} version"
        sh "docker-compose -H ssh://${TEST_HOST} version"
      }
    }

    stage('build/test') {
      steps {
        //sh "cat docker-compose.build.yml > docker-compose.yml"
        sh "cat docker-compose.build.yml"
        sh "docker-compose -H ssh://${TEST_HOST} -f docker-compose.build.yml stop"
        sh "docker-compose -H ssh://${TEST_HOST} -f docker-compose.build.yml build"
        sh "docker-compose -H ssh://${TEST_HOST} -f docker-compose.build.yml up -d"
        sh "docker -H ssh://${TEST_HOST} container ls"
      }
    }

    stage('cleanup') {
      steps {
        sh "echo 'cleanup'"
        //sh "docker-compose -H ssh://${TEST_HOST} stop"
        //sh "docker -H ssh://${TEST_HOST} container prune -f"
      }
    }

    stage('deploy') {
      steps {
        sh "cat docker-compose.prod.yml > docker-compose.yml"
        sh "cat docker-compose.yml"
        //sh "docker-compose -H ssh://${TEST_HOST} stop"
        //sh "docker -H ssh://${TEST_HOST} container prune -f"
      }
    }
  }
}