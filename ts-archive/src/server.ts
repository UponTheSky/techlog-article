import http from 'http';
import { app } from './app';

import { PORT } from './utils/config';
import * as logger from './utils/logger';

const httpServer = http.createServer(app);

httpServer.listen(PORT, () => {
  logger.info(`The HTTP server running on ${PORT}`);
});

/**
 *
 * You may do for the HTTPS protocol
 *
 * import https from 'https';
 *
 * const httpsServer = https.createServer(app);
 * httpsServer.listen(PORT, () => {});
 */
