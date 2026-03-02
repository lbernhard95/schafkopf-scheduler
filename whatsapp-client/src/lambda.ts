import type { Handler } from 'aws-lambda';
import { getConfig } from './apps/schafkopf-scheduler/config';
import { SchafkopfScheduler } from './apps/schafkopf-scheduler/scheduler';

export const handler: Handler = async () => {
  const config = getConfig();
  const scheduler = new SchafkopfScheduler(config);
  await scheduler.run();
};
