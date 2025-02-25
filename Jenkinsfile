# Create the Jenkinsfile
echo 'pipeline {
    agent any
    environment {
        PYTHON = "python3"
        PIP = "pip"
    }
    stages {
        stage("Installation des dépendances") {
            steps {
                echo "📦 Installation des dépendances..."
                sh "make install"
            }
        }
        stage("Préparation des données") {
            steps {
                echo "⚙️ Préparation des données..."
                sh "make prepare"
            }
        }
        stage("Entraînement du modèle") {
            steps {
                echo "🤖 Entraînement du modèle..."
                sh "make train"
            }
        }
        stage("Évaluation du modèle") {
            steps {
                echo "📊 Évaluation du modèle..."
                sh "make evaluate"
            }
        }
        stage("Vérifications (Lint/Sécurité)") {
            parallel {
                stage("💡 Linting") {
                    steps {
                        sh "make lint"
                    }
                }
                stage("🔐 Sécurité") {
                    steps {
                        sh "make security"
                    }
                }
            }
        }
        stage("Nettoyage") {
            steps {
                echo "🧹 Nettoyage des fichiers temporaires..."
                sh "make clean"
            }
        }
    }
    post {
        success {
            echo "✅ Pipeline exécuté avec succès !"
        }
        failure {
            echo "❌ Le pipeline a échoué."
        }
    }
}' > Jenkinsfile
