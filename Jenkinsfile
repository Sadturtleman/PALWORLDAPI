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
                        pylint PALWORLDAPI\\src --output-format=json > pylint.json || exit /b 0
                        pylint-json2html -f json -o pylint_report.html pylint.json

                        if exist pylint_html rmdir /S /Q pylint_html
                        mkdir pylint_html
                        move pylint_report.html pylint_html\\index.html
                    '''

                    if (env.CHANGE_ID) { // PR일 때만 점수 체크
                        echo "Detected Pull Request: #${env.CHANGE_ID}, Checking pylint score"

                        bat '''
                            @echo off
                            call %VENV_DIR%\\Scripts\\activate
                            pylint PALWORLDAPI\\src > pylint_score.txt || exit /b 0
                        '''

                        def pylintScoreText = readFile('pylint_score.txt')
                        def matcher = (pylintScoreText =~ /Your code has been rated at ([0-9\\.]+)/)
                        if (matcher) {
                            def pylintScore = matcher[0][1].toFloat()
                            echo "Pylint Score: ${pylintScore}"

                            if (pylintScore < MIN_SCORE.toFloat()) {
                                error("🚫 PR 빌드 실패: Pylint 점수(${pylintScore})가 기준(${MIN_SCORE}) 미달입니다.")
                            }
                        } else {
                            error("Pylint 점수를 읽을 수 없습니다.")
                        }
                    } else {
                        echo "일반 push 빌드이므로 pylint 점수 체크를 건너뜁니다."
                    }
                }
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
