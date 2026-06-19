"""
Génère le fichier CSV de démonstration pour les scripts ML.
Contexte : scoring de risque crédit (Coface-like).
"""

from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_STATE = 42
N_SAMPLES = 1500
OUTPUT_PATH = Path(__file__).parent / "data" / "credit_risk.csv"


def generate_credit_risk_dataset(n_samples: int = N_SAMPLES, random_state: int = RANDOM_STATE) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    countries = ["FR", "DE", "ES", "IT", "BE"]
    sectors = ["Retail", "Tech", "Energy", "Construction", "Finance"]

    country = rng.choice(countries, size=n_samples)
    sector = rng.choice(sectors, size=n_samples)
    revenue = rng.lognormal(mean=5.2, sigma=0.7, size=n_samples).round(2)
    debt_ratio = rng.beta(2, 5, size=n_samples).round(3)
    days_late = rng.poisson(lam=8, size=n_samples)
    num_employees = rng.integers(5, 500, size=n_samples)
    credit_score = rng.integers(300, 850, size=n_samples)
    years_in_business = rng.integers(1, 40, size=n_samples)

    # Score latent pour créer une cible réaliste et corrélée aux features
    latent = (
        -0.0004 * revenue
        + 4.5 * debt_ratio
        + 0.03 * days_late
        - 0.008 * credit_score
        - 0.02 * years_in_business
        + np.where(sector == "Construction", 0.8, 0)
        + np.where(sector == "Energy", 0.4, 0)
        + np.where(country == "ES", 0.3, 0)
        + rng.normal(0, 0.5, size=n_samples)
    )
    default_prob = 1 / (1 + np.exp(-latent))
    defaulted = (rng.random(n_samples) < default_prob).astype(int)

    # Perte attendue (régression) : corrélée au risque de défaut
    exposure = revenue * rng.uniform(0.1, 0.6, size=n_samples)
    expected_loss = (
        defaulted * exposure * rng.uniform(0.35, 0.95, size=n_samples)
        + (1 - defaulted) * exposure * default_prob * rng.uniform(0.01, 0.15, size=n_samples)
    ).round(2)

    df = pd.DataFrame(
        {
            "company_id": [f"C{i:04d}" for i in range(1, n_samples + 1)],
            "country": country,
            "sector": sector,
            "revenue": revenue,
            "debt_ratio": debt_ratio,
            "days_late": days_late,
            "num_employees": num_employees,
            "credit_score": credit_score,
            "years_in_business": years_in_business,
            "defaulted": defaulted,
            "expected_loss": expected_loss,
        }
    )
    return df


if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset = generate_credit_risk_dataset()
    dataset.to_csv(OUTPUT_PATH, index=False)
    print(f"Dataset généré : {OUTPUT_PATH}")
    print(f"Shape : {dataset.shape}")
    print(f"Taux de défaut : {dataset['defaulted'].mean():.2%}")
