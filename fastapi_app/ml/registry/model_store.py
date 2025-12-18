import mlflow
import joblib
from pathlib import Path

class NetPredictModelStore:
    BASE_PATH = Path("models")

    @staticmethod
    def save(model, name, metrics=None):
        mlflow.start_run()
        if metrics:
            for k, v in metrics.items():
                mlflow.log_metric(k, v)
        path = NetPredictModelStore.BASE_PATH / f"{name}.joblib"
        joblib.dump(model, path)
        mlflow.log_artifact(str(path))
        mlflow.end_run()

    @staticmethod
    def load(name):
        return joblib.load(NetPredictModelStore.BASE_PATH / f"{name}.joblib")