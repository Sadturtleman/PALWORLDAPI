pipeline {
    agent any
    stages {
        stage('Prepare'){
            steps {
                git credentialsId : '{github}',
                    branch : '{main}',
                    url : 'https://github.com/Sadturtleman/PALWORLDAPI.git'
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
