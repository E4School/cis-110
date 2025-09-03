
Goal, make scripts that automate the mass production of good pedagogical content related to DSRP and parameterized by the vocabulary words.  The point is to create reading material, and also to create textual relationships that can be used to enhance the wiki.  Also, final exam questions will be generated from the Cabrera-style analysis, serving to test students' systemic understanding and their systems thinking skills. 

Step 1: Concept -> DSRP content

* Currently Trying: python scripts/enhance-wiki-definitions.py --model gpt-5 --custom-prompt "Using Cabrera's approach to systems thinking, please model the steps for thinking about {term} that a beginning student in a foundational computer information systems course might benefit from seeing." --output-file cabrera-dialectic-1 --test --yes   

* Works okay: python scripts/enhance-wiki-definitions.py --model gpt-5 --custom-prompt "Using the DSRP thinking framework, generate for the term '{term}' (definition: {current_definition}): 1) Distinctions: What is {term}? What is not {term}? 2) Systems: Does {term} have parts? Can you think of {term} as a part? 3) Relationships: What kinds of things is {term} related to? Can you think of {term} as a relationship? 4) Perspectives: From the perspective of {term}, what questions arise? Can you think about {term} different from perspectives (if so list some)? Note that not every all of these questions will be answerable for all things; say "Not applicable" if the question is not relevant. Output in Markdown with sections: Distinctions, Systems, Relationships, Perspectives. Answer like a highly educated, deep thinker, well-versed in subject matters that are technical, scientific, and philosophical." --output-file dsrp-questions --test --yes
  - Criticism: Produces more of a checklist and less of a model for thinking



---

Key socratic questions:

* Distinctions
  - What is __________?
  - What is not __________?
* Systems
  - Does _________ have parts?
  - Can you think of _________ as a part?
* Relationships
  - Is ________ related to __________?
  - Can you think of ________ as a relationship?
* Perspectives
  - From the perspective of __________, [insert question]?
  - Can you think about ____________ from a different perspective?