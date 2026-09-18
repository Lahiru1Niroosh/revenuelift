import pandas as pd

# Baseline assumptions — documented explicitly, not hidden
BASELINE_MONTHLY_SESSIONS = 50000       # assumption: a mid-size e-commerce site's monthly session volume
BASELINE_CONVERSION_RATE = 0.102738     # from Phase A3 control group
BASELINE_AOV = 77.79                    # from Phase A3 control group
MOBILE_TRAFFIC_SHARE = 0.55             # matches the device split used in data generation

# Key results carried forward from Phases A3-A6
overall_lift_raw_p = 0.015064
overall_lift_adjusted_p = 0.050213
mobile_lift_absolute = 0.0334
mobile_lift_adjusted_p = 0.003
page_load_regressed = True
refund_rate_regressed_significantly = False

# --- Revenue projection: mobile-only rollout (the defensible scope) ---
mobile_sessions_monthly = BASELINE_MONTHLY_SESSIONS * MOBILE_TRAFFIC_SHARE
additional_conversions_monthly = mobile_sessions_monthly * mobile_lift_absolute
additional_revenue_monthly = additional_conversions_monthly * BASELINE_AOV
additional_revenue_annual = additional_revenue_monthly * 12

# --- Decision logic ---
if mobile_lift_adjusted_p < 0.05 and overall_lift_adjusted_p >= 0.05:
    recommendation = "Ship with Caveats — Mobile Only"
    confidence = "High (mobile), Low (desktop/aggregate)"
    rationale = (
        "The aggregate conversion lift does not survive multiple-testing correction "
        "(adjusted p=0.050), so a blanket rollout claim is not statistically defensible. "
        "However, the mobile segment effect is robust after correction (adjusted p=0.003) "
        "and represents the majority of traffic. Recommend rolling out to mobile only, "
        "re-testing desktop independently, and monitoring page load time, which regressed significantly."
    )
elif overall_lift_adjusted_p < 0.05:
    recommendation = "Ship"
    confidence = "High"
    rationale = "Conversion lift is significant even after multiple-testing correction."
else:
    recommendation = "Do Not Ship"
    confidence = "Low"
    rationale = "No conversion effect survives multiple-testing correction."

# --- Assemble final output row ---
result = pd.DataFrame([{
    'recommendation': recommendation,
    'confidence': confidence,
    'rationale': rationale,
    'overall_lift_raw_p': overall_lift_raw_p,
    'overall_lift_adjusted_p': overall_lift_adjusted_p,
    'mobile_lift_absolute': mobile_lift_absolute,
    'mobile_lift_adjusted_p': mobile_lift_adjusted_p,
    'page_load_time_regressed': page_load_regressed,
    'refund_rate_regressed_significantly': refund_rate_regressed_significantly,
    'baseline_monthly_sessions': BASELINE_MONTHLY_SESSIONS,
    'mobile_traffic_share': MOBILE_TRAFFIC_SHARE,
    'projected_additional_revenue_monthly': round(additional_revenue_monthly, 2),
    'projected_additional_revenue_annual': round(additional_revenue_annual, 2),
}])

print(result.to_string(index=False))
result.to_csv('data/experiment_results.csv', index=False)
print("\nSaved to data/experiment_results.csv")