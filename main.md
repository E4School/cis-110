# CIS110

## 1. Computer Fundamentals & Architecture
- **Explain the IPOS model of activities characteristics of computers**  Input (data entry), Processing (CPU executes instructions transforming data), Output (results presented to user/devices), Storage (persistent retention). It frames every program as a pipeline where correctness, performance, and usability hinge on clean inputs, efficient processing, appropriate output formatting, and reliable storage.
- **Describe the stored program concept and why it distinguishes computers from other simpler devices**  Instructions are stored in memory alongside data, allowing a general‑purpose machine to change behavior simply by loading different code (flexibility, reprogrammability). Simpler devices (e.g., hard‑wired calculators) have fixed logic; changing behavior requires hardware redesign.
- **Explain how a processor works**  The CPU repeatedly performs the fetch‑decode‑execute cycle: fetch instruction from memory (via program counter), decode (control unit interprets opcode, sets control signals), execute (ALU / other units perform operation), write back results, update PC. Modern CPUs add pipelining, caches, out‑of‑order execution, and branch prediction to increase throughput.
- **Explain the difference between RAM and ROM and why most computers have both**  RAM is volatile, fast read/write working memory; contents lost on power off. ROM (or flash/firmware) is non‑volatile, primarily read (or infrequently written) and holds bootstrap / firmware code needed before RAM and storage subsystems initialize. Together they enable reliable startup plus flexible runtime execution.
- **Explain what I/O devices are and why they are important to computing**  Peripherals that allow interaction with the external world (input: keyboard, sensors; output: displays, printers). They convert between human/physical signals and digital data, enabling practical usefulness of computation.
- **Analyze how the components of a computer system work together to execute a simple program**  User initiates program (stored on persistent storage) → OS loader copies executable segments into RAM → CPU fetches instructions using addresses resolved via MMU/cache hierarchy → instructions request data (caches / RAM / storage via I/O bus) → results buffered and eventually output via drivers to devices; OS schedules CPU time and manages resources throughout.
- **Compare and contrast different computer architectures (desktop, mobile, embedded systems)**  Desktop: high performance, modular, higher power draw. Mobile: energy efficiency, integrated system‑on‑chip, thermal constraints, wireless focus. Embedded: purpose‑specific, minimal UI, real‑time constraints, long lifecycle, often hardened. Trade‑offs revolve around performance vs power vs specialization.
- **Trace the flow of data through a computer system from input to output**  Input device generates signals → driver interprets and places data into OS buffers → user process reads data (system call) → CPU processes, manipulating in registers and RAM (caches accelerate) → results passed to output subsystem (system call) → driver formats & sends to device → device renders (screen, printer, network packet).

## 2. Storage Media & File Systems
- **Discuss the relative strengths and weaknesses of magnetic, optical, and solid-state storage technology**  Magnetic (HDD): high capacity, low cost/GB, slower seek, mechanical wear. Optical (DVD/Blu‑ray): removable, good for archiving/distribution, slower, limited rewrite cycles, lower capacity now. Solid‑state (SSD/NVMe): very fast, shock‑resistant, lower latency, higher cost/GB (though narrowing), finite write endurance.
- **Explain the role of file management**  Organizes storage for retrieval, version tracking, collaboration, and data integrity (naming, hierarchy, metadata usage, backups).
- **Discuss file naming conventions and the role of the file extension**  Conventions: descriptive, version tokens, no spaces/special chars (or consistent). Extension signals format to OS/application for association and parsing.
- **Explain the difference between an absolute path and a relative path**  Absolute: full location from root drive. Relative: location expressed from current working directory or parent reference.
- **Explain the difference between the logical and physical storage models for a file**  Logical: hierarchical directories & filenames. Physical: actual block locations managed by filesystem & hardware translation layers (e.g., wear leveling on SSDs).
- **Design an efficient file organization system for a specific use case (academic, professional, creative)**  Example academic: /Course/Week#/Topic/ with consistent prefixes (YYYY-MM-DD), separate /Resources, /Drafts, /Final, using version suffixes (v1, v2) and periodic archival.

## 3. Operating Systems & Process Concepts
- **Explain what a device driver is**  Low‑level software that provides a standardized interface between OS subsystems and specific hardware, translating generic OS calls into device‑specific commands and handling interrupts/events.
- **Explain the role of the operating system**  Abstracts hardware, schedules processes/threads, manages memory, filesystems, I/O, security (auth, permissions), networking, and provides APIs.
- **Explain the difference between multitasking, multiprocessing, and multithreading**  Multitasking: OS interleaves processes (logical concurrency). Multiprocessing: multiple physical cores/CPUs execute tasks truly in parallel. Multithreading: multiple threads within a process sharing memory space for finer concurrency.
- **Analyze how the components of a computer system work together to execute a simple program**  User initiates program (stored on persistent storage) → OS loader copies executable segments into RAM → CPU fetches instructions using addresses resolved via MMU/cache hierarchy → instructions request data (caches / RAM / storage via I/O bus) → results buffered and eventually output via drivers to devices; OS schedules CPU time and manages resources throughout.

## 4. Software, Licensing, and Development Lifecycle
- **Explain the difference between system software and application software**  System software manages hardware/resources (OS, utilities); application software performs end‑user tasks.
- **Discuss the purpose of software licensing and identify common types**  Defines legal use/redistribution; types: proprietary EULA, GPL (copyleft), MIT/Apache (permissive), shareware/trial, subscription (SaaS).
- **Explain the difference between local apps and Web based apps**  Local: installed, offline capable, deeper hardware integration. Web: delivered via browser, easy updates, cross‑platform, relies on network.
- **Explain the role of the basic office suite applications and their relation to each other**  Word processor (documents), spreadsheet (tabular quantitative analysis), presentation tool (visual communication). They share data (embedding, linking) and common UI paradigms.
- **Troubleshoot common software installation and configuration problems**  Steps: verify system requirements, check network/firewall, validate checksum/signature, run installer logs, isolate conflicting processes, clean environment variables, re‑install dependencies.
- **Compare different operating systems and their strengths for various computing tasks**  Windows: broad hardware/software ecosystem. macOS: integrated hardware + creative software. Linux: server, customization, containerization. Mobile OS (iOS/Android): touch, sensor integration.
- **Evaluate software alternatives based on functionality, cost, and licensing requirements**  Build comparison matrix (features, TCO, support, extensibility, compliance). Select option meeting must‑have features with lowest risk/long‑term cost.
- **Explain the software development lifecycle and how it impacts end users**  Phases (requirements → design → implementation → testing → deployment → maintenance) influence stability, security, and responsiveness to user feedback; mature processes reduce regressions.

## 5. Web Fundamentals
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

## 6. Social Media & Digital Communication
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

## 7. Intellectual Property & Digital Ethics
- **List the six rights that are exclusively exercised by copyright holders**  Reproduction, distribution, public performance, public display, derivative works, digital audio transmission (sound recordings).
- **List the four factors that characterize fair use**  Purpose and character, nature of the work, amount/substantiality, effect on market value.
- **Analyze the ethical implications of data collection by social media platforms**  Tensions: personalization vs surveillance, consent clarity, data minimization, algorithmic bias, secondary use without informed user control.
- **Evaluate data privacy and ethical considerations in database design**  Minimize data collection, apply encryption (at rest, in transit), role‑based access, retention limits, consent tracking, audit logging, anonymization/pseudonymization.

## 8. Cybersecurity Core Concepts
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

## 9. Database Concepts
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

## 10. Performance & Evaluation Concepts
- **Evaluate the trade-offs between performance, cost, and energy efficiency in computer design**  Increasing cores/clocks boosts performance but raises power/thermal design and cost. Energy efficiency improves battery life / operating cost but may reduce peak performance. Optimal design selects sufficient performance headroom while minimizing total cost of ownership (purchase + energy + cooling) for target workload.

## 11. Communication & Documentation
- **Explain how Wikipedia articles are written and edited**  Collaborative editing via MediaWiki; neutral point of view and verifiability policies; revision history + talk pages mediate disputes; consensus governs content.

## 12. Data & Information Literacy
- **Evaluate the credibility and reliability of online information sources**  Assess source authority, evidence citation, corroboration by independent outlets, update history, potential conflicts of interest, and bias indicators.

## 13. Security & Privacy in Web Context
- **Analyze the security implications of different web technologies (cookies, JavaScript, HTTPS)**  Cookies can enable CSRF / tracking if not scoped (SameSite, HttpOnly); JavaScript introduces XSS risk; HTTPS mitigates eavesdropping but not application logic flaws; improper CSP/CORS settings expand attack surface.

## 14. Cloud & Deployment (Optional Enrichment)
- **Explain how cloud computing relates to web technologies and modern applications**  Cloud provides scalable infrastructure (compute, storage, functions, CDN) underpinning web backends; enables elasticity, global distribution, managed services (databases, auth) that web apps leverage for performance and reliability.
