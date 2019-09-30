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

    /*
    stage('pull') {
      steps {
        git url: 'https://github.com/yuichi110/docker-web.git', branch: 'master'
      }
    }

    stage('hello') {
      steps {
        sh "pwd"
        sh "ls"
        sh "docker --version"
      }
    }
    */
  }
}