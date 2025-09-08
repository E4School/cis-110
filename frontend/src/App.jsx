import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import './App.css';
import ExamDashboard from './components/ExamDashboard';
import ExamInterface from './components/ExamInterface';
import WikiPage from './components/WikiPage';

function AppContent() {
  const location = useLocation();
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

  const startExam = (examData) => {
    setCurrentExam(examData);
  };

  const endExam = () => {
    setCurrentExam(null);
  };

  const isWikiPage = location.pathname.startsWith('/wiki');
  const isExamPage = currentExam || (!isWikiPage && location.pathname === '/');

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
        <div className="header-content">
          <div className="header-title">
            <h1>CIS110</h1>
            <p>Computer Information Systems Foundations</p>
          </div>
          <nav className="main-nav">
            <Link 
              to="/" 
              className={`nav-link ${isExamPage ? 'active' : ''}`}
            >
              Exams
            </Link>
            <Link 
              to="/wiki" 
              className={`nav-link ${isWikiPage ? 'active' : ''}`}
            >
              Wiki
            </Link>
          </nav>
        </div>
      </header>

      <main>
        <Routes>
          <Route path="/" element={
            currentExam ? (
              <ExamInterface 
                questions={currentExam.questions} 
                settings={currentExam.settings}
                onEndExam={endExam}
              />
            ) : (
              <ExamDashboard 
                questions={questions} 
                onStartExam={startExam}
              />
            )
          } />
          <Route path="/wiki/*" element={<WikiPage />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App
