# GROUP 3: Corporate IT Policy Dispute

**Vocabulary:** cloud applications, data classification, compliance policies, automated storage, data governance

**BACKSTORY:** MegaCorp's legal department discovered that employees are using unauthorized **cloud applications** for document collaboration, creating GDPR compliance risks due to unclear **data classification** and cross-border data transfers. David's IT team identified that sensitive customer information is being stored in unapproved SaaS tools without proper **compliance policies**, while **automated storage** systems are syncing this data across multiple jurisdictions. Lisa's legal team had been advising employees that standard **cloud applications** were acceptable for internal use, not realizing that **data governance** regulations require explicit controls for customer data processing. The problem escalated when a departing employee's cloud accounts contained customer PII distributed across dozens of **cloud applications**, all synchronized through **automated storage** without **data classification** controls. A GDPR audit revealed that **compliance policies** weren't being enforced consistently, and **data governance** frameworks lacked visibility into shadow IT usage. David wants to restrict unauthorized **cloud applications** and implement mandatory **data classification**, while Lisa argues that **compliance policies** education and flexible **data governance** would solve the problem without disrupting workflows.

**DAVID (IT Director):** "We have no visibility into what **cloud applications** employees are using. Customer data is scattered across unauthorized platforms without proper **data classification**."

**LISA (Legal Counsel):** "Employees need productivity tools for collaboration. We can't just block **cloud applications** without providing approved alternatives that support their workflows."

**DAVID:** "But they're processing customer PII in unsecured **cloud applications**. Our **automated storage** policies can't enforce **data classification** on external platforms."

**LISA:** "So train them on **compliance policies** and provide guidance on approved **cloud applications**. Don't just block everything and break productivity."

**DAVID:** "**Compliance policies** training takes months to implement. Meanwhile, customer data is being processed without **data governance** controls, and **automated storage** makes tracking impossible."

**LISA:** "Then implement graduated **data governance** controls instead of blanket restrictions. Help employees choose compliant **cloud applications** rather than forcing underground workarounds."

### Tech Industry Criticism

1. **Unrealistic Shadow IT Discovery**: What corporation with GDPR compliance requirements doesn't have DLP (Data Loss Prevention) tools or CASB (Cloud Access Security Broker) solutions already monitoring cloud app usage? This sounds like it was written by someone who's never worked in enterprise security.

2. **Oversimplified GDPR Compliance**: Real GDPR compliance isn't just about "cross-border data transfers" - it involves data processing lawful basis, data subject rights, breach notification timelines, and privacy impact assessments. This scenario reads like a surface-level understanding from a compliance checklist.

3. **Naive IT Security Discussion**: No IT director would say "we have no visibility" in 2025. Modern enterprises use endpoint detection, network monitoring, and cloud security posture management. The conversation lacks mention of identity providers, SSO, or conditional access policies.

4. **Buzzword Overuse**: "Data classification" appears in every other sentence but they never discuss actual classification schemes (public, internal, confidential, restricted) or DLP policy enforcement mechanisms.

5. **Missing Technical Implementation**: Where's the discussion of API security, OAuth scopes, data residency requirements, or technical controls like encryption at rest/in transit? Real IT-legal conversations include specific technical mitigations.

6. **Unrealistic Legal Perspective**: Legal counsel wouldn't be "advising employees that cloud applications were acceptable" without involving IT security for technical risk assessment. This shows a fundamental misunderstanding of how enterprise legal-IT coordination works.

7. **Vague "Automated Storage" References**: What does this even mean? Cloud sync services? Backup solutions? Data lakes? Real professionals would specify the actual technology stack and integration points.

8. **Missing Business Context**: No discussion of business impact, user productivity metrics, cost of compliance tools, or timeline for remediation. Real enterprise discussions include budget allocation and resource planning.

## Scenario Improvement Analysis

**Criticism 1 (Shadow IT Discovery)**: Valid point about modern enterprise security tools. Suggestion: Reframe as a mid-sized company that's rapidly scaling and hasn't implemented full CASB/DLP solutions yet, or focus on limitations of current monitoring tools in detecting sophisticated shadow IT usage.

**Criticism 2 (GDPR Oversimplification)**: Accurate criticism. Suggestion: Add specific GDPR concerns like "Article 6 lawful basis for processing" or "Article 35 DPIA requirements" to show deeper understanding of regulatory complexity.

**Criticism 3 (IT Security Discussion)**: Excellent point about visibility tools. Suggestion: David should reference specific gaps like "our CASB only covers sanctioned apps" or "we lack visibility into personal device usage outside our MDM."

**Criticism 4 (Data Classification Overuse)**: Valid concern about forced vocabulary usage. Suggestion: Use natural variations like "sensitivity labeling," "information classification schemes," or "data handling requirements" while maintaining vocabulary coverage.

**Criticism 5 (Technical Implementation)**: Good point about missing technical depth. Suggestion: Include discussion of "OAuth scope limitations," "API security gateways," or "data residency controls" to add technical authenticity.

**Criticism 6 (Legal Perspective)**: Accurate criticism about legal-IT coordination. Suggestion: Lisa should acknowledge "we should have consulted IT security for risk assessment" or reference existing legal-IT review processes.

**Criticism 7 (Automated Storage Vagueness)**: Valid technical criticism. Suggestion: Specify actual technologies like "OneDrive sync clients," "Google Drive integration," or "cloud backup services" to add technical precision.

**Criticism 8 (Business Context)**: Important missing element. Suggestion: Add discussion of "quarterly compliance audit costs," "productivity impact metrics," or "Q4 implementation timeline" to provide realistic business framing.

**Path Forward**: The scenario needs more technical specificity and realistic enterprise security context while maintaining vocabulary integration. Consider setting this in a mid-sized company undergoing rapid digital transformation where existing security controls are insufficient for current scale.