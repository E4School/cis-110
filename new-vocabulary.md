# Prerequisite & Supporting Vocabulary for Learning Goals

This document lists words, concepts, and phrases that students likely need to understand to successfully meet the articulated learning goals. Terms are grouped by conceptual domain; some appear in multiple domains but are listed once in their primary category. Sub‑bullets indicate brief cues or disambiguations, not full definitions.

## 1. Computer Fundamentals & Architecture

- Computer system (system)
- Hardware / Software boundary
- IPOS model (Input, Processing, Output, Storage)
- Input device / Output device
- Storage (persistent storage)
- Stored program concept
- Instruction / Opcode / Machine cycle (fetch–decode–execute)
- Program counter (PC)
- Control unit / ALU
- Register / Cache / Main memory (RAM)
- RAM (volatile) vs ROM / Firmware (non‑volatile)
- Boot / Bootstrap / Loader
- Device driver
- Bus (data / address / control)
- System on a Chip (SoC)
- Embedded system
- Architecture (desktop, mobile, embedded)
- Performance (throughput, latency)
- Energy efficiency / Power consumption / Thermal constraints
- Trade‑off
- Total Cost of Ownership (TCO)
- Data path / Data flow

### Relational Sentences
- A computer system coordinates hardware and software across the hardware/software boundary following the IPOS model where input devices feed data, processing transforms it, output devices present results, and storage keeps persistent data.
- The stored program concept lets instructions (opcodes) flow through the machine cycle (fetch–decode–execute) governed by the program counter (PC), control unit, and ALU along the data path (data flow).
- Registers, cache, and main memory (RAM) form a performance hierarchy distinct from ROM and firmware, balancing throughput, latency, energy efficiency, and thermal constraints.
- During boot a bootstrap loader initializes firmware, loads the OS via the loader, and activates each device driver that uses address, data, and control lines on the bus.
- A System on a Chip (SoC) integrates control unit, ALU, cache, and peripherals for embedded systems and mobile architecture variants, whereas desktop architecture may externalize more components.
- Designers analyze trade‑offs between performance, power consumption, and Total Cost of Ownership (TCO) when choosing storage technologies and architecture configurations.

## 2. Storage Media & File Systems

- Magnetic storage (HDD)
- Optical storage (CD/DVD/Blu‑ray)
- Solid‑state storage (SSD / NVMe / Flash)
- Seek time / Latency
- Wear leveling
- File / Folder (Directory)
- File extension
- Absolute path vs Relative path
- Logical vs Physical storage model
- File naming conventions
- Backup / Archiving
- Versioning / Version control (basic concept)
- Checksum / Integrity verification

### Relational Sentences
- Magnetic storage (HDD), optical storage (CD/DVD/Blu‑ray), and solid‑state storage (SSD, NVMe Flash) differ in typical seek time and latency, influencing performance trade‑offs.
- SSD controllers use wear leveling to extend Flash lifespan while maintaining low latency compared to HDD mechanical seek time.
- Files reside inside folders (directories) and are identified by a file extension that informs software how to interpret their logical content distinct from the physical storage model.
- Absolute paths specify a file’s full location while relative paths depend on a current working directory, both governed by file naming conventions that enhance portability.
- Backup and archiving policies preserve versions, enabling versioning or basic version control and allowing integrity verification with a checksum after restoration.

## 3. Operating Systems & Process Concepts

- Operating System (OS)
- Process / Thread
- Multitasking / Multiprocessing / Multithreading
- Scheduling
- Concurrency vs Parallelism
- Memory management
- Interrupt / Interrupt handler
- System call / API
- Permissions / Access control
- Configuration / Environment variables

### Relational Sentences
- An operating system (OS) manages processes and their threads to enable multitasking, multiprocessing, and multithreading through scheduling algorithms.
- Concurrency allows multiple tasks to make progress while parallelism executes threads simultaneously on multiple cores under OS scheduling.
- Memory management allocates and protects each process’s address space while enforcing permissions and access control models.
- System calls expose an API boundary where user processes request OS services, often triggered or influenced by configuration and environment variables.
- Hardware devices raise interrupts that invoke interrupt handlers so the OS can preempt processes and maintain responsive multitasking.

## 4. Software, Licensing, and Development Lifecycle

- System software vs Application software
- Software license (EULA, Proprietary, Open Source, Copyleft, Permissive)
- Shareware / Trial / Subscription (SaaS)
- Update / Patch
- Installation / Uninstall
- Dependency
- Software Development Lifecycle (SDLC): Requirements, Design, Implementation, Testing, Deployment, Maintenance
- Regression
- Usability vs Functionality

### Relational Sentences
- System software provides platform services that application software consumes, with both governed by software license terms like EULA, proprietary, open source, copyleft, or permissive models.
- Distribution models include shareware, trial, or subscription (SaaS), each affecting update and patch delivery cadence.
- Installation resolves each dependency while uninstall removes associated artifacts and may leave shared dependencies in place.
- The Software Development Lifecycle (requirements, design, implementation, testing, deployment, maintenance) iterates to reduce regression risk when applying a patch or adding functionality.
- Teams balance usability vs functionality, sometimes deferring noncritical features to avoid introducing regressions late in maintenance.

## 5. Web Fundamentals

- Internet vs Web
- Client / Server
- HTTP / HTTPS
- URL (scheme, host/domain, path, query, fragment)
- Request / Response
- Status code (general idea)
- Browser (cache, history, privacy modes)
- Hyperlink
- HTML / DOM
- Tag / Element / Attribute
- CSS (selector, rule, declaration)
- JavaScript (script, event, asynchronous / fetch)
- Cookie (session, tracking)
- Caching (browser/server)
- Content Delivery Network (CDN)
- Cloud computing (scalability, elasticity)
- Accessibility (a11y) / ARIA roles
- Responsive design
- Cross‑Site Scripting (XSS) (basic awareness)
- CORS / CSP (basic awareness)

### Relational Sentences
- The Internet provides underlying network infrastructure while the Web uses HTTP or HTTPS for client/server communication defined by request and response exchanges with status codes.
- A URL encodes scheme, host (domain), path, query, and fragment so a browser can fetch hyperlinked resources and construct or update the DOM from HTML tags, elements, and attributes.
- CSS selectors apply rules (declarations) to elements while JavaScript scripts attach event handlers and perform asynchronous fetch calls to update the DOM dynamically.
- Cookies persist session identifiers or tracking data; browser and server caching plus a Content Delivery Network (CDN) reduce latency by reusing cached content.
- Cloud computing offers scalability and elasticity so web applications can adapt responsive design layouts while preserving accessibility (a11y) with ARIA roles.
- Security measures like CSP and CORS restrict resource origins, mitigating Cross‑Site Scripting (XSS) injection vectors.

## 6. Social Media & Digital Communication

- Social media platform
- Network effect
- Profile (handle, avatar, bio)
- Six degrees of separation
- Blog / Blogging
- User‑generated content (UGC)
- Webmail vs Local mail client
- IMAP vs POP
- Online identity (credentials, activity history, connections)
- Cyberbullying
- Privacy settings
- Algorithmic curation / Filter bubble
- Engagement
- Credibility / Source reliability
- Digital citizenship / Digital footprint
- Screen time / Digital wellness / Digital detox
- Pseudonymity

### Relational Sentences
- A social media platform amplifies user‑generated content (UGC) as profiles with handles, avatars, and bios interact, forming a network effect often described by six degrees of separation.
- Online identity combines credentials, activity history, and connections, leaving a digital footprint that digital citizenship norms encourage users to steward responsibly.
- Algorithmic curation can create a filter bubble that shapes perceived credibility and source reliability, influencing engagement metrics.
- Privacy settings, plus choices like pseudonymity, govern exposure and can mitigate risks such as cyberbullying.
- Managing screen time supports digital wellness; intentional digital detox periods counter engagement‑driven overuse.
- Webmail and local mail clients implement IMAP or POP protocols to access messaging alongside blogging channels in broader digital communication ecosystems.

## 7. Intellectual Property & Digital Ethics

- Copyright
- Exclusive rights (reproduction, distribution, public performance, public display, derivative works, digital audio transmission)
- Fair use (four factors)
- Creative Commons (licensing variants notionally)
- Plagiarism
- Open source
- Proprietary software
- Data collection / Data minimization
- Algorithmic bias
- Surveillance
- Consent / Informed consent
- Ethical considerations / Secondary use

### Relational Sentences
- Copyright grants exclusive rights including reproduction, distribution, public performance, public display, derivative works, and digital audio transmission.
- Fair use balances these rights through four factors while Creative Commons licenses pre‑declare permitted uses to reduce plagiarism risk and clarify derivative work terms.
- Open source and proprietary software models differ in redistribution and modification allowances defined by license terms.
- Ethical considerations in data collection emphasize data minimization and informed consent to prevent unauthorized secondary use.
- Surveillance systems can exacerbate algorithmic bias if data minimization and consent safeguards are weak.

## 8. Cybersecurity Core Concepts

- Encryption / Ciphertext / Key / Decryption
- Two‑factor authentication (2FA) / Multi‑factor (MFA)
- Password entropy / Passphrase
- Malware (virus, worm, trojan, ransomware, spyware)
- Rootkit
- Exploit / Vulnerability / Patch
- Zero‑day exploit
- Intrusion (recon, privilege escalation, lateral movement, exfiltration)
- Firewall
- Spoofing (IP, email)
- Social engineering (phishing, pretexting, baiting, tailgating)
- Risk assessment (assets, threats, vulnerabilities, controls)
- Least privilege
- Encryption at rest / in transit
- Forward secrecy
- Integrity / Authenticity
- Security vs Usability trade‑off

### Relational Sentences
- Encryption transforms plaintext into ciphertext using a key, and decryption reverses it; forward secrecy ensures past sessions remain secure even if long‑term keys leak.
- Encryption at rest protects stored data while encryption in transit protects data between hosts, both supporting integrity and authenticity goals.
- Two‑factor or multi‑factor authentication boosts resistance to credential theft beyond password entropy or a passphrase alone.
- Malware categories (virus, worm, trojan, ransomware, spyware) and rootkits exploit vulnerabilities until a patch closes the exploit vector.
- A zero‑day exploit targets an unknown vulnerability before defenders can patch, increasing intrusion risk across recon, privilege escalation, lateral movement, and exfiltration stages.
- Firewalls and least privilege policies reduce attack surface and mitigate spoofing or social engineering attempts like phishing, pretexting, baiting, and tailgating.
- Risk assessment catalogs assets, threats, vulnerabilities, and controls to balance the security vs usability trade‑off in defensive posture.

## 9. Database Concepts

- Database / Table / Row (Record) / Column (Field)
- Schema
- Primary key / Foreign key (FK) (implied; relationships)
- Relationship (one‑to‑many, many‑to‑many)
- Normalization (1NF, 2NF, 3NF)
- SQL (SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER)
- Query / Query optimization (intro)
- Index
- Transaction / ACID (conceptual awareness)
- Big data (volume, velocity, variety)
- NoSQL (document, key‑value, wide‑column, graph)
- Denormalization
- Data privacy / Anonymization / Pseudonymization
- Data retention policy
- ORM (Object‑Relational Mapping) (intro)

### Relational Sentences
- A database organizes data into tables whose rows (records) and columns (fields) conform to a schema expressing relationships via primary and foreign keys.
- Relationship types (one‑to‑many, many‑to‑many) influence normalization choices (1NF, 2NF, 3NF) to reduce redundancy.
- SQL statements (SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER) manipulate data while queries benefit from indexes during query optimization.
- Transactions enforce ACID properties so multi‑statement operations remain consistent and isolated even under concurrency.
- Big data characteristics (volume, velocity, variety) motivate NoSQL models (document, key‑value, wide‑column, graph) or selective denormalization for performance.
- Data privacy goals can be supported through anonymization or pseudonymization guided by a data retention policy.
- An ORM maps objects to tables, abstracting SQL while still requiring awareness of indexing and normalization impacts.

## 10. Performance & Evaluation Concepts (Cross‑Cutting)

- Throughput vs Latency
- Scalability (vertical, horizontal)
- Efficiency
- Bottleneck
- Trade‑off analysis
- Benchmark / Metric
- Optimization vs Premature optimization (principle)

### Relational Sentences
- Throughput measures total work over time while latency measures per‑operation delay, and a bottleneck limits both.
- Scalability can be vertical (bigger node) or horizontal (more nodes) and is evaluated with benchmarks and metrics.
- Efficiency gains require trade‑off analysis to ensure improvements do not degrade maintainability or cost disproportionately.
- Optimization guided by metrics avoids premature optimization, which wastes effort without measurable bottleneck relief.

## 11. Communication & Documentation

- Documentation / README
- Specification / Requirements
- Revision history / Versioning
- Tutorial / Guide
- Use case
- Stakeholder
- Neutral point of view (NPOV)
- Consensus (collaborative editing)

### Relational Sentences
- A specification records requirements from stakeholders while documentation and the README summarize implementation context.
- Tutorials and guides translate requirements and use cases into actionable learning for new contributors.
- Revision history tracks versioning so collaborative editing can reach consensus while preserving a neutral point of view (NPOV).

## 12. Data & Information Literacy

- Data vs Information
- Metadata
- Visualization (chart/graph)
- Pattern recognition
- Abstraction
- Logical reasoning
- Iteration
- Distinction (implicit DSRP)
- Categorization / Taxonomy
- Relationship (concept mapping)
- Perspective (viewpoint)

### Relational Sentences
- Data becomes information when contextualized with metadata that clarifies source, meaning, or structure.
- Visualization (charts/graphs) aids pattern recognition and supports logical reasoning about relationships among variables.
- Abstraction involves distinction and categorization (taxonomy) to simplify complexity while preserving essential relationships.
- Concept mapping reveals relationship structure and invites multiple perspectives (viewpoints) during iterative refinement cycles.

## 13. Security & Privacy in Web Context (Overlap)

- Session
- SameSite / HttpOnly (cookie scopes basics)
- TLS / Certificate
- Mixed content
- Tracking / Third‑party scripts
- Content Security Policy (CSP)
- Cross‑Origin Resource Sharing (CORS)

### Relational Sentences
- A session identifier often resides in a cookie whose SameSite and HttpOnly attributes constrain cross‑site requests and script access.
- TLS with a valid certificate protects session confidentiality and integrity while preventing downgrade and many mixed content warnings.
- Tracking frequently relies on third‑party scripts whose origins can be limited by a Content Security Policy (CSP) and CORS configuration.
- Mixed content occurs when secure pages load insecure resources, undermining TLS guarantees and enabling tracking or injection vectors.

## 14. Cloud & Deployment (Optional enrichment)

- Elasticity / Autoscaling
- Serverless / Functions as a Service (FaaS)
- Container / Virtual machine
- Multi‑tenancy
- Load balancing
- High availability
- Disaster recovery / Backup strategy

### Relational Sentences
- Elasticity leverages autoscaling to adjust resources dynamically for high availability under variable load.
- Serverless (FaaS) abstractions complement container or virtual machine deployments by offloading infrastructure management.
- Multi‑tenancy shares compute resources across tenants while load balancing distributes traffic among instances to avoid single bottlenecks.
- A disaster recovery and backup strategy underpins high availability objectives when failures exceed autoscaling resilience.
