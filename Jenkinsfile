pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        VENV_DIR = 'venv'
        MIN_SCORE = 8.0
        PYTHONUTP8 = '1'
    }

    stages {
        stage('Prepare') {
            steps {
                checkout scm
                bat '''
                    @echo off
                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate && pip install -r requirements.txt
                '''
            }
        }

        stage('Static Code Analysis') {
            steps {
                script {
                    bat '''
                        @echo off
                        call %VENV_DIR%\\Scripts\\activate.bat

                        pylint PALWORLDAPI\\src --output-format=json > pylint.json
                        pylint-json2html -f json -o pylint_report.html pylint.json
                        
                        if exist pylint_html rmdir /S /Q pylint_html
                        mkdir pylint_html
                        move pylint_report.html pylint_html\\report.html
                    '''

                    def pylintJson = readJSON(file: 'pylint.json')
                    echo "=== Pylint JSON 출력 (디버깅) ==="
                    for (item in pylintJson) {
                        echo "Item: ${item}"
                    }

                    def pylintScore = "0"
                    for (item in pylintJson) {
                        if (item.type == 'report' && item.score != null) {
                            pylintScore = item.score.toString()
                            break
                        }
                    }
                    echo "최종 추출한 Pylint Score: ${pylintScore}"
                    writeFile file: 'pylint_html/index.html', text: """
                    <html>
                        <body>
                            <h2>Pylint Score: ${pylintScore}</h2>
                            ${readFile('pylint_html/report.html')}
                        </body>
                    </html>
                    """

                    echo "Pylint Score: ${pylintScore}"

                    if (env.CHANGE_ID) {
                        if (pylintScore.toDouble() < MIN_SCORE.toDouble()) {
                            error("🚫 PR 빌드 실패: Pylint 점수(${pylintScore})가 기준(${MIN_SCORE}) 미달입니다.")
                        }
                    }
                }
            }
        }

        stage('test') {
            steps { echo 'test stage' }
        }

        stage('build') {
            steps { echo 'build stage' }
        }

        stage('docker build') {
            steps { echo 'docker build stage' }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'pylint_html/index.html', onlyIfSuccessful: false
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
