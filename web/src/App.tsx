import React from 'react';
import { Button, Typography } from '@mui/material';
import {Api} from "./api/Api";

const App: React.FC = () => {

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Welcome to My Material App
      </Typography>
      <Button variant="contained" color="primary" onClick={() => {
          new Api().helloGet().then(msg => console.log(msg))
      }}>
        Hello Material-UI
      </Button>
    </div>
  );
};

export default App;