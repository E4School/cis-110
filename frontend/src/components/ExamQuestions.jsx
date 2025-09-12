import React, { useState, useEffect } from 'react';
import * as yaml from 'js-yaml';

import './ExamQuestions.css';

// Additional answer levels with their display names (reversed order - kindergarten first)
const ADDITIONAL_ANSWER_LEVELS = [
  { key: 'answer_kindergarten', label: 'Kindergarten Level' },

    // Note that the display labels are different from the keys.
    // For example, 'answer_3rd_grade' is displayed as '7th Grade Level'.
    // That's by design.  Let's keep it that way, as they keys represent
    // what I asked AI ("Give a 7th Grade Level explanation") vs what I think
    // an actual 7th Grade Level explanation should be. 
    // ~Stephen
  { key: 'answer_3rd_grade', label: '7th Grade Level' },
  { key: 'answer_7th_grade', label: 'High School Level' },
  { key: 'answer_high_school', label: 'Undergraduate Level' },
  { key: 'answer_undergraduate', label: 'Postgraduate Level' }
];

// Function to process text and highlight vocabulary words with tooltips
const processAnswerText = (text, vocabList) => {
  if (!text || !vocabList || vocabList.length === 0) {
    return text;
  }

  // Create a map of vocabulary words to their definitions
  const vocabItems = vocabList.map(item => ({
    word: item.word,
    definition: item.definition,
    regex: new RegExp(`\\b${item.word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi')
  }));

  // Sort by word length (longest first) to handle multi-word terms properly
  vocabItems.sort((a, b) => b.word.length - a.word.length);

  let processedText = text;
  const replacements = [];
  let replacementIndex = 0;

  // Find all vocabulary word matches
  vocabItems.forEach(({ word, definition, regex }) => {
    let match;
    while ((match = regex.exec(processedText)) !== null) {
      const placeholder = `__VOCAB_${replacementIndex}__`;
      replacements.push({
        placeholder,
        word: match[0], // Use the actual matched text (preserves original case)
        definition,
        index: replacementIndex
      });
      
      // Replace the matched text with placeholder
      processedText = processedText.substring(0, match.index) + 
        placeholder + 
        processedText.substring(match.index + match[0].length);
      
      // Reset regex lastIndex to continue searching from the beginning
      regex.lastIndex = 0;
      replacementIndex++;
      
      // Re-search from beginning since we modified the string
      break;
    }
    // Reset regex for next iteration
    regex.lastIndex = 0;
  });

  // Split text by placeholders and replace with React elements
  if (replacements.length === 0) {
    return text;
  }

  const parts = processedText.split(/(__VOCAB_\d+__)/);
  
  return parts.map((part, index) => {
    const replacement = replacements.find(r => r.placeholder === part);
    if (replacement) {
      return (
        <span
          key={`vocab-${replacement.index}-${index}`}
          className="vocab-word"
          title={replacement.definition}
        >
          {replacement.word}
        </span>
      );
    }
    return part;
  });
};

function ExamQuestions({ yamlPath, currentPath }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedAnswers, setExpandedAnswers] = useState({});

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        setLoading(true);
        
        // Construct the full path to the YAML file
        // If yamlPath is relative (doesn't contain '/'), resolve it relative to currentPath
        // If yamlPath contains '/', treat it as absolute from textbook root
        let fullPath;
        if (yamlPath.includes('/')) {
          // Absolute path from textbook root
          fullPath = `/textbook/${yamlPath}`;
        } else {
          // Relative path - resolve relative to current page directory
          // For pages like "content/overviews/02-storage/concepts", we need the directory part
          const currentDir = currentPath === 'index' ? '' : currentPath.split('/').slice(0, -1).join('/');
          const basePath = currentDir ? `/textbook/${currentDir}` : '/textbook';
          fullPath = `${basePath}/${yamlPath}`;
        }
        
        console.log('ExamQuestions path resolution:', { yamlPath, currentPath, fullPath });
        
        const response = await fetch(fullPath);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch questions: ${response.status}`);
        }
        
        const yamlText = await response.text();
        const indexData = yaml.load(yamlText);
        
        // Check if this is the new format with file references
        if (indexData?.questions && indexData.questions[0]?.file) {
          // New format: load individual question files
          const questionPromises = indexData.questions.map(async (questionRef) => {
            // Question files should be relative to the exam-questions.yml file location
            let examQuestionsDir;
            if (yamlPath.includes('/')) {
              // Absolute path from textbook root
              examQuestionsDir = yamlPath.split('/').slice(0, -1).join('/');
            } else {
              // Relative path - use current page directory (without the page name)
              examQuestionsDir = currentPath === 'index' ? '' : currentPath.split('/').slice(0, -1).join('/');
            }
            
            const questionPath = examQuestionsDir ? 
              `/textbook/${examQuestionsDir}/${questionRef.file}` : 
              `/textbook/${questionRef.file}`;
              
            const questionResponse = await fetch(questionPath);
            if (!questionResponse.ok) {
              throw new Error(`Failed to fetch question file: ${questionRef.file}`);
            }
            
            const questionYaml = await questionResponse.text();
            const questionData = yaml.load(questionYaml);
            return questionData;
          });
          
          const questions = await Promise.all(questionPromises);
          setQuestions(questions);
        } else {
          // Legacy format: questions are directly in the main file
          const questions = indexData?.questions || [];
          setQuestions(questions);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (yamlPath) {
      fetchQuestions();
    }
  }, [yamlPath, currentPath]);

  if (loading) {
    return <div>Loading exam questions...</div>;
  }

  if (error) {
    return <div>Error loading exam questions: {error}</div>;
  }

  // Toggle accordion expansion
  const toggleAnswer = (questionId, answerKey) => {
    const key = `${questionId}-${answerKey}`;
    setExpandedAnswers(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  return (
    <div className="exam-questions">
      {questions.map((q, index) => (
        <div key={q.id || index} className="question-item">
          <h3>Question {q.id || index + 1}</h3>
          <p><strong>{q.question}</strong></p>
          
          {/* Main answer - always shown (no accordion) */}
          {q.answer && (
            <div className="answer main-answer">
              <p>{processAnswerText(q.answer, q.vocab_answer)}</p>
            </div>
          )}
          
          {/* Additional answer levels as accordions */}
          <div className="answer-levels">
            {ADDITIONAL_ANSWER_LEVELS.map(({ key, label }) => {
              if (!q[key]) return null; // Skip if this answer level doesn't exist
              
              const questionId = q.id || index;
              const expandKey = `${questionId}-${key}`;
              const isExpanded = expandedAnswers[expandKey] || false;
              
              // Get the corresponding vocabulary list for this answer level
              const vocabKey = key.replace('answer_', 'vocab_');
              const vocabList = q[vocabKey] || [];
              
              return (
                <div key={key} className="answer-accordion">
                  <button 
                    className="accordion-header"
                    onClick={() => toggleAnswer(questionId, key)}
                    aria-expanded={isExpanded}
                  >
                    <span className="accordion-title">{label}</span>
                    <span className={`accordion-icon ${isExpanded ? 'expanded' : ''}`}>
                      ▼
                    </span>
                  </button>
                  
                  {isExpanded && (
                    <div className="accordion-content">
                      <div className="answer">
                        <p>{processAnswerText(q[key], vocabList)}</p>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          
          {q.topics && q.topics.length > 0 && (
            <div className="topics">
              <strong>Topics:</strong> {q.topics.join(', ')}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default ExamQuestions;
