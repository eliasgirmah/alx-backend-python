pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        REPO_DIR = 'messaging_app'
        GIT_CREDENTIALS_ID = 'github-creds'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: "${GIT_CREDENTIALS_ID}", url: 'https://github.com/eliasgirmah/alx-backend-python.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y python3-pip python3-venv
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r ${REPO_DIR}/requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest ${REPO_DIR} --junitxml=test-results.xml
                '''
            }
        }

        stage('Publish Test Report') {
            steps {
                junit 'test-results.xml'
            }
        }
    }
}
