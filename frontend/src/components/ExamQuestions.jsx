import React, { useState, useEffect } from 'react';
import * as yaml from 'js-yaml';

import './ExamQuestions.css';

function ExamQuestions({ yamlPath, currentPath }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
        const data = yaml.load(yamlText);
        const questions = data?.questions || [];
        
        setQuestions(questions);
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

  return (
    <div className="exam-questions">
      {questions.map((q, index) => (
        <div key={q.id || index} className="question-item">
          <h3>Question {q.id || index + 1}</h3>
          <p><strong>{q.question}</strong></p>
          <div className="answer">
            <p><strong>Answer:</strong> {q.answer}</p>
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
