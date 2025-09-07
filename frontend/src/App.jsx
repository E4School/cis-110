import React, { useState, useEffect } from 'react';
import './App.css';
import ExamDashboard from './components/ExamDashboard';
import ExamInterface from './components/ExamInterface';

function App() {
  const [questions, setQuestions] = useState([]);
  const [currentExam, setCurrentExam] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/questions.json')
      .then(response => response.json())
      .then(data => {
        setQuestions(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading questions:', error);
        setLoading(false);
      });
  }, []);

  const startExam = (examQuestions) => {
    setCurrentExam(examQuestions);
  };

  const endExam = () => {
    setCurrentExam(null);
  };

  if (loading) {
    return (
      <div className="app loading">
        <h2>Loading CIS-110 Exam System...</h2>
      </div>
    );
  }

  return (
    <div className="app">
      <header>
        <h1>CIS-110 Exam System</h1>
        <p>Computer Information Systems Fundamentals</p>
      </header>

      {currentExam ? (
        <ExamInterface 
          questions={currentExam} 
          onEndExam={endExam}
        />
      ) : (
        <ExamDashboard 
          questions={questions} 
          onStartExam={startExam}
        />
      )}
    </div>
  );
}

export default App
