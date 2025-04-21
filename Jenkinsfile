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
            pip install -r requirements.txt
        '''
    }
}


        stages {
        stage('Run Selenium Tests') {
            steps {
                script {
                    // Activate the virtual environment with bash
                    sh 'bash -c "source venv/bin/activate && python -m unittest discover -s tests"'
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
