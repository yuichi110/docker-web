pipeline {
  agent any
  stages {
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
  }
}