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
                bat 'python -m venv venv'
                bat '.\\venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }
        stage('Static Code Analysis') {
            steps {
                echo 'Static Code Analysis stage'
                bat '''
                    .\\venv\\Scripts\\activate
                    pylint PALWORLDAPI\\src > pylint_report.txt || exit /b 0
                    type pylint_report.txt
                '''

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
