pipeline {
    agent any

    environment {
        ENVIRONMENT = "prod"
    }

    tools {
        python 'Python 3.12'  // Название должно совпадать с настройкой в Global Tool Configuration
    }

    stages {
        stage('Setup venv and install deps') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
