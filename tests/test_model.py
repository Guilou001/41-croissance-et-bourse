import numpy as np
import pandas as pd
import pytest
from scipy.stats import pearsonr

from crb.experiment import balanced
from crb.model import forecasts, geometric, paired_correlations, real_return


def test_real_gain_uses_a_quotient():
    assert real_return(0.10, 0.10) == pytest.approx(0)
    assert real_return(0.20, 0.10) == pytest.approx(1 / 11)


def test_geometric_growth_is_not_arithmetic():
    assert geometric([-0.2, 0.25]) == pytest.approx(0, abs=1e-14)
    assert np.mean([-0.2, 0.25]) == pytest.approx(0.025)


def test_geometric_preserves_country_dimension():
    result = geometric([[0.1, 0], [0.1, 0.21]], axis=0)
    np.testing.assert_allclose(result, [0.1, 0.1])


def test_vectorized_correlations_agree_with_independent_scipy():
    x = np.array([[1, 2, 3], [4, 8, 1]])
    y = np.array([[2, 4, 8], [1, 7, 3]])
    expected = [pearsonr(a, b).statistic for a, b in zip(x, y, strict=True)]
    np.testing.assert_allclose(paired_correlations(x, y), expected)


def sample_panel():
    year = np.arange(1950, 2021)
    return pd.DataFrame(
        {
            "iso": "AAA",
            "year": year,
            "growth": 0.02 + 0.005 * np.sin(year),
            "real_equity": 0.03 + 0.05 * np.cos(year),
        }
    )


def test_no_future_return_in_training():
    d = sample_panel()
    original = forecasts(d)
    changed = d.copy()
    changed.loc[changed.year >= 2000, "real_equity"] = 0.9
    revised = forecasts(changed)
    np.testing.assert_allclose(
        original.loc[original.year <= 2000, "prediction"], revised.loc[revised.year <= 2000, "prediction"]
    )
    assert (original.training_last_year < original.year).all()


def test_gdp_publication_delay():
    d = sample_panel()
    a = forecasts(d)
    changed = d.copy()
    changed.loc[changed.year >= 1999, "growth"] = 0.8
    b = forecasts(changed)
    np.testing.assert_allclose(a.loc[a.year <= 2000, "prediction"], b.loc[b.year <= 2000, "prediction"])
    assert (a.latest_predictor_year == a.year - 2).all()


def test_constant_returns_match_benchmark():
    d = sample_panel()
    d.real_equity = 0.05
    p = forecasts(d)
    np.testing.assert_allclose(p.prediction, 0.05, atol=1e-12)
    np.testing.assert_allclose(p.benchmark, 0.05, atol=1e-12)


def test_country_missing_one_year_is_excluded_from_balanced_panel():
    d = pd.DataFrame(
        {
            "year": [2000, 2001, 2000, 2001],
            "iso": ["A", "A", "B", "B"],
            "growth": [0.01, 0.02, 0.03, 0.04],
            "real_equity": [0.1, 0.1, 0.1, np.nan],
        }
    )
    g, r = balanced(d, 2000, 2001)
    assert g.columns.tolist() == r.columns.tolist() == ["A"]


def test_bankruptcy_not_converted_to_finite_geometric_gain():
    with pytest.raises(ValueError):
        geometric([0.1, -1])
