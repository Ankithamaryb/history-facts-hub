pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Ankithamaryb/history-facts-hub.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t history-facts-app .'
            }
        }

        stage('Run Flask Container') {
            steps {
                sh 'docker run -d -p 5000:5000 history-facts-app'
            }
        }
    }
}
