# Algorithmic Bias - Dsrp Questions

# Is it a System?
- Yes, Algorithmic Bias can be thought of as a system. It emerges from interacting components—data, models, objectives, training procedures, deployment contexts, governance processes, and human actors—whose interactions produce patterned, measurable disparities across groups. The phenomenon has feedback loops (e.g., biased outputs influence future data), boundary conditions (institutional, legal, domain-specific), and multi-scale structure (from feature engineering choices to societal impacts).
- Classification:
  - A system (when considered as the socio-technical phenomenon producing inequitable outcomes).
  - A part of a system (as one component of broader socio-technical systems like hiring, credit, health, or justice).
  - A relationship between systems (as the patterned inequity arising from interactions among datasets, models, institutions, and populations).
  - A boundary between systems (surfacing at the interface where algorithmic decisions meet social identity categories and legal norms).
  - A cognitive tool (less so; the concept of “algorithmic bias” is also a lens for diagnosing dysfunctions in complex systems).

# Distinctions
- What it is (inside the boundary):
  - Systematic, group-differentiated error or unfairness in algorithmic decision-making (e.g., higher false positive rates for one demographic group).
  - A socio-technical phenomenon caused by data-generation processes, modeling choices, deployment contexts, and institutional incentives.
  - Manifested in real applications (hiring filters, loan underwriting, facial recognition, predictive policing, healthcare triage).
  - Addressable via practices such as dataset documentation, performance stratified by groups, fairness-aware modeling, transparency, human oversight, and accountability mechanisms.

- What it is not (outside the boundary):
  - Random noise or idiosyncratic single-instance errors without patterned group disparity.
  - Purely technical model underperformance unrelated to social categories or protected classes.
  - The totality of societal inequity (it is a contributor and amplifier, not the whole cause).
  - Bias only “in the data” or only “in the model”: algorithmic bias is not reducible to a single locus.
  - A solved problem through accuracy alone; high average accuracy can coexist with high disparity.

# Systems
- Parts of Algorithmic Bias (viewed as a system):
  - Data subsystem: sampling frames, labeling practices, measurement error, historical prejudices embedded in outcomes.
  - Modeling subsystem: objectives (loss functions), architectures, regularization, feature selection, hyperparameters.
  - Evaluation subsystem: metrics (accuracy, calibration, equalized odds, demographic parity), validation splits, subgroup analyses.
  - Deployment context: user interfaces, thresholding, human-in-the-loop design, organizational policies, incentive structures.
  - Governance/ethics/legal: documentation (datasheets/model cards), audits, reporting, compliance, recourse mechanisms.
  - Feedback dynamics: how decisions alter future data (e.g., policing intensity affecting crime reports).
  - Stakeholders: applicants, decision-subjects, operators, auditors, regulators, impacted communities.

- Algorithmic Bias as a part:
  - Within AI/ML risk management systems (one risk category alongside privacy, robustness, security).
  - Within organizational decision systems (a failure mode within hiring/credit/healthcare decision pipelines).
  - Within societal inequity systems (a technological amplifier or attenuator within broader structures of discrimination).

# Relationships
- Related systems:
  - Data ecosystems (collection, curation, annotation markets).
  - Legal-regulatory systems (anti-discrimination law, AI governance frameworks, standards bodies).
  - Economic systems (labor markets, credit markets) that both shape and are shaped by algorithmic decisions.
  - Technical assurance systems (auditing, certification, monitoring, incident reporting).
  - Sociocultural systems (norms around fairness, identity, and legitimacy).

- Algorithmic Bias as a relationship:
  - Between datasets and populations: mismatch between training data distributions and real-world group distributions.
  - Between model objectives and social values: optimization for aggregate loss versus equitable outcomes.
  - Between institutions and individuals: power asymmetries mediated by algorithmic decision tools.
  - Between historical data and future allocation: path dependence where past inequities inform future predictions.

# Perspectives
- Questions from the perspective of Algorithmic Bias as a system:
  - Where do disparities originate within the pipeline, and how do they propagate across stages?
  - Which feedback loops amplify or dampen disparities over time?
  - What metrics (and trade-offs) best capture fairness given the domain’s constraints?
  - How do changes at one layer (e.g., loss function) affect outcomes at others (e.g., long-term population impacts)?
  - What governance and accountability mechanisms effectively realign incentives and reduce harm?

- Perspectives from other systems:
  - Regulator’s perspective: Are outcomes compliant with anti-discrimination law? Is there documentation, auditability, and evidence of subgroup performance?
  - Data steward’s perspective: How were labels produced? What are coverage gaps, measurement errors, and consent constraints?
  - Model developer’s perspective: What fairness definitions are appropriate? How to adjust objectives, constraints, or post-processing to meet them?
  - Impacted individual’s perspective: Is the decision explainable? Is there recourse and remedy? Are appeals timely and accessible?
  - Organizational executive’s perspective: What are the risk, reputation, and compliance implications? How to align incentives with responsible outcomes?
  - Community advocate’s perspective: Do systems uphold dignity and equity? Were communities consulted in design and evaluation?
  - Ethicist/philosopher’s perspective: Which moral theories of fairness are implicit in metric choices? What harms are distributive vs. recognitional?
  - Systems engineer’s perspective: How to instrument monitoring for drift and subgroup performance in production? What incident response processes exist?

- Not applicable:
  - None. All DSRP aspects can be meaningfully applied to Algorithmic Bias.
