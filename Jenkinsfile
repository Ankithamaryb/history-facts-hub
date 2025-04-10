pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/Ankithamaryb/historical-facts-hub.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t flask-app .'
                }
            }
        }

        stage('Run Flask App') {
            steps {
                script {
                    sh 'docker run -d --rm --name flask-app --network flask-net -p 5000:5000 flask-app'
                }
            }
        }
    }
}
