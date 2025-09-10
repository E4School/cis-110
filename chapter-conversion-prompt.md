# Chapter Conversion Prompt: Making Chapters Isomorphic to Chapter 1

Use this prompt to convert any textbook chapter to match Chapter 1's comprehensive interactive structure.

## Task Overview
Convert the specified chapter to have the same structure, interactivity, and educational progression as Chapter 1, including React component integration, vocabulary tooltips, and multi-level educational content.

## Directory Structure Setup

1. **Ensure chapter directory exists**: `content/overviews/0X-chapter-name/`
2. **Create questions subdirectory**: `content/overviews/0X-chapter-name/questions/`

## Core Files to Create/Update

### 1. Navigation File (`index.md`)
```markdown
# Chapter Title: Descriptive Subtitle

[Video coming soon]

## Chapter Contents

- [**Big Picture Concepts**](concepts) - Start here
- [**Exam Questions**](exam-questions) - Practice questions and detailed answers
- [**Vocabulary**](vocabulary) - Giant list of related terms and definitions (use this only for reference)

## Recommended Videos

[Chapter-related videos to be added]
```

### 2. Component Integration Files

**`exam-questions.md`**:
```markdown
# Exam Questions

{{ExamQuestions:exam-questions.yml}}
```

**`concepts.md`**:
```markdown
# Chapter Name - Big Picture Concepts

This section presents key concepts through an interactive concept map.

{{ConceptMap:concept-map.yml}}
```

**`vocabulary.md`**:
```markdown
# Chapter Name - Vocabulary

This section contains vocabulary terms from all chapter topics.

{{VocabList:exam-questions.yml}}
```

### 3. Question Infrastructure (`exam-questions.yml`)
```yaml
questions:
  - "questions/q01.yml"
  - "questions/q02.yml"
  - "questions/q03.yml"
  - "questions/q04.yml"
  # Add more as needed (typically 4-6 questions per chapter)
```

### 4. Concept Map (`concept-map.yml`)
**CRITICAL**: Must use `concept_map` as root key, not `concepts`
```yaml
concept_map:
  - category: "Category Name"
    concepts:
      - name: "Concept Name"
        exam_questions:
          - "questions/q01.yml"
          - "questions/q02.yml"
      - name: "Another Concept"
        exam_questions:
          - "questions/q03.yml"
  - category: "Another Category"
    concepts:
      - name: "Different Concept"
        exam_questions:
          - "questions/q04.yml"
```

## Individual Question File Structure (`questions/qXX.yml`)

Each question file MUST contain all these fields:

```yaml
id: [unique number]
question: "[Question text]"
answer: "[Graduate-level comprehensive answer with technical depth]"
vocab_answer: 
  - word: "term"
    definition: "definition for graduate level"
answer_kindergarten: "[Simple analogy-based explanation]"
vocab_kindergarten: 
  - word: "term"
    definition: "simple definition for kindergarten"
answer_3rd_grade: "[Concrete examples with basic concepts]"
vocab_3rd_grade: 
  - word: "term"
    definition: "definition for 3rd grade level"
answer_7th_grade: "[More technical with proper terminology]"
vocab_7th_grade: 
  - word: "term"
    definition: "definition for 7th grade level"
answer_high_school: "[Advanced concepts and relationships]"
vocab_high_school: 
  - word: "term"
    definition: "definition for high school level"
answer_undergraduate: "[Highly technical with advanced terminology]"
vocab_undergraduate: 
  - word: "term"
    definition: "definition for undergraduate level"
topics: ["topic1", "topic2", "topic3"]
```

## Content Requirements

### Question Coverage
- **4-6 comprehensive questions** covering all major chapter topics
- Questions should build understanding progressively
- Cover both conceptual understanding and practical applications

### Educational Progression
Each question must have 6 levels:
1. **Kindergarten**: Simple analogies, everyday objects
2. **3rd Grade**: Concrete examples, basic vocabulary
3. **7th Grade**: Proper terminology, foundational concepts
4. **High School**: Advanced relationships, technical depth
5. **Undergraduate**: Professional terminology, complex interactions
6. **Graduate** (main answer): Comprehensive technical explanation

### Vocabulary Standards
- **300-400+ vocabulary terms per question**
- Progressive complexity across educational levels
- Terms should support tooltip functionality
- Definitions tailored to each educational level
- Include both domain-specific and supporting vocabulary

### Concept Map Organization
- **4-6 logical categories** organizing chapter concepts
- Each concept linked to relevant question files
- Categories should reflect natural topic groupings
- Concepts should cover all major chapter themes

## Quality Checklist

### File Structure ✅
- [ ] `index.md` (navigation)
- [ ] `exam-questions.md` (component integration)
- [ ] `exam-questions.yml` (question references)
- [ ] `concepts.md` (component integration)
- [ ] `concept-map.yml` (concept organization)
- [ ] `vocabulary.md` (component integration)
- [ ] `questions/q01.yml` through `questions/qXX.yml`

### Content Quality ✅
- [ ] All 6 educational levels per question
- [ ] 300+ vocabulary terms per question
- [ ] Progressive complexity maintained
- [ ] Technical accuracy at all levels
- [ ] Consistent YAML formatting
- [ ] Proper concept-question linking

### Interactive Features ✅
- [ ] Vocabulary tooltip integration
- [ ] React component references correct
- [ ] Concept map uses correct format (`concept_map` root key)
- [ ] Educational level progression logical
- [ ] Cross-references between concepts and questions

## Common Pitfalls to Avoid

1. **Concept Map Format**: Use `concept_map` as root key, not `concepts`
2. **Component References**: Include `.yml` file extensions in component calls
3. **Vocabulary Progression**: Ensure definitions increase in complexity across levels
4. **YAML Structure**: Follow exact format for all required fields
5. **Educational Levels**: Don't skip any of the 6 required levels
6. **File Naming**: Use consistent `qXX.yml` naming pattern

## Example Conversion Process

1. **Analyze existing chapter** - identify main topics and current questions
2. **Plan 4-6 comprehensive questions** covering all topics
3. **Create directory structure** and navigation files
4. **Develop each question** with full 6-level progression
5. **Build concept map** linking concepts to questions
6. **Create component integration files**
7. **Test all components** load correctly
8. **Verify vocabulary tooltips** function properly

## Success Criteria

The converted chapter should have:
- Same interactive features as Chapter 1
- Consistent educational progression
- Rich vocabulary supporting tooltips
- Logical concept organization
- Comprehensive topic coverage
- Professional technical depth
- Engaging analogies for younger levels

This structure creates a consistent, interactive learning experience across all textbook chapters while maintaining educational rigor at every level.
