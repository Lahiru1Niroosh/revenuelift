# Statistical Methodology — RevenueLift

## Significance Testing
- Conversion rate: two-proportion z-test
- AOV: independent two-sample t-test
- Guardrails (refund rate, support ticket rate): two-proportion z-test
- Guardrail (page load time): independent two-sample t-test
- Segment analysis: two-proportion z-test, run separately within each device_type and user_type level

## Multiple Testing Correction
Across Phases A3–A5, 10 significance tests were run (1 primary metric, 1 secondary metric, 3 guardrails, 5 segment cuts). Running this many tests at a raw α=0.05 inflates the false-positive rate well above 5%, so a **Benjamini-Hochberg (FDR) correction** was applied across all 10 p-values.

BH was chosen over Bonferroni because Bonferroni's conservatism sharply increases the false-negative rate at this test count, while BH controls the expected proportion of false discoveries at a more reasonable power cost — the standard choice in industry A/B testing programs.

**Key finding:** the primary conversion-rate result (raw p=0.0151) does **not** survive correction (adjusted p=0.0502) — a result that would have been reported as significant is now a caveat, not a conclusion, once corrected for the number of tests run. The mobile segment result (raw p=0.0006, adjusted p=0.003) survives correction and is the most statistically robust finding in the analysis. The `user_type=new` segment result also fails to survive correction (adjusted p=0.086).