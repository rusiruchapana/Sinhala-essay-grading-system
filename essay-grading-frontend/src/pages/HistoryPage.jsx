import { useState, useEffect } from 'react';
import { 
  Box, Paper, Typography, Table, TableBody, 
  TableCell, TableContainer, TableHead, 
  TableRow, Chip, CircularProgress, Alert,
  IconButton, Dialog, DialogTitle, DialogContent,
  DialogContentText, DialogActions, Button
} from '@mui/material';
import { Delete, Visibility } from '@mui/icons-material';
import { getAllEssays, deleteEssay } from '../services/api';

const METRIC_COLORS = {
  'Word Count': '#4caf50',
  'Word Richness': '#2196f3',
  'Relevance': '#9c27b0',
  'Spelling': '#ff9800',
  'Grammar': '#f44336'
};

export const HistoryPage = () => {
  const [essays, setEssays] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedEssay, setSelectedEssay] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [deleteId, setDeleteId] = useState(null);

  useEffect(() => {
    const fetchEssays = async () => {
      try {
        const data = await getAllEssays();
        setEssays(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchEssays();
  }, []);

  const handleViewEssay = (essay) => {
    setSelectedEssay(essay);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedEssay(null);
  };

  const handleDeleteClick = (id) => {
    setDeleteId(id);
  };

  const confirmDelete = async () => {
    try {
      await deleteEssay(deleteId);
      setEssays(essays.filter(essay => essay.id !== deleteId));
    } catch (err) {
      setError(err.message);
    } finally {
      setDeleteId(null);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" my={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ my: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        Grading History
      </Typography>
      
      {essays.length === 0 ? (
        <Alert severity="info">
          No graded essays found in history.
        </Alert>
      ) : (
        <Paper elevation={3}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Topic</TableCell>
                  <TableCell align="center">Word Count</TableCell>
                  <TableCell align="center">Score</TableCell>
                  <TableCell align="center">Date</TableCell>
                  <TableCell align="center">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {essays.map((essay) => (
                  <TableRow key={essay.id}>
                    <TableCell>{essay.topic}</TableCell>
                    <TableCell align="center">
                      {essay.word_count}/{essay.required_word_count}
                    </TableCell>
                    <TableCell align="center">
                      <Chip 
                        label={`${essay.total_marks.toFixed(1)}/100`}
                        color={
                          essay.total_marks >= 80 ? 'success' :
                          essay.total_marks >= 60 ? 'primary' : 'error'
                        }
                      />
                    </TableCell>
                    <TableCell align="center">
                      {new Date(essay.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell align="center">
                      <IconButton 
                        color="primary"
                        onClick={() => handleViewEssay(essay)}
                      >
                        <Visibility />
                      </IconButton>
                      <IconButton 
                        color="error"
                        onClick={() => handleDeleteClick(essay.id)}
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      {/* Essay Detail Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          Essay Details: {selectedEssay?.topic}
        </DialogTitle>
        <DialogContent dividers>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1">Metrics:</Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 1 }}>
              <Chip 
                label={`Word Count: ${selectedEssay?.word_count_marks}`}
                sx={{ backgroundColor: METRIC_COLORS['Word Count'] + '30', color: 'text.primary' }}
              />
              <Chip 
                label={`Word Richness: ${selectedEssay?.word_richness_marks}`}
                sx={{ backgroundColor: METRIC_COLORS['Word Richness'] + '30', color: 'text.primary' }}
              />
              <Chip 
                label={`Relevance: ${selectedEssay?.relevance_marks}`}
                sx={{ backgroundColor: METRIC_COLORS['Relevance'] + '30', color: 'text.primary' }}
              />
              <Chip 
                label={`Spelling: ${selectedEssay?.spelling_marks}`}
                sx={{ backgroundColor: METRIC_COLORS['Spelling'] + '30', color: 'text.primary' }}
              />
              <Chip 
                label={`Grammar: ${selectedEssay?.grammar_marks}`}
                sx={{ backgroundColor: METRIC_COLORS['Grammar'] + '30', color: 'text.primary' }}
              />
              <Chip 
                label={`Total: ${selectedEssay?.total_marks}`}
                color="primary"
              />
            </Box>
          </Box>
          
          <Typography variant="subtitle1" sx={{ mt: 2 }}>Essay Text:</Typography>
          <Paper elevation={0} sx={{ p: 2, mt: 1, backgroundColor: 'background.default' }}>
            <Typography>{selectedEssay?.essay_text}</Typography>
          </Paper>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={Boolean(deleteId)} onClose={() => setDeleteId(null)}>
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete this essay? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteId(null)}>Cancel</Button>
          <Button onClick={confirmDelete} color="error">Delete</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};