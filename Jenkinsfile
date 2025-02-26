pipeline {
    agent any

    stages {
        stage('Installation des dépendances') {
            steps {
                echo '📦 Installation des dépendances...'
                sh 'make install'
            }
        }

        stage('Préparation des données') {
            steps {
                echo '📊 Préparation des données...'
                sh 'make prepare'
            }
        }

        stage('Phase 1: Entraînement du modèle') {
            steps {
                echo '🤖 Entraînement du modèle...'
                sh 'make train'  // Updated from 'train_phase1' to 'train'
            }
        }

        stage('Évaluation du modèle') {
            steps {
                echo '📈 Évaluation du modèle...'
                sh 'make evaluate'
            }
        }

        stage('Vérifications (Lint/Sécurité)') {
            parallel {
                stage('💡 Linting') {
                    steps {
                        echo '🔍 Vérification de la qualité du code...'
                        sh 'make lint'
                    }
                }

                stage('🔐 Sécurité') {
                    steps {
                        echo '🔎 Vérification de la sécurité du code...'
                        sh 'make security'
                    }
                }
            }
        }

        stage('Nettoyage') {
            steps {
                echo '🧹 Nettoyage des fichiers inutiles...'
                sh 'make clean'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline terminé avec succès !'
        }
        failure {
            echo '❌ Le pipeline a échoué.'
        }
    }
}

