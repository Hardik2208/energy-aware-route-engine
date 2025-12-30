import joblib
from pathlib import Path

from typing import Any

def load_energy_model(model_path: str) -> Any:

    model_file = Path(model_path)

    if not model_file.exists():
        raise FileNotFoundError(
            f"Energy model not found at: {model_path}"
        )

    return joblib.load(model_file)
