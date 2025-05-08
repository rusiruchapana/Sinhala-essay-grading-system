import { useState, useRef } from 'react';
import { 
  Box, Button, TextField, Typography, Paper,
  FormControl, InputLabel, Select, MenuItem, Alert
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { gradeEssay } from '../services/api';

export const EssayForm = ({ onGrade }) => {
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

  const handleTextChange = (e) => {
    setFormData({ ...formData, essay: e.target.value, file: null });
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    
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
      const result = await gradeEssay(data);
      onGrade(result);
    } catch (err) {
      setError(err.message || 'An error occurred while grading the essay');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        Submit Your Essay
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
            Upload Word Document
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
          label="Paste Your Sinhala Essay"
          name="essay"
          multiline
          rows={6}
          fullWidth
          variant="outlined"
          value={formData.essay}
          onChange={handleTextChange}
          sx={{ mb: 2 }}
        />

        <TextField
          label="Topic"
          name="topic"
          fullWidth
          variant="outlined"
          value={formData.topic}
          onChange={handleChange}
          required
          sx={{ mb: 2 }}
        />

        <FormControl fullWidth sx={{ mb: 3 }}>
          <InputLabel>Required Word Count</InputLabel>
          <Select
            name="required_word_count"
            value={formData.required_word_count}
            onChange={handleChange}
            label="Required Word Count"
          >
            <MenuItem value={100}>100 words</MenuItem>
            <MenuItem value={200}>200 words</MenuItem>
            <MenuItem value={300}>300 words</MenuItem>
            <MenuItem value={500}>500 words</MenuItem>
          </Select>
        </FormControl>

        <Button
          type="submit"
          variant="contained"
          color="primary"
          size="large"
          fullWidth
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Grading...' : 'Grade Essay'}
        </Button>
      </form>
    </Paper>
  );
};