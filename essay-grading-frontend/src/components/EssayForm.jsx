import { useState, useRef } from 'react';
import { 
  Box, Button, TextField, Typography, Paper,
  FormControl, Alert, CircularProgress
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { gradeEssay } from '../services/api';

export const EssayForm = ({ onGrade, onNewSubmission }) => {
  const [formData, setFormData] = useState({
    essay: '',
    required_word_count: 200,
    topic: '',
    file: null
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, file: e.target.files[0], essay: '' });
    setError(null);
  };

  

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    onNewSubmission(); // Hide previous results
    
    if (!formData.essay && !formData.file) {
      setError('Please either upload a file or paste your essay');
      setIsSubmitting(false);
      return;
    }

    const data = new FormData();
    if (formData.file) {
      data.append('file', formData.file);
    } else {
      data.append('essay', formData.essay);
    }
    data.append('required_word_count', formData.required_word_count);
    data.append('topic', formData.topic);

    try {
      const response = await gradeEssay(data);
      console.log(response);
      if (response.error) {
        // Handle backend validation errors
        console.log(response.error);
        setError(
          response.details 
            ? `${response.error}: ${response.details}`
            : response.error
        );
        
      } else {
        onGrade(response);
      }
    } catch (err) {
      // Handle network errors
      if (err.response) {
        // Backend returned an error response
        const errorData = err.response.data;
        //console.log(errorData.details);
        setError(
          errorData.details 
            ? `${errorData.error}: ${errorData.details}`
            : errorData.error || 'An error occurred while grading the essay'
        );
      } else if (err.request) {
        // Request was made but no response received
        setError('Server is not responding. Please try again later.');
      } else {
        // Something else happened
        setError(err.message || 'An error occurred while grading the essay');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        Submit Your Sinhala Essay
      </Typography>
      


      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <form onSubmit={handleSubmit}>
        <Box sx={{ mb: 2 }}>
          <Button
            variant="outlined"
            component="label"
            startIcon={<CloudUploadIcon />}
            fullWidth
          >
            Upload Sinhala Word Document (.docx)
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept=".docx"
              hidden
            />
          </Button>
          {formData.file && (
            <Typography variant="caption" sx={{ mt: 1, display: 'block' }}>
              Selected: {formData.file.name}
            </Typography>
          )}
        </Box>

        <Typography variant="body1" align="center" sx={{ my: 2 }}>
          OR
        </Typography>

        

        <TextField
          label="Topic (in Sinhala)"
          name="topic"
          fullWidth
          variant="outlined"
          value={formData.topic}
          onChange={handleChange}
          required
          sx={{ mb: 2 }}
        />

        <FormControl fullWidth sx={{ mb: 3 }}>
          <TextField
            label="Required Word Count"
            name="required_word_count"
            type="number"
            value={formData.required_word_count}
            onChange={handleChange}
            variant="outlined"
            inputProps={{ min: 1 }}
          />
        </FormControl>

        <Button
          type="submit"
          variant="contained"
          color="primary"
          size="large"
          fullWidth
          disabled={isSubmitting}
          startIcon={isSubmitting ? <CircularProgress size={20} /> : null}
        >
          {isSubmitting ? 'Grading...' : 'Grade Essay'}
        </Button>
      </form>
    </Paper>
  );
};