import { AppBar, Toolbar, Typography, Switch, Button } from '@mui/material';
import { Link } from 'react-router-dom';

export const Navbar = ({ darkMode, toggleDarkMode }) => (
  <AppBar position="static">
    <Toolbar>
      <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
        Sinhala Essay Grader
      </Typography>
      <Button 
        color="inherit" 
        component={Link} 
        to="/" 
        sx={{ mr: 2 }}
      >
        Grade Essay
      </Button>
      <Button 
        color="inherit" 
        component={Link} 
        to="/history"
        sx={{ mr: 2 }}
      >
        History
      </Button>
      <Switch 
        checked={darkMode} 
        onChange={toggleDarkMode} 
        color="secondary" 
      />
    </Toolbar>
  </AppBar>
);