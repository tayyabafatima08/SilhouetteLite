import joblib

from attack.config import MODEL_PATH
from attack.features.extract_features import extract_features

_bundle = None


def _load():
    global _bundle
    if _bundle is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"No trained model at {MODEL_PATH}. "
                "Run: python -m attack.model.train_classifier"
            )
        _bundle = joblib.load(MODEL_PATH)
    return _bundle


def predict(trace):
    model = _load()["model"]
    probs = model.predict_proba([extract_features(trace)])[0]
    idx = probs.argmax()
    return {"site": str(model.classes_[idx]), "confidence": float(probs[idx])}


if __name__ == "__main__":
    from attack.load_dataset import load_dataset

    traces, labels, _ = load_dataset()
    for i in [0, 100, 500, 900]:
        out = predict(traces[i])
        print(f"actual={labels[i]}  predicted={out['site']}  confidence={out['confidence']:.2f}")