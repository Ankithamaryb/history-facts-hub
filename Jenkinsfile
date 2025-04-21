pipeline {
    agent any

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
            . venv/bin/activate
            pip install -r automation/requirements.txt
        '''
    }
}


        stage('Run Selenium Tests') {
            steps {
                sh '''
                source venv/bin/activate
                pytest Automation/ --html=report.html
                '''
            }
        }

        stage('Publish Selenium Report') {
            steps {
                publishHTML(target: [
                    reportDir: '.', 
                    reportFiles: 'report.html', 
                    reportName: 'Selenium Test Report'
                ])
            }
        }
    }
}
