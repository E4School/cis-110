import React, { useState, useEffect } from 'react';
import * as yaml from 'js-yaml';

import './ConceptMap.css';

function ConceptMap({ yamlPath, currentPath }) {
  console.log('ConceptMap component mounted with:', { yamlPath, currentPath });
  const [conceptMap, setConceptMap] = useState([]);
  const [questionDetails, setQuestionDetails] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedCategories, setExpandedCategories] = useState({});
  const [expandedQuestions, setExpandedQuestions] = useState({});

  useEffect(() => {
    const fetchConceptMap = async () => {
      try {
        setLoading(true);
        
        // Construct the full path to the YAML file
        const directoryPath = currentPath ? currentPath.split('/').slice(0, -1).join('/') : '';
        const fullPath = directoryPath ? 
          `/textbook/${directoryPath}/${yamlPath}` : 
          `/textbook/${yamlPath}`;
        
        const response = await fetch(fullPath);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch concept map: ${response.status}`);
        }
        
        const yamlText = await response.text();
        const conceptMapData = yaml.load(yamlText);
        
        console.log('Loaded concept map data:', conceptMapData);
        
        if (!conceptMapData?.concept_map) {
          throw new Error('Invalid concept map format: missing concept_map array');
        }
        
        setConceptMap(conceptMapData.concept_map);
        
        // Initialize all categories as expanded by default
        const initialExpandedCategories = {};
        conceptMapData.concept_map.forEach((category, index) => {
          initialExpandedCategories[index] = true;
        });
        setExpandedCategories(initialExpandedCategories);
        
        // Collect all unique question file references
        const questionFiles = new Set();
        conceptMapData.concept_map.forEach(category => {
          category.concepts?.forEach(concept => {
            concept.exam_questions?.forEach(questionFile => {
              questionFiles.add(questionFile);
            });
          });
        });
        
        // Fetch all referenced question files
        const questionPromises = Array.from(questionFiles).map(async (questionFile) => {
          const questionPath = directoryPath ? 
            `/textbook/${directoryPath}/${questionFile}` : 
            `/textbook/${questionFile}`;
            
          try {
            const questionResponse = await fetch(questionPath);
            if (!questionResponse.ok) {
              console.warn(`Failed to fetch question file: ${questionFile}`);
              return [questionFile, null];
            }
            
            const questionYaml = await questionResponse.text();
            const questionData = yaml.load(questionYaml);
            return [questionFile, questionData];
          } catch (err) {
            console.warn(`Error loading question file ${questionFile}:`, err);
            return [questionFile, null];
          }
        });
        
        const questionResults = await Promise.all(questionPromises);
        const questionDetailsMap = Object.fromEntries(questionResults);
        
        console.log('Loaded question details:', questionDetailsMap);
        setQuestionDetails(questionDetailsMap);
        
      } catch (err) {
        console.error('Error fetching concept map:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchConceptMap();
  }, [yamlPath, currentPath]);

  const toggleCategory = (categoryIndex) => {
    setExpandedCategories(prev => ({
      ...prev,
      [categoryIndex]: !prev[categoryIndex]
    }));
  };

  const toggleQuestions = (categoryIndex, conceptIndex) => {
    const key = `${categoryIndex}-${conceptIndex}`;
    setExpandedQuestions(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const getQuestionTitle = (questionFile) => {
    const questionData = questionDetails[questionFile];
    if (!questionData) return questionFile;
    
    return questionData.question || questionFile;
  };

  const getQuestionId = (questionFile) => {
    const questionData = questionDetails[questionFile];
    if (!questionData) return '';
    
    return questionData.id ? `Q${questionData.id}` : '';
  };

  if (loading) {
    return <div className="concept-map-loading">Loading concept map...</div>;
  }

  if (error) {
    return <div className="concept-map-error">Error loading concept map: {error}</div>;
  }

  if (!conceptMap.length) {
    return <div className="concept-map-empty">No concept map data available.</div>;
  }

  return (
    <div className="concept-map">
      <h2>Concept Map</h2>
      <p className="concept-map-description">
        This map shows how concepts relate to exam questions. Click on categories to expand them.
      </p>
      
      <div className="concept-categories">
        {conceptMap.map((category, categoryIndex) => (
          <div key={categoryIndex} className="concept-category">
            <button
              className={`category-header ${expandedCategories[categoryIndex] ? 'expanded' : ''}`}
              onClick={() => toggleCategory(categoryIndex)}
            >
              <span className="category-title">{category.category}</span>
              <span className="expand-icon">
                {expandedCategories[categoryIndex] ? '−' : '+'}
              </span>
            </button>
            
            {expandedCategories[categoryIndex] && (
              <div className="category-content">
                {category.concepts?.map((concept, conceptIndex) => (
                  <div key={conceptIndex} className="concept-item">
                    <div className="concept-content">
                      <div className="concept-header">
                        <span className="concept-name">{concept.name}</span>
                        {concept.description && (
                          <span className="concept-description">({concept.description})</span>
                        )}
                      </div>
                      
                      {concept.exam_questions?.length > 0 && (
                        <div className="concept-questions">
                          <button
                            className={`questions-header ${expandedQuestions[`${categoryIndex}-${conceptIndex}`] ? 'expanded' : ''}`}
                            onClick={() => toggleQuestions(categoryIndex, conceptIndex)}
                          >
                            <span>{concept.exam_questions.length} question{concept.exam_questions.length !== 1 ? 's' : ''}</span>
                            <span className="expand-icon">
                              {expandedQuestions[`${categoryIndex}-${conceptIndex}`] ? '−' : '+'}
                            </span>
                          </button>
                          
                          {expandedQuestions[`${categoryIndex}-${conceptIndex}`] && (
                            <ul className="questions-list">
                              {concept.exam_questions.map((questionFile, questionIndex) => (
                                <li key={questionIndex} className="question-item">
                                  <div className="question-header">
                                    <span className="question-id">
                                      {getQuestionId(questionFile)}
                                    </span>
                                    <span className="question-title">
                                      {getQuestionTitle(questionFile)}
                                    </span>
                                  </div>
                                </li>
                              ))}
                            </ul>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ConceptMap;
