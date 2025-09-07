import React, { useState } from 'react';
import { ExamTypes } from '../types/Question';
import './ExamDashboard.css';

function ExamDashboard({ questions, onStartExam }) {
  const [examType, setExamType] = useState(ExamTypes.PRACTICE);
  const [selectedChapters, setSelectedChapters] = useState([]);
  const [questionCount, setQuestionCount] = useState(10);

  // Get unique chapters from questions
  const chapters = [...new Set(questions.map(q => q.chapter))].sort((a, b) => a - b);
  
  // Get chapter titles
  const chapterTitles = chapters.reduce((acc, ch) => {
    const question = questions.find(q => q.chapter === ch);
    acc[ch] = question ? question.chapterTitle : `Chapter ${ch}`;
    return acc;
  }, {});

  const handleChapterToggle = (chapter) => {
    setSelectedChapters(prev => 
      prev.includes(chapter) 
        ? prev.filter(ch => ch !== chapter)
        : [...prev, chapter]
    );
  };

  const selectAllChapters = () => {
    setSelectedChapters(chapters);
  };

  const clearAllChapters = () => {
    setSelectedChapters([]);
  };

  const generateExam = () => {
    const chaptersToUse = selectedChapters.length > 0 ? selectedChapters : chapters;
    const availableQuestions = questions.filter(q => chaptersToUse.includes(q.chapter));
    
    // Shuffle and limit questions
    const shuffled = [...availableQuestions].sort(() => Math.random() - 0.5);
    const examQuestions = shuffled.slice(0, Math.min(questionCount, shuffled.length));
    
    onStartExam(examQuestions);
  };

  const getQuestionCountByChapter = (chapter) => {
    return questions.filter(q => q.chapter === chapter).length;
  };

  const totalAvailableQuestions = selectedChapters.length > 0 
    ? questions.filter(q => selectedChapters.includes(q.chapter)).length
    : questions.length;

  return (
    <div className="exam-dashboard">
      <div className="dashboard-section">
        <h2>Exam Configuration</h2>
        
        <div className="exam-type-selector">
          <h3>Exam Type</h3>
          <div className="radio-group">
            <label>
              <input 
                type="radio" 
                value={ExamTypes.PRACTICE}
                checked={examType === ExamTypes.PRACTICE}
                onChange={(e) => setExamType(e.target.value)}
              />
              Practice Exam (Untimed, Show Answers)
            </label>
            <label>
              <input 
                type="radio" 
                value={ExamTypes.FINAL}
                checked={examType === ExamTypes.FINAL}
                onChange={(e) => setExamType(e.target.value)}
              />
              Final Exam (Timed, No Answers Shown)
            </label>
          </div>
        </div>

        <div className="chapter-selector">
          <h3>Select Chapters</h3>
          <div className="chapter-controls">
            <button onClick={selectAllChapters} type="button">Select All</button>
            <button onClick={clearAllChapters} type="button">Clear All</button>
          </div>
          <div className="chapter-list">
            {chapters.map(chapter => (
              <label key={chapter} className="chapter-item">
                <input
                  type="checkbox"
                  checked={selectedChapters.includes(chapter)}
                  onChange={() => handleChapterToggle(chapter)}
                />
                <span className="chapter-info">
                  <strong>Chapter {chapter}:</strong> {chapterTitles[chapter]}
                  <em>({getQuestionCountByChapter(chapter)} questions)</em>
                </span>
              </label>
            ))}
          </div>
        </div>

        <div className="question-count-selector">
          <h3>Number of Questions</h3>
          <input
            type="number"
            min="1"
            max={totalAvailableQuestions}
            value={questionCount}
            onChange={(e) => setQuestionCount(parseInt(e.target.value))}
          />
          <p>Available questions: {totalAvailableQuestions}</p>
        </div>

        <div className="exam-summary">
          <h3>Exam Summary</h3>
          <ul>
            <li>Type: {examType === ExamTypes.PRACTICE ? 'Practice' : 'Final'} Exam</li>
            <li>Chapters: {selectedChapters.length === 0 ? 'All' : selectedChapters.join(', ')}</li>
            <li>Questions: {Math.min(questionCount, totalAvailableQuestions)}</li>
            <li>Time Limit: {examType === ExamTypes.FINAL ? '2 minutes per question' : 'Unlimited'}</li>
          </ul>
        </div>

        <button 
          className="start-exam-btn"
          onClick={generateExam}
          disabled={totalAvailableQuestions === 0}
        >
          Start Exam
        </button>
      </div>

      <div className="dashboard-section">
        <h2>Question Bank Overview</h2>
        <div className="stats">
          <div className="stat-item">
            <span className="stat-number">{questions.length}</span>
            <span className="stat-label">Total Questions</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{chapters.length}</span>
            <span className="stat-label">Chapters</span>
          </div>
        </div>
        
        <div className="chapter-breakdown">
          <h3>Questions by Chapter</h3>
          {chapters.map(chapter => (
            <div key={chapter} className="chapter-stat">
              <span>Ch. {chapter}</span>
              <span>{getQuestionCountByChapter(chapter)} questions</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ExamDashboard;
