# Hardware: How We Got Physics To Do Math REALLY Fast

### Vocab
- Computer system (system)
- Hardware / Software boundary
- IPOS model (Input, Processing, Output, Storage)
- Input device / Output device
- Storage (persistent storage)
- Stored program concept
- Instruction / Opcode / Machine cycle (fetch–decode–execute)
- Program counter (PC)
- Control unit / ALU
- Register / Cache / Main memory (RAM)
- RAM (volatile) vs ROM / Firmware (non‑volatile)
- Boot / Bootstrap / Loader
- Device driver
- Bus (data / address / control)
- System on a Chip (SoC)
- Embedded system
- Architecture (desktop, mobile, embedded)
- Performance (throughput, latency)
- Energy efficiency / Power consumption / Thermal constraints
- Trade‑off
- Total Cost of Ownership (TCO)
- Data path / Data flow
- Throughput vs Latency
- Scalability (vertical, horizontal)
- Efficiency
- Bottleneck
- Trade‑off analysis
- Benchmark / Metric
- Optimization vs Premature optimization (principle)

### Relational Sentences
- A computer system coordinates hardware and software across the hardware/software boundary following the IPOS model where input devices feed data, processing transforms it, output devices present results, and storage keeps persistent data.
- The stored program concept lets instructions (opcodes) flow through the machine cycle (fetch–decode–execute) governed by the program counter (PC), control unit, and ALU along the data path (data flow).
- Registers, cache, and main memory (RAM) form a performance hierarchy distinct from ROM and firmware, balancing throughput, latency, energy efficiency, and thermal constraints.
- During boot a bootstrap loader initializes firmware, loads the OS via the loader, and activates each device driver that uses address, data, and control lines on the bus.
- A System on a Chip (SoC) integrates control unit, ALU, cache, and peripherals for embedded systems and mobile architecture variants, whereas desktop architecture may externalize more components.
- Designers analyze trade‑offs between performance, power consumption, and Total Cost of Ownership (TCO) when choosing storage technologies and architecture configurations.
- Throughput measures total work over time while latency measures per‑operation delay, and a bottleneck limits both.
- Scalability can be vertical (bigger node) or horizontal (more nodes) and is evaluated with benchmarks and metrics.
- Efficiency gains require trade‑off analysis to ensure improvements do not degrade maintainability or cost disproportionately.
- Optimization guided by metrics avoids premature optimization, which wastes effort without measurable bottleneck relief.

### Exam Questions
- **Explain the IPOS model of activities characteristics of computers**  Input (data entry), Processing (CPU executes instructions transforming data), Output (results presented to user/devices), Storage (persistent retention). It frames every program as a pipeline where correctness, performance, and usability hinge on clean inputs, efficient processing, appropriate output formatting, and reliable storage.
- **Describe the stored program concept and why it distinguishes computers from other simpler devices**  Instructions are stored in memory alongside data, allowing a general‑purpose machine to change behavior simply by loading different code (flexibility, reprogrammability). Simpler devices (e.g., hard‑wired calculators) have fixed logic; changing behavior requires hardware redesign.
- **Explain how a processor works**  The CPU repeatedly performs the fetch‑decode‑execute cycle: fetch instruction from memory (via program counter), decode (control unit interprets opcode, sets control signals), execute (ALU / other units perform operation), write back results, update PC. Modern CPUs add pipelining, caches, out‑of‑order execution, and branch prediction to increase throughput.
- **Explain the difference between RAM and ROM and why most computers have both**  RAM is volatile, fast read/write working memory; contents lost on power off. ROM (or flash/firmware) is non‑volatile, primarily read (or infrequently written) and holds bootstrap / firmware code needed before RAM and storage subsystems initialize. Together they enable reliable startup plus flexible runtime execution.
- **Explain what I/O devices are and why they are important to computing**  Peripherals that allow interaction with the external world (input: keyboard, sensors; output: displays, printers). They convert between human/physical signals and digital data, enabling practical usefulness of computation.
- **Analyze how the components of a computer system work together to execute a simple program**  User initiates program (stored on persistent storage) → OS loader copies executable segments into RAM → CPU fetches instructions using addresses resolved via MMU/cache hierarchy → instructions request data (caches / RAM / storage via I/O bus) → results buffered and eventually output via drivers to devices; OS schedules CPU time and manages resources throughout.
- **Compare and contrast different computer architectures (desktop, mobile, embedded systems)**  Desktop: high performance, modular, higher power draw. Mobile: energy efficiency, integrated system‑on‑chip, thermal constraints, wireless focus. Embedded: purpose‑specific, minimal UI, real‑time constraints, long lifecycle, often hardened. Trade‑offs revolve around performance vs power vs specialization.
- **Trace the flow of data through a computer system from input to output**  Input device generates signals → driver interprets and places data into OS buffers → user process reads data (system call) → CPU processes, manipulating in registers and RAM (caches accelerate) → results passed to output subsystem (system call) → driver formats & sends to device → device renders (screen, printer, network packet).
- **Evaluate the trade-offs between performance, cost, and energy efficiency in computer design**  Increasing cores/clocks boosts performance but raises power/thermal design and cost. Energy efficiency improves battery life / operating cost but may reduce peak performance. Optimal design selects sufficient performance headroom while minimizing total cost of ownership (purchase + energy + cooling) for target workload.
