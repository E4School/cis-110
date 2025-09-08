# Algorithm - Cabrera Dialectic 2

Generated on 2025-09-03 12:55:16

What it is vs. what it isn’t
- An algorithm: a finite, unambiguous sequence of steps that transforms inputs into outputs.
- Not the same as code: code is a language-specific implementation of the abstract steps.
- Not a heuristic if steps are vague or may not yield the right answer; heuristics trade certainty for speed or simplicity.
- Not a data structure, though it often uses them; data structures store/organize data, algorithms operate on it.
- Randomized algorithms still qualify: the steps are unambiguous even if they include well-defined randomness.

Boundary questions to clarify scope
- Where does it start? At receipt/validation of input.
- Where does it end? Upon producing output and halting (termination condition).
- What assumptions must hold? Preconditions on inputs, resources, and environment.
- What guarantees are promised? Postconditions: correctness, performance bounds, resource usage.

Elements and organization (parts within the whole)
- Inputs: type, format, constraints.
- Steps: sequence, branching (if/else), iteration/recursion, data access patterns.
- State: variables, temporary storage, invariants that must remain true.
- Decision logic: comparisons, thresholds, tie-breaking rules.
- Termination condition: ensures finiteness.
- Outputs: type, format, correctness criteria.
- Analysis artifacts: correctness argument, complexity (time/space), edge cases, test suite.

How the pieces nest
- A complex algorithm is composed of subroutines (e.g., partition inside quicksort; relax inside Dijkstra).
- The algorithm sits inside a program that handles I/O, errors, and user interaction.
- Data structures enable operations (e.g., heaps for priority queues) that shape performance.
- In products, multiple algorithms chain together (e.g., parsing input → core computation → formatting output).

Core flows and mappings
- Input → validate → transform/normalize → core procedure → produce output → verify conditions.
- Preconditions → steps preserve invariants → termination → postconditions.
- Data complexity → operation count → runtime → energy/memory usage.

Trade-offs and tensions to reason about
- Time vs. space: faster often uses more memory (e.g., memoization).
- Worst-case vs. average-case behavior.
- Simplicity/readability vs. raw speed.
- Exactness vs. efficiency (approximation algorithms).
- Generality vs. specialization to specific data distributions.
- Determinism vs. randomized performance guarantees.

Multiple lenses to interrogate the same algorithm
- User: Does it give the right answer quickly enough on my device?
- Developer: Is it implementable, testable, maintainable? Clear invariants? Good failure modes?
- Mathematician: Can we prove termination and correctness? What are tight bounds?
- Systems engineer: How does it behave under memory/CPU constraints, cache, or parallelism?
- Ethicist/sociotechnical analyst: When the algorithm is part of decision systems (e.g., routing, ranking), what are the implications for fairness, transparency, and accountability?

Quality checks and probes
- Termination: Identify and justify the decreasing measure (e.g., input size shrinks).
- Correctness: State and prove invariants; use induction for recursive forms; test representative and adversarial cases.
- Complexity: Derive Big-O; profile real data; consider constant factors and cache behavior.
- Robustness: Validate inputs, handle edge conditions, define behavior on invalid inputs.
- Stability and idempotence where relevant (e.g., stable sorting, repeatable results).

Everyday anchors and their anatomy
- Unlocking a phone: input (passcode) → stepwise digit comparison → accept/reject → lockout after N failures (termination and security policy).
- Sorting contacts: choose a comparison rule → apply sorting procedure → guarantee order and stability (names with same last name).
- Map shortest route: model as a graph → apply path-finding (e.g., Dijkstra/A*) → output route; trade speed vs. optimality depending on heuristics and traffic updates.

Questions that sharpen thinking and design
- What exact problem class is this solving? What are valid inputs?
- What invariant, if maintained, forces correctness at the end?
- What’s the clearest termination argument?
- Which data structure choice best matches the operation frequency?
- What’s the acceptable performance envelope (time, space, energy) on target platforms?
- What are the simplest changes that break it? How will it fail safely?
- Can we substitute a simpler algorithm with comparable results for typical cases?

Mental pocket model
- Define the contract (pre/postconditions).
- Choose representations (data structures).
- Specify a finite, unambiguous step sequence that maintains invariants.
- Prove or test for termination and correctness.
- Measure and tune for the real constraints you actually face.
