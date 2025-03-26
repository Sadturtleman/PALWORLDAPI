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

                // pylint JSON 리포트 생성
                bat '''
                    @echo off
                    call .\\venv\\Scripts\\activate
                    echo === Running pylint and generating JSON ===
                    pylint PALWORLDAPI\\src --output-format=json > pylint.json || exit /b 0
                '''

                // JSON 확인
                bat '''
                    @echo off
                    echo === Showing JSON contents ===
                    type pylint.json
                '''

                // HTML 생성
                bat '''
                    @echo off
                    echo === Converting JSON to HTML ===
                    .\\venv\\Scripts\\pylint-json2html -f json -o pylint_report.html pylint.json
                '''

                // 리포트용 디렉토리 생성 + 이름 변경
                bat '''
                    @echo off
                    mkdir pylint_html
                    move pylint_report.html pylint_html\\index.html
                '''

                // 확인용 출력
                bat '''
                    @echo off
                    echo === Final directory contents ===
                    dir pylint_html
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

    post {
        always {
            archiveArtifacts artifacts: 'pylint_html/index.html', onlyIfSuccessful: true
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'pylint_html',
                reportFiles: 'index.html',
                reportName: 'Pylint HTML Report'
            ])
        }
    }
}
