# CIS110

## Hardware: How We Got Physics To Do Math REALLY Fast

### Vocab
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
- Throughput vs Latency
- Scalability (vertical, horizontal)
- Efficiency
- Bottleneck
- Trade‑off analysis
- Benchmark / Metric
- Optimization vs Premature optimization (principle)

### Relational Sentences
- A computer system coordinates hardware and software across the hardware/software boundary following the IPOS model where input devices feed data, processing transforms it, output devices present results, and storage keeps persistent data.
- The stored program concept lets instructions (opcodes) flow through the machine cycle (fetch–decode–execute) governed by the program counter (PC), control unit, and ALU along the data path (data flow).
- Registers, cache, and main memory (RAM) form a performance hierarchy distinct from ROM and firmware, balancing throughput, latency, energy efficiency, and thermal constraints.
- During boot a bootstrap loader initializes firmware, loads the OS via the loader, and activates each device driver that uses address, data, and control lines on the bus.
- A System on a Chip (SoC) integrates control unit, ALU, cache, and peripherals for embedded systems and mobile architecture variants, whereas desktop architecture may externalize more components.
- Designers analyze trade‑offs between performance, power consumption, and Total Cost of Ownership (TCO) when choosing storage technologies and architecture configurations.
- Throughput measures total work over time while latency measures per‑operation delay, and a bottleneck limits both.
- Scalability can be vertical (bigger node) or horizontal (more nodes) and is evaluated with benchmarks and metrics.
- Efficiency gains require trade‑off analysis to ensure improvements do not degrade maintainability or cost disproportionately.
- Optimization guided by metrics avoids premature optimization, which wastes effort without measurable bottleneck relief.

- **Explain the IPOS model of activities characteristics of computers**  Input (data entry), Processing (CPU executes instructions transforming data), Output (results presented to user/devices), Storage (persistent retention). It frames every program as a pipeline where correctness, performance, and usability hinge on clean inputs, efficient processing, appropriate output formatting, and reliable storage.
- **Describe the stored program concept and why it distinguishes computers from other simpler devices**  Instructions are stored in memory alongside data, allowing a general‑purpose machine to change behavior simply by loading different code (flexibility, reprogrammability). Simpler devices (e.g., hard‑wired calculators) have fixed logic; changing behavior requires hardware redesign.
- **Explain how a processor works**  The CPU repeatedly performs the fetch‑decode‑execute cycle: fetch instruction from memory (via program counter), decode (control unit interprets opcode, sets control signals), execute (ALU / other units perform operation), write back results, update PC. Modern CPUs add pipelining, caches, out‑of‑order execution, and branch prediction to increase throughput.
- **Explain the difference between RAM and ROM and why most computers have both**  RAM is volatile, fast read/write working memory; contents lost on power off. ROM (or flash/firmware) is non‑volatile, primarily read (or infrequently written) and holds bootstrap / firmware code needed before RAM and storage subsystems initialize. Together they enable reliable startup plus flexible runtime execution.
- **Explain what I/O devices are and why they are important to computing**  Peripherals that allow interaction with the external world (input: keyboard, sensors; output: displays, printers). They convert between human/physical signals and digital data, enabling practical usefulness of computation.
- **Analyze how the components of a computer system work together to execute a simple program**  User initiates program (stored on persistent storage) → OS loader copies executable segments into RAM → CPU fetches instructions using addresses resolved via MMU/cache hierarchy → instructions request data (caches / RAM / storage via I/O bus) → results buffered and eventually output via drivers to devices; OS schedules CPU time and manages resources throughout.
- **Compare and contrast different computer architectures (desktop, mobile, embedded systems)**  Desktop: high performance, modular, higher power draw. Mobile: energy efficiency, integrated system‑on‑chip, thermal constraints, wireless focus. Embedded: purpose‑specific, minimal UI, real‑time constraints, long lifecycle, often hardened. Trade‑offs revolve around performance vs power vs specialization.
- **Trace the flow of data through a computer system from input to output**  Input device generates signals → driver interprets and places data into OS buffers → user process reads data (system call) → CPU processes, manipulating in registers and RAM (caches accelerate) → results passed to output subsystem (system call) → driver formats & sends to device → device renders (screen, printer, network packet).
- **Evaluate the trade-offs between performance, cost, and energy efficiency in computer design**  Increasing cores/clocks boosts performance but raises power/thermal design and cost. Energy efficiency improves battery life / operating cost but may reduce peak performance. Optimal design selects sufficient performance headroom while minimizing total cost of ownership (purchase + energy + cooling) for target workload.


## Storage: How We Got Physics To Remember Stuff

### Vocab
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
- **Discuss the relative strengths and weaknesses of magnetic, optical, and solid-state storage technology**  Magnetic (HDD): high capacity, low cost/GB, slower seek, mechanical wear. Optical (DVD/Blu‑ray): removable, good for archiving/distribution, slower, limited rewrite cycles, lower capacity now. Solid‑state (SSD/NVMe): very fast, shock‑resistant, lower latency, higher cost/GB (though narrowing), finite write endurance.
- **Explain the role of file management**  Organizes storage for retrieval, version tracking, collaboration, and data integrity (naming, hierarchy, metadata usage, backups).
- **Discuss file naming conventions and the role of the file extension**  Conventions: descriptive, version tokens, no spaces/special chars (or consistent). Extension signals format to OS/application for association and parsing.
- **Explain the difference between an absolute path and a relative path**  Absolute: full location from root drive. Relative: location expressed from current working directory or parent reference.
- **Explain the difference between the logical and physical storage models for a file**  Logical: hierarchical directories & filenames. Physical: actual block locations managed by filesystem & hardware translation layers (e.g., wear leveling on SSDs).
- **Design an efficient file organization system for a specific use case (academic, professional, creative)**  Example academic: /Course/Week#/Topic/ with consistent prefixes (YYYY-MM-DD), separate /Resources, /Drafts, /Final, using version suffixes (v1, v2) and periodic archival.

## Operating Systems: Programs That Run Programs  

### Vocab
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
- **Explain what a device driver is**  Low‑level software that provides a standardized interface between OS subsystems and specific hardware, translating generic OS calls into device‑specific commands and handling interrupts/events.
- **Explain the role of the operating system**  Abstracts hardware, schedules processes/threads, manages memory, filesystems, I/O, security (auth, permissions), networking, and provides APIs.
- **Explain the difference between multitasking, multiprocessing, and multithreading**  Multitasking: OS interleaves processes (logical concurrency). Multiprocessing: multiple physical cores/CPUs execute tasks truly in parallel. Multithreading: multiple threads within a process sharing memory space for finer concurrency.
- **Analyze how the components of a computer system work together to execute a simple program**  User initiates program (stored on persistent storage) → OS loader copies executable segments into RAM → CPU fetches instructions using addresses resolved via MMU/cache hierarchy → instructions request data (caches / RAM / storage via I/O bus) → results buffered and eventually output via drivers to devices; OS schedules CPU time and manages resources throughout.

## Software Systems: How We Make Them

### Vocab
- System software vs Application software
- Software license (EULA, Proprietary, Open Source, Copyleft, Permissive)
- Shareware / Trial / Subscription (SaaS)
- Update / Patch
- Installation / Uninstall
- Dependency
- Software Development Lifecycle (SDLC): Requirements, Design, Implementation, Testing, Deployment, Maintenance
- Regression
- Usability vs Functionality
- Documentation / README
- Specification / Requirements
- Revision history / Versioning
- Tutorial / Guide
- Use case
- Stakeholder
- Neutral point of view (NPOV)
- Consensus (collaborative editing)

### Relational Sentences
- System software provides platform services that application software consumes, with both governed by software license terms like EULA, proprietary, open source, copyleft, or permissive models.
- Distribution models include shareware, trial, or subscription (SaaS), each affecting update and patch delivery cadence.
- Installation resolves each dependency while uninstall removes associated artifacts and may leave shared dependencies in place.
- The Software Development Lifecycle (requirements, design, implementation, testing, deployment, maintenance) iterates to reduce regression risk when applying a patch or adding functionality.
- Teams balance usability vs functionality, sometimes deferring noncritical features to avoid introducing regressions late in maintenance.
- A specification records requirements from stakeholders while documentation and the README summarize implementation context.
- Tutorials and guides translate requirements and use cases into actionable learning for new contributors.
- Revision history tracks versioning so collaborative editing can reach consensus while preserving a neutral point of view (NPOV).

### Final Exam Questions and Answers
- **Explain the difference between system software and application software**  System software manages hardware/resources (OS, utilities); application software performs end‑user tasks.
- **Discuss the purpose of software licensing and identify common types**  Defines legal use/redistribution; types: proprietary EULA, GPL (copyleft), MIT/Apache (permissive), shareware/trial, subscription (SaaS).
- **Explain the difference between local apps and Web based apps**  Local: installed, offline capable, deeper hardware integration. Web: delivered via browser, easy updates, cross‑platform, relies on network.
- **Explain the role of the basic office suite applications and their relation to each other**  Word processor (documents), spreadsheet (tabular quantitative analysis), presentation tool (visual communication). They share data (embedding, linking) and common UI paradigms.
- **Troubleshoot common software installation and configuration problems**  Steps: verify system requirements, check network/firewall, validate checksum/signature, run installer logs, isolate conflicting processes, clean environment variables, re‑install dependencies.
- **Compare different operating systems and their strengths for various computing tasks**  Windows: broad hardware/software ecosystem. macOS: integrated hardware + creative software. Linux: server, customization, containerization. Mobile OS (iOS/Android): touch, sensor integration.
- **Evaluate software alternatives based on functionality, cost, and licensing requirements**  Build comparison matrix (features, TCO, support, extensibility, compliance). Select option meeting must‑have features with lowest risk/long‑term cost.
- **Explain the software development lifecycle and how it impacts end users**  Phases (requirements → design → implementation → testing → deployment → maintenance) influence stability, security, and responsiveness to user feedback; mature processes reduce regressions.
- **Explain how Wikipedia articles are written and edited**  Collaborative editing via MediaWiki; neutral point of view and verifiability policies; revision history + talk pages mediate disputes; consensus governs content.


## Databases: How Systems Remember Stuff

### Vocab

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

- **Define basic database terminology, such as fields, records, rows, columns, and tables**  Table: structured collection; row/record: single entity instance; column/field: attribute; schema: structural definition.
- **Explain what a relational database is**  A structured collection organizing data into tables with defined relationships enforced via keys and set‑based query logic (relational algebra).
- **Explain the process of normalization**  Decomposing tables to reduce redundancy and anomalies (1NF atomic values, 2NF remove partial dependencies, 3NF remove transitive dependencies) balancing with performance.
- **Explain what SQL is and identify common SQL commands and give a concrete example**  Declarative language for defining/manipulating data. Core: SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER. Example: `SELECT name, price FROM products WHERE price > 100 ORDER BY price DESC;`.
- **Explain what big data is**  Datasets of high volume, velocity, or variety that exceed traditional relational processing capabilities; require distributed storage/compute (Hadoop, Spark) and specialized tooling.
- **Explain what NoSQL is**  Non‑relational data stores (document, key‑value, wide‑column, graph) optimizing for horizontal scalability, flexible schemas, or specific access patterns.
- **Design a simple database schema for a real-world scenario**  Example bookstore: Tables: Authors(id PK, name), Books(id PK, title, author_id FK, price), Orders(id PK, customer_id FK, order_date), OrderItems(order_id FK, book_id FK, qty). Index frequent lookups (Books.title, Orders.order_date).
- **Write basic SQL queries to retrieve and manipulate data**  Retrieval: `SELECT title FROM Books WHERE price < 20;` Manipulation: `UPDATE Books SET price = price * 0.9 WHERE author_id = 7;` Insertion: `INSERT INTO Authors(name) VALUES ('Ada Lovelace');`
- **Analyze the trade-offs between different database types for specific applications**  Relational: strong consistency/ACID; Document: flexible schema, denormalization for speed; Key‑value: ultra‑fast simple lookups; Graph: relationship traversal efficiency; Wide‑column: high write scalability for large sparse datasets.
- **Explain how databases integrate with web applications and business systems**  App layer uses drivers/ORM to execute SQL/queries, caches results, enforces business rules; transactions ensure consistency; APIs or message queues connect downstream analytics, reporting, and services.

## Web Fundamentals: How Billions of Systems Talk To Each Other

### Vocab
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
- **Explain how the Web works**  Clients (browsers) send HTTP(S) requests to servers using URLs; servers process (often via application logic + databases) and return responses (HTML, JSON, media). Hyperlinks interconnect documents forming a navigable graph.
- **Discuss the integration of three technologies that are foundational for the Web**  HTML structures content; CSS controls presentation; JavaScript enables dynamic behavior and client‑side logic. Together they separate concerns—structure, style, interactivity—allowing iterative and maintainable development.
- **Explain what the four parts of a URL are**  Scheme (protocol, e.g., https), host (domain), path (resource location), and optional query (key=value parameters) + fragment (in‑page anchor). (Some models treat port or fragment as additional components.)
- **Explain what a hyperlink is**  An element (usually an <a> tag) referencing another resource by URL enabling non‑linear navigation.
- **Explain the role of a Web browser with respect to caching, history, and privacy**  Browser caches resources (improves performance), maintains history (navigation convenience), and mediates privacy (cookie storage, tracking prevention, sandboxing). User settings balance speed versus confidentiality.
- **Explain what HTTP and HTTPS are**  Application‑layer request/response protocols; HTTPS layers HTTP over TLS to encrypt and authenticate, protecting confidentiality and integrity.
- **Explain what a Web cookie is**  Small key/value data stored client‑side by the browser, sent with subsequent requests to same domain—used for sessions, preferences, tracking.
- **Explain what HTML is**  Markup language defining semantic structure of web documents (headings, paragraphs, media, forms). Parsed into the DOM.
- **Identify 5 common HTML tags and explain what they do**  <h1>-<h6>: headings hierarchy; <p>: paragraph; <a>: hyperlink; <img>: embeds image; <div>: generic block container; <form>: user input submission context.
- **Explain what CSS is**  Stylesheet language that selects DOM elements and applies presentation rules (layout, color, typography, responsive adjustments).
- **Explain the role of JavaScript in a Web page**  Enables dynamic DOM manipulation, event handling, asynchronous network calls (fetch), client logic, and integration with APIs and storage.
- **Design a simple webpage that demonstrates understanding of HTML structure and CSS styling**  (Example) HTML skeleton with semantic header/main/footer; CSS for responsive layout using flexbox; styled navigation; accessible alt text. (*Omitted source for brevity—can be added on request.*)
- **Evaluate the accessibility and usability of web interfaces**  Check semantic markup, ARIA where needed, color contrast, keyboard navigation, responsive scaling, meaningful alt text, and consistent feedback; usability aligns with predictable navigation and minimized cognitive load.

## Web Advanced: Why Systems Don't Get Hacked

### Vocab
- Session
- SameSite / HttpOnly (cookie scopes basics)
- TLS / Certificate
- Mixed content
- Tracking / Third‑party scripts
- Content Security Policy (CSP)
- Cross‑Origin Resource Sharing (CORS)
- Elasticity / Autoscaling
- Serverless / Functions as a Service (FaaS)
- Container / Virtual machine
- Multi‑tenancy
- Load balancing
- High availability
- Disaster recovery / Backup strategy

### Relational Sentences
- A session identifier often resides in a cookie whose SameSite and HttpOnly attributes constrain cross‑site requests and script access.
- TLS with a valid certificate protects session confidentiality and integrity while preventing downgrade and many mixed content warnings.
- Tracking frequently relies on third‑party scripts whose origins can be limited by a Content Security Policy (CSP) and CORS configuration.
- Mixed content occurs when secure pages load insecure resources, undermining TLS guarantees and enabling tracking or injection vectors.
- Elasticity leverages autoscaling to adjust resources dynamically for high availability under variable load.
- Serverless (FaaS) abstractions complement container or virtual machine deployments by offloading infrastructure management.
- Multi‑tenancy shares compute resources across tenants while load balancing distributes traffic among instances to avoid single bottlenecks.
- A disaster recovery and backup strategy underpins high availability objectives when failures exceed autoscaling resilience.

### Final Exam Questions and Answers

- **Analyze the security implications of different web technologies (cookies, JavaScript, HTTPS)**  Cookies can enable CSRF / tracking if not scoped (SameSite, HttpOnly); JavaScript introduces XSS risk; HTTPS mitigates eavesdropping but not application logic flaws; improper CSP/CORS settings expand attack surface.
- **Explain how cloud computing relates to web technologies and modern applications**  Cloud provides scalable infrastructure (compute, storage, functions, CDN) underpinning web backends; enables elasticity, global distribution, managed services (databases, auth) that web apps leverage for performance and reliability.

## Cybersecurity: Oops, Systems Do Get Hacked

### Vocab

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

- **Explain what encryption is**  Transforming plaintext into ciphertext using an algorithm + key to ensure confidentiality (reversible only with key).
- **Explain what two-factor authentication is**  Combining two independent credential factors (something you know, have, are) to reduce compromise risk.
- **Discuss issues with creating a strong password**  Balancing memorability vs entropy; risks: reuse, predictable patterns, social engineering exposure; mitigations: passphrases, managers.
- **Explain what malware is**  Malicious software designed to exploit, disrupt, steal, or extort (viruses, worms, trojans, ransomware, spyware).
- **Explain what a rootkit is**  Stealth malware that hides its presence by modifying low‑level system components (kernel/drivers) to maintain privileged concealed access.
- **Identify common malware exploits**  Unpatched vulnerabilities (buffer overflows), phishing delivery, drive‑by downloads, malicious macros, supply chain tampering.
- **Describe how an online intrusion takes place**  Recon (enumerate targets) → initial access (phish/exploit) → privilege escalation → lateral movement → data exfiltration / persistence setup → cleanup or ransomware deployment.
- **Explain what a zero-day exploit is**  Attack leveraging a previously unknown and unpatched vulnerability; defenders have “zero days” to prepare.
- **Explain the role of a firewall**  Filters traffic per policy (ports, IPs, protocols), enforcing segmentation and reducing attack surface.
- **Explain what spoofing is**  Masquerading as a trusted entity (IP, MAC, email, caller ID) to bypass controls or mislead users.
- **Explain what social engineering is**  Psychological manipulation to elicit confidential actions/information (phishing, pretexting, baiting, tailgating).
- **Develop a comprehensive personal cybersecurity strategy including risk assessment**  Inventory assets → assess threats/vulnerabilities → apply controls (MFA, updates, least privilege, backups, password manager, encrypted storage, phishing training) → monitor & review.
- **Analyze real-world security breaches and identify prevention strategies**  Typically involve patch delays, credential reuse, misconfigurations. Strategies: timely patching, zero trust segmentation, strong auth, encryption at rest/in transit, continuous monitoring.
- **Evaluate the security posture of common online services and applications**  Assess encryption usage, MFA availability, breach history, logging transparency, data minimization, compliance certifications.
- **Design secure communication protocols for sensitive information sharing**  Use end‑to‑end encryption (modern AEAD ciphers), forward secrecy (ephemeral keys via Diffie-Hellman), mutual authentication, integrity checks, minimal metadata.
- **Assess the balance between security measures and usability in system design**  Overly strict controls cause workarounds; iterative user testing finds equilibrium where friction yields meaningful risk reduction.

## People: How Systems Shape Society 

### Vocab
- Social media platform
- Network effect
- Profile (handle, avatar, bio)
- Six degrees of separation
- Blog / Blogging
- User‑generated content (UGC)
- Webmail vs Local mail client
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

### Final Exam Questions and Answers
- **Explain what social media is**  Platforms enabling user‑generated content creation, sharing, and interaction at scale via network effects.
- **List three elements of a social media profile**  Username/handle, profile image, bio (plus often links or interests).
- **Explain how 6 degrees of separation applies to social networking**  Suggests short path lengths between any two users, facilitating rapid information diffusion and virality.
- **Discuss why blogs were considered a disruptive technology**  Lowered publishing barrier, disintermediated traditional media gatekeepers, accelerated niche and real‑time commentary.
- **Discuss the pros and cons of Webmail and local mail**  Webmail: ubiquitous access, reduced client maintenance, server‑side filtering; cons: privacy dependence on provider, offline limitations. Local (client) mail: offline access, potential privacy control; cons: configuration, sync, backup overhead.
- **List the elements that constitute an online identity**  Credentials (username/email), profile attributes, activity history, connections, behavioral metadata (time, device), and content artifacts.
- **List four techniques for dealing with cyberbullies**  Document incidents, block/report offenders, adjust privacy settings, seek support (trusted adults/platform moderation), avoid escalation.
- **Design a digital citizenship plan that balances online engagement with privacy protection**  Use pseudonymous accounts where appropriate, strong unique passwords & MFA, minimal oversharing, scheduled screen breaks, curated follows, periodic privacy audits.
- **Compare traditional media distribution models with modern digital platforms**  Traditional: centralized editorial control, scheduled releases. Digital: decentralized creators, algorithmic feeds, on‑demand consumption, rapid iteration, monetization fragmentation.
- **Assess the impact of algorithmic content curation on information consumption**  Filter bubbles, engagement amplification, potential polarization, but also personalization efficiency; transparency and user controls are mitigating factors.


## You: How Systems Shapes You

### Vocab
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
- Data becomes information when contextualized with metadata that clarifies source, meaning, or structure.
- Visualization (charts/graphs) aids pattern recognition and supports logical reasoning about relationships among variables.
- Abstraction involves distinction and categorization (taxonomy) to simplify complexity while preserving essential relationships.
- Concept mapping reveals relationship structure and invites multiple perspectives (viewpoints) during iterative refinement cycles.

- **List the six rights that are exclusively exercised by copyright holders**  Reproduction, distribution, public performance, public display, derivative works, digital audio transmission (sound recordings).
- **List the four factors that characterize fair use**  Purpose and character, nature of the work, amount/substantiality, effect on market value.
- **Analyze the ethical implications of data collection by social media platforms**  Tensions: personalization vs surveillance, consent clarity, data minimization, algorithmic bias, secondary use without informed user control.
- **Evaluate data privacy and ethical considerations in database design**  Minimize data collection, apply encryption (at rest, in transit), role‑based access, retention limits, consent tracking, audit logging, anonymization/pseudonymization.
- **Evaluate the credibility and reliability of online information sources**  Assess source authority, evidence citation, corroboration by independent outlets, update history, potential conflicts of interest, and bias indicators.
