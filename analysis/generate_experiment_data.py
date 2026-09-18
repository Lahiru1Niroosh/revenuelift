import duckdb
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)  # reproducibility — same "random" data every run

SAMPLE_SIZE_PER_GROUP = 3835
DEVICE_SPLIT = {'mobile': 0.55, 'desktop': 0.35, 'tablet': 0.10}
USER_TYPE_SPLIT = {'new': 0.6, 'returning': 0.4}

# Conversion rates by variant AND device — this is where the segment story lives
CONVERSION_RATES = {
    ('control',   'mobile'):  0.095,
    ('control',   'desktop'): 0.105,
    ('control',   'tablet'):  0.090,
    ('treatment', 'mobile'):  0.125,  # strong lift on mobile
    ('treatment', 'desktop'): 0.108,  # negligible lift on desktop
    ('treatment', 'tablet'):  0.100,
}

REFUND_RATE = {'control': 0.04, 'treatment': 0.055}  # treatment regresses here

def generate_sessions(variant, n):
    devices = np.random.choice(list(DEVICE_SPLIT), size=n, p=list(DEVICE_SPLIT.values()))
    user_types = np.random.choice(list(USER_TYPE_SPLIT), size=n, p=list(USER_TYPE_SPLIT.values()))
    start = datetime(2026, 1, 1)
    session_starts = [start + timedelta(minutes=int(m)) for m in np.random.uniform(0, 60*24*30, n)]

    converted = np.array([
        np.random.random() < CONVERSION_RATES[(variant, d)] for d in devices
    ])

    return pd.DataFrame({
        'user_id': np.random.randint(100000, 999999, n),
        'variant': variant,
        'device_type': devices,
        'user_type': user_types,
        'session_start': session_starts,
        'converted': converted
    })

control = generate_sessions('control', SAMPLE_SIZE_PER_GROUP)
treatment = generate_sessions('treatment', SAMPLE_SIZE_PER_GROUP)
sessions = pd.concat([control, treatment], ignore_index=True)
sessions.insert(0, 'session_id', range(1, len(sessions) + 1))

# Orders — one per converted session
converted_sessions = sessions[sessions['converted']].copy()
n_orders = len(converted_sessions)

order_values = np.round(np.random.gamma(shape=4, scale=15, size=n_orders) + 20, 2)  # realistic-ish AOV spread

refunded = np.array([
    np.random.random() < REFUND_RATE[v] for v in converted_sessions['variant']
])

orders = pd.DataFrame({
    'order_id': range(1, n_orders + 1),
    'session_id': converted_sessions['session_id'].values,
    'order_value': order_values,
    'refunded': refunded,
    'created_at': converted_sessions['session_start'].values
})

# Write to DuckDB
con = duckdb.connect('data/revenuelift.duckdb')
con.execute("CREATE OR REPLACE TABLE sessions AS SELECT * FROM sessions")
con.execute("CREATE OR REPLACE TABLE orders AS SELECT * FROM orders")
con.close()

print(f"Sessions generated: {len(sessions)}")
print(f"Orders generated: {len(orders)}")
print("\nConversion rate by variant:")
print(sessions.groupby('variant')['converted'].mean())
print("\nConversion rate by variant and device:")
print(sessions.groupby(['variant', 'device_type'])['converted'].mean())
print("\nRefund rate by variant:")
print(orders.merge(sessions[['session_id', 'variant']], on='session_id').groupby('variant')['refunded'].mean())