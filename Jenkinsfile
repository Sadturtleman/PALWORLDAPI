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
                    call .\\venv\\Scripts\\activate
                    call pylint PALWORLDAPI\\src > pylint_report.txt 2>&1 || exit /b 0
                    echo ==== Pylint Report Begin ====
                    type pylint_report.txt
                    echo ==== Pylint Report End ====
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
