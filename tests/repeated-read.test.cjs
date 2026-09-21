const assert = require('node:assert/strict');
const http = require('node:http');
const path = require('node:path');
const { test } = require('node:test');
const newman = require('newman');

for (const mode of ['stable', 'changed', 'http-error', 'disconnect']) {
  test(`repeated read detects ${mode}`, { timeout: 20000 }, async () => {
    let requests = 0;
    const server = http.createServer((req, res) => {
      assert.equal(req.method, 'GET');
      assert.equal(req.url, '/posts/2');
      requests += 1;
      if (requests === 2 && mode === 'disconnect') {
        req.socket.destroy();
        return;
      }
      const changed = requests === 2 && mode === 'changed';
      const status = requests === 2 && mode === 'http-error' ? 500 : 200;
      res.writeHead(status, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ id: 2, userId: 1, title: changed ? 'changed' : 'same', body: 'text' }));
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    try {
      const summary = await new Promise((resolve, reject) => newman.run({
        collection: path.join(__dirname, '../postman/booking-api.postman_collection.json'),
        folder: 'Idempotency',
        envVar: [{ key: 'baseUrl', value: `http://127.0.0.1:${server.address().port}` }],
        reporters: [],
        timeoutRequest: 1000,
      }, (err, result) => err ? reject(err) : resolve(result)));
      assert.equal(requests, 2, 'must make two independent HTTP requests');
      if (mode === 'stable') {
        assert.equal(summary.run.failures.length, 0);
      } else {
        assert.ok(summary.run.failures.length > 0, 'a broken repeated read must fail the collection');
      }
    } finally {
      server.closeAllConnections();
      await new Promise(resolve => server.close(resolve));
    }
  });
}
