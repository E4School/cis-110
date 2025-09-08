import React, { useState, useEffect } from 'react';
import * as yaml from 'js-yaml';

import './ExamQuestions.css';

function ExamQuestions({ yamlPath, currentPath }) {
  console.log('ExamQuestions component created with yamlPath:', yamlPath, 'currentPath:', currentPath);
  
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
        
        console.log('ExamQuestions: Directory path:', directoryPath);
        console.log('ExamQuestions: Fetching from path:', fullPath);
        
        const response = await fetch(fullPath);
        
        if (!response.ok) {
          console.error('ExamQuestions: Failed to fetch:', response.status, response.statusText);
          throw new Error(`Failed to fetch questions: ${response.status}`);
        }
        
        console.log('ExamQuestions: Response headers:', response.headers);
        console.log('ExamQuestions: Content-Type:', response.headers.get('content-type'));
        
        const yamlText = await response.text();
        console.log('ExamQuestions: YAML content length:', yamlText.length);
        console.log('ExamQuestions: YAML content start:', yamlText.substring(0, 200) + '...');
        
        const data = yaml.load(yamlText);
        console.log('ExamQuestions: Parsed data:', data);
        console.log('ExamQuestions: Data type:', typeof data);
        console.log('ExamQuestions: Is data an array?', Array.isArray(data));
        console.log('ExamQuestions: Data keys:', Object.keys(data || {}));
        console.log('ExamQuestions: Raw data.questions:', data?.questions);
        
        const questions = data?.questions || [];
        console.log('ExamQuestions: Extracted questions:', questions);
        console.log('ExamQuestions: Questions type:', typeof questions);
        console.log('ExamQuestions: Is questions an array?', Array.isArray(questions));
        console.log('ExamQuestions: Questions length:', questions.length);
        
        // Temporary test: add a hardcoded question if none found
        if (questions.length === 0) {
          console.log('No questions found, adding test question');
          questions.push({
            id: 'test',
            question: 'Test question - this is a placeholder',
            answer: 'Test answer - if you see this, the component rendering works',
            topics: ['test']
          });
        }
        
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

  console.log('ExamQuestions render: questions array:', questions);

  return (
    <div className="exam-questions">
      <div>Debug: Found {questions.length} questions</div>
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
