import React, { useState, useEffect } from 'react';
import * as yaml from 'js-yaml';
import compiledContentService from '../services/compiledContentService';

import './VocabList.css';

function VocabList({ yamlPath, currentPath }) {
  console.log('VocabList component mounted with:', { yamlPath, currentPath });
  const [vocabulary, setVocabulary] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedWords, setExpandedWords] = useState({});

  useEffect(() => {
    const fetchVocabulary = async () => {
      try {
        setLoading(true);
        
        // Construct the full path to the YAML file
        const directoryPath = currentPath ? currentPath.split('/').slice(0, -1).join('/') : '';
        const fullPath = directoryPath ? 
          `${directoryPath}/${yamlPath}` : 
          yamlPath;
        
        const indexData = await compiledContentService.getYaml(fullPath);
        
        // Check if this is the new format with file references
        if (indexData?.questions && indexData.questions[0]?.file) {
          // New format: load individual question files
          const questionPromises = indexData.questions.map(async (questionRef) => {
            const questionPath = directoryPath ? 
              `${directoryPath}/${questionRef.file}` : 
              questionRef.file;
              
            const questionData = await compiledContentService.getYaml(questionPath);
            return questionData;
          });
          
          const questions = await Promise.all(questionPromises);
          
          // Extract vocabulary from all questions
          const vocabMap = extractVocabulary(questions);
          setVocabulary(vocabMap);
          
        } else {
          // Legacy format: questions are directly in the main file
          const questions = indexData?.questions || [];
          const vocabMap = extractVocabulary(questions);
          setVocabulary(vocabMap);
        }
        
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (yamlPath) {
      fetchVocabulary();
    }
  }, [yamlPath, currentPath]);

  // Extract vocabulary from all questions and organize by word
  const extractVocabulary = (questions) => {
    const vocabMap = {};
    
    // Vocabulary field names to check
    const vocabFields = [
      'vocab_answer',
      'vocab_kindergarten', 
      'vocab_3rd_grade',
      'vocab_7th_grade',
      'vocab_high_school',
      'vocab_undergraduate'
    ];
    
    // Level labels for context
    const levelLabels = {
      vocab_answer: 'General',
      vocab_kindergarten: 'Kindergarten',
      vocab_3rd_grade: '7th Grade',
      vocab_7th_grade: 'High School', 
      vocab_high_school: 'Undergraduate',
      vocab_undergraduate: 'Postgraduate'
    };

    questions.forEach((question, qIndex) => {
      vocabFields.forEach(field => {
        const vocabData = question[field];
        if (!vocabData) return;
        
        // Handle both array format (legacy) and object format (new)
        if (Array.isArray(vocabData)) {
          // Check if it's new format (array of objects) or legacy format (array of strings)
          if (vocabData.length > 0 && typeof vocabData[0] === 'object' && vocabData[0].word) {
            // New format: word/definition objects
            vocabData.forEach(item => {
              if (item.word && item.definition) {
                if (!vocabMap[item.word]) {
                  vocabMap[item.word] = [];
                }
                vocabMap[item.word].push({
                  definition: item.definition,
                  level: levelLabels[field],
                  questionId: question.id || qIndex + 1,
                  context: field
                });
              }
            });
          } else {
            // Legacy format: just word strings
            vocabData.forEach(word => {
              if (!vocabMap[word]) {
                vocabMap[word] = [];
              }
              vocabMap[word].push({
                definition: `[Definition needed for ${word}]`,
                level: levelLabels[field],
                questionId: question.id || qIndex + 1,
                context: field
              });
            });
          }
        }
      });
    });

    return vocabMap;
  };

  // Toggle word expansion
  const toggleWord = (word) => {
    setExpandedWords(prev => ({
      ...prev,
      [word]: !prev[word]
    }));
  };

  if (loading) {
    return <div className="vocab-list loading">Loading vocabulary...</div>;
  }

  if (error) {
    return <div className="vocab-list error">Error loading vocabulary: {error}</div>;
  }

  const sortedWords = Object.keys(vocabulary).sort((a, b) => 
    a.toLowerCase().localeCompare(b.toLowerCase())
  );

  return (
    <div className="vocab-list">
      <h2>Vocabulary</h2>
      <div className="vocab-count">
        {sortedWords.length} terms found
      </div>
      
      <div className="vocab-items">
        {sortedWords.map(word => {
          const definitions = vocabulary[word];
          const isExpanded = expandedWords[word] || false;
          const hasMultipleDefinitions = definitions.length > 1;
          
          return (
            <div key={word} className="vocab-item">
              <button 
                className="vocab-header"
                onClick={() => toggleWord(word)}
                aria-expanded={isExpanded}
              >
                <span className="vocab-word">{word}</span>
                {hasMultipleDefinitions && (
                  <span className="definition-count">
                    ({definitions.length} definitions)
                  </span>
                )}
                <span className={`vocab-icon ${isExpanded ? 'expanded' : ''}`}>
                  ▼
                </span>
              </button>
              
              {isExpanded && (
                <div className="vocab-content">
                  {definitions.map((def, index) => (
                    <div key={index} className="vocab-definition">
                      <div className="definition-text">{def.definition}</div>
                      <div className="definition-meta">
                        <span className="definition-level">{def.level}</span>
                        <span className="definition-question">Question {def.questionId}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default VocabList;
