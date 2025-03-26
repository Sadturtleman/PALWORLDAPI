pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        VENV_DIR = 'venv'
        MIN_SCORE = 8.0
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
                        call %VENV_DIR%\\Scripts\\activate

                        echo === Running pylint and generating HTML report ===
                        pylint PALWORLDAPI\\src --output-format=json > pylint.json
                        pylint-json2html -f json -o pylint_report.html pylint.json

                        if exist pylint_html rmdir /S /Q pylint_html
                        mkdir pylint_html

                        rem HTML 보고서에 점수 추가
                        echo ^<h2 style="padding:10px; background:#f2f2f2;"^>Pylint Score: >> pylint_html\\index.html
                    '''

                    def pylintJson = readJSON(file: 'pylint.json')
                    def pylintScore = pylintJson.find { it.type == 'report' }?.score ?: "0"

                    // 점수를 HTML에 직접 추가하는 방식
                    writeFile file: 'pylint_html/index.html', text: """
                    <html>
                        <body>
                            <h2 style="padding:10px; background:#f2f2f2;">🚀 Pylint Score: ${pylintScore}</h2>
                            ${readFile('pylint_report.html')}
                        </body>
                    </html>
                    """

                    echo "Pylint Score: ${pylintScore}"

                    if (env.CHANGE_ID) {
                        echo "Detected PR #${env.CHANGE_ID}, Checking pylint score"
                        if (pylintScore.toString().toDouble() < MIN_SCORE.toString().toDouble()) {
                            error("🚫 PR 빌드 실패: Pylint 점수(${pylintScore})가 기준(${MIN_SCORE}) 미달입니다.")
                        }
                    } else {
                        echo "일반 push 빌드이므로 pylint 점수 체크를 건너뜁니다."
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
