# Cybersecurity: Oops, Systems Do Get Hacked

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
