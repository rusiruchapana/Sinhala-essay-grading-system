import { useState } from 'react';
import { Container, Typography } from '@mui/material';
import { EssayForm } from '../components/EssayForm';
import { GradingResults } from '../components/GradingResults';

export const GradingPage = () => {
  const [results, setResults] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const handleNewSubmission = () => {
    setShowResults(false); // Hide results when new submission starts
  };

  const handleGrade = (gradingResults) => {
    setResults(gradingResults);
    setShowResults(true); // Show results when grading is complete
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Sinhala Essay Grading System
      </Typography>
      
      <EssayForm 
        onGrade={handleGrade} 
        onNewSubmission={handleNewSubmission} 
      />
      {showResults && <GradingResults results={results} />}
    </Container>
  );
};