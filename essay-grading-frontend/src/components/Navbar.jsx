import { AppBar, Toolbar, Typography, IconButton, Switch } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

export const Navbar = ({ darkMode, toggleDarkMode }) => (
  <AppBar position="static">
    <Toolbar>
      <IconButton edge="start" color="inherit" aria-label="menu">
        <MenuIcon />
      </IconButton>
      <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
        Sinhala Essay Grader
      </Typography>
      <Switch checked={darkMode} onChange={toggleDarkMode} color="secondary" />
    </Toolbar>
  </AppBar>
);