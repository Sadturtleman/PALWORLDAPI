pipeline {

    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Prepare') {
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
                    @echo off
                    call .\\venv\\Scripts\\activate
                    call pylint PALWORLDAPI\\src > pylint_report.txt 2>&1
                    echo ==== Pylint Report Begin ====
                    more pylint_report.txt
                    echo ==== Pylint Report End ====
                '''
            }
        }

        stage('test') {
            steps {
                echo 'test stage'
                // 필요 시 여기에 테스트 명령 추가
                // 예: bat 'call .\\venv\\Scripts\\activate && python -m unittest discover tests'
            }
        }

        stage('build') {
            steps {
                echo 'build stage'
                // 예: bat 'call .\\venv\\Scripts\\activate && python setup.py sdist bdist_wheel'
            }
        }

        stage('docker build') {
            steps {
                echo 'docker build stage'
                // 예: bat 'docker build -t palworld-api .'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'pylint_report.txt', onlyIfSuccessful: true
        }
    }
}
