import React, { useState, useEffect } from 'react';
import './ExamInterface.css';

function ExamInterface({ questions, settings, onEndExam }) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [showAnswer, setShowAnswer] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);
  const [questionStartTime, setQuestionStartTime] = useState(Date.now());

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeSpent(prev => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    setQuestionStartTime(Date.now());
  }, [currentQuestionIndex]);

  const currentQuestion = questions[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === questions.length - 1;
  const hasAnswered = answers.hasOwnProperty(currentQuestion.id);

  const handleAnswerChange = (answer) => {
    setAnswers(prev => ({
      ...prev,
      [currentQuestion.id]: {
        answer,
        timeSpent: Date.now() - questionStartTime
      }
    }));
  };

  const goToNextQuestion = () => {
    if (!isLastQuestion) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const goToPreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const submitExam = () => {
    setShowResults(true);
  };

  const calculateScore = () => {
    const answeredQuestions = Object.keys(answers).length;
    const totalQuestions = questions.length;
    
    // For now, we'll just count completion since these are short-answer questions
    // In a real system, you'd need human grading or more sophisticated checking
    return {
      answered: answeredQuestions,
      total: totalQuestions,
      percentage: Math.round((answeredQuestions / totalQuestions) * 100)
    };
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (showResults) {
    const score = calculateScore();
    return (
      <div className="exam-results">
        <h2>Exam Complete!</h2>
        
        <div className="score-summary">
          <div className="score-circle">
            <span className="score-percentage">{score.percentage}%</span>
            <span className="score-label">Completed</span>
          </div>
          <div className="score-details">
            <p>Questions Answered: {score.answered} / {score.total}</p>
            <p>Time Spent: {formatTime(timeSpent)}</p>
            <p>Average per Question: {formatTime(Math.round(timeSpent / questions.length))}</p>
          </div>
        </div>

        <div className="question-review">
          <h3>Your Responses</h3>
          {questions.map((question, index) => {
            const userAnswer = answers[question.id];
            return (
              <div key={question.id} className="question-result">
                <div className="question-header">
                  <h4>Question {index + 1} (Chapter {question.chapter})</h4>
                </div>
                <p className="question-text">{question.question}</p>
                <div className="answer-comparison">
                  <div className="user-answer">
                    <strong>Your Answer:</strong>
                    <p>{userAnswer ? userAnswer.answer : 'Not answered'}</p>
                  </div>
                  <div className="correct-answer">
                    <strong>Model Answer:</strong>
                    <p>{question.answer}</p>
                  </div>
                </div>
                {userAnswer && (
                  <p className="time-spent">
                    Time spent: {formatTime(Math.round(userAnswer.timeSpent / 1000))}
                  </p>
                )}
              </div>
            );
          })}
        </div>

        <button className="return-dashboard-btn" onClick={onEndExam}>
          Return to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="exam-interface">
      <div className="exam-header">
        <div className="progress-info">
          <span>Question {currentQuestionIndex + 1} of {questions.length}</span>
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>
        <div className="time-info">
          <span>Time: {formatTime(timeSpent)}</span>
        </div>
      </div>

      <div className="question-section">
        <div className="question-meta">
          <span className="chapter-tag">Chapter {currentQuestion.chapter}</span>
          <span className="question-type">{currentQuestion.type}</span>
          {settings?.showAnswerToggle && (
            <button 
              onClick={() => setShowAnswer(!showAnswer)}
              className={`show-answer-toggle ${showAnswer ? 'active' : ''}`}
            >
              {showAnswer ? 'Hide Answer' : 'Show Answer'}
            </button>
          )}
        </div>
        
        <h2 className="question-text">{currentQuestion.question}</h2>

        {settings?.showAnswerToggle && showAnswer && (
          <div className="answer-reveal">
            <strong>Answer:</strong>
            <p>{currentQuestion.answer}</p>
          </div>
        )}

        <div className="answer-section">
          <textarea
            placeholder="Enter your answer here..."
            value={answers[currentQuestion.id]?.answer || ''}
            onChange={(e) => handleAnswerChange(e.target.value)}
            rows="6"
            className="answer-input"
          />
        </div>
      </div>

      <div className="navigation-section">
        <div className="nav-buttons">
          <button 
            onClick={goToPreviousQuestion}
            disabled={currentQuestionIndex === 0}
            className="nav-btn prev-btn"
          >
            ← Previous
          </button>
          
          {isLastQuestion ? (
            <button 
              onClick={submitExam}
              className="submit-btn"
              disabled={Object.keys(answers).length === 0}
            >
              Submit Exam
            </button>
          ) : (
            <button 
              onClick={goToNextQuestion}
              className="nav-btn next-btn"
            >
              Next →
            </button>
          )}
        </div>

        <div className="question-status">
          <p>
            {hasAnswered ? '✓ Answered' : '○ Not answered'} 
            {hasAnswered && ` (${answers[currentQuestion.id].answer.length} characters)`}
          </p>
        </div>
      </div>

      <div className="exam-overview">
        <h3>Question Overview</h3>
        <div className="question-grid">
          {questions.map((_, index) => (
            <button
              key={index}
              className={`question-nav-item ${
                index === currentQuestionIndex ? 'current' : ''
              } ${answers[questions[index].id] ? 'answered' : 'unanswered'}`}
              onClick={() => setCurrentQuestionIndex(index)}
            >
              {index + 1}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ExamInterface;
