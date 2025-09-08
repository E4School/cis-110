# Abstraction - Categories 1

Generated on 2025-09-03 13:17:57

Short answer: Abstraction is both a member of several broader categories and a category that contains many subtypes.

DSRP lens (brief)
- Distinctions: Abstraction is not mere omission; it is purposeful focus on essentials with hidden detail controlled by an interface.
- Systems (part–whole): The “abstraction” idea contains parts such as intent (simplify), mechanism (hide details, expose interface), and level (higher/lower).
- Relationships: Closely related to encapsulation, information hiding, modularity, generalization, modeling, and decomposition.
- Perspectives: Meaning shifts across disciplines (cognition, CS/software, math, systems engineering). Category placement depends on the perspective.

Categorization

1) As a member (parents it belongs to)
- Cognitive science/psychology: cognitive process; concept formation; generalization mechanism
- Computer science (theory): foundational CS concept; representation/modeling principle
- Software engineering: design principle; architecture principle; modularity principle
- Systems thinking: complexity-management strategy; black-boxing/level-of-detail strategy
- Mathematics/philosophy of science: idealization/abstraction process; modeling method

2) As a category (subcategories/kinds of abstraction)
- Data and type abstraction: abstract data types (ADTs), interfaces, modules, algebraic data types, type classes, traits
- Procedural/control abstraction: procedures/functions, higher-order functions, iterators, control structures, coroutines
- Interface/service abstraction: APIs, microservice contracts, RPC/REST/GraphQL interfaces
- Resource abstraction: files vs. disks, virtual memory, processes/threads, VMs/containers, cloud services
- Architectural abstraction: layers (UI/domain/infrastructure), hexagonal/ports-and-adapters, SOA, clean architecture boundaries
- Model/representation abstraction: maps and models, UML/ER diagrams, schemas, logical vs. physical data models, level-of-detail models
- Policy/mechanism abstraction: separating policy (what) from mechanism (how)
- Temporal/behavioral abstraction: state machines, protocols, transactions, idempotency contracts
- Security/privacy abstraction: capability models, access-control interfaces, differential privacy abstractions

3) Siblings (other members under common parents)
- Under cognitive process: categorization, chunking, attention, idealization, simplification
- Under CS foundational ideas: algorithms, decomposition, representation, automation, modeling
- Under software engineering principles: modularity, encapsulation, information hiding, separation of concerns, cohesion/coupling management, interface segregation, layering

Notes on closely related distinctions
- Encapsulation vs. abstraction: Encapsulation hides internal state/structure; abstraction hides unnecessary detail by exposing an interface that matches intent. They often co-occur but are distinct.
- Information hiding: A design principle that implements abstraction; sometimes treated as a subcategory or mechanism depending on perspective.

Verdict
- Abstraction is both:
  - A member of multiple higher-level categories (e.g., cognitive process; software engineering principle).
  - A category that contains many concrete forms (data/type, control/procedural, interface/service, resource, architectural, modeling, etc.).
Category membership and sibling sets vary by perspective (cognition, CS theory, software engineering, systems).


---

## 2025-09-03 13:20:28

Genus–differentia (what it is, by kind and distinguishing features)
- As a cognitive/process concept
  - Genus: Mental representational process.
  - Differentia: Selectively retains features invariant or salient for a purpose while omitting particulars, enabling reasoning at an appropriate level of detail.

- As an engineering/design principle (computing)
  - Genus: Software/system design principle.
  - Differentia: Specifies behavior via a stable interface or contract while hiding implementation details, so components interact through the specification rather than internal steps—controlling complexity, enabling reuse, and easing change.

Is it a category, a member, or both?
- Both.
  - Category: “Abstraction” as a type of process/principle and family of techniques (e.g., data abstraction, control abstraction).
  - Members: Particular abstractions (e.g., a specific API, a class interface, a virtualization layer, a map of Paris) are instances of that category.

Taxonomic placement and relations

Parents (supercategories)
- Cognitive/philosophical
  - Mental operation
  - Representational process
  - Concept-formation method
  - Idealization/modeling method
- Computing/engineering
  - Software engineering principle
  - Programming language and type-system concept
  - Systems/architectural design principle
  - Complexity management technique

Siblings (coordinated categories at the same level)
- Cognitive/philosophical
  - Generalization
  - Categorization
  - Idealization
  - Analogy
  - Modeling/simplification
- Computing/engineering
  - Encapsulation
  - Information hiding
  - Modularity
  - Decomposition/composition
  - Parameterization/generics
  - Polymorphism
  - Layering
  - Virtualization
  - Separation of concerns
  - Contracts/specifications

Subcategories (not exhaustive; many overlap)
- Cognitive/mathematical
  - Feature abstraction (focusing on salient attributes)
  - Structural abstraction (capturing relational form)
  - Mathematical abstraction (sets, functions, algebraic structures)
  - Levels of abstraction (coarse vs fine-grained modeling)
- Computing/software
  - Data abstraction (abstract data types; representation independence)
  - Type abstraction (interfaces, abstract classes, module signatures)
  - Control abstraction (procedures, higher-order functions, iterators)
  - Interface/API abstraction (service contracts, REST/GRPC interfaces)
  - Module/class abstraction (object/class interfaces, modules/packages)
  - Resource abstraction (files, sockets, threads, transactions)
  - Hardware/OS abstraction (HALs, virtual memory, syscalls)
  - Virtualization/containerization (VMs, containers as resource abstractions)
  - Architectural abstraction (layers, services, microservices boundaries)
  - Declarative abstraction (SQL, regex, query languages hiding execution)
  - Pattern-based abstractions (Facade, Adapter, Strategy)
  - Abstraction barriers (well-defined layers that prevent leaking implementation)

Notes
- Individual examples like “calling a function without seeing its code,” “using a map,” or “accessing a service through an API” are members (instances) of the Abstraction category.
- Some siblings are closely related: e.g., encapsulation and information hiding often co-occur with abstraction but are distinct emphases (mechanism vs interface focus).
