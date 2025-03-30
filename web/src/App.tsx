import React from 'react';
import { OpenAPI } from './client';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './pages/Home/Home';
import Unsubscribe from './pages/Unsubscribe';
import { Paper } from '@mui/material';

// Create a custom theme
const theme = createTheme({
  palette: {
    mode: 'dark', // Set the palette mode to dark
    primary: {
      main: '#FFA500', // Orange color for primary
    },
    background: {
      default: '#333333', // Dark gray background
      paper: '#424242', // Darker gray for paper elements
    },
  },
});

OpenAPI.BASE = process.env.REACT_APP_API_URL!;

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <div style={{ maxWidth: '100wh', height: '100vh', background: '#333333', padding: '20px' }}>
        <Paper elevation={3} sx={{ maxWidth: 1000, height: '80vh', margin: 'auto', padding: '20px' }}>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/unsubscribe" element={<Unsubscribe />}>
                <Route path="*" element={<Home />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </Paper>
      </div>
    </ThemeProvider>
  );
};

export default App;
