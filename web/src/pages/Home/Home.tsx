import React, { useEffect, useState } from 'react';
import { Stack, Typography } from '@mui/material';
import { SubscribeCountResponse, getSubscriberCountSubscribersCountGet } from '../../client';
import EmailSubscribe from './EmailSubscribe';
import { CssBaseline } from '@mui/material';
import SchedulingState from './SchedulingState';


const Home: React.FC = () => {
    const [memberCount, setMemberCount] = useState<SubscribeCountResponse | undefined>()
    useEffect(() => {
        getSubscriberCountSubscribersCountGet()
            .then(d => setMemberCount(d))
            .catch(e => console.log(e))
    }, []);
    return (
        <div>
            <Stack spacing={2}
                alignItems="center"
                justifyContent="center" >
                <CssBaseline />
                <Typography variant="h4" component="h1" gutterBottom={false}>
                    [at] Schafkopf Group
                </Typography>
                <Typography style={{ minHeight: '1em' }}>
                    {memberCount !== undefined ? `Already ${memberCount.count} members subscribed` : "\u00A0"}
                </Typography>
                <EmailSubscribe />
            </Stack>
            <div style={{ marginTop: 50 }}>
                <Stack spacing={2}
                    alignItems="center"
                    justifyContent="center">
                    <SchedulingState />
                </Stack>
            </div>
        </div>
    );
};

export default Home;