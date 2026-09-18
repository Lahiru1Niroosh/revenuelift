import duckdb
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats

con = duckdb.connect('data/revenuelift.duckdb')

results = []

def proportion_guardrail(name, control_events, control_n, treatment_events, treatment_n):
    count = np.array([treatment_events, control_events])
    nobs = np.array([treatment_n, control_n])
    z_stat, p_value = proportions_ztest(count, nobs)

    control_rate = control_events / control_n
    treatment_rate = treatment_events / treatment_n
    change = treatment_rate - control_rate

    se = np.sqrt(control_rate*(1-control_rate)/control_n + treatment_rate*(1-treatment_rate)/treatment_n)
    ci_low = change - 1.96 * se
    ci_high = change + 1.96 * se

    regressed = (p_value < 0.05) and (change > 0)  # worse direction = rate went UP

    print(f"=== Guardrail: {name} ===")
    print(f"Control rate:   {control_rate:.4%}")
    print(f"Treatment rate: {treatment_rate:.4%}")
    print(f"Change: {change:.4%}  |  95% CI: [{ci_low:.4%}, {ci_high:.4%}]")
    print(f"P-value: {p_value:.6f}")
    print(f"Regressed significantly: {'YES — FLAG FOR REVIEW' if regressed else 'NO'}\n")

    results.append({'metric': name, 'p_value': p_value, 'regressed': regressed})

# --- Guardrail 1: Refund rate ---
refunds = con.execute("""
    SELECT s.variant, COUNT(*) as total_orders, SUM(CASE WHEN o.refunded THEN 1 ELSE 0 END) as refunds
    FROM orders o
    JOIN sessions s ON o.session_id = s.session_id
    GROUP BY s.variant
""").fetchdf()
c = refunds[refunds['variant'] == 'control'].iloc[0]
t = refunds[refunds['variant'] == 'treatment'].iloc[0]
proportion_guardrail("Refund Rate", c['refunds'], c['total_orders'], t['refunds'], t['total_orders'])

# --- Guardrail 2: Support ticket rate ---
tickets = con.execute("""
    SELECT variant, COUNT(*) as total, SUM(CASE WHEN support_ticket THEN 1 ELSE 0 END) as tickets
    FROM sessions
    GROUP BY variant
""").fetchdf()
c = tickets[tickets['variant'] == 'control'].iloc[0]
t = tickets[tickets['variant'] == 'treatment'].iloc[0]
proportion_guardrail("Support Ticket Rate", c['tickets'], c['total'], t['tickets'], t['total'])

# --- Guardrail 3: Page load time (continuous — t-test, not a proportion) ---
load_times = con.execute("SELECT variant, page_load_time_seconds FROM sessions").fetchdf()
control_load = load_times[load_times['variant'] == 'control']['page_load_time_seconds']
treatment_load = load_times[load_times['variant'] == 'treatment']['page_load_time_seconds']

t_stat, load_p_value = stats.ttest_ind(treatment_load, control_load)
load_regressed = (load_p_value < 0.05) and (treatment_load.mean() > control_load.mean())

print("=== Guardrail: Page Load Time ===")
print(f"Control mean:   {control_load.mean():.3f}s")
print(f"Treatment mean: {treatment_load.mean():.3f}s")
print(f"Difference: {treatment_load.mean() - control_load.mean():.3f}s")
print(f"P-value: {load_p_value:.6f}")
print(f"Regressed significantly: {'YES — FLAG FOR REVIEW' if load_regressed else 'NO'}\n")

results.append({'metric': 'Page Load Time', 'p_value': load_p_value, 'regressed': load_regressed})

# --- Summary ---
print("=== Guardrail Summary ===")
for r in results:
    print(f"{r['metric']}: {'REGRESSED' if r['regressed'] else 'OK'} (p={r['p_value']:.4f})")

con.close()