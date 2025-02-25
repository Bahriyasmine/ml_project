import argparse
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn
import seaborn as sns
import matplotlib.pyplot as plt
from model_pipeline import prep, model, evaluate_model
from sklearn.metrics import precision_recall_curve, roc_curve, auc

# Ensure that seaborn and matplotlib are installed
try:
    import seaborn
    import matplotlib.pyplot as plt
except ImportError:
    import pip
    pip.main(['install', 'seaborn'])
    pip.main(['install', 'matplotlib'])
    import seaborn
    import matplotlib.pyplot as plt

CSV_FILE = "Churn_Modelling.csv"
MODEL_FILE = "model.joblib"

# Initialize MLflow tracking URI (optional)
mlflow.set_tracking_uri("http://127.0.0.1:5000")  # Use this line if you're running a local MLflow server.
mlflow.set_experiment("yasminebahriexperiment")  # Set the default experiment

def read_csv():
    try:
        data = pd.read_csv(CSV_FILE)
        print(f"Data loaded from {CSV_FILE}")
        return data
    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found.")
        return None

def save_model(clf):
    joblib.dump(clf, MODEL_FILE)
    print(f"Model saved to {MODEL_FILE}")

def load_model():
    try:
        clf = joblib.load(MODEL_FILE)
        print(f"Model loaded from {MODEL_FILE}")
        return clf
    except FileNotFoundError:
        print(f"Error: {MODEL_FILE} not found. Train the model first.")
        return None

def plot_roc_curve(y_test, y_score):
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(10, 8))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()

def plot_precision_recall_curve(y_test, y_score):
    precision, recall, _ = precision_recall_curve(y_test, y_score)
    plt.figure(figsize=(10, 8))
    plt.plot(recall, precision, color='b', lw=2)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.show()

def plot_histogram(y_test, y_pred):
    plt.figure(figsize=(10, 8))
    sns.histplot(y_pred, kde=True, color="blue")
    plt.title("Prediction Histogram")
    plt.xlabel("Predicted Values")
    plt.ylabel("Frequency")
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="ML Pipeline")
    parser.add_argument("--prepare", action="store_true", help="Prepare data")
    parser.add_argument("--train", action="store_true", help="Train model")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate model")
    parser.add_argument("--load", action="store_true", help="Load and evaluate existing model")
    parser.add_argument("--save", action="store_true", help="Save trained model")
    args = parser.parse_args()

    data = read_csv()
    if data is None:
        return

    if args.prepare or args.train or args.evaluate or args.load or args.save:
        try:
            x_train, x_test, y_train, y_test = prep()
            print("Data prepared.")
        except TypeError:
            print("Error: prep() function should not take arguments. Adjust model_pipeline.py.")
            return

    # Start MLflow experiment
    with mlflow.start_run():
        if args.train or args.save:
            clf = model(x_train, y_train)
            mlflow.log_param("model_type", "AdaBoost")  # Example of logging hyperparameters
            mlflow.log_param("n_estimators", 50)  # Example hyperparameter for AdaBoost
            accuracy, report = evaluate_model(clf, x_test, y_test)  # Now unpacking two values (accuracy, report)
            mlflow.log_metric("accuracy", accuracy)

            print("Model trained and saved.")
            save_model(clf)
            mlflow.sklearn.log_model(clf, "model")
            plot_roc_curve(y_test, clf.predict_proba(x_test)[:, 1])  # Using probabilities for ROC curve
            plot_precision_recall_curve(y_test, clf.predict_proba(x_test)[:, 1])  # Using probabilities
            plot_histogram(y_test, clf.predict(x_test))

        if args.evaluate:
            clf = model(x_train, y_train)
            accuracy, report = evaluate_model(clf, x_test, y_test)  # Now unpacking two values (accuracy, report)
            print(f"Accuracy: {accuracy}")
            print(f"Classification Report:\n{report}")
            mlflow.log_metric("accuracy", accuracy)
            plot_roc_curve(y_test, clf.predict_proba(x_test)[:, 1])  # Using probabilities for ROC curve
            plot_precision_recall_curve(y_test, clf.predict_proba(x_test)[:, 1])  # Using probabilities
            plot_histogram(y_test, clf.predict(x_test))

        if args.load:
            clf = load_model()
            if clf:
                accuracy, report = evaluate_model(clf, x_test, y_test)  # Now unpacking two values (accuracy, report)
                print(f"Accuracy: {accuracy}")
                print(f"Classification Report:\n{report}")
                mlflow.log_metric("accuracy", accuracy)
                plot_roc_curve(y_test, clf.predict_proba(x_test)[:, 1])  # Using probabilities for ROC curve
                plot_precision_recall_curve(y_test, clf.predict_proba(x_test)[:, 1])  # Using probabilities
                plot_histogram(y_test, clf.predict(x_test))

if __name__ == "__main__":
    main()

