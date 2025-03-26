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
                    echo === Running pylint and generating JSON ===
                    pylint PALWORLDAPI\\src --output-format=json > pylint.json || exit /b 0
                '''
                
                bat '''
                    @echo off
                    echo === Showing JSON contents ===
                    type pylint.json
                '''
                
                bat '''
                    @echo off
                    echo === Converting JSON to HTML ===
                    python -m pylint_json2html -f json -o pylint_report.html pylint.json
                '''

                bat '''
                    @echo off
                    echo === Final directory contents ===
                    dir
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
            archiveArtifacts artifacts: 'pylint_report.html', onlyIfSuccessful: true
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'pylint_report.html',
                reportName: 'Pylint HTML Report'
            ])
        }
    }
}
