import React from 'react';
import { Button, Typography } from '@mui/material';
import { OpenAPI, helloGet } from './client';

OpenAPI.BASE = process.env.REACT_APP_API_URL!;

const App: React.FC = () => {

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Welcome to My Material App
      </Typography>
      <Button variant="contained" color="primary" onClick={() => {
         helloGet().then(msg => console.log("data", msg)).catch(e => console.log("error", e))
      }}>
        Hello Material-UI
      </Button>
    </div>
  );
};

export default App;