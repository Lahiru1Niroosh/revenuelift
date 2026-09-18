import duckdb
import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

con = duckdb.connect('data/revenuelift.duckdb')

def run_segment_test(df, segment_col, segment_value):
    subset = df[df[segment_col] == segment_value]
    control = subset[subset['variant'] == 'control']
    treatment = subset[subset['variant'] == 'treatment']

    control_n = len(control)
    treatment_n = len(treatment)
    control_conv = control['converted'].sum()
    treatment_conv = treatment['converted'].sum()

    control_cr = control_conv / control_n
    treatment_cr = treatment_conv / treatment_n
    lift = treatment_cr - control_cr

    count = np.array([treatment_conv, control_conv])
    nobs = np.array([treatment_n, control_n])
    z_stat, p_value = proportions_ztest(count, nobs)

    return {
        'segment': f"{segment_col}={segment_value}",
        'control_n': control_n,
        'treatment_n': treatment_n,
        'control_cr': control_cr,
        'treatment_cr': treatment_cr,
        'absolute_lift': lift,
        'relative_lift_pct': (lift / control_cr) * 100 if control_cr > 0 else np.nan,
        'p_value': p_value,
        'significant': p_value < 0.05
    }

sessions = con.execute("SELECT * FROM sessions").fetchdf()

results = []
for device in sessions['device_type'].unique():
    results.append(run_segment_test(sessions, 'device_type', device))
for user_type in sessions['user_type'].unique():
    results.append(run_segment_test(sessions, 'user_type', user_type))

results_df = pd.DataFrame(results)
pd.set_option('display.float_format', lambda x: f'{x:.4f}')
print(results_df.to_string(index=False))

# Overall result for comparison (Simpson's Paradox check)
overall_control_cr = sessions[sessions['variant']=='control']['converted'].mean()
overall_treatment_cr = sessions[sessions['variant']=='treatment']['converted'].mean()
overall_direction = 'positive' if overall_treatment_cr > overall_control_cr else 'negative'

print(f"\nOverall effect direction: {overall_direction} ({overall_control_cr:.4%} -> {overall_treatment_cr:.4%})")

reversed_segments = results_df[
    ((results_df['absolute_lift'] > 0) != (overall_direction == 'positive'))
]
if len(reversed_segments) > 0:
    print("\n⚠ SIMPSON'S PARADOX WATCH — segment(s) where direction reverses vs. overall:")
    print(reversed_segments[['segment', 'absolute_lift', 'p_value', 'significant']].to_string(index=False))
else:
    print("\nNo segment reverses the overall direction.")

results_df.to_csv('data/segment_results.csv', index=False)
con.close()