
Goal, make scripts that automate the mass production of good pedagogical content (related to DSRP and parameterized by the vocabulary words?).  The point is to kinda automatically:

1) create reading material, 
2) create textual relationships that can be used to form a wiki
  - Relationship graph analysis can, I hope, be used to generate meaningful stories: E.g. connections between topics (more reading material)
  - Efficiently "cover" the material with the minimal set of lessons
3) generate exam questions - drawn from or generated from reading material
  - Kinda have these (via the learning goals), but I might want to add more.  And future courses might have fuzzier goals that aren't straightforwardly convertible to assessments


### Learning Goals -> Exam Questions and Answers (Final Exam Delivery system)

* TODO: Finish the exam delivery UI

* DONE? Questions might need to be added after additional supporting material has been added.  And more questions might actually help...

### Questions and Answers -> Concepts (Vocabulary)

* DONE?  Might iterate once more, after additional content has been created.

### Concepts -> Relational Sentences / Diagrams / Stories / Mnemonics
 
* TODO: 
  - create wiki pages
  - create course content pages
  - explain it like I'm 5 answers for each question
  -  

### Relational Sentences / Diagrams / etc. -> Mnemonic Material / Wiki / Videos / Learning Processes and Systems


---

Other ideas...

### Concept -> DSRP content

Use AI to generate DSRP content for each vocabulary word.

* Best so far:
  - python scripts/enhance-wiki-definitions.py --model gpt-5 --custom-prompt "Using Cabrera's approach to systems thinking, please model the steps for thinking about the term '{term}' ({current_definition}).  Do not mention Cabrera explicitly nor the fact that you are modeling steps for thinking.  Just produce some Cabrera-style DSRP thinking about this topic without labeling it as such." --output-file dsrp-1 --test --yes   
  - Assessment: It's not bad.

* Older version: 
  - python scripts/enhance-wiki-definitions.py --model gpt-5 --custom-prompt "Using the DSRP thinking framework, generate for the term '{term}' (definition: {current_definition}): 1) Distinctions: What is {term}? What is not {term}? 2) Systems: Does {term} have parts? Can you think of {term} as a part? 3) Relationships: What kinds of things is {term} related to? Can you think of {term} as a relationship? 4) Perspectives: From the perspective of {term}, what questions arise? Can you think about {term} different from perspectives (if so list some)? Note that not every all of these questions will be answerable for all things; say "Not applicable" if the question is not relevant. Output in Markdown with sections: Distinctions, Systems, Relationships, Perspectives. Answer like a highly educated, deep thinker, well-versed in subject matters that are technical, scientific, and philosophical." --output-file dsrp-questions --test --yes
  - Criticism: Produces more of a checklist and less of a model for thinking

### Concept -> Category analysis

python scripts/enhance-wiki-definitions.py --model gpt-5 --custom-prompt "Consider this term: '{term}' ({current_definition}).  Using DSRP, analyze the term {term} ({current_definition}) with a focus on its categorization: is it a category, a member of a category, or both? List parent, sibling, and subcategories as appropriate." --output-file categories-1 --test --yes   

python scripts/enhance-wiki-definitions.py --model gpt-5 --custom-prompt "Give a taxonomic / genus–differentia analysis of {term} ({current_definition}). State if it is a category, a member of a category, or both, and list parent, sibling, and subcategories." --output-file categories-1 --test --yes   

### Concept -> Linguistics and Examples

python scripts/enhance-wiki-definitions.py --model gpt-5 --custom-prompt "Give an OED style analysis of {term} ({current_definition}), covering part of speech, senses, historical development, stakeholder/contextual uses, and example sentences." --output-file expanded-definition --test --yes   

### Concept -> Related concepts

python scripts/enhance-wiki-definitions.py --model gpt-5 --custom-prompt "For the term {term} ({current_definition}), please select the top ten most related concepts from this list: {concept_list}" --output-file related-concepts --test --yes   

### Concept -> Related Concept Sentences  (Depends on Related Concepts)

python scripts/enhance-wiki-definitions.py --model gpt-5 --custom-prompt "For the term {term} ({current_definition}), please generate sentences that explain the relationship between it and the related terms in this list: {FILE:./related-concepts.md}" --output-file related-concept-sentences --test --yes   

### Concept -> Educational justifications


### Concept -> Exam Questions


### Concept Graph -> Clusters / Lists / Groups


### Clusters / Lists / Groups -> Stories / More DSRP / Etc.


### Stories / More DSRP / Etc. -> Efficient Sequence of Reading Material + Exam Questions



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