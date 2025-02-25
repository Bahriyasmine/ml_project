pipeline {
    agent any
    environment {
        PYTHON = 'python3'
        PIP = 'pip'
    }
    stages {
        stage('Installation des dépendances') {
            steps {
                echo '📦 Installation des dépendances...'
                sh 'make install'
            }
        }
        stage('Préparation des données') {
            steps {
                echo '⚙️ Préparation des données...'
                sh 'make prepare'
            }
        }
        stage('Phase 1: Entraînement du modèle') {
            steps {
                echo '🤖 Entraînement du modèle phase 1...'
                sh 'make train_phase1'
            }
        }
        stage('Phase 2: Affinement du modèle') {
            steps {
                echo '⚙️ Affinement du modèle phase 2...'
                sh 'make train_phase2'
            }
        }
        stage('Phase 3: Evaluation du modèle') {
            steps {
                echo '📊 Évaluation du modèle phase 3...'
                sh 'make evaluate'
            }
        }
        stage('Vérifications (Lint/Sécurité)') {
            parallel {
                stage('💡 Linting') {
                    steps {
                        sh 'make lint'
                    }
                }
                stage('🔐 Sécurité') {
                    steps {
                        sh 'make security'
                    }
                }
            }
        }
        stage('Nettoyage') {
            steps {
                echo '🧹 Nettoyage des fichiers temporaires...'
                sh 'make clean'
            }
        }
    }
    post {
        success {
            echo '✅ Pipeline exécuté avec succès !'
        }
        failure {
            echo '❌ Le pipeline a échoué.'
        }
    }
}

