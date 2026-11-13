from pathlib import Path

ATTACK_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = ATTACK_DIR.parent

DATA_DIR = PACKAGE_ROOT / "data"
MODEL_PATH = ATTACK_DIR / "model" / "rf_model.joblib"
RESULTS_DIR = ATTACK_DIR / "results"

SEED = 42