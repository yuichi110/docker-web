pipeline {
  environment {
    BUILD_HOST = "root@172.30.0.102"
    PROD_HOST = "root@172.30.0.103"
  }

  agent any
  stages {
    stage('Check docker version') {
      steps {
        sh "docker --version | tee .dv-jenkins"
        sh "docker -H ssh://${BUILD_HOST} --version | tee .dv-build"
        //sh "docker -H ssh://${PROD_HOST} --version | tee dv-prod"
        sh 'test "`cat .dv-jenkins`" = "`cat .dv-build`"'
        //sh "test '`cat dv-local`' = '`cat dv-prod`'"
      }
    }

    stage('Check docker-compose version') {
      steps {
        sh "docker-compose --version | tee .dcv-jenkins"
        sh "docker-compose -H ssh://${BUILD_HOST} --version | tee .dcv-build"
        //sh "docker-compose -H ssh://${PROD_HOST} --version | tee dcv-prod"
        sh 'test "`cat .dcv-jenkins`" = "`cat .dcv-build`"'
        //sh "test '`cat dcv-local`' = '`cat dcv-prod`'"
      }
    }

    stage('Make .env file') {
      steps {
        sh "echo 'Jenkins Build Number: ${BUILD_NUMBER}'"
        sh "echo 'BUILD_NUMBER=${BUILD_NUMBER}' > .env"
        sh "echo 'TIME_STAMP=`date +%Y%m%d-%H%M%S-%N`' >> .env"
        sh "cat .env"
      }
    }

    stage('Build Image') {
      steps {
        sh "cat docker-compose.build.yml"
        sh "docker-compose -H ssh://${BUILD_HOST} -f docker-compose.build.yml build"
        sh "docker-compose -H ssh://${BUILD_HOST} -f docker-compose.build.yml up -d"
        sh "docker -H ssh://${BUILD_HOST} container ls"
      }
    }

    stage('Test Containers') {
      steps {
        sh "docker ssh://${BUILD_HOST} -f container exec mykvs-apptest pytest -v test_app.py"
        sh "docker ssh://${BUILD_HOST} -f container exec mykvs-webtest pytest -v test_static.py"
        sh "docker ssh://${BUILD_HOST} -f container exec mykvs-webtest pytest -v test_selenium.py"
        sh "docker-compose -H ssh://${BUILD_HOST} -f docker-compose.build.yml stop"
      }
    }

    stage('Register Images') {
      steps {
        sh "echo 'upload'"
      }
    }

    stage('Deploy Image') {
      steps {
        sh "cat docker-compose.prod.yml"
        //sh "docker-compose -H ssh://${PROD_HOST} -f docker-compose.prod.yml up -d"
        //sh "docker -H ssh://${PROD_HOST} container ls"
      }
    }
  }
}