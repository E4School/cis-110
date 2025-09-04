# Web Fundamentals: How Billions of Systems Talk To Each Other

### Vocab
- Internet vs Web
- Client / Server
- HTTP / HTTPS
- URL (scheme, host/domain, path, query, fragment)
- Request / Response
- Status code (general idea)
- Browser (cache, history, privacy modes)
- Hyperlink
- HTML / DOM
- Tag / Element / Attribute
- CSS (selector, rule, declaration)
- JavaScript (script, event, asynchronous / fetch)
- Cookie (session, tracking)
- Caching (browser/server)
- Content Delivery Network (CDN)
- Cloud computing (scalability, elasticity)
- Accessibility (a11y) / ARIA roles
- Responsive design
- Cross‑Site Scripting (XSS) (basic awareness)
- CORS / CSP (basic awareness)

### Relational Sentences
- The Internet provides underlying network infrastructure while the Web uses HTTP or HTTPS for client/server communication defined by request and response exchanges with status codes.
- A URL encodes scheme, host (domain), path, query, and fragment so a browser can fetch hyperlinked resources and construct or update the DOM from HTML tags, elements, and attributes.
- CSS selectors apply rules (declarations) to elements while JavaScript scripts attach event handlers and perform asynchronous fetch calls to update the DOM dynamically.
- Cookies persist session identifiers or tracking data; browser and server caching plus a Content Delivery Network (CDN) reduce latency by reusing cached content.
- Cloud computing offers scalability and elasticity so web applications can adapt responsive design layouts while preserving accessibility (a11y) with ARIA roles.
- Security measures like CSP and CORS restrict resource origins, mitigating Cross‑Site Scripting (XSS) injection vectors.
- **Explain how the Web works**  Clients (browsers) send HTTP(S) requests to servers using URLs; servers process (often via application logic + databases) and return responses (HTML, JSON, media). Hyperlinks interconnect documents forming a navigable graph.
- **Discuss the integration of three technologies that are foundational for the Web**  HTML structures content; CSS controls presentation; JavaScript enables dynamic behavior and client‑side logic. Together they separate concerns—structure, style, interactivity—allowing iterative and maintainable development.
- **Explain what the four parts of a URL are**  Scheme (protocol, e.g., https), host (domain), path (resource location), and optional query (key=value parameters) + fragment (in‑page anchor). (Some models treat port or fragment as additional components.)
- **Explain what a hyperlink is**  An element (usually an <a> tag) referencing another resource by URL enabling non‑linear navigation.
- **Explain the role of a Web browser with respect to caching, history, and privacy**  Browser caches resources (improves performance), maintains history (navigation convenience), and mediates privacy (cookie storage, tracking prevention, sandboxing). User settings balance speed versus confidentiality.
- **Explain what HTTP and HTTPS are**  Application‑layer request/response protocols; HTTPS layers HTTP over TLS to encrypt and authenticate, protecting confidentiality and integrity.
- **Explain what a Web cookie is**  Small key/value data stored client‑side by the browser, sent with subsequent requests to same domain—used for sessions, preferences, tracking.
- **Explain what HTML is**  Markup language defining semantic structure of web documents (headings, paragraphs, media, forms). Parsed into the DOM.
- **Identify 5 common HTML tags and explain what they do**  <h1>-<h6>: headings hierarchy; <p>: paragraph; <a>: hyperlink; <img>: embeds image; <div>: generic block container; <form>: user input submission context.
- **Explain what CSS is**  Stylesheet language that selects DOM elements and applies presentation rules (layout, color, typography, responsive adjustments).
- **Explain the role of JavaScript in a Web page**  Enables dynamic DOM manipulation, event handling, asynchronous network calls (fetch), client logic, and integration with APIs and storage.
- **Design a simple webpage that demonstrates understanding of HTML structure and CSS styling**  (Example) HTML skeleton with semantic header/main/footer; CSS for responsive layout using flexbox; styled navigation; accessible alt text. (*Omitted source for brevity—can be added on request.*)
- **Evaluate the accessibility and usability of web interfaces**  Check semantic markup, ARIA where needed, color contrast, keyboard navigation, responsive scaling, meaningful alt text, and consistent feedback; usability aligns with predictable navigation and minimized cognitive load.
