import { Box, Paper, Typography, LinearProgress, Divider, Alert } from '@mui/material';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

// Define consistent colors for all metrics
const METRIC_COLORS = {
  'Word Count': '#4caf50',    // Green
  'Word Richness': '#2196f3', // Blue
  'Relevance': '#9c27b0',     // Purple
  'Spelling': '#ff9800',      // Orange
  'Grammar': '#f44336'        // Red
};

const GradingResultItem = ({ label, value, max = 100 }) => {
  // Get the color for this specific metric
  const color = METRIC_COLORS[label] || '#4caf50'; // Default to green
  
  return (
    <Box sx={{ mb: 2 }}>
      <Typography variant="body1" gutterBottom>
        {label}: {value}/{max}
      </Typography>
      <LinearProgress
        variant="determinate"
        value={(value / max) * 100}
        sx={{ 
          height: 10, 
          borderRadius: 5,
          backgroundColor: `${color}30`, // 30% opacity for background
          '& .MuiLinearProgress-bar': {
            backgroundColor: color
          }
        }}
      />
    </Box>
  );
};

export const GradingResults = ({ results }) => {
  if (!results) return null;

  // Prepare chart data using the same color mapping
  const chartData = {
    labels: Object.keys(METRIC_COLORS),
    datasets: [{
      data: [
        results.word_count_marks,
        results.word_richness_marks,
        results.relevance_marks,
        results.spelling_marks,
        results.grammar_marks
      ],
      backgroundColor: Object.values(METRIC_COLORS),
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
      
      <Alert severity="info" sx={{ mt: 2 }}>
        Your essay has been graded and saved successfully!
      </Alert>
    </Paper>
  );
};