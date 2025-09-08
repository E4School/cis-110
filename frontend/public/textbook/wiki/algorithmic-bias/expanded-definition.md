# Algorithmic Bias - Expanded Definition

Algorithmic bias, n. (also algorithm bias; occasionally attrib. and as adj. in algorithmically biased)

Pronunciation: /ˌælɡəˈrɪðmɪk ˈbaɪəs/

Inflections: plural algorithmic biases

Etymology: Formed from algorithmic adj. ‘relating to an algorithm’ + bias n. In this sense, bias follows established statistical and psychological uses (‘systematic deviation’), now applied to computational systems.

Core definition:
1. The systematic and unfair skewing of outcomes produced by a computational system (e.g., a model, algorithm, or pipeline) such that certain individuals or groups are consistently advantaged or disadvantaged. Arises from properties of data, design and training choices, deployment context, or feedback effects.

Extended senses:
2. Statistical/ML sense. A measurable disparity in model performance, error rates, or allocations across protected or meaningful subpopulations (e.g., differences in false positive/negative rates, calibration, or allocation parity).

3. Governance and ethics sense. A risk category in automated decision-making that requires mitigation through process controls (dataset documentation, transparency, auditing, human oversight, accountability) to meet legal, ethical, or organizational standards of nondiscrimination and fairness.

4. Attributive and participial uses. algorithmic-bias audit; algorithmically biased system; algorithmic-bias mitigation.

Historical development:
- Prefiguring concepts: Discussions of “bias in algorithms” and “bias in expert systems” appear in the 1980s–1990s, paralleling concerns in statistics about sampling and measurement bias.
- Early usage: The collocation algorithmic bias gains currency in the late 2000s to early 2010s with the rise of large-scale machine learning in hiring, credit scoring, advertising, and criminal justice.
- Public attention: Mid-2010s reporting and academic work (e.g., on predictive policing tools, online ad delivery skew, face recognition error disparities, and risk assessment systems) popularize the term and spur policy responses.
- Institutionalization: Late 2010s–2020s see formal guidance in industry standards, data protection and AI regulation, model risk management, and internal audit functions, with “bias” often operationalized via fairness metrics and impact assessments.

Stakeholder and contextual uses:
- Data science/ML engineering: Refers to measurable performance disparities; addressed through dataset curation, reweighting, debiasing, algorithm selection, thresholding, post-processing, and continuous monitoring.
- Product and UX: Focus on harms to users and cohorts; includes inclusive design, representative testing, and clear user messaging about limitations.
- Compliance, risk, and audit: Categorized as model risk or discrimination risk; managed via documentation (datasheets, model cards), testing across subgroups, transparency, human-in-the-loop controls, and incident response.
- Legal and policy: Intersects with equal opportunity, anti-discrimination, consumer protection, data protection, sectoral rules (e.g., credit, employment, housing), and emerging AI regulations; emphasizes explainability, impact assessments, and redress.
- Research and ethics: Examines sources (historical and measurement biases, label subjectivity, deployment shift, feedback loops), normative choices (which fairness criteria), and trade-offs (accuracy, privacy, utility).
- Affected communities and advocacy: Centers lived experience, disparate impacts, due process, and accountability; calls for participatory design, transparency, and stronger oversight.

Sources and mechanisms:
- Data: Unrepresentative samples, historical discrimination encoded in labels, measurement error, missingness, proxy variables.
- Modeling: Objective functions that ignore fairness constraints; regularization and class imbalance handling; thresholding choices.
- Deployment and feedback: Context mismatch, selection effects, automation bias by users, and feedback loops that entrench disparities.
- Use and interpretation: Overreliance on scores without context; lack of appeals; opaque explanations.

Mitigation and evaluation practices:
- Check performance across groups; define relevant subpopulations.
- Use multiple fairness metrics (e.g., calibration, equalized odds, demographic parity) and be explicit about trade-offs.
- Improve and document datasets; assess consent, provenance, sampling frames, and labeling.
- Increase transparency via model cards, datasheets, and user-facing explanations.
- Add human oversight, appeals processes, governance, and accountability.
- Monitor post-deployment drift and impacts; perform periodic audits.

Example sentences:
Sense 1 (general)
- The city paused deployment after an external review found algorithmic bias against applicants from certain neighborhoods.
- Advocacy groups argued that algorithmic bias in the screening tool mirrored past discrimination.

Sense 2 (statistical/ML)
- We detected algorithmic bias as a 12% gap in false positive rates between groups, even though overall accuracy was similar.
- Threshold adjustments reduced one metric of algorithmic bias but worsened calibration, highlighting a fairness trade-off.

Sense 3 (governance/ethics)
- The policy mandates annual assessments for algorithmic bias and requires a documented mitigation plan.
- Regulators now treat unmanaged algorithmic bias as a form of compliance failure.

Attributive/participial
- The team conducted an algorithmic-bias audit before launch.
- Complaints described the system as algorithmically biased in its loan approvals.

Usage notes:
- The term may conflate normative judgment (“unfair”) with statistical deviation; technical work often specifies the metric and population.
- Bias can originate in data, model, or context; mitigation is most effective when it treats the full lifecycle.
- “Fairness” criteria are not interchangeable; stakeholders should agree on definitions aligned with legal and social goals.
- Transparency and human oversight are complements, not substitutes, for quantitative evaluation.
