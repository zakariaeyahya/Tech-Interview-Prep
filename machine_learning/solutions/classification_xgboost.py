"""
Pipeline CLASSIFICATION - Multi-algorithmes
===========================================
Algorithmes :
- Régression logistique (LogisticRegression)
- Random Forest (RandomForestClassifier)
- Gradient Boosting (GradientBoostingClassifier)
- XGBoost (XGBClassifier)

Techniques déséquilibre :
- SMOTE, ADASYN, RandomOverSampler, SMOTETomek
- class_weight='balanced' / scale_pos_weight

Métriques : accuracy, precision, recall, F1, ROC-AUC, matrice de confusion
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import ADASYN, RandomOverSampler, SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore", category=FutureWarning)

RANDOM_STATE = 42
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "credit_risk.csv"
TARGET = "defaulted"
CATEGORICAL_FEATURES = ["country", "sector"]
NUMERIC_FEATURES = [
    "revenue",
    "debt_ratio",
    "days_late",
    "num_employees",
    "credit_score",
    "years_in_business",
]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES

SAMPLERS = {
    "none": None,
    "smote": SMOTE(random_state=RANDOM_STATE, k_neighbors=5),
    "adasyn": ADASYN(random_state=RANDOM_STATE, n_neighbors=5),
    "random_over": RandomOverSampler(random_state=RANDOM_STATE),
    "smote_tomek": SMOTETomek(random_state=RANDOM_STATE),
}


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    print("=" * 60)
    print("EXPLORATION DES DONNÉES")
    print("=" * 60)
    print(f"Shape : {df.shape}")
    print(f"\nTaux de défaut (classe 1) : {df[TARGET].mean():.2%}")
    print(f"\nDistribution des classes :\n{df[TARGET].value_counts(normalize=True)}")
    print(f"\nValeurs manquantes :\n{df[FEATURES + [TARGET]].isnull().sum()}")
    return df


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
            ("num", StandardScaler(), NUMERIC_FEATURES),
        ]
    )


def get_classifiers(scale_pos_weight: float = 1.0) -> dict[str, object]:
    """Registre de tous les classificateurs disponibles."""
    return {
        "logistic_regression": LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE,
            class_weight="balanced",
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            random_state=RANDOM_STATE,
            class_weight="balanced",
            n_jobs=-1,
        ),
        "gradient_boosting": GradientBoostingClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
        ),
        "xgboost": xgb.XGBClassifier(
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            scale_pos_weight=scale_pos_weight,
        ),
    }


def build_pipeline(
    model_name: str = "xgboost",
    sampler_name: str = "smote",
    scale_pos_weight: float = 1.0,
) -> ImbPipeline:
    classifiers = get_classifiers(scale_pos_weight)
    if model_name not in classifiers:
        raise ValueError(f"Modèle inconnu : {model_name}. Disponibles : {list(classifiers)}")

    steps: list = [("preprocessor", build_preprocessor())]
    sampler = SAMPLERS.get(sampler_name)
    if sampler is not None:
        steps.append(("sampler", sampler))
    steps.append(("classifier", classifiers[model_name]))
    return ImbPipeline(steps)


def evaluate_predictions(y_test: pd.Series, y_pred: np.ndarray, y_proba: np.ndarray, label: str = "") -> dict:
    print(f"\n--- {label} ---" if label else "")
    print(f"Accuracy  : {(y_pred == y_test).mean():.4f}")
    print(f"Precision : {precision_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"Recall    : {recall_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"F1        : {f1_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"ROC-AUC   : {roc_auc_score(y_test, y_proba):.4f}")
    return {
        "accuracy": (y_pred == y_test).mean(),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }


def compare_algorithms(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    sampler_name: str = "smote",
    scale_pos_weight: float = 1.0,
) -> tuple[pd.DataFrame, ImbPipeline, str]:
    """Entraîne et compare tous les algorithmes de classification."""
    print("\n" + "=" * 60)
    print(f"COMPARAISON DES ALGORITHMES (sampler={sampler_name})")
    print("=" * 60)

    rows = []
    fitted: dict[str, ImbPipeline] = {}

    for name in get_classifiers(scale_pos_weight):
        pipeline = build_pipeline(name, sampler_name=sampler_name, scale_pos_weight=scale_pos_weight)
        pipeline.fit(X_train, y_train)
        fitted[name] = pipeline

        y_proba = pipeline.predict_proba(X_test)[:, 1]
        y_pred = pipeline.predict(X_test)
        metrics = evaluate_predictions(y_test, y_pred, y_proba, label=name)
        rows.append({"algorithm": name, **metrics})

    comparison = pd.DataFrame(rows).sort_values("f1", ascending=False)
    print("\n" + comparison.to_string(index=False))

    best_name = comparison.iloc[0]["algorithm"]
    print(f"\n>>> Meilleur algorithme (F1 test) : {best_name}")
    return comparison, fitted[best_name], best_name


def compare_samplers(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_name: str = "xgboost",
    scale_pos_weight: float = 1.0,
) -> pd.DataFrame:
    print("\n" + "=" * 60)
    print(f"COMPARAISON RÉÉCHANTILLONNAGE — {model_name}")
    print("=" * 60)

    rows = []
    for sampler_name in SAMPLERS:
        pipeline = build_pipeline(model_name, sampler_name, scale_pos_weight)
        pipeline.fit(X_train, y_train)
        y_proba = pipeline.predict_proba(X_test)[:, 1]
        y_pred = pipeline.predict(X_test)
        rows.append(
            {
                "sampler": sampler_name,
                "f1": f1_score(y_test, y_pred, zero_division=0),
                "recall": recall_score(y_test, y_pred, zero_division=0),
                "precision": precision_score(y_test, y_pred, zero_division=0),
                "roc_auc": roc_auc_score(y_test, y_proba),
            }
        )

    comparison = pd.DataFrame(rows).sort_values("f1", ascending=False)
    print(comparison.to_string(index=False))
    return comparison


def cross_validate_model(pipeline: ImbPipeline, X: pd.DataFrame, y: pd.Series, model_name: str = "") -> dict:
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    scorers = {"accuracy": "accuracy", "precision": "precision", "recall": "recall", "f1": "f1", "roc_auc": "roc_auc"}

    print("\n" + "=" * 60)
    print(f"VALIDATION CROISÉE STRATIFIÉE — {model_name}")
    print("=" * 60)

    results = {}
    for name, scoring in scorers.items():
        scores = cross_val_score(pipeline, X, y, cv=cv, scoring=scoring, n_jobs=-1)
        results[name] = scores
        print(f"{name:12s} : {scores.mean():.4f} (+/- {scores.std():.4f})")
    return results


def tune_hyperparameters(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_name: str = "xgboost",
    sampler_name: str = "smote",
    scale_pos_weight: float = 1.0,
    method: str = "random",
) -> GridSearchCV | RandomizedSearchCV:
    pipeline = build_pipeline(model_name, sampler_name, scale_pos_weight)

    param_grids = {
        "logistic_regression": {
            "classifier__C": [0.01, 0.1, 1, 10],
            "classifier__penalty": ["l2"],
            "classifier__solver": ["lbfgs", "saga"],
        },
        "random_forest": {
            "classifier__n_estimators": [100, 200, 300],
            "classifier__max_depth": [5, 8, 12, None],
            "classifier__min_samples_leaf": [1, 3, 5],
        },
        "gradient_boosting": {
            "classifier__n_estimators": [100, 200],
            "classifier__max_depth": [3, 5, 7],
            "classifier__learning_rate": [0.01, 0.05, 0.1],
        },
        "xgboost": {
            "classifier__max_depth": [3, 5, 7],
            "classifier__learning_rate": [0.01, 0.05, 0.1],
            "classifier__n_estimators": [100, 200, 300],
            "classifier__subsample": [0.7, 0.8, 1.0],
        },
    }

    param_grid = param_grids[model_name]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    print("\n" + "=" * 60)
    print(f"HYPERPARAMETER TUNING — {model_name} ({method.upper()})")
    print("=" * 60)

    SearchClass = GridSearchCV if method == "grid" else RandomizedSearchCV
    kwargs = {"n_iter": 15, "random_state": RANDOM_STATE} if method != "grid" else {}
    search = SearchClass(
        pipeline, param_grid, cv=cv, scoring="f1", n_jobs=-1, verbose=1, **kwargs
    )
    search.fit(X_train, y_train)
    print(f"Meilleurs paramètres : {search.best_params_}")
    print(f"Meilleur F1 (CV)      : {search.best_score_:.4f}")
    return search


def evaluate_model(model: ImbPipeline, X_test: pd.DataFrame, y_test: pd.Series, threshold: float = 0.5, label: str = "") -> dict:
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    print("\n" + "=" * 60)
    print(f"ÉVALUATION DÉTAILLÉE {f'— {label}' if label else ''} (seuil={threshold})")
    print("=" * 60)
    evaluate_predictions(y_test, y_pred, y_proba)

    precision_vals, recall_vals, _ = precision_recall_curve(y_test, y_proba)
    pr_auc = np.trapezoid(precision_vals, recall_vals)
    print(f"PR-AUC    : {pr_auc:.4f}")
    print("\nMatrice de confusion :\n", confusion_matrix(y_test, y_pred))
    print("\n", classification_report(y_test, y_pred, target_names=["Pas défaut", "Défaut"]))

    return {"y_proba": y_proba, "y_pred": y_pred}


def find_optimal_threshold(y_test: pd.Series, y_proba: np.ndarray, metric: str = "f1") -> float:
    best_score, best_t = 0.0, 0.5
    for t in np.arange(0.05, 0.96, 0.01):
        y_pred = (y_proba >= t).astype(int)
        score = {"precision": precision_score, "recall": recall_score, "f1": f1_score}[metric](
            y_test, y_pred, zero_division=0
        )
        if score > best_score:
            best_score, best_t = score, t
    print(f"\nSeuil optimal ({metric}) : {best_t:.2f} -> score = {best_score:.4f}")
    return best_t


def plot_evaluation(model: ImbPipeline, X_test, y_test, output_dir: Path, model_name: str = "best") -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=axes[0, 0], cmap="Blues")
    axes[0, 0].set_title(f"Matrice de confusion — {model_name}")
    RocCurveDisplay.from_predictions(y_test, y_proba, ax=axes[0, 1])
    PrecisionRecallDisplay.from_predictions(y_test, y_proba, ax=axes[1, 0])

    clf = model.named_steps["classifier"]
    if hasattr(clf, "feature_importances_"):
        imp = clf.feature_importances_
        top_n = min(15, len(imp))
        idx = np.argsort(imp)[-top_n:]
        axes[1, 1].barh(range(top_n), imp[idx])
        axes[1, 1].set_title("Feature importance")
    elif hasattr(clf, "coef_"):
        coef = np.abs(clf.coef_[0])
        top_n = min(15, len(coef))
        idx = np.argsort(coef)[-top_n:]
        axes[1, 1].barh(range(top_n), coef[idx])
        axes[1, 1].set_title("Coefficients absolus (Logistic Regression)")

    plt.tight_layout()
    path = output_dir / f"classification_{model_name}.png"
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"\nGraphiques sauvegardés : {path}")


def plot_algorithm_comparison(comparison: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    comparison.set_index("algorithm")[["precision", "recall", "f1", "roc_auc"]].plot(kind="bar", ax=ax, rot=45)
    ax.set_title("Comparaison des algorithmes (test)")
    ax.set_ylabel("Score")
    plt.tight_layout()
    path = output_dir / "classification_comparison.png"
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"Comparaison sauvegardée : {path}")


def main() -> None:
    df = load_data()
    X, y = df[FEATURES], df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    print(f"\nTrain : {len(X_train)} | Test : {len(X_test)}")
    print(f"Taux défaut train : {y_train.mean():.2%} | test : {y_test.mean():.2%}")

    neg, pos = (y_train == 0).sum(), (y_train == 1).sum()
    scale_pos_weight = neg / pos
    print(f"scale_pos_weight (XGBoost) : {scale_pos_weight:.2f}")

    # 1. Comparer tous les algorithmes (avec SMOTE)
    comparison, best_model, best_name = compare_algorithms(
        X_train, y_train, X_test, y_test, sampler_name="smote", scale_pos_weight=scale_pos_weight
    )
    plot_algorithm_comparison(comparison, Path(__file__).resolve().parent.parent / "outputs")

    # 2. Comparer techniques de rééchantillonnage sur le meilleur algo
    compare_samplers(X_train, y_train, X_test, y_test, model_name=best_name, scale_pos_weight=scale_pos_weight)

    # 3. Validation croisée
    cross_validate_model(
        build_pipeline(best_name, "smote", scale_pos_weight), X_train, y_train, model_name=best_name
    )

    # 4. Hyperparameter tuning du meilleur
    search = tune_hyperparameters(
        X_train, y_train, model_name=best_name, sampler_name="smote",
        scale_pos_weight=scale_pos_weight, method="random",
    )
    tuned_model = search.best_estimator_

    # 5. Évaluation détaillée + seuil optimal
    results = evaluate_model(tuned_model, X_test, y_test, label=best_name)
    optimal_t = find_optimal_threshold(y_test, results["y_proba"], metric="f1")
    evaluate_model(tuned_model, X_test, y_test, threshold=optimal_t, label=f"{best_name} (seuil optimisé)")

    plot_evaluation(tuned_model, X_test, y_test, Path(__file__).resolve().parent.parent / "outputs", best_name)

    print("\n" + "=" * 60)
    print("ALGORITHMES & TECHNIQUES COUVERTS")
    print("=" * 60)
    print("""
    Algorithmes :
    - Regression logistique (LogisticRegression + class_weight)
    - Random Forest (RandomForestClassifier)
    - Gradient Boosting (GradientBoostingClassifier)
    - XGBoost (XGBClassifier + scale_pos_weight)

    Techniques desequilibre :
    - SMOTE | ADASYN | RandomOverSampler | SMOTETomek

    Evaluation :
    - StratifiedKFold | GridSearch / RandomizedSearch
    - Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC
    - Matrice de confusion | Seuil optimal | Courbes ROC/PR
    """)


if __name__ == "__main__":
    main()
