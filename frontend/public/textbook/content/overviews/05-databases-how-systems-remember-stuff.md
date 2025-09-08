# Databases: How Systems Remember Stuff

### Vocab

- Database / Table / Row (Record) / Column (Field)
- Schema
- Primary key / Foreign key (FK) (implied; relationships)
- Relationship (one‑to‑many, many‑to‑many)
- Normalization (1NF, 2NF, 3NF)
- SQL (SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER)
- Query / Query optimization (intro)
- Index
- Transaction / ACID (conceptual awareness)
- Big data (volume, velocity, variety)
- NoSQL (document, key‑value, wide‑column, graph)
- Denormalization
- Data privacy / Anonymization / Pseudonymization
- Data retention policy
- ORM (Object‑Relational Mapping) (intro)

### Relational Sentences
- A database organizes data into tables whose rows (records) and columns (fields) conform to a schema expressing relationships via primary and foreign keys.
- Relationship types (one‑to‑many, many‑to‑many) influence normalization choices (1NF, 2NF, 3NF) to reduce redundancy.
- SQL statements (SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER) manipulate data while queries benefit from indexes during query optimization.
- Transactions enforce ACID properties so multi‑statement operations remain consistent and isolated even under concurrency.
- Big data characteristics (volume, velocity, variety) motivate NoSQL models (document, key‑value, wide‑column, graph) or selective denormalization for performance.
- Data privacy goals can be supported through anonymization or pseudonymization guided by a data retention policy.
- An ORM maps objects to tables, abstracting SQL while still requiring awareness of indexing and normalization impacts.

### Exam Questions
- **Define basic database terminology, such as fields, records, rows, columns, and tables**  Table: structured collection; row/record: single entity instance; column/field: attribute; schema: structural definition.
- **Explain what a relational database is**  A structured collection organizing data into tables with defined relationships enforced via keys and set‑based query logic (relational algebra).
- **Explain the process of normalization**  Decomposing tables to reduce redundancy and anomalies (1NF atomic values, 2NF remove partial dependencies, 3NF remove transitive dependencies) balancing with performance.
- **Explain what SQL is and identify common SQL commands and give a concrete example**  Declarative language for defining/manipulating data. Core: SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER. Example: `SELECT name, price FROM products WHERE price > 100 ORDER BY price DESC;`.
- **Explain what big data is**  Datasets of high volume, velocity, or variety that exceed traditional relational processing capabilities; require distributed storage/compute (Hadoop, Spark) and specialized tooling.
- **Explain what NoSQL is**  Non‑relational data stores (document, key‑value, wide‑column, graph) optimizing for horizontal scalability, flexible schemas, or specific access patterns.
- **Design a simple database schema for a real-world scenario**  Example bookstore: Tables: Authors(id PK, name), Books(id PK, title, author_id FK, price), Orders(id PK, customer_id FK, order_date), OrderItems(order_id FK, book_id FK, qty). Index frequent lookups (Books.title, Orders.order_date).
- **Write basic SQL queries to retrieve and manipulate data**  Retrieval: `SELECT title FROM Books WHERE price < 20;` Manipulation: `UPDATE Books SET price = price * 0.9 WHERE author_id = 7;` Insertion: `INSERT INTO Authors(name) VALUES ('Ada Lovelace');`
- **Analyze the trade-offs between different database types for specific applications**  Relational: strong consistency/ACID; Document: flexible schema, denormalization for speed; Key‑value: ultra‑fast simple lookups; Graph: relationship traversal efficiency; Wide‑column: high write scalability for large sparse datasets.
- **Explain how databases integrate with web applications and business systems**  App layer uses drivers/ORM to execute SQL/queries, caches results, enforces business rules; transactions ensure consistency; APIs or message queues connect downstream analytics, reporting, and services.
