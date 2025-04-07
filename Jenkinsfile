def pylintScore = "N/A"
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
                        pylint PALWORLDAPI\\src\\main.py --output-format=json > pylint.json 2>&1
                        pylint PALWORLDAPI\\src\\main.py > pylint_score.txt 2>&1
                        pylint-json2html -f json -o pylint_report.html pylint.json
                        if exist pylint_html rmdir /S /Q pylint_html
                        mkdir pylint_html
                        move pylint_report.html pylint_html\\report.html
                    '''

                    try {
                        def scoreText = readFile('pylint_score.txt')
                        def matcher = (scoreText =~ /rated at ([\\d\\.]+)/)
                        if (matcher.find()) {
                            pylintScore = matcher.group(1)
                        } else {
                            echo "⚠️ 점수 매칭 실패. 기본값 유지."
                            pylintScore = "0.0"
                        }
                    } catch (e) {
                        echo "❌ 점수 파일 읽기 실패: ${e.message}"
                        pylintScore = "0.0"
                    }

                    echo "🚀 Pylint Score: ${pylintScore}"

                    if (env.CHANGE_ID) {
                        echo "Detected PR #${env.CHANGE_ID}, Checking pylint score"
                        if (pylintScore.toDouble() < MIN_SCORE.toDouble()) {
                            error("🚫 PR 빌드 실패: Pylint 점수(${pylintScore})가 기준(${MIN_SCORE}) 미달입니다.")
                        }
                    } else {
                        echo "일반 push 빌드이므로 pylint 점수 체크를 건너뜁니다."
                    }

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

        success {
            script {
                def desc = "**💯 Pylint Score:** `${pylintScore}`\n✅ Build passed!"
                sendDiscordMessage("✅ Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}", desc, 65280)
            }
        }

        failure {
            script {
                def desc = "**💯 Pylint Score:** `${pylintScore}`\n❌ Build failed!"
                sendDiscordMessage("❌ Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}", desc, 16711680)
            }
        }
    }
}

def sendDiscordMessage(title, description, color) {
    withCredentials([string(credentialsId: 'DISCORD_WEBHOOK', variable: 'DISCORD_WEBHOOK')]) {
        writeFile file: 'send-discord.ps1', text: '''[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$WebhookUrl = $env:DISCORD_WEBHOOK
$Title = $env:DISCORD_TITLE
$Description = $env:DISCORD_DESCRIPTION
$Color = [int]$env:DISCORD_COLOR
$BuildUrl = $env:DISCORD_URL

$payload = @{
    username = "JenkinsBot"
    embeds = @(
        @{
            title = $Title
            description = $Description
            color = $Color
            url = $BuildUrl
            footer = @{ text = "Jenkins CI/CD" }
            timestamp = (Get-Date).ToString("o")
        }
    )
} | ConvertTo-Json -Depth 10

try {
    Invoke-RestMethod -Uri $WebhookUrl -Method Post -ContentType "application/json" -Body $payload
    Write-Output "✅ Discord message sent successfully."
} catch {
    Write-Error "❌ Failed to send Discord message: $($_.Exception.Message)"
    exit 1
}
''', encoding: 'UTF-8'

        withEnv([
            "DISCORD_WEBHOOK=${DISCORD_WEBHOOK}",
            "DISCORD_TITLE=${title}",
            "DISCORD_DESCRIPTION=${description}",
            "DISCORD_COLOR=${color}",
            "DISCORD_URL=${env.BUILD_URL}"
        ]) {
            bat '''powershell -ExecutionPolicy Bypass -Command "& { .\\send-discord.ps1 }"'''
        }
    }
}
