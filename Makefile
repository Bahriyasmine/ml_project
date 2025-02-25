# Variables
PYTHON = python3
PIP = pip
REQUIREMENTS_FILE = requirements.txt
MAIN_SCRIPT = main.py
MODEL_FILE = model.joblib
SEND_NOTIF_SCRIPT = send_notif.py
SEND_EMAIL_SCRIPT = send_email.py

# 1. Installation des dépendances
install:
	@$(PIP) install -r $(REQUIREMENTS_FILE)

# 2. Préparation des données et Exécution des étapes liées au modèle
prepare:
	@$(PYTHON) $(MAIN_SCRIPT) --prepare

train:
	@$(PYTHON) $(MAIN_SCRIPT) --train --save
	@$(PYTHON) $(SEND_NOTIF_SCRIPT) "Training Complete" "The ML model has been successfully trained and saved."
	@$(PYTHON) $(SEND_EMAIL_SCRIPT) "Model Training Complete" "The ML model has been successfully trained and saved."

evaluate:
	@$(PYTHON) $(MAIN_SCRIPT) --evaluate --load
	@$(PYTHON) $(SEND_NOTIF_SCRIPT) "Evaluation Complete" "The ML model has been successfully evaluated."
	@$(PYTHON) $(SEND_EMAIL_SCRIPT) "Model Evaluation Complete" "The ML model has been successfully evaluated."

load:
	@$(PYTHON) $(MAIN_SCRIPT) --load
	@$(PYTHON) $(SEND_NOTIF_SCRIPT) "Model Loaded" "The ML model has been successfully loaded."
	@$(PYTHON) $(SEND_EMAIL_SCRIPT) "Model Loaded" "The ML model has been successfully loaded."

save:
	@$(PYTHON) $(MAIN_SCRIPT) --save
	@$(PYTHON) $(SEND_NOTIF_SCRIPT) "Model Saved" "The ML model has been successfully saved."
	@$(PYTHON) $(SEND_EMAIL_SCRIPT) "Model Saved" "The ML model has been successfully saved."

# 3. Notifications et Emails
send-notif:
	@$(PYTHON) $(SEND_NOTIF_SCRIPT) "Custom Notification" "This is a custom notification."

send-email:
	@$(PYTHON) $(SEND_EMAIL_SCRIPT) "Custom Email" "This is a custom email."

# 4. Etapes CI
lint:
	@pylint $(MAIN_SCRIPT) model_pipeline.py $(SEND_NOTIF_SCRIPT) $(SEND_EMAIL_SCRIPT)

format:
	@black $(MAIN_SCRIPT) model_pipeline.py $(SEND_NOTIF_SCRIPT) $(SEND_EMAIL_SCRIPT)

security:
	@bandit -r $(MAIN_SCRIPT) model_pipeline.py $(SEND_NOTIF_SCRIPT) $(SEND_EMAIL_SCRIPT)

# 5. Nettoyage
clean:
	@rm -f $(MODEL_FILE) *.joblib
	@find . -type d -name "__pycache__" -exec rm -rf {} +

# 6. Aide
help:
	@echo "Commandes disponibles :"
	@echo "  make install       - Installer les dépendances"
	@echo "  make prepare       - Préparer les données"
	@echo "  make train         - Entraîner le modèle"
	@echo "  make evaluate      - Évaluer le modèle"
	@echo "  make load          - Charger le modèle"
	@echo "  make save          - Sauvegarder le modèle"
	@echo "  make send-notif    - Envoyer une notification"
	@echo "  make send-email    - Envoyer un email"
	@echo "  make lint          - Vérifier la qualité du code"
	@echo "  make format        - Formater le code"
	@echo "  make security      - Vérifier la sécurité du code"
	@echo "  make clean         - Nettoyer les fichiers inutiles"

# Tâche par défaut
default: install

