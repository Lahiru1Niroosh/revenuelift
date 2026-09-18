import pandas as pd
from statsmodels.stats.multitest import multipletests

# Collect every p-value produced across Phases A3-A5
tests = [
    {'phase': 'A3', 'test': 'Primary: Conversion Rate',        'p_value': 0.015064},
    {'phase': 'A3', 'test': 'Secondary: AOV',                  'p_value': 0.275275},
    {'phase': 'A4', 'test': 'Guardrail: Refund Rate',          'p_value': 0.291538},
    {'phase': 'A4', 'test': 'Guardrail: Support Ticket Rate',  'p_value': 0.945817},
    {'phase': 'A4', 'test': 'Guardrail: Page Load Time',       'p_value': 0.000000},
    {'phase': 'A5', 'test': 'Segment: device_type=mobile',     'p_value': 0.0006},
    {'phase': 'A5', 'test': 'Segment: device_type=tablet',     'p_value': 0.9370},
    {'phase': 'A5', 'test': 'Segment: device_type=desktop',    'p_value': 0.1082},
    {'phase': 'A5', 'test': 'Segment: user_type=new',          'p_value': 0.0344},
    {'phase': 'A5', 'test': 'Segment: user_type=returning',    'p_value': 0.9582},
]

df = pd.DataFrame(tests)

# Benjamini-Hochberg correction (less conservative than Bonferroni, standard for exploratory analysis)
reject, p_adjusted, _, _ = multipletests(df['p_value'], alpha=0.05, method='fdr_bh')

df['p_adjusted'] = p_adjusted
df['significant_raw'] = df['p_value'] < 0.05
df['significant_after_correction'] = reject

pd.set_option('display.float_format', lambda x: f'{x:.6f}')
print(df.to_string(index=False))

flipped = df[df['significant_raw'] & ~df['significant_after_correction']]
print(f"\nTests significant at raw α=0.05 but NOT after correction: {len(flipped)}")
if len(flipped) > 0:
    print(flipped[['test', 'p_value', 'p_adjusted']].to_string(index=False))

df.to_csv('data/multiple_testing_results.csv', index=False)