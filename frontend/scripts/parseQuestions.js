import fs from 'fs';
import path from 'path';

// Parse markdown files and extract exam questions
function parseExamQuestions(contentDir) {
  const questions = [];
  const files = fs.readdirSync(contentDir).filter(f => f.endsWith('.md'));
  
  files.forEach(file => {
    const filePath = path.join(contentDir, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    
    // Extract chapter number and title from filename
    const match = file.match(/(\d+)-(.+)\.md/);
    if (!match) return;
    
    const chapterNumber = parseInt(match[1]);
    const chapterTitle = match[2].replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    
    // Find the "### Exam Questions" section
    const examSectionMatch = content.match(/### Exam Questions([\s\S]*?)(?=\n### |$)/);
    if (!examSectionMatch) return;
    
    const examSection = examSectionMatch[1];
    
    // Parse questions (format: - **Question** Answer)
    const questionMatches = examSection.matchAll(/- \*\*(.*?)\*\*\s+(.*?)(?=\n- \*\*|$)/gs);
    
    for (const questionMatch of questionMatches) {
      const question = questionMatch[1].trim();
      const answer = questionMatch[2].trim();
      
      questions.push({
        id: `ch${chapterNumber}-${questions.filter(q => q.chapter === chapterNumber).length + 1}`,
        chapter: chapterNumber,
        chapterTitle,
        question,
        answer,
        type: 'short-answer'
      });
    }
  });
  
  return questions;
}

// Generate the questions JSON file
const contentDir = path.join(process.cwd(), '..', 'content');
const questions = parseExamQuestions(contentDir);

// Write to public directory so it can be fetched by the React app
const outputPath = path.join(process.cwd(), 'public', 'questions.json');
fs.writeFileSync(outputPath, JSON.stringify(questions, null, 2));

console.log(`Extracted ${questions.length} questions from ${[...new Set(questions.map(q => q.chapter))].length} chapters`);
console.log('Questions saved to public/questions.json');
