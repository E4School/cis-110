# Absolute Path - Categories 1

Generated on 2025-09-03 13:17:34

Here’s a concise DSRP analysis of “Absolute Path,” with emphasis on categorization.

Distinctions (what it is vs. is not)
- Is: a type of file system path that begins at the root and uniquely locates a resource regardless of the current working directory.
- Is not: a relative path (depends on working directory), a URL/URI (web addressing), or merely a “canonical” path (resolution/normalization property).
- Synonyms: full path, fully qualified path (FQP/FQPN).

Systems (parts/structure of the concept)
- Components: root indicator (e.g., / or C:\), directory segments, separators, filename, optional extension.
- Windows variants: drive letter + root (C:\...), UNC authority (\\server\share\...), NT device prefix (\\?\...).
- POSIX variants: leading slash (e.g., /home/alex/...).

Relationships (how it connects to other concepts)
- Independent of working directory; anchored to the filesystem root.
- Used in scripts/configs for unambiguous resource location; trade-off vs portability.
- Related to security (path traversal mitigation), portability, and symlink resolution (canonicalization).

Perspectives (views that shift categorization)
- OS perspective: Windows vs POSIX forms.
- User/developer perspective: “absolute path” as a category (type) vs a specific string as a member (instance).

Categorization focus
- Is it a category, a member, or both?
  - As a concept/type (“Absolute Path”): it is a category (a class of paths).
  - Any concrete string like C:\Users\Alex\Documents\report.docx or /home/alex/report.docx is a member (instance) of that category.
  - OS-specific forms (e.g., UNC absolute paths) can be treated as subcategories within the broader category.

Hierarchy and related categories

- Parent categories (choose level of granularity you need)
  - File system path (pathname)
  - Pathname types
  - File system concepts (within Operating Systems)

- Sibling categories (other pathname types or closely related path concepts)
  - Relative path
  - Canonical/real path (absolute or relative after resolving symlinks) — often treated as a property/type
  - Normalized path (property/type: redundant segments removed)
  - UNC path (Windows; note: typically a subcategory of absolute path)
  - Device path (Windows \\?\ or \\.\ prefixes; typically absolute)
  - Home-relative path (~ on POSIX; expands to an absolute path but itself is not absolute until expanded)

- Subcategories of Absolute Path
  - By OS:
    - POSIX absolute paths: start with /
    - Windows absolute paths:
      - Drive-letter absolute paths: C:\...
      - UNC absolute paths: \\server\share\folder\file
      - NT device absolute paths: \\?\C:\..., \\.\PhysicalDrive0
  - By resolution/state:
    - Logical absolute path (may include symlinks)
    - Canonical/real absolute path (symlinks resolved)
  - By target:
    - Absolute directory paths
    - Absolute file paths

Bottom line
- “Absolute Path” is best treated as a category (type of file system path). Specific full path strings are members of that category. OS-specific absolute forms (POSIX, Windows drive-letter, UNC, device paths) are useful subcategories.


---

## 2025-09-03 13:20:05

Genus–differentia definition
- Genus: pathname (file path) — a string that designates a location within a filesystem namespace.
- Differentia: begins at the root of the filesystem (not the current working directory) and fully specifies a unique location, so resolution is independent of where the reference is made.

Category status
- It is a category (a type of pathname). Individual strings like C:\Users\Alex\Documents\report.docx or /home/alex/Documents/report.docx are members of this category.

Immediate parent category
- Pathname (a.k.a. file path, filepath, pathname string)

Core differentiating properties
- Root-anchored: starts at the filesystem root.
- Context-independent: resolves to the same location regardless of the process’s current working directory.
- OS-constrained syntax: 
  - POSIX: leading slash (/usr/bin/python)
  - Windows: drive-letter root (C:\Windows\System32) or UNC/device roots (\\server\share, \\?\C:\…)

Sibling categories (other kinds of pathnames)
- Relative path — interpreted with respect to a current working directory (e.g., ../logs/app.log).
- Rooted path (Windows) — begins with a backslash but omits the drive; anchored to the current drive’s root (e.g., \Windows\System32); not fully absolute.
- Normalized path — a pathname with redundant components removed (e.g., no . or ..), which can be absolute or relative.
- Canonical path (general notion) — a unique, fully resolved path with symlinks resolved; often absolute but the term itself isn’t limited to absolute paths.
- Environment-expanded path — path after expanding variables like %USERPROFILE% or $HOME; can be absolute or relative.

Subcategories (not exhaustive)
- POSIX absolute path — leading slash; components separated by / (e.g., /var/log/syslog).
- Windows absolute path (drive-letter) — [A–Z]:\ root with \ separators (e.g., D:\Projects\app\README.md).
- Windows UNC absolute path — network root \\server\share\… (e.g., \\fileserver\dept\budget.xlsx).
- Windows device-namespace absolute path — NT namespace (e.g., \\?\C:\very\long\path.txt, \\.\COM1).
- Canonical absolute path — absolute path after normalization and symlink/junction resolution.
- Absolute directory path vs absolute file path — absolute references where the last component is a directory (often ends with a separator on some tools) versus a file.

Notes and edge cases
- On Windows, a path like \Temp is not fully absolute; it depends on the current drive (rooted path).
- A URL’s “absolute URL” is a different domain and shouldn’t be confused with filesystem absolute paths.
