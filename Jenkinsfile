pipeline {
  environment {
    DOCKERHUB_USER = "yuichi110"
    BUILD_HOST = "root@10.149.245.115"
    PROD_HOST = "root@10.149.245.116"
    BUILD_TIMESTAMP = sh(script: "date +%Y%m%d.%H%M%S", returnStdout: true).trim()
  }

  agent any
  stages {
    stage('Check Login') {
      steps {
        sh "test -f ~/.docker/config.json"
        sh "cat ~/.docker/config.json | grep docker.io"
      }
    }
    /*
    stage('Setup') {
      steps {
        sh "echo 'Jenkins Build Number: ${BUILD_NUMBER}'"
        sh "echo 'BUILD_NUMBER=${BUILD_NUMBER}' > .env"
        sh "echo 'DOCKERHUB_USER=${DOCKERHUB_USER}' >> .env"
        sh "echo 'TIME_STAMP=`date +%Y%m%d-%H%M%S-%N`' >> .env"
        sh "cat .env"
      }
    }
    */
    stage('Build') {
      steps {
        sh "cat docker-compose.build.yml"
        sh "docker-compose -H ssh://${BUILD_HOST} -f docker-compose.build.yml up -d --build"
        sh "docker -H ssh://${BUILD_HOST} container ls"
      }
    }
    stage('Test') {
      steps {
        sh "docker -H ssh://${BUILD_HOST} container exec c5kvs_apptest pytest -v test_app.py"
        sh "docker -H ssh://${BUILD_HOST} container exec c5kvs_webtest pytest -v test_static.py"
        sh "docker -H ssh://${BUILD_HOST} container exec c5kvs_webtest pytest -v test_selenium.py"
      }
    }
    stage('Register') {
      steps {
        sh "docker -H ssh://${BUILD_HOST} tag c5kvs_web ${DOCKERHUB_USER}/c5kvs_web:${BUILD_TIMESTAMP}"
        sh "docker -H ssh://${BUILD_HOST} tag c5kvs_app ${DOCKERHUB_USER}/c5kvs_app:${BUILD_TIMESTAMP}"
        sh "docker -H ssh://${BUILD_HOST} push ${DOCKERHUB_USER}/mykvs_web:${BUILD_TIMESTAMP}"
        sh "docker -H ssh://${BUILD_HOST} push ${DOCKERHUB_USER}/mykvs_app:${BUILD_TIMESTAMP}"
      }
    }
    /*
    stage('Deploy') {
      steps {
        sh "cat docker-compose.prod.yml"
        sh "docker-compose -H ssh://${PROD_HOST} -f docker-compose.prod.yml build"
        sh "docker-compose -H ssh://${PROD_HOST} -f docker-compose.prod.yml up -d"
        sh "docker -H ssh://${PROD_HOST} container ls"
      }
    }
    */
  }
}