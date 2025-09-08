# Algorithm - Categories 1

Generated on 2025-09-03 13:18:19

Short answer: Algorithm is both a category and a member. As a concept, “Algorithm” is a category that contains many specific algorithms; any particular algorithm (e.g., Quicksort) is a member of that category.

DSRP categorization view

- Category: “Algorithm” (the general concept: a clear, finite, step-by-step procedure that maps inputs to outputs via unambiguous rules).
- Members (examples): Euclid’s algorithm, Quicksort, Mergesort, Dijkstra’s algorithm, BFS/DFS, A*, PageRank, RSA key generation, Gradient Descent, K-Means, FFT.

Parent categories (context-dependent)
- Procedure/Method/Process (general)
- Computational procedure (computer science)
- Problem-solving method (applied math/CS)
- Formal specification/recipe for computation (theoretical CS)
- Information-processing method (information science)

Sibling categories (under different plausible parents)
- Under “Computational procedure”: heuristic (may sacrifice correctness/guarantees), protocol (interaction procedure among agents), workflow, recipe (everyday analogue).
- Under “Computing constructs”: data structure, program (implementation of an algorithm), specification, model.
- Under “Problem-solving method”: strategy, rule, policy, optimization method.

Subcategories of Algorithm (non-exhaustive)
- By determinism: deterministic, randomized, nondeterministic (theoretical model).
- By guarantee: exact, approximate.
- By interaction/timing: offline, online, streaming.
- By computational model: sequential, parallel, distributed, concurrent; external-memory/I-O efficient.
- By design technique: divide-and-conquer, dynamic programming, greedy, backtracking, branch-and-bound, local search.
- By domain/task: sorting, searching, selection, graph algorithms, string algorithms, cryptographic algorithms, numerical linear algebra, optimization, machine learning training/inference, compression.
- By complexity/resource profile: sublinear, linear-time, n log n, polynomial-time, exponential-time; space-bounded classes.
- By access/assumption: comparison-based, hashing-based, cache-aware/oblivious.

Perspective note
- As a type (category): “Algorithm” organizes and defines what counts as an algorithm.
- As a token (member): any named procedure (e.g., Dijkstra’s algorithm) is a member of that category.


---

## 2025-09-03 13:20:50

Genus–differentia (definition)
- Genus: procedure (a prescribed sequence of actions for transforming inputs into outputs)
- Differentia: finite and effectively computable sequence of unambiguous steps that, for any valid input, specifies how to produce the corresponding output independent of any particular programming language or machine representation; may include controlled randomness but is fully specified.

Taxonomic status
- Algorithm is both:
  - a member of broader categories (e.g., procedure, computational method)
  - a category containing instances (e.g., Quicksort, Dijkstra’s algorithm, Euclid’s GCD)

Immediate parent categories (from general to more specific)
- Procedure / method (general problem-solving or operational procedures)
- Formal/effective procedure (precisely specified, executable by a mechanical agent)
- Computational method (procedures intended for computation)
- Mathematical/computational artifact (abstract objects used in computation)

Representative siblings (sharing a parent such as “procedure/method”)
- Heuristic (procedure not guaranteed to be correct/optimal; may trade rigor for speed)
- Protocol (prescribed interaction procedure among agents or systems)
- Recipe/workflow (procedural instructions, often informal or domain-specific)
- Policy/rule set (prescriptive decision procedure, may lack finiteness or completeness)
- Data processing pipeline (procedural composition; often not specified at algorithmic level)

Subcategories of algorithm (non-exhaustive)
- By determinism/randomness:
  - Deterministic algorithms
  - Randomized algorithms (Las Vegas, Monte Carlo)
- By optimality/guarantees:
  - Exact algorithms
  - Approximation algorithms
  - Heuristics-as-algorithms (well-specified but not guaranteed optimal)
- By control strategy/paradigm:
  - Divide-and-conquer
  - Greedy
  - Dynamic programming
  - Backtracking/branch-and-bound
  - Recursive vs. iterative
  - Parallel and distributed algorithms
  - Online vs. offline algorithms
  - Streaming/sublinear-time algorithms
- By domain/problem class:
  - Sorting and searching algorithms (e.g., Quicksort, binary search)
  - Graph algorithms (e.g., Dijkstra, BFS/DFS, Kruskal)
  - Numerical algorithms (e.g., Newton–Raphson, Gaussian elimination)
  - Cryptographic algorithms (e.g., AES, RSA; also protocols built atop algorithms)
  - String/text algorithms (e.g., KMP, Boyer–Moore)
  - Optimization algorithms (e.g., simplex, gradient descent)
  - Machine learning algorithms (e.g., k-means, decision tree training)
  - Computational geometry, combinatorial, and randomized algorithms

Notes/contrasts
- Program vs. algorithm: a program is a concrete implementation; an algorithm is the abstract plan the code realizes.
- Not every procedure is an algorithm: informal, ambiguous, or non-terminating procedures fall outside the category.
- Desiderata (not definitional): correctness, termination, and efficiency; practical design balances time, space, and simplicity.
