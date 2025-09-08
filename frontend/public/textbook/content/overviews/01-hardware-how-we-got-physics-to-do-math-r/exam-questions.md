# Hardware Exam Questions

Practice questions with detailed answers to test your understanding.

## Question 1: IPOS Model
**Explain the IPOS model of activities characteristic of computers**

**Answer:** Input (data entry), Processing (CPU executes instructions transforming data), Output (results presented to user/devices), Storage (persistent retention). It frames every program as a pipeline where correctness, performance, and usability hinge on clean inputs, efficient processing, appropriate output formatting, and reliable storage.

## Question 2: Stored Program Concept
**Describe the stored program concept and why it distinguishes computers from other simpler devices**

**Answer:** Instructions are stored in memory alongside data, allowing a general‑purpose machine to change behavior simply by loading different code (flexibility, reprogrammability). Simpler devices (e.g., hard‑wired calculators) have fixed logic; changing behavior requires hardware redesign.

## Question 3: Processor Operation
**Explain how a processor works**

**Answer:** The CPU repeatedly performs the fetch‑decode‑execute cycle: fetch instruction from memory (via program counter), decode (control unit interprets opcode, sets control signals), execute (ALU / other units perform operation), write back results, update PC. Modern CPUs add pipelining, caches, out‑of‑order execution, and branch prediction to increase throughput.

## Question 4: Memory Types
**Explain the difference between RAM and ROM and why most computers have both**

**Answer:** RAM is volatile, fast read/write working memory; contents lost on power off. ROM (or flash/firmware) is non‑volatile, primarily read (or infrequently written) and holds bootstrap / firmware code needed before RAM and storage subsystems initialize. Together they enable reliable startup plus flexible runtime execution.

## Question 5: I/O Devices
**Explain what I/O devices are and why they are important to computing**

**Answer:** Peripherals that allow interaction with the external world (input: keyboard, sensors; output: displays, printers). They convert between human/physical signals and digital data, enabling practical usefulness of computation.

## Question 6: System Integration
**Analyze how the components of a computer system work together to execute a simple program**

**Answer:** User initiates program (stored on persistent storage) → OS loader copies executable segments into RAM → CPU fetches instructions using addresses resolved via MMU/cache hierarchy → instructions request data (caches / RAM / storage via I/O bus) → results buffered and eventually output via drivers to devices; OS schedules CPU time and manages resources throughout.

## Question 7: Architecture Comparison
**Compare and contrast different computer architectures (desktop, mobile, embedded systems)**

**Answer:** Desktop: high performance, modular, higher power draw. Mobile: energy efficiency, integrated system‑on‑chip, thermal constraints, wireless focus. Embedded: purpose‑specific, minimal UI, real‑time constraints, long lifecycle, often hardened. Trade‑offs revolve around performance vs power vs specialization.

## Question 8: Data Flow
**Trace the flow of data through a computer system from input to output**

**Answer:** Input device generates signals → driver interprets and places data into OS buffers → user process reads data (system call) → CPU processes, manipulating in registers and RAM (caches accelerate) → results passed to output subsystem (system call) → driver formats & sends to device → device renders (screen, printer, network packet).

## Question 9: Design Trade-offs
**Evaluate the trade-offs between performance, cost, and energy efficiency in computer design**

**Answer:** Increasing cores/clocks boosts performance but raises power/thermal design and cost. Energy efficiency improves battery life / operating cost but may reduce peak performance. Optimal design selects sufficient performance headroom while minimizing total cost of ownership (purchase + energy + cooling) for target workload.

[← Back to Chapter](index)
