// src/Newsletter.tsx
import React, { useEffect, useState } from 'react';
import Timeline from '@mui/lab/Timeline';
import TimelineItem from '@mui/lab/TimelineItem';
import TimelineSeparator from '@mui/lab/TimelineSeparator';
import TimelineConnector from '@mui/lab/TimelineConnector';
import TimelineContent from '@mui/lab/TimelineContent';
import TimelineOppositeContent from '@mui/lab/TimelineOppositeContent';
import TimelineDot from '@mui/lab/TimelineDot';
import { Timer, CheckCircle, QuestionMark } from '@mui/icons-material';
import Typography from '@mui/material/Typography';
import { Button, CircularProgress } from '@mui/material';
import { PollResponse, getPollPollGet } from '../../client';
import moment from 'moment';

const SchedulingState: React.FC = () => {
  const [poll, setPoll] = useState<PollResponse | undefined>(undefined)

  useEffect(() => {
    getPollPollGet()
      .then(poll => setPoll(poll))
      .catch(e => console.log(e))
  }, []);

  return (<>
    {poll === undefined ? <CircularProgress /> :
      <Timeline position="alternate" style={{ width: 700 }}>
        <TimelineItem>
          <TimelineOppositeContent
            sx={{ m: 'auto 0' }}
            align="right"
            variant="body2"
            color="text.secondary"
          >
            {formatDatetime(poll.current_poll_started)}
          </TimelineOppositeContent>
          <TimelineSeparator>
            <TimelineConnector />
            <SuccessIcon />
            <TimelineConnector />
          </TimelineSeparator>
          <TimelineContent sx={{ m: 'auto 0' }}>
            <Typography variant="h6" component="span">
              Poll Created
            </Typography>
          </TimelineContent>
        </TimelineItem>

        <TimelineItem>
          {poll.next_schafkopf_event === null &&
            <TimelineOppositeContent
              sx={{ m: 'auto 0' }}
              align="right"
              variant="body2"
              color="text.secondary"
            >
              <Button variant="outlined" color="primary" onClick={() => window.open(poll.bitpoll_link)}>Vote Now</Button>
            </TimelineOppositeContent>
          }
          <TimelineSeparator>
            <TimelineConnector />
            {poll.next_schafkopf_event === null ?
              <RunningIcon /> : <SuccessIcon />
            }
            <TimelineConnector />
          </TimelineSeparator>
          <TimelineContent sx={{ m: 'auto 0' }}>
            <Typography variant="h6" component="span">
              Waiting for Votes
            </Typography>
          </TimelineContent>
        </TimelineItem>

        <TimelineItem>
          {poll.next_schafkopf_event !== null && <TimelineOppositeContent
            sx={{ m: 'auto 0' }}
            variant="body2"
            color="text.secondary"
          >
            {formatDatetime(poll.next_schafkopf_event!)}
          </TimelineOppositeContent>}
          <TimelineSeparator>
            <TimelineConnector />
            {poll.next_schafkopf_event === null ?
              <PendingIcon /> : <SuccessIcon />
            }
            <TimelineConnector />
          </TimelineSeparator>
          <TimelineContent sx={{ m: 'auto 0' }}>
            <Typography variant="h6" component="span">
              Next Schafkopf Round
            </Typography>
          </TimelineContent>
        </TimelineItem>

        <TimelineItem>
          <TimelineOppositeContent
            sx={{ m: 'auto 0' }}
            variant="body2"
            color="text.secondary"
          >
            {formatDatetime(poll.start_next_poll_date)}
          </TimelineOppositeContent>
          <TimelineSeparator>
            <TimelineConnector />
            <TimelineDot color={poll.next_schafkopf_event === null ? "grey" : "primary"} variant="outlined">
              <Timer />
            </TimelineDot>
            <TimelineConnector />
          </TimelineSeparator>
          <TimelineContent sx={{ m: 'auto 0' }}>
            <Typography variant="h6" component="span">
              New Poll
            </Typography>
          </TimelineContent>
        </TimelineItem>
      </Timeline>
    }</>
  );
};

const SuccessIcon: React.FC = () => {
  return <TimelineDot color="success">
    <CheckCircle />
  </TimelineDot>
}

const RunningIcon: React.FC = () => {
  return <TimelineDot color="grey" variant="outlined">
    <CircularProgress color="primary" style={{ margin: -7, padding: 10 }} />
  </TimelineDot>
}

const PendingIcon: React.FC = () => {
  return <TimelineDot color="grey" variant="outlined">
    <QuestionMark />
  </TimelineDot>
}

const formatDatetime = (d: string) => {

  return moment(d).format("dddd DD.MM.")
}
export default SchedulingState;
