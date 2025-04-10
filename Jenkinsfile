pipeline {
    agent any

    stages {  // 

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Ankithamaryb/flask-docker-demo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                    . venv/bin/activate
                    nohup python app.py &
                '''
            }
        }

    } // 
}
