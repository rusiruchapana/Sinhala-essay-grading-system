import { useState, useMemo } from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { lightTheme, darkTheme } from './styles/theme';
import { Navbar } from './components/Navbar';
import { GradingPage } from './pages/GradingPage';

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const theme = useMemo(() => darkMode ? darkTheme : lightTheme, [darkMode]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Navbar 
          darkMode={darkMode} 
          toggleDarkMode={() => setDarkMode(!darkMode)} 
        />
        <Routes>
          <Route path="/" element={<GradingPage />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;