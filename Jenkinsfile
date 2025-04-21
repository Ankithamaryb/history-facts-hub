pipeline {
    agent any

    environment {
        PATH = "C:/Users/spank/AppData/Local/Microsoft/WindowsApps:$PATH"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/Ankithamaryb/history-facts-hub.git', branch: 'main', credentialsId: 'github-token'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-new-image .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 5001:5000 --name historical-facts-hub-container my-new-image'
            }
        }

        stage('Install Selenium Requirements') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/scripts/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                script {
                    dir('historicalfactshub') {
                        sh '''
                            source ../venv/scripts/activate
                            python -m unittest discover -s automation
                        '''
                    }
                }
            }
        }

        stage('Publish Selenium Report') {
            steps {
                sh 'source venv/scripts/activate'
                publishHTML(target: [
                    reportDir: '.', 
                    reportFiles: 'report.html', 
                    reportName: 'Selenium Test Report'
                ])
            }
        }
    }
}
