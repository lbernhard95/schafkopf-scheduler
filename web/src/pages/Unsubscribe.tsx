import { CircularProgress, Stack, Typography } from '@mui/material';
import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { deleteSubscriberFromMailingListSubscriberDelete } from '../client';
import { CheckCircle } from '@mui/icons-material';

const Home: React.FC = () => {
    const [searchParams] = useSearchParams();
    const email = searchParams.get("email")
    const [unsubscribed, setUnsubscribed] = useState<boolean>(false)
    const [loading, setLoading] = useState<boolean>(true)

    deleteSubscriberFromMailingListSubscriberDelete({ email: email! })
        .then(() => setUnsubscribed(true))
        .catch(() => setUnsubscribed(false))
        .finally(() => setLoading(false))

    return (<div>
        <Stack spacing={2}
            alignItems="center"
            justifyContent="center">
            {loading ? <CircularProgress />
                : unsubscribed ? <div><CheckCircle color='success' /> <Typography style={{ minHeight: '1em' }}>
                    Succesfully Unsubscribed!
                </Typography></div> : <Typography style={{ minHeight: '1em' }}>
                    Something went wrong :(
                </Typography>
            }
        </Stack>
    </div>
    );
};

export default Home;
