# GROUP 6: Development Security Crisis

**BACKSTORY:** StreamTech's video platform processes millions of transactions daily through Kumar's custom **function** architecture, with Elena's **pivot tables** providing real-time analytics for business decisions. Last week, their security team discovered a **trojan** embedded in a widely-used open-source library that Kumar's **streaming** **function** depends on, creating immediate **data breach** risks that could compromise the **pivot tables** feeding executive dashboards. The **trojan** was specifically designed to target **streaming** platforms, and removing it would break Kumar's core **function** that handles payment processing and user analytics. Elena's **pivot tables** drive critical business decisions about **streaming** content licensing and revenue projections, but the **data breach** risk means they might have to shut down the **function** entirely. The crisis escalated when Elena discovered that the **trojan** had already compromised data integrity in several **pivot tables**, potentially affecting millions in revenue calculations. Kumar needs weeks to rebuild the **function** without the infected dependency, but Elena's **streaming** analytics **pivot tables** are essential for a board presentation happening tomorrow. The CEO demands a solution that maintains both **streaming** service reliability and **data breach** prevention.

**KUMAR (Backend Developer):** "I wrote a **function** for the **streaming** service, but security found a **trojan** in one of our dependencies. They're worried about a **data breach** affecting our **pivot tables**."

**ELENA (Business Analyst):** "Can you rewrite that **function** without the infected library? I need those **pivot tables** working for tomorrow's **streaming** analytics presentation."

**KUMAR:** "The **streaming** infrastructure depends on that **function**. Removing the **trojan**-infected code breaks our **data breach** prevention and all the **pivot tables**."

**ELENA:** "So we ship **streaming** services with a known **trojan**? That's worse than broken **pivot tables** - it's a guaranteed **data breach**."

**KUMAR:** "I'm saying this **function** needs proper auditing. Rushing **streaming** features while ignoring **trojan** threats creates more **data breach** risks."

**ELENA:** "But without working **pivot tables**, we can't show **streaming** revenue projections. The **function** has to work despite the **trojan** situation."

### Critical Thinking Questions:
- Any serious streaming platform would be using supply chain security tools like Snyk or OWASP dependency check. Finding trojans manually in dependencies is what happens when you skip basic DevSecOps practices.
- Pivot tables for streaming analytics? Real streaming platforms use Kafka, Spark, and time-series databases for real-time analytics. Excel pivot tables are for business analysts, not streaming infrastructure.
- Why would a backend developer be writing custom functions instead of using established frameworks like Spring Boot or Express? This sounds like someone reinventing the wheel because they don't know industry standards.

## Scenario Improvement Analysis

**Validity of Criticisms:** The criticisms are valid. The scenario reflects outdated understanding of modern software development and security practices:

1. **Missing security tooling** - Modern development includes automated dependency scanning and vulnerability detection
2. **Inappropriate analytics tools** - Pivot tables are not used for real-time streaming analytics infrastructure
3. **Unrealistic development practices** - Custom function development instead of using established frameworks suggests poor architectural decisions

**Proposed Rewrite to Address Criticisms:**

The scenario should focus on realistic DevSecOps challenges:

- **Setting**: Streaming platform discovering a critical vulnerability in a widely-used open-source dependency through automated security scanning
- **Conflict**: Backend developer Kumar advocates for immediate patching despite potential service disruption, while business analyst Elena needs to maintain analytics availability for upcoming board presentation
- **Technical issues**: Focus on dependency management, security patch deployment strategies, and maintaining business intelligence during security updates
- **Tools and practices**: Use realistic technologies like automated vulnerability scanning, CI/CD pipeline security gates, and modern analytics platforms (not pivot tables)
- **Stakes**: Balancing security response time with business continuity, customer data protection, and regulatory compliance requirements
- **Resolution path**: Include options for staged deployment, hot-fix vs. full update strategies, and risk assessment frameworks that reflect actual DevSecOps practices

This maintains the educational focus on security vs. business pressure while using authentic software development challenges and modern security tooling.