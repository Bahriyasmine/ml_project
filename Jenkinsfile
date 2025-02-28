pipeline {
    agent any

    environment {
        // Set any environment variables here if needed
        CSV_FILE = "Churn_Modelling.csv"
        MODEL_FILE = "model.joblib"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo '📦 Installing dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Prepare Data') {
            steps {
                echo '📊 Preparing data...'
                sh 'python3 main.py --prepare' // Updated to python3
            }
        }

        stage('Train Model') {
            steps {
                echo '🤖 Training model...'
                sh 'python3 main.py --train' // Updated to python3
            }
        }

        stage('Evaluate Model') {
            steps {
                echo '📈 Evaluating model...'
                sh 'python3 main.py --evaluate' // Updated to python3
            }
        }

        stage('Save Model') {
            steps {
                echo '💾 Saving model...'
                sh 'python3 main.py --save' // Updated to python3
            }
        }

        stage('Load Model & Evaluate') {
            steps {
                echo '🔄 Loading and evaluating model...'
                sh 'python3 main.py --load' // Updated to python3
            }
        }

        stage('Post-Training Checks') {
            parallel {
                stage('Linting') {
                    steps {
                        echo '🔍 Checking code quality...'
                        sh 'flake8 .' // This assumes flake8 is installed
                    }
                }

                stage('Security') {
                    steps {
                        echo '🔐 Checking security...'
                        sh 'bandit -r .' // This assumes bandit is installed
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                echo '🧹 Cleaning up...'
                sh 'rm -rf __pycache__'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}

