import React from 'react';
import './ExamDashboard.css';

function ExamDashboard({ questions, onStartExam }) {
  // Get unique chapters from questions
  const chapters = [...new Set(questions.map(q => q.chapter))].sort((a, b) => a - b);
  
  const generateExam = () => {
    const examQuestions = [];
    
    // Select 50% of questions from each chapter
    chapters.forEach(chapter => {
      const chapterQuestions = questions.filter(q => q.chapter === chapter);
      const halfCount = Math.ceil(chapterQuestions.length * 0.5);
      
      // Shuffle and take 50%
      const shuffled = [...chapterQuestions].sort(() => Math.random() - 0.5);
      const selected = shuffled.slice(0, halfCount);
      
      examQuestions.push(...selected);
    });
    
    // Final shuffle of all selected questions
    const finalExam = examQuestions.sort(() => Math.random() - 0.5);
    
    onStartExam(finalExam);
  };

  const getQuestionCountByChapter = (chapter) => {
    return questions.filter(q => q.chapter === chapter).length;
  };

  const totalExamQuestions = chapters.reduce((total, chapter) => {
    const chapterCount = getQuestionCountByChapter(chapter);
    return total + Math.ceil(chapterCount * 0.5);
  }, 0);

  return (
    <div className="exam-dashboard-simple">
      <div className="exam-overview">
        <h2>CIS-110 Practice Exam</h2>
        <p>Test your knowledge across all course topics</p>
        
        <div className="exam-details">
          <div className="detail-item">
            <strong>{totalExamQuestions} </strong>
            <span>Questions</span>
          </div>
        </div>

        <button 
          className="generate-exam-btn"
          onClick={generateExam}
          disabled={questions.length === 0}
        >
          Generate Exam
        </button>
      </div>
    </div>
  );
}

export default ExamDashboard;
