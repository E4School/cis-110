# Algorithmic Bias - Categories 1

Generated on 2025-09-03 13:18:40

Here’s a DSRP (Distinctions, Systems, Relationships, Perspectives) categorization of “Algorithmic Bias,” with emphasis on whether it is a category, a member of a category, or both.

Categorization
- Status: Both
  - As a member: It is a member of broader categories like Bias, AI/ML Risks, and Ethical Issues in AI.
  - As a category: It is a category that contains multiple subtypes/sources (e.g., data bias, evaluation bias) and domain-specific instances (e.g., hiring bias).

Parent categories (what Algorithmic Bias is a member of)
- Bias (general)
- Statistical bias (systematic error)
- Algorithmic/AI risk
- Ethical issues in AI (AI ethics)
- Sociotechnical harms
- Discrimination (legal/policy framing when bias leads to protected-class harms; overlapping parent)

Sibling categories (share the same parent, depending on the parent chosen)
- Under Bias (general):
  - Cognitive bias (e.g., confirmation bias)
  - Measurement bias
  - Sampling/selection bias
  - Observer/experimenter bias
  - Publication bias
- Under AI/ML risk:
  - Privacy risks (e.g., reidentification)
  - Security/robustness risks (e.g., adversarial examples)
  - Safety risks (e.g., catastrophic failures)
  - Explainability/opacity (lack of interpretability)
  - Misinformation/propagation harms
- Under Ethical issues in AI:
  - Surveillance and autonomy harms
  - Manipulation/nudging
  - Accountability gaps

Subcategories of Algorithmic Bias (what it categorizes)
- By source/stage in the ML pipeline (Suresh & Guttag-style taxonomy plus deployment):
  - Data bias
    - Sampling/coverage bias
    - Historical bias (structural inequities embedded in data)
    - Measurement/labeling bias
    - Class imbalance
  - Model/Objective bias
    - Inductive bias/design choices (architecture, features)
    - Objective/metric choice (loss functions that trade off group outcomes)
    - Regularization/thresholding choices
  - Evaluation bias
    - Metrics that hide subgroup disparities (e.g., overall accuracy masking group error rates)
    - Poor benchmarking datasets lacking subgroup coverage
  - Deployment/Use bias
    - Population shift (train–serve mismatch)
    - Proxy/threshold decisions that disadvantage groups
    - Human-in-the-loop operational practices that amplify bias
  - Interaction/Feedback bias
    - Reinforcement loops from user feedback or recommender exposure
- By harm type
  - Allocative harms (resource access: loans, jobs)
  - Representational harms (stereotyping, misrecognition)
- By domain (instances within the category)
  - Hiring tools, loan approvals, facial recognition, predictive policing, healthcare triage, education/edtech scoring

DSRP framing
- Distinctions
  - Is: systematic, group-differential unfairness arising in algorithmic systems.
  - Is not: random error/noise; mere model inaccuracy; fairness as a property.
- Systems
  - Whole: a sociotechnical system (data, model, deployment, policy, people).
  - Parts: data generation, labeling, modeling, evaluation, deployment, feedback loops, governance.
- Relationships
  - Causes: biased/incomplete data; design and training choices; evaluation and operational policies.
  - Effects: disparate error rates, unfair allocations, eroded trust; feedback loops reinforcing inequity.
- Perspectives
  - Statistical: systematic error across groups.
  - Ethical: unfair treatment and harm.
  - Legal/policy: discrimination and compliance risk.
  - Stakeholder: developers, users, impacted communities, auditors, regulators see different problem boundaries and remedies.

Bottom line
- Algorithmic Bias is both a member (of Bias, AI Risk, Ethical Issues) and a category (containing multiple subtypes and domain-specific instances). The useful categorization depends on the level of analysis: conceptual (sources/harm types) versus applied (domain instances).


---

## 2025-09-03 13:21:15

Genus–differentia definition
- Genus: A form of systemic bias in decision-making systems.
- Differentia: Occurs specifically in automated or computational (algorithmic) systems when their outputs produce systematic, unfair advantages or disadvantages across groups (often defined by protected attributes), due to properties of the data, model design/optimization, evaluation, or deployment context; the effect is measurable as consistent performance or outcome disparities rather than random error.

Ontological status
- Both. It is:
  - A member of the broader category “bias,” and
  - A category that contains more specific types of algorithmic bias.

Parent categories (supercategories)
- Bias (general)
- Systemic bias / structural bias
- Statistical and measurement bias (inference/estimation context)
- AI/ML risks and harms
- Discrimination mechanisms (socio-technical)

Sibling categories (under the respective parents)
- Under Bias: human cognitive bias, sampling bias, measurement bias, media bias
- Under Statistical/measurement bias: selection bias, label bias, confounding bias, omitted-variable bias
- Under AI/ML risks: privacy risks, security/robustness failures (adversarial examples), lack of interpretability, model drift
- Under Discrimination mechanisms: institutional discrimination, human decision-maker bias, policy bias

Subcategories of algorithmic bias
- By pipeline origin:
  - Data bias: sampling bias, historical bias, measurement bias, label bias, survivorship/selective-labels bias
  - Feature/target bias: proxy-variable bias, construct validity/target definition bias
  - Model/optimization bias: objective-function bias (e.g., optimizing overall accuracy at the expense of subgroup errors), regularization/inductive choices that skew group performance
  - Evaluation bias: metric choice bias, benchmark/dataset shift, unrepresentative test sets
  - Deployment/context bias: feedback-loop/performative effects, automation bias in end-users, domain shift, missing or misused uncertainty
- By effect type:
  - Disparate treatment vs disparate impact
  - Allocative harm vs quality-of-service harm vs representational harm
  - Group fairness violations (e.g., error-rate parity, demographic parity, equalized odds) vs individual fairness violations
  - Intersectional bias (compounded disparities across multiple attributes)
  - Calibration disparity, FPR/FNR disparity, ranking/exposure bias
- By domain/application:
  - Hiring and admissions screening bias
  - Credit/loan underwriting bias
  - Facial recognition demographic bias
  - Predictive policing/recidivism risk bias
  - Healthcare triage/risk scoring bias
  - Ad delivery and content moderation bias
- By mechanism:
  - Feedback amplification and retraining bias
  - Confounding/omitted-variable bias
  - Proxy discrimination
  - Label leakage and target shift

Clarifications and near relations
- Related but distinct: inductive bias (a learning-theory concept) is not inherently unfair; algorithmic discrimination is a legal/policy framing of certain effects of algorithmic bias.
- Typical instances/exemplars: disparate error rates in commercial facial recognition by gender/skin tone; COMPAS risk scores with differing FPR/FNR across races; ad delivery skew for employment/credit housing ads.

Practical criteria/diagnostics (necessary-and-typical features)
- Locus: automated system (model, rules, or pipeline)
- Systematic disparity: consistent performance or outcome differences across groups
- Causal pathways: data, modeling choices, evaluation, or deployment context
- Observability: measurable through subgroup analysis; may persist or amplify over time
- Normative judgment: deemed unfair relative to legal, ethical, or policy standards

Mitigation levers (category-typical remedies)
- Dataset improvement and documentation, subgroup performance auditing, transparent objectives/metrics, fairness-aware learning or post-processing, human oversight and accountability, and monitoring in deployment.
