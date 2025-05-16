import { 
  Box, Paper, Typography, LinearProgress,  Alert,
  Grid, Chip, useTheme
} from '@mui/material';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const METRIC_COLORS = {
  'Word Count': '#4caf50',
  'Word Richness': '#2196f3',
  'Relevance': '#9c27b0',
  'Spelling': '#ff9800',
  'Grammar': '#f44336'
};

const ScoreCard = ({ label, value }) => {
  const color = METRIC_COLORS[label] || '#4caf50';
  
  return (
    <Paper elevation={2} sx={{ p: 3, height: '100%' }}>
      <Typography variant="h6" gutterBottom>
        {label}
      </Typography>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <LinearProgress
          variant="determinate"
          value={value}
          sx={{
            flexGrow: 1,
            height: 10,
            borderRadius: 5,
            backgroundColor: `${color}30`,
            '& .MuiLinearProgress-bar': {
              backgroundColor: color
            }
          }}
        />
        <Chip 
          label={`${value.toFixed(1)}%`} 
          color={
            value >= 80 ? 'success' :
            value >= 60 ? 'primary' : 'error'
          }
        />
      </Box>
    </Paper>
  );
};

export const GradingResults = ({ results }) => {
  const theme = useTheme();

  if (!results) return null;

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
    <Paper elevation={3} sx={{ p: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h3" component="div" gutterBottom>
          Final Score: <span style={{ color: theme.palette.primary.main }}>
            {results.total_marks.toFixed(1)}/100
          </span>
        </Typography>
        <Chip 
          label={
            results.total_marks >= 80 ? 'Excellent' :
            results.total_marks >= 60 ? 'Good' : 'Needs Improvement'
          }
          color={
            results.total_marks >= 80 ? 'success' :
            results.total_marks >= 60 ? 'primary' : 'error'
          }
          size="large"
          sx={{ fontSize: '1rem', p: 2 }}
        />
      </Box>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        {Object.entries({
          'Word Count': results.word_count_marks,
          'Word Richness': results.word_richness_marks,
          'Relevance': results.relevance_marks,
          'Spelling': results.spelling_marks,
          'Grammar': results.grammar_marks
        }).map(([label, value]) => (
          <Grid item xs={12} sm={6} md={4} key={label}>
            <ScoreCard label={label} value={value} />
          </Grid>
        ))}
      </Grid>

      <Box sx={{ maxWidth: 500, mx: 'auto', mb: 4 }}>
        <Doughnut 
          data={chartData} 
          options={{
            responsive: true,
            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  font: {
                    size: 14
                  },
                  padding: 20
                }
              },
            },
            cutout: '65%',
          }}
        />
      </Box>

      <Alert severity="info" sx={{ mt: 2 }}>
        Your essay has been saved. You can view all your graded essays from the history section.
      </Alert>
    </Paper>
  );
};