from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Assumptions, matching docs/experiment_design.md
baseline_conversion_rate = 0.10   # current checkout's conversion rate — pick a realistic e-commerce baseline
minimum_detectable_lift = 0.02    # 2 percentage points, as committed in the design doc
alpha = 0.05
power = 0.8

# Convert the two proportions into Cohen's h (effect size for proportions)
effect_size = proportion_effectsize(
    baseline_conversion_rate,
    baseline_conversion_rate + minimum_detectable_lift
)

analysis = NormalIndPower()
sample_size_per_group = analysis.solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    ratio=1.0,          # equal split between control and treatment
    alternative='two-sided'
)

sample_size_per_group = int(round(sample_size_per_group))

print(f"Baseline conversion rate: {baseline_conversion_rate}")
print(f"Minimum detectable lift: {minimum_detectable_lift}")
print(f"Effect size (Cohen's h): {effect_size:.4f}")
print(f"Required sample size per group: {sample_size_per_group}")
print(f"Total required sample size: {sample_size_per_group * 2}")