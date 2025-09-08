# Web Advanced: Why Systems Don't Get Hacked

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

### Exam Questions

- **Analyze the security implications of different web technologies (cookies, JavaScript, HTTPS)**  Cookies can enable CSRF / tracking if not scoped (SameSite, HttpOnly); JavaScript introduces XSS risk; HTTPS mitigates eavesdropping but not application logic flaws; improper CSP/CORS settings expand attack surface.
- **Explain how cloud computing relates to web technologies and modern applications**  Cloud provides scalable infrastructure (compute, storage, functions, CDN) underpinning web backends; enables elasticity, global distribution, managed services (databases, auth) that web apps leverage for performance and reliability.
