pipeline {
    agent any

    stages {  // 

        stage('Checkout Code') {
            steps {
                git credentialsId: 'github-token', branch: 'main', url: 'https://github.com/Ankithamaryb/history-facts-hub.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'docker build -t historical-facts-hub .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh '''
                    docker rm -f flask-app || true
                    docker run -d --name flask-app \
                      --network flask-net \
                      -p 5000:5000 \
                      historical-facts-hub
                '''
            }
        }

    } // 
}
