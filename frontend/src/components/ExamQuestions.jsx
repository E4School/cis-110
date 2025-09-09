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
        // Remove the filename from currentPath to get just the directory
        const directoryPath = currentPath ? currentPath.split('/').slice(0, -1).join('/') : '';
        const fullPath = directoryPath ? 
          `/textbook/${directoryPath}/${yamlPath}` : 
          `/textbook/${yamlPath}`;
        
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
            const questionPath = directoryPath ? 
              `/textbook/${directoryPath}/${questionRef.file}` : 
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
              <p>{q.answer}</p>
            </div>
          )}
          
          {/* Additional answer levels as accordions */}
          <div className="answer-levels">
            {ADDITIONAL_ANSWER_LEVELS.map(({ key, label }) => {
              if (!q[key]) return null; // Skip if this answer level doesn't exist
              
              const questionId = q.id || index;
              const expandKey = `${questionId}-${key}`;
              const isExpanded = expandedAnswers[expandKey] || false;
              
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
                        <p>{q[key]}</p>
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
