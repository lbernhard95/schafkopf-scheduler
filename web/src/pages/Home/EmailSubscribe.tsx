// src/Newsletter.tsx
import React, { useState } from 'react';
import { TextField, Container, Typography } from '@mui/material';
import { subscribeToSchafkopfRoundsSubscribePost } from '../../client';
import { LoadingButton } from '@mui/lab';

const EmailSubscribe: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [submitted, setSubmitted] = useState<boolean>(false);

  const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    setIsSubmitting(true)
    event.preventDefault();
    subscribeToSchafkopfRoundsSubscribePost({
      requestBody: {
        email: email
      }
    }).then(() => {
      console.log('Email submitted:', email);
      setSubmitted(true);
    }).catch(
        (e) => console.log(e)
    ).finally(() => {
      setEmail('')
      setIsSubmitting(false)
    })
  };

  return (
    <Container component="main" maxWidth="xs">
        {submitted ? (
          <Typography variant="body1" color="primary">
            Thank you for subscribing!
          </Typography>
        ) : (
          <form onSubmit={handleSubmit}>
            <TextField
              label="Email Address"
              variant="outlined"
              fullWidth
              margin="normal"
              value={email}
              onChange={handleEmailChange}
              required
            />
            <LoadingButton loading={isSubmitting} type="submit" variant="contained" color="primary" fullWidth>
              Subscribe
            </LoadingButton>
          </form>
        )}
    </Container>
  );
};

export default EmailSubscribe;
