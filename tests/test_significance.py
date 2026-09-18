import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats


def test_proportions_ztest_known_case():
    """
    Known reference case: 100 vs 100 samples, 20 vs 30 successes.
    Verified against an independent online two-proportion z-test calculator.
    """
    count = np.array([20, 30])
    nobs = np.array([100, 100])
    z_stat, p_value = proportions_ztest(count, nobs)

    assert round(z_stat, 2) == -1.63
    assert p_value < 0.11 and p_value > 0.09


def test_proportions_ztest_identical_groups_not_significant():
    """Identical conversion rates should never be flagged as significant."""
    count = np.array([50, 50])
    nobs = np.array([500, 500])
    z_stat, p_value = proportions_ztest(count, nobs)

    assert p_value > 0.05
    assert round(z_stat, 4) == 0.0


def test_ttest_known_case():
    """
    Known reference case: two small samples with a clear mean difference.
    """
    group_a = [10, 12, 9, 11, 10]
    group_b = [15, 14, 16, 13, 15]

    t_stat, p_value = stats.ttest_ind(group_b, group_a)

    assert t_stat > 0          # group_b is higher
    assert p_value < 0.01      # difference should be clearly significant


def test_ttest_identical_distributions_not_significant():
    group_a = [10, 11, 12, 13, 14]
    group_b = [10, 11, 12, 13, 14]

    t_stat, p_value = stats.ttest_ind(group_b, group_a)

    assert round(t_stat, 4) == 0.0
    assert p_value > 0.99