# Operating Systems: Programs That Run Programs

### Vocab
- Operating System (OS)
- Process / Thread
- Multitasking / Multiprocessing / Multithreading
- Scheduling
- Concurrency vs Parallelism
- Memory management
- Interrupt / Interrupt handler
- System call / API
- Permissions / Access control
- Configuration / Environment variables

### Relational Sentences
- An operating system (OS) manages processes and their threads to enable multitasking, multiprocessing, and multithreading through scheduling algorithms.
- Concurrency allows multiple tasks to make progress while parallelism executes threads simultaneously on multiple cores under OS scheduling.
- Memory management allocates and protects each process’s address space while enforcing permissions and access control models.
- System calls expose an API boundary where user processes request OS services, often triggered or influenced by configuration and environment variables.
- Hardware devices raise interrupts that invoke interrupt handlers so the OS can preempt processes and maintain responsive multitasking.
- **Explain what a device driver is**  Low‑level software that provides a standardized interface between OS subsystems and specific hardware, translating generic OS calls into device‑specific commands and handling interrupts/events.
- **Explain the role of the operating system**  Abstracts hardware, schedules processes/threads, manages memory, filesystems, I/O, security (auth, permissions), networking, and provides APIs.
- **Explain the difference between multitasking, multiprocessing, and multithreading**  Multitasking: OS interleaves processes (logical concurrency). Multiprocessing: multiple physical cores/CPUs execute tasks truly in parallel. Multithreading: multiple threads within a process sharing memory space for finer concurrency.
- **Analyze how the components of a computer system work together to execute a simple program**  User initiates program (stored on persistent storage) → OS loader copies executable segments into RAM → CPU fetches instructions using addresses resolved via MMU/cache hierarchy → instructions request data (caches / RAM / storage via I/O bus) → results buffered and eventually output via drivers to devices; OS schedules CPU time and manages resources throughout.
