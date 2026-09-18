# Experiment Design — RevenueLift

## Hypothesis
- **H0 (null):** The new checkout flow (treatment) has no effect on conversion rate compared to the current checkout (control).
- **H1 (alternative):** The new checkout flow changes conversion rate compared to the current checkout.

## Metrics

**Primary metric**
- Conversion rate — proportion of sessions that result in a completed order.

**Secondary metric**
- Average order value (AOV) — mean order value among converted sessions.

**Guardrail metrics** (must not regress, even if the primary metric wins)
- Refund rate — proportion of orders refunded within 7 days.
- Page load time (simulated) — should not meaningfully worsen under the new flow.
- Support ticket rate — proportion of sessions generating a support ticket.

## Statistical commitments (locked before any data is generated or seen)
- Significance level: **α = 0.05**
- Desired statistical power: **0.8**
- Minimum detectable effect: a **2 percentage-point lift** in conversion rate (this will drive the sample size calculation in Phase A1)

## Rule
These choices are fixed as of this document. If results come in and any of the above changes, that's p-hacking — the analysis restarts from this document, not from cherry-picked adjustments.