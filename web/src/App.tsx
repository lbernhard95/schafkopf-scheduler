import React from 'react';
import {Stack, Paper, Typography, Divider } from '@mui/material';
import { OpenAPI } from './client';
import EmailSubscribe from './pages/EmailSubscribe';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import SchedulingState from './pages/SchedulingState';

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
      <Paper elevation={3} sx={{ maxWidth: 1000, height: '80vh', margin: 'auto', marginTop: "15px", padding: '20px' }}>
        <Stack spacing={2}
        alignItems="center"
        justifyContent="center"
        sx={{ height: '100%' }} >
          <Typography variant="h4" component="h1" gutterBottom>
            [at] Schafkopf Group
          </Typography>
          <CssBaseline/>
          <EmailSubscribe/>
          <Divider></Divider>
          <SchedulingState/>
        </Stack>
      </Paper>
    </ThemeProvider>
  );
};

export default App;