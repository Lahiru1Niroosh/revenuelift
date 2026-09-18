# Results Summary — RevenueLift

## Headline Result
- Overall conversion rate: 10.27% (control) → 11.42% (treatment), raw p=0.0151
- **After Benjamini-Hochberg correction: adjusted p=0.0502 — does NOT survive correction**

## Segment Result (the robust finding)
- Mobile: 9.37% → 12.71% conversion, +35.6% relative lift, adjusted p=0.003 — survives correction
- Desktop: trends negative (not significant, adjusted p=0.216)
- New users: raw p=0.034, adjusted p=0.086 — does not survive correction
- Returning users: flat, not significant

## Guardrails
- Refund rate: 4.31% → 5.94%, not statistically significant (p=0.292)
- Support ticket rate: flat, not significant (p=0.946)
- Page load time: 2.51s → 2.58s, **statistically significant regression** (p<0.0001)

## Recommendation
**Ship with Caveats — Mobile Only.** The aggregate effect is not statistically robust once corrected for multiple testing, but the mobile segment effect is — and mobile is the majority of traffic. Recommend a mobile-only rollout, independent re-test on desktop, and monitoring of page load time before any broader rollout.

## Projected Impact
~$857,401 in additional annual revenue (mobile-only scope), based on 50,000 baseline monthly sessions and 55% mobile traffic share.