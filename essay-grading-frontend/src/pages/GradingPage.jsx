import { useState } from 'react';
import { Box, Container, Typography } from '@mui/material';
import { EssayForm } from '../components/EssayForm';
import { GradingResults } from '../components/GradingResults';

export const GradingPage = () => {
  const [results, setResults] = useState(null);

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Sinhala Essay Grading System
      </Typography>
      
      <Box sx={{ my: 4 }}>
        <EssayForm onGrade={setResults} />
        <GradingResults results={results} />
      </Box>
    </Container>
  );
};