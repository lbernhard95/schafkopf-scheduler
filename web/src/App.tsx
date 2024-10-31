import React, {useEffect, useState } from 'react';
import {Stack, Paper, Typography } from '@mui/material';
import { OpenAPI, SubscribeCountResponse, getSubscriberCountSubscribersCountGet } from './client';
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
  const [memberCount, setMemberCount] = useState<SubscribeCountResponse | undefined>()
  useEffect(() => {
    getSubscriberCountSubscribersCountGet()
        .then(d => setMemberCount(d))
        .catch(e => console.log(e))
  }, []);
  return (
    <ThemeProvider theme={theme}>
      <Paper elevation={3} sx={{ maxWidth: 1000, height: '80vh', margin: 'auto', marginTop: "15px", padding: '20px' }}>
        <Stack spacing={2}
          alignItems="center"
          justifyContent="center" >
          <CssBaseline/>
          <Typography variant="h4" component="h1" gutterBottom={false}>
            [at] Schafkopf Group
          </Typography>
          <Typography style={{ minHeight: '1em' }}>
            {memberCount !== undefined ? `Already ${memberCount.count} members subscribed` : "\u00A0"}
          </Typography>
          <EmailSubscribe/>
        </Stack>
        <div  style={{ marginTop: 50}}>
        <Stack spacing={2}
        alignItems="center"
        justifyContent="center">
          <SchedulingState/>
        </Stack>
          </div>
      </Paper>
    </ThemeProvider>
  );
};

export default App;