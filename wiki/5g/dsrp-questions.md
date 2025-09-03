# 5G - Dsrp Questions

## 2025-09-03 11:46:20

## Is it a System?
- Classification: 5G can be understood as:
  - A system: It comprises interacting technical, regulatory, economic, and social components organized to deliver mobile broadband and low-latency connectivity.
  - A part of a system: It is a generational layer within the larger telecommunications ecosystem and the broader cyber-physical-digital infrastructure.
  - A set of relationships between systems: It coordinates spectrum, devices, radio access networks, backhaul, clouds, edge, and application layers via standardized interfaces.
  - A boundary between systems: It functions as the interface between user equipment and the internet/compute fabric, and between radio and core networks.
  - A cognitive tool: As a category (“5G”) it frames expectations about speed, latency, and capabilities, guiding policy, investment, and design decisions.
  - Something else related to systems: A sociotechnical paradigm that reorganizes value chains (e.g., via network slicing and edge compute).

## Distinctions
- What 5G is (as a system):
  - The fifth-generation mobile network standard and infrastructure (3GPP Releases 15–18 and beyond) that delivers enhanced mobile broadband (eMBB), ultra-reliable low latency communications (URLLC), and massive machine-type communications (mMTC).
  - A layered, interoperable stack: user equipment (UE), radio access network (RAN, including macro and small cells), transport/backhaul, 5G core (service-based architecture), spectrum assets (low/mid/high bands), orchestration and slicing, security controls, and associated operational processes.
  - A performance envelope: higher throughput, lower latency, higher density, differentiated QoS, and geographic variability due to propagation characteristics.

- What 5G is not (outside the boundary):
  - It is not “the internet” itself, nor application-layer services (e.g., Netflix, Fortnite, Teams) though it enables them.
  - It is not Wi‑Fi or wired broadband, though it interworks with both.
  - It is not a single frequency band or a single technology (e.g., mmWave only); it encompasses a spectrum portfolio and multiple radio techniques.
  - It is not merely marketing speed labels; it is a standards-based architecture with measurable KPIs and compliance requirements.
  - It is not guaranteed uniform performance; coverage, capacity, and latency vary by deployment, spectrum, and backhaul.

## Systems
- Does 5G have parts? Yes. Examples:
  - Physical layer: antennas (massive MIMO, beamforming), radios, small cells, macro sites, fronthaul/backhaul (fiber/microwave).
  - Spectrum: low-band (coverage), mid-band (capacity/coverage balance), high-band/mmWave (peak throughput, short range).
  - Protocol stack: NR (New Radio), numerologies, scheduling, HARQ, QoS flows, control/user plane split.
  - Core network: service-based architecture (AMF, SMF, UPF, PCF, NRF, etc.), slicing, policy, charging, authentication.
  - Orchestration and automation: SDN/NFV, CI/CD, telemetry, closed-loop assurance.
  - Security: SIM/eSIM, 5G-AKA, slice isolation, signaling security, supply-chain controls.
  - Operational ecosystem: spectrum licensing, site permitting, energy systems, maintenance, and SLAs.

- Can you think of 5G as a part?
  - Of national digital infrastructure and critical infrastructure.
  - Of an end-to-end compute continuum (device edge → RAN edge → regional cloud → core cloud).
  - Of Industry 4.0 control systems and smart city platforms.
  - Of a multi-access connectivity fabric alongside Wi‑Fi 6/7, fiber, and satellite.

## Relationships
- Other systems 5G is related to:
  - Cloud and edge computing: MEC/edge nodes host latency-sensitive workloads; cloud provides control, scaling, and data services.
  - Application ecosystems: AR/VR, telemedicine, autonomous systems, smart grids, logistics, gaming; these depend on 5G’s QoS/URLLC capabilities.
  - Spectrum management and regulation: national policies shape deployments and interference environments.
  - Device ecosystems: chipsets, OS stacks, RF front ends; device capabilities shape achievable performance.
  - Power and physical infrastructure: energy availability and site access govern density and resilience.
  - Security and trust frameworks: identity, encryption, lawful intercept, supply chain assurance.
  - Alternative access systems: Wi‑Fi, satellite NTN, fixed wireless, fiber; 5G interworks and competes/cooperates with them.

- Can 5G be seen as a relationship between systems?
  - Yes. It is the coordination mechanism between mobile devices and the global compute/network fabric, translating spectrum, radio resources, and policies into end-to-end service guarantees.
  - Network slicing is itself a set of relationships mapping tenant/application requirements to isolated logical networks across shared physical assets.
  - 5G mediates relationships between physical mobility patterns and resource allocation (e.g., handover, beam management, scheduler decisions).

## Perspectives
- Questions from the perspective of 5G as a system:
  - How do we optimize the trade-offs among spectrum bands to meet heterogeneous SLAs (throughput, latency, reliability) under mobility and interference?
  - What are the resilience modes under power constraints, backhaul loss, or disasters; how do slices degrade gracefully?
  - How do we assure slice isolation and low-latency paths end-to-end when workloads span RAN edge and public cloud?
  - What governance is needed to balance lawful intercept, privacy, and zero-trust principles in a multi-tenant architecture?
  - How does energy efficiency scale with densification, and what are the lifecycle carbon implications?

- Perspectives from other systems:
  - Application developer: What APIs/QoS primitives (network exposure functions) can I rely on to guarantee latency/jitter for real-time apps?
  - Cloud/edge operator: How do I place workloads to meet URLLC while maximizing utilization and minimizing egress costs?
  - Regulator: How do allocation and sharing models (licensed, unlicensed, CBRS) affect competition, rural coverage, and security?
  - Enterprise/CIO: Should I build a private 5G network or use a slice from an MNO? What are TCO, security posture, and integration costs?
  - Security analyst: What are the new attack surfaces (virtualized core, API exposure, supply chain) and controls for slice isolation?
  - Urban planner/society: How does densification affect public space, equity of access, and environmental footprint?
  - Competing access tech (Wi‑Fi): Where do Wi‑Fi 7 and 5G complement vs. substitute each other in indoor/enterprise scenarios?
  - End user: What practical differences will I experience vs. 4G (latency-sensitive apps, consistency indoors, battery life)?

Not applicable: None.
