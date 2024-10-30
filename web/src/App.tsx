import React from 'react';
import { Button, Typography } from '@mui/material';

const App: React.FC = () => {
  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Welcome to My Material App
      </Typography>
      <Button variant="contained" color="primary">
        Hello Material-UI
      </Button>
    </div>
  );
};

export default App;