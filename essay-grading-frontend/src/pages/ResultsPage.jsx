import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Box, Button, Container, Typography } from '@mui/material';
import { GradingResults } from '../components/GradingResults';

export const ResultsPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const results = location.state?.results;

  useEffect(() => {
    if (!results) {
      navigate('/'); // Redirect if no results data
    }
  }, [results, navigate]);

  if (!results) return null;

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
        <Typography variant="h4" component="h1">
          Grading Results
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/')}
          sx={{ px: 4 }}
        >
          Grade Another Essay
        </Button>
      </Box>
      
      <GradingResults results={results} />
    </Container>
  );
};