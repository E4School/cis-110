# Storage: How We Got Physics To Remember Stuff

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
