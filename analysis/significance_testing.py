import duckdb
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats

con = duckdb.connect('data/revenuelift.duckdb')

# --- Conversion rate: two-proportion z-test ---
sessions = con.execute("""
    SELECT variant, COUNT(*) as total, SUM(CASE WHEN converted THEN 1 ELSE 0 END) as conversions
    FROM sessions
    GROUP BY variant
""").fetchdf()

control_row = sessions[sessions['variant'] == 'control'].iloc[0]
treatment_row = sessions[sessions['variant'] == 'treatment'].iloc[0]

count = np.array([treatment_row['conversions'], control_row['conversions']])
nobs = np.array([treatment_row['total'], control_row['total']])

z_stat, p_value = proportions_ztest(count, nobs)

control_cr = control_row['conversions'] / control_row['total']
treatment_cr = treatment_row['conversions'] / treatment_row['total']
absolute_lift = treatment_cr - control_cr
relative_lift = (absolute_lift / control_cr) * 100

# 95% confidence interval for the difference in proportions
se = np.sqrt(control_cr*(1-control_cr)/control_row['total'] + treatment_cr*(1-treatment_cr)/treatment_row['total'])
ci_low = absolute_lift - 1.96 * se
ci_high = absolute_lift + 1.96 * se

print("=== Conversion Rate: Two-Proportion Z-Test ===")
print(f"Control conversion rate:   {control_cr:.4%}")
print(f"Treatment conversion rate: {treatment_cr:.4%}")
print(f"Absolute lift: {absolute_lift:.4%}")
print(f"Relative lift: {relative_lift:.2f}%")
print(f"95% CI for absolute lift: [{ci_low:.4%}, {ci_high:.4%}]")
print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value: {p_value:.6f}")
print(f"Significant at α=0.05: {'YES' if p_value < 0.05 else 'NO'}")

# --- AOV: independent t-test ---
orders = con.execute("""
    SELECT o.order_value, s.variant
    FROM orders o
    JOIN sessions s ON o.session_id = s.session_id
""").fetchdf()

control_aov = orders[orders['variant'] == 'control']['order_value']
treatment_aov = orders[orders['variant'] == 'treatment']['order_value']

t_stat, aov_p_value = stats.ttest_ind(treatment_aov, control_aov)

print("\n=== Average Order Value: Independent T-Test ===")
print(f"Control AOV:   ${control_aov.mean():.2f}")
print(f"Treatment AOV: ${treatment_aov.mean():.2f}")
print(f"Difference: ${treatment_aov.mean() - control_aov.mean():.2f}")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {aov_p_value:.6f}")
print(f"Significant at α=0.05: {'YES' if aov_p_value < 0.05 else 'NO'}")

con.close()