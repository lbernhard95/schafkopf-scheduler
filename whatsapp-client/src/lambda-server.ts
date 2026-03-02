import { getConfig } from './apps/schafkopf-scheduler/config';
import { SchafkopfScheduler } from './apps/schafkopf-scheduler/scheduler';

const PORT = process.env.PORT || 8080;

Bun.serve({
  port: PORT,
  async fetch(req) {
    const url = new URL(req.url);

    // Health check endpoint
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ status: 'ok' }), {
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Main scheduler endpoint
    if (url.pathname === '/' && req.method === 'GET') {
      try {
        const config = getConfig();
        const scheduler = new SchafkopfScheduler(config);
        const messageId = await scheduler.run();

        return new Response(
          JSON.stringify({
            success: true,
            messageId,
          }),
          {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          }
        );
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return new Response(
          JSON.stringify({
            success: false,
            error: errorMessage,
          }),
          {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
          }
        );
      }
    }

    // 404 for unknown paths
    return new Response(JSON.stringify({ error: 'Not found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' },
    });
  },
});

console.log(`Server running on port ${PORT}`);
