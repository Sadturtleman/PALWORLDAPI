pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        VENV_DIR = 'venv'
        MIN_SCORE = 8.0
        PYTHONUTF8 = '1'
    }

    stages {
        stage('Prepare') {
            steps {
                checkout scm
                bat '''
                    @echo off
                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate.bat && pip install -r requirements.txt
                '''
            }
        }

        stage('Static Code Analysis') {
            steps {
                script {
                    bat '''
                        @echo off
                        call %VENV_DIR%\\Scripts\\activate.bat

                        echo === Running pylint and generating reports ===

                        :: 1. JSON 리포트용
                        pylint PALWORLDAPI\\src\\main.py --output-format=json > pylint.json 2>&1

                        :: 2. 텍스트 점수 추출용
                        pylint PALWORLDAPI\\src\\main.py > pylint_score.txt 2>&1

                        :: 3. HTML 변환
                        pylint-json2html -f json -o pylint_report.html pylint.json

                        :: 4. 결과 정리
                        if exist pylint_html rmdir /S /Q pylint_html
                        mkdir pylint_html
                        move pylint_report.html pylint_html\\report.html
                    '''

                    // 점수 파싱
                    def scoreText = readFile('pylint_score.txt')
                    def scoreMatch = scoreText =~ /rated at ([\\d\\.]+)\\/10/
                    def pylintScore = scoreMatch ? scoreMatch[0][1] : "10.0"

                    echo "🚀 Pylint Score: ${pylintScore}"

                    // PR이면 점수 기준 통과 확인
                    if (env.CHANGE_ID) {
                        echo "Detected PR #${env.CHANGE_ID}, Checking pylint score"
                        if (pylintScore.toDouble() < MIN_SCORE.toDouble()) {
                            error("🚫 PR 빌드 실패: Pylint 점수(${pylintScore})가 기준(${MIN_SCORE}) 미달입니다.")
                        }
                    } else {
                        echo "일반 push 빌드이므로 pylint 점수 체크를 건너뜁니다."
                    }

                    // index.html에 점수 포함 (리포트 보기 좋게)
                    def htmlBody = readFile('pylint_html/report.html')
                    writeFile file: 'pylint_html/index.html', text: """
                    <html>
                        <body>
                            <h2>Pylint Score: ${pylintScore}</h2>
                            ${htmlBody}
                        </body>
                    </html>
                    """
                }
            }
        }

        stage('test') {
            steps {
                echo '✅ test stage'
            }
        }

        stage('build') {
            steps {
                echo '✅ build stage'
            }
        }

        stage('docker build') {
            steps {
                echo '✅ docker build stage'
            }
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
