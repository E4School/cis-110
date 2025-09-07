// Question type definition (JSX compatible)
// Question: { id, chapter, chapterTitle, question, answer, type }

// Exam result type 
// ExamResult: { questionId, userAnswer, isCorrect, timeSpent }

// Exam configuration type
// ExamConfig: { type, chapters, questionCount, timeLimit }

export const QuestionTypes = {
  SHORT_ANSWER: 'short-answer',
  MULTIPLE_CHOICE: 'multiple-choice'
};

export const ExamTypes = {
  PRACTICE: 'practice',
  FINAL: 'final'
};
