pipeline {
    agent any
    triggers{
        githubPush()
    }
    stages {
        stage('Prepare'){
            steps {
                echo 'Prepare stage'
                checkout scm
            }
        }
        stage('test') {
            steps {
                echo 'test stage'
            }
        }
        stage('build') {
            steps {
                echo 'build stage'
            }
        }
        stage('docker build') {
            steps {
                echo 'docker build stage'
            }
        }
    }
}
