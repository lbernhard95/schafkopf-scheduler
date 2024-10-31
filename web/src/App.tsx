import React from 'react';
import {Container, Paper, Typography } from '@mui/material';
import { OpenAPI } from './client';
import EmailSubscribe from './pages/EmailSubscribe';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

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
    <Container component="main" maxWidth="lg" style={{ paddingTop: '20px'}}>
      <Paper elevation={3} style={{ padding: '20px', textAlign: 'center' }}>
      <Typography variant="h4" component="h1" gutterBottom>
        [at] Schafkopf Group
      </Typography>
        <CssBaseline/>
        <EmailSubscribe/>
      </Paper>
    </Container>
    </ThemeProvider>
  );
};

export default App;