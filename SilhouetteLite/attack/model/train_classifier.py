import joblib
from sklearn.ensemble import RandomForestClassifier

from attack.config import MODEL_PATH, RESULTS_DIR, SEED
from attack.load_dataset import load_dataset, split
from attack.features.extract_features import extract_batch, FEATURE_NAMES
from attack.evaluate import evaluate, save_results, print_summary


def train():
    traces, labels, using_real = load_dataset()
    if not using_real:
        print("NOTE: real dataset not found in data/, using synthetic data\n")

    X = extract_batch(traces)
    X_train, X_test, y_train, y_test = split(X, labels)

    clf = RandomForestClassifier(
        n_estimators=150, min_samples_leaf=5, random_state=SEED, n_jobs=-1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    metrics = evaluate(y_test, y_pred)
    print_summary(metrics)

    importances = sorted(
        zip(FEATURE_NAMES, clf.feature_importances_),
        key=lambda pair: pair[1],
        reverse=True,
    )
    metrics["top_features"] = [
        {"feature": name, "importance": float(imp)} for name, imp in importances[:10]
    ]
    print("\ntop leaking features:")
    for name, imp in importances[:10]:
        print(f"  {name}: {imp:.3f}")

    save_results(metrics, RESULTS_DIR, y_test, y_pred)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": clf, "sites": sorted(set(labels)), "feature_names": FEATURE_NAMES},
        MODEL_PATH,
        compress=3,
    )
    print(f"\nsaved model -> {MODEL_PATH}")
    print(f"saved metrics -> {RESULTS_DIR}")


if __name__ == "__main__":
    train()