# Algorithmic Bias - Cabrera Dialectic 2

Generated on 2025-09-03 12:55:55

Distinctions (what it is and isn’t)
- What it is: Consistent, systematic advantages/disadvantages for groups in algorithmic outputs.
- What it isn’t: Random errors, occasional mistakes, or mere differences that do not systematically affect groups.
- Outcomes vs processes: Biased outcomes can arise even if code is “neutral” when data or use context is biased.
- Technical vs societal: Statistical bias (estimation error) differs from social bias (unfair impact). Both can interact.
- Subtypes to watch:
  - Representation bias (who’s in the data, sample imbalance)
  - Measurement/label bias (proxies, flawed labels)
  - Historical/structural bias (data encodes past inequities)
  - Evaluation bias (one-size-fits-all metrics)
  - Deployment/use bias (thresholds, contexts, human-in-the-loop)
  - Feedback bias (system outputs change the world and future data)
- Scope boundaries: Define target task, population, protected attributes, context of use, and harms of interest. Decide what counts as “fair” for this application.

Parts and wholes (how it’s structured)
- Pipeline parts:
  - Problem framing (objective, target, constraints)
  - Data sourcing (coverage, consent, provenance)
  - Labeling (criteria, annotator guidance, inter-rater reliability)
  - Preprocessing/feature engineering (proxy detection, leakage)
  - Modeling (loss functions, regularization, fairness constraints)
  - Evaluation (overall and subgroup metrics; stress tests)
  - Deployment (thresholds, human oversight, UI, explanations)
  - Monitoring (drift, post-deployment audits, incident response)
- Nested systems:
  - Technical system sits inside organizational incentives, legal/compliance requirements, societal norms, and domain-specific processes (e.g., hiring or lending pipelines).
- Control points in each part:
  - Framing: articulate fairness definitions and harms
  - Data: audits, documentation (datasheets, lineage), gap-filling or reweighting
  - Labels: bias reviews, gold standards, blinded annotation
  - Modeling: hyperparameter/fairness sweeps, robust objectives
  - Evaluation: stratified metrics, intersectional analysis, uncertainty
  - Deployment: policy guardrails, appeals, override protocols
  - Monitoring: dashboards per group, alerts, periodic revalidation

Relationships (causes, effects, feedbacks, trade-offs)
- Causal pathways:
  - Underrepresentation → higher error rates → unfair denial/approval patterns
  - Proxy features (e.g., zipcode) → reconstruct protected status → disparate impact
  - Threshold choices → different FPR/FNR across groups → unequal burdens
- Feedback loops:
  - Predictive policing increases patrols → more recorded incidents → model “learns” higher risk → perpetuation/escalation
  - Credit denials reduce credit history building → future denials
- Metric tensions:
  - Can’t generally satisfy calibration and equalized odds simultaneously when base rates differ; choose and justify trade-offs.
- Intervention effects:
  - Reweighting/augmentation → improved subgroup recall but possible precision loss
  - Post-processing thresholds by group → parity gains, potential perceptions of individual unfairness; require governance and transparency
- Accountability linkages:
  - Documentation → auditability → corrective action → trust
  - Oversight and appeal mechanisms → mitigation of harm when errors occur

Perspectives (viewpoints, scales, contexts)
- Stakeholders:
  - Impacted individuals/communities: focus on lived experience, false positives/negatives, recourse
  - Domain experts (e.g., clinicians, loan officers): utility, safety, workflow fit
  - Developers/ML engineers: technical feasibility, debt, monitoring
  - Product/business: outcomes, costs, timelines, incentive structures
  - Regulators/ethicists/auditors: compliance, transparency, due process
- Scales:
  - Short-term model metrics vs long-term societal outcomes and distributional effects
  - Individual fairness (similar individuals treated similarly) vs group fairness (parity across groups)
- Context sensitivity:
  - High-stakes domains (health, criminal justice, credit) require stronger evidence, human-in-the-loop, and formal harm assessments.
- Counterfactual thinking:
  - Would this decision change if sensitive attributes were different, holding relevant factors constant?

Practical checklist
- Define
  - What harms are we trying to prevent? Which fairness criteria are appropriate here and why?
  - Which groups and intersections will we evaluate?
- Diagnose
  - Compute performance and error types per group; include calibration, TPR/FPR, PPV/NPV, and uncertainty.
  - Run stress tests: distribution shifts, worst-case subgroup performance, counterfactual evaluations.
- Data work
  - Audit coverage and label quality; document provenance and known limitations.
  - Address gaps via augmentation, reweighting, or targeted data collection; reduce proxy leakage.
- Model work
  - Compare models with and without fairness-aware training; examine trade-offs explicitly.
  - Tune thresholds (possibly per group) with governance review and justification.
- Transparency
  - Produce datasheets/model cards; document decisions, metrics, trade-offs, and known risks.
  - Provide user-facing explanations suitable for the domain.
- Oversight and accountability
  - Establish human review for edge/high-stakes cases; define appeal and error-correction processes.
  - Monitor in production with alerts on subgroup metrics and drift; schedule regular audits.
  - Record incidents and implement corrective actions; revisit incentives that might pressure unsafe shortcuts.

Guiding questions
- Where could unfairness enter in our pipeline, and what evidence do we have?
- Which trade-offs are we accepting, and who bears their costs?
- How will we know if things get worse after deployment, and what will we do next?
