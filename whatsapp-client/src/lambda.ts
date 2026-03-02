import type { Handler } from 'aws-lambda';
import { loadConfig, getDefaultConfigPath } from './apps/schafkopf-scheduler/config';
import { SchafkopfScheduler } from './apps/schafkopf-scheduler/scheduler';

export const handler: Handler = async () => {
  const config = loadConfig(getDefaultConfigPath());
  const scheduler = new SchafkopfScheduler(config);
  await scheduler.run();
};
