"""
Pipeline RÉGRESSION - Multi-algorithmes
=======================================
Algorithmes :
- Régression linéaire (LinearRegression)
- Régression polynomiale (PolynomialFeatures + LinearRegression)
- XGBoost (XGBRegressor)

Techniques :
- Train/Test split, KFold CV, GridSearchCV / RandomizedSearchCV
- Métriques : RMSE, MAE, R², MAPE | Analyse des résidus | Overfitting
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
    median_absolute_error,
    r2_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    RandomizedSearchCV,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler

warnings.filterwarnings("ignore", category=FutureWarning)

RANDOM_STATE = 42
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "credit_risk.csv"
TARGET = "expected_loss"
CATEGORICAL_FEATURES = ["country", "sector"]
NUMERIC_FEATURES = [
    "revenue",
    "debt_ratio",
    "days_late",
    "num_employees",
    "credit_score",
    "years_in_business",
    "defaulted",
]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    print("=" * 60)
    print("EXPLORATION DES DONNÉES")
    print("=" * 60)
    print(f"Shape : {df.shape}")
    print(f"\nStatistiques cible ({TARGET}) :\n{df[TARGET].describe()}")
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


def get_regression_models() -> dict[str, Callable[[], Pipeline]]:
    """Registre de tous les algorithmes de régression disponibles."""

    def linear_regression() -> Pipeline:
        return Pipeline(
            [
                ("preprocessor", build_preprocessor()),
                ("regressor", LinearRegression()),
            ]
        )

    def polynomial_regression(degree: int = 2) -> Pipeline:
        return Pipeline(
            [
                ("preprocessor", build_preprocessor()),
                ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
                ("regressor", LinearRegression()),
            ]
        )

    def xgboost_regressor() -> Pipeline:
        return Pipeline(
            [
                ("preprocessor", build_preprocessor()),
                (
                    "regressor",
                    xgb.XGBRegressor(
                        objective="reg:squarederror",
                        random_state=RANDOM_STATE,
                        n_estimators=300,
                        max_depth=5,
                        learning_rate=0.05,
                        subsample=0.8,
                        colsample_bytree=0.8,
                    ),
                ),
            ]
        )

    return {
        "linear_regression": linear_regression,
        "polynomial_regression_deg2": lambda: polynomial_regression(degree=2),
        "polynomial_regression_deg3": lambda: polynomial_regression(degree=3),
        "xgboost": xgboost_regressor,
    }


def build_pipeline(model_name: str = "xgboost") -> Pipeline:
    models = get_regression_models()
    if model_name not in models:
        raise ValueError(f"Modèle inconnu : {model_name}. Disponibles : {list(models)}")
    return models[model_name]()


def compute_regression_metrics(y_true: pd.Series | np.ndarray, y_pred: np.ndarray) -> dict:
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    medae = median_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    mask = np.array(y_true) != 0
    mape = mean_absolute_percentage_error(y_true[mask], y_pred[mask]) if mask.any() else np.nan
    return {"RMSE": rmse, "MAE": mae, "MedAE": medae, "R2": r2, "MAPE": mape}


def print_metrics(metrics: dict, prefix: str = "") -> None:
    label = f"{prefix} " if prefix else ""
    print(f"{label}RMSE  : {metrics['RMSE']:.2f}")
    print(f"{label}MAE   : {metrics['MAE']:.2f}")
    print(f"{label}MedAE : {metrics['MedAE']:.2f}")
    print(f"{label}R²    : {metrics['R2']:.4f}")
    print(f"{label}MAPE  : {metrics['MAPE']:.2%}")


def compare_algorithms(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> pd.DataFrame:
    """Entraîne et compare tous les algorithmes de régression."""
    print("\n" + "=" * 60)
    print("COMPARAISON DES ALGORITHMES DE RÉGRESSION")
    print("=" * 60)

    rows = []
    fitted_models: dict[str, Pipeline] = {}

    for name, factory in get_regression_models().items():
        model = factory()
        model.fit(X_train, y_train)
        fitted_models[name] = model

        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        train_m = compute_regression_metrics(y_train, y_pred_train)
        test_m = compute_regression_metrics(y_test, y_pred_test)

        rows.append(
            {
                "algorithm": name,
                "train_R2": train_m["R2"],
                "test_R2": test_m["R2"],
                "test_RMSE": test_m["RMSE"],
                "test_MAE": test_m["MAE"],
                "test_MAPE": test_m["MAPE"],
                "overfit_gap": train_m["R2"] - test_m["R2"],
            }
        )

    comparison = pd.DataFrame(rows).sort_values("test_RMSE")
    print(comparison.to_string(index=False))

    best_name = comparison.iloc[0]["algorithm"]
    print(f"\n>>> Meilleur algorithme (RMSE test) : {best_name}")
    return comparison, fitted_models[best_name], best_name


def cross_validate_model(model: Pipeline, X: pd.DataFrame, y: pd.Series, model_name: str = "", cv_folds: int = 5) -> dict:
    cv = KFold(n_splits=cv_folds, shuffle=True, random_state=RANDOM_STATE)
    scorers = {"neg_rmse": "neg_root_mean_squared_error", "neg_mae": "neg_mean_absolute_error", "r2": "r2"}

    print("\n" + "=" * 60)
    print(f"VALIDATION CROISÉE — {model_name or 'modèle'}")
    print("=" * 60)

    results = {}
    for name, scoring in scorers.items():
        scores = cross_val_score(model, X, y, cv=cv, scoring=scoring, n_jobs=-1)
        if "neg" in name:
            scores = -scores
        results[name] = scores
        print(f"{name:12s} : {scores.mean():.4f} (+/- {scores.std():.4f})")
    return results


def tune_hyperparameters(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_name: str = "xgboost",
    method: str = "random",
) -> GridSearchCV | RandomizedSearchCV:
    pipeline = build_pipeline(model_name)

    param_grids = {
        "linear_regression": {},
        "polynomial_regression_deg2": {
            "poly__degree": [2, 3],
        },
        "polynomial_regression_deg3": {
            "poly__degree": [2, 3, 4],
        },
        "xgboost": {
            "regressor__max_depth": [3, 5, 7],
            "regressor__learning_rate": [0.01, 0.05, 0.1],
            "regressor__n_estimators": [100, 200, 300],
            "regressor__subsample": [0.7, 0.8, 1.0],
        },
    }

    param_grid = param_grids.get(model_name, {})
    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    print("\n" + "=" * 60)
    print(f"HYPERPARAMETER TUNING — {model_name} ({method.upper()})")
    print("=" * 60)

    if not param_grid:
        print("Pas de grille de hyperparamètres pour ce modèle.")
        pipeline.fit(X_train, y_train)
        search = GridSearchCV(pipeline, {}, cv=cv)
        search.best_estimator_ = pipeline
        search.best_score_ = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="neg_root_mean_squared_error").mean()
        return search

    SearchClass = GridSearchCV if method == "grid" else RandomizedSearchCV
    kwargs = {"n_iter": 15, "random_state": RANDOM_STATE} if method != "grid" else {}
    search = SearchClass(
        pipeline,
        param_grid,
        cv=cv,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
        verbose=1,
        **kwargs,
    )
    search.fit(X_train, y_train)
    print(f"Meilleurs paramètres : {search.best_params_}")
    print(f"Meilleur RMSE (CV)     : {-search.best_score_:.2f}")
    return search


def evaluate_model(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series, label: str = "") -> dict:
    y_pred = model.predict(X_test)
    metrics = compute_regression_metrics(y_test, y_pred)
    residuals = y_test.values - y_pred

    print("\n" + "=" * 60)
    print(f"ÉVALUATION TEST {f'— {label}' if label else ''}")
    print("=" * 60)
    print_metrics(metrics)
    print(f"\nRésidus — mean : {residuals.mean():.2f} | std : {residuals.std():.2f}")
    return {"y_pred": y_pred, "residuals": residuals, "metrics": metrics}


def analyze_overfitting(model: Pipeline, X_train, y_train, X_test, y_test) -> None:
    train_m = compute_regression_metrics(y_train, model.predict(X_train))
    test_m = compute_regression_metrics(y_test, model.predict(X_test))

    print("\n" + "=" * 60)
    print("ANALYSE OVERFITTING (Train vs Test)")
    print("=" * 60)
    print("--- TRAIN ---")
    print_metrics(train_m)
    print("\n--- TEST ---")
    print_metrics(test_m)
    if train_m["R2"] - test_m["R2"] > 0.15:
        print("\n[!] Ecart R2 important : risque d'overfitting (typique regression polynomiale).")


def plot_evaluation(model: Pipeline, X_test, y_test, output_dir: Path, model_name: str = "best") -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    y_pred = model.predict(X_test)
    residuals = y_test.values - y_pred

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    axes[0, 0].scatter(y_test, y_pred, alpha=0.5, edgecolors="k", linewidth=0.3)
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    axes[0, 0].plot(lims, lims, "r--", lw=2)
    axes[0, 0].set_xlabel("Valeurs réelles")
    axes[0, 0].set_ylabel("Prédictions")
    axes[0, 0].set_title(f"Prédictions vs Réel — {model_name}")

    axes[0, 1].scatter(y_pred, residuals, alpha=0.5, edgecolors="k", linewidth=0.3)
    axes[0, 1].axhline(0, color="r", linestyle="--")
    axes[0, 1].set_title("Résidus vs Prédictions")

    axes[1, 0].hist(residuals, bins=30, edgecolor="black", alpha=0.7)
    axes[1, 0].set_title("Distribution des résidus")

    regressor = model.named_steps["regressor"]
    if hasattr(regressor, "feature_importances_"):
        imp = regressor.feature_importances_
        top_n = min(15, len(imp))
        idx = np.argsort(imp)[-top_n:]
        axes[1, 1].barh(range(top_n), imp[idx])
        axes[1, 1].set_title("Feature importance (XGBoost)")
    elif hasattr(regressor, "coef_"):
        coef = np.abs(regressor.coef_)
        top_n = min(15, len(coef))
        idx = np.argsort(coef)[-top_n:]
        axes[1, 1].barh(range(top_n), coef[idx])
        axes[1, 1].set_title("Coefficients absolus (Linéaire/Polynôme)")
    else:
        axes[1, 1].text(0.5, 0.5, "Pas d'importance disponible", ha="center", va="center")
        axes[1, 1].axis("off")

    plt.tight_layout()
    plot_path = output_dir / f"regression_{model_name}.png"
    plt.savefig(plot_path, dpi=120)
    plt.close()
    print(f"\nGraphiques sauvegardés : {plot_path}")


def plot_algorithm_comparison(comparison: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    comparison.plot(x="algorithm", y=["test_RMSE", "test_MAE"], kind="bar", ax=axes[0], rot=45)
    axes[0].set_title("Erreurs par algorithme (test)")
    axes[0].set_ylabel("Erreur")

    comparison.plot(x="algorithm", y=["train_R2", "test_R2"], kind="bar", ax=axes[1], rot=45)
    axes[1].set_title("R² train vs test (overfitting)")
    axes[1].set_ylabel("R²")

    plt.tight_layout()
    path = output_dir / "regression_comparison.png"
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"Comparaison sauvegardée : {path}")


def main() -> None:
    df = load_data()
    X, y = df[FEATURES], df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    print(f"\nTrain : {len(X_train)} | Test : {len(X_test)}")

    # 1. Comparer tous les algorithmes
    comparison, best_model, best_name = compare_algorithms(X_train, y_train, X_test, y_test)
    plot_algorithm_comparison(comparison, Path(__file__).resolve().parent.parent / "outputs")

    # 2. CV sur le meilleur modèle
    cross_validate_model(build_pipeline(best_name), X_train, y_train, model_name=best_name)

    # 3. Tuning du meilleur modèle
    search = tune_hyperparameters(X_train, y_train, model_name=best_name, method="random")
    tuned_model = search.best_estimator_

    # 4. Évaluation détaillée
    evaluate_model(tuned_model, X_test, y_test, label=best_name)
    analyze_overfitting(tuned_model, X_train, y_train, X_test, y_test)
    plot_evaluation(tuned_model, X_test, y_test, Path(__file__).resolve().parent.parent / "outputs", best_name)

    print("\n" + "=" * 60)
    print("ALGORITHMES & TECHNIQUES COUVERTS")
    print("=" * 60)
    print("""
    Algorithmes :
    - Regression lineaire (LinearRegression)
    - Regression polynomiale (PolynomialFeatures deg 2 & 3)
    - XGBoost (XGBRegressor)

    Techniques :
    - Train/Test split | KFold CV | GridSearch / RandomizedSearch
    - RMSE, MAE, R2, MAPE | Residus | Detection overfitting
    - Comparaison visuelle des algorithmes
    """)


if __name__ == "__main__":
    main()
