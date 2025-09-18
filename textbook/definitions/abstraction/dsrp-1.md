# Abstraction - Cabrera Dialectic 2

Generated on 2025-09-03 12:54:49

Clarify the idea
- What it is vs. what it isn’t:
  - Is: focusing on essentials; hiding incidental detail behind a stable interface.
  - Isn’t: ignoring reality; it’s selective representation with a purpose.
- Boundary decisions:
  - Interface (public contract) vs. implementation (hidden mechanism).
  - Essential features vs. accidental complexity.
  - General concepts (e.g., “List”) vs. concrete instances (e.g., “array of 10 ints”).
- Signals vs. noise:
  - Keep: name, purpose, inputs/outputs, invariants.
  - Hide: data layout, control flow, optimizations.

Organize it
- Parts of an abstraction:
  - Interface: names, types, pre/postconditions, error model.
  - Contract: what must hold (invariants), performance envelope, security posture.
  - Semantics: meaning of operations independent of implementation.
  - Evidence: tests/specs/docs/examples.
- Wholes and nesting:
  - Layers: hardware → OS → runtime → libraries → app → UI.
  - Common forms: data type, class, module, service, API, DSL, map/diagram.
  - Levels of granularity: function → module → subsystem → architecture.
- Exemplars:
  - Map vs. city; function call vs. source code; data type/class vs. raw memory; API vs. service internals.

Map interactions
- Causes and effects:
  - Hiding detail reduces cognitive load → easier to reason/change.
  - Clear interfaces reduce coupling → safer refactors.
  - Stable contracts enable reuse and substitution.
- Constraints and enablers:
  - Types/specs constrain behavior → enable composition.
  - Versioning and compatibility rules stabilize interfaces across change.
- Trade-offs:
  - Too little hiding → tight coupling, fragile code.
  - Too much/poor fit → “leaky” abstractions, extra indirection, performance cost.
  - Wrong level → either oversimplifies (missing needed detail) or overcomplicates (unnecessary knobs).
- Feedback loops:
  - Usage reveals mismatches → refine interface or add affordances.
  - Performance anomalies surface leaks → rework boundary or implementation.
  - Evolving domain → retire or generalize abstractions.
- Dependencies:
  - Clients depend on contract, not internals; tests/types enforce this.
  - Observability (logs/metrics) provides a controlled “window” without breaking hiding.

Shift viewpoints
- By role:
  - User/client: cares about contract, reliability, docs, examples.
  - Implementer: cares about invariants, algorithms, data layout.
  - Maintainer/ops: cares about observability, versioning, rollout safety.
  - Security: cares about least privilege, input contracts, side-channel exposure.
- By time horizon:
  - Short-term: speed of development, ease of use.
  - Long-term: evolvability, API stability, backward compatibility.
- By scale:
  - Micro (function signature) vs. macro (service boundary) changes what’s “essential.”
- By context:
  - Debugging or performance tuning may temporarily pierce the abstraction (with tooling) without rewriting clients.
  - Teaching/learning may choose a simpler abstraction first, then refine.

Practical moves
- Choose the level: What question must this representation answer? Anything not serving that is hidden.
- State the contract: Names, types, pre/postconditions, error cases, complexity guarantees.
- Prove it: Examples, property tests, types/specs, CI checks.
- Decouple deliberately: Depend on interfaces; invert dependencies where helpful.
- Watch for smells:
  - Repeated cross-layer knowledge, brittle tests tied to internals, frequent “just this one” backdoors, “primitive obsession,” excessive parameter lists.
- Evolve safely:
  - Additive changes preferred; deprecate with shims; semantic versioning; compatibility tests.
- Know when not to abstract:
  - One-off code, volatile domains, critical hot paths where overhead outweighs clarity, situations demanding full-fidelity control.
