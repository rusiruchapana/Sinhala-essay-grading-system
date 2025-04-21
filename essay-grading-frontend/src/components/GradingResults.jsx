import { Box, Paper, Typography, LinearProgress, Divider } from '@mui/material';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const GradingResultItem = ({ label, value, max = 100 }) => (
  <Box sx={{ mb: 2 }}>
    <Typography variant="body1" gutterBottom>
      {label}: {value}/{max}
    </Typography>
    <LinearProgress
      variant="determinate"
      value={(value / max) * 100}
      sx={{ height: 10, borderRadius: 5 }}
      color={
        value >= 80 ? 'success' :
        value >= 60 ? 'primary' :
        'error'
      }
    />
  </Box>
);

export const GradingResults = ({ results }) => {
  if (!results) return null;

  const chartData = {
    labels: ['Word Count', 'Word Richness', 'Relevance', 'Spelling', 'Grammar'],
    datasets: [{
      data: [
        results.word_count_marks,
        results.word_richness_marks,
        results.relevance_marks,
        results.spelling_marks,
        results.grammar_marks
      ],
      backgroundColor: [
        '#4caf50',  // Green
        '#2196f3',  // Blue
        '#9c27b0',  // Purple
        '#ff9800',  // Orange
        '#f44336'   // Red
      ],
      borderWidth: 1,
    }]
  };

  return (
    <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
      <Typography variant="h5" gutterBottom align="center">
        Grading Results
      </Typography>
      <Divider sx={{ my: 2 }} />
      
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 4 }}>
        <Box sx={{ flex: 1 }}>
          <GradingResultItem label="Word Count" value={results.word_count_marks} />
          <GradingResultItem label="Word Richness" value={results.word_richness_marks} />
          <GradingResultItem label="Relevance" value={results.relevance_marks} />
          <GradingResultItem label="Spelling" value={results.spelling_marks} />
          <GradingResultItem label="Grammar" value={results.grammar_marks} />
          
          <Typography variant="h6" sx={{ mt: 3 }}>
            Total Score: {results.total_marks}/100
          </Typography>
        </Box>
        
        <Box sx={{ flex: 1, maxWidth: 300, mx: 'auto' }}>
          <Doughnut 
            data={chartData} 
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'bottom',
                },
              },
            }}
          />
        </Box>
      </Box>
    </Paper>
  );
};