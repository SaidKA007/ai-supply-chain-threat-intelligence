"""One-shot loopback HTTP demonstration. No shell and no real file collection.

This packaging-time helper adds stricter validation than the original notebook.
It only sends this module's fixed fictional payload to 127.0.0.1.
"""
from datetime import datetime, timezone
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import hashlib
import json
import threading

DEMO_PAYLOAD = {
    'company': 'NIGHTMARE AI LAB',
    'classification': 'FICTIONAL DATA',
    'api_key': 'DEMO-ONLY',
    'simulation': True,
}


def send_fictional_data(output: Path) -> dict:
    """Start receiver, send fixed JSON, verify bytes and stop the server."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    # Each call uses an in-memory receipt; an old file cannot prove a new transfer.
    receipt = {}
    body = json.dumps(DEMO_PAYLOAD, sort_keys=True).encode('utf-8')
    digest = hashlib.sha256(body).hexdigest()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            self.connection.settimeout(5)
            if self.path != '/receive':
                self.send_error(404)
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
            except ValueError:
                self.send_error(400)
                return
            if not 0 < length <= 4096:
                self.send_error(413)
                return
            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw)
            except (ValueError, UnicodeError):
                self.send_error(400)
                return
            if payload != DEMO_PAYLOAD:
                self.send_error(400, 'Only the fixed fictional lab payload is accepted')
                return
            (output / 'received_demo_payload.json').write_bytes(raw)
            receipt.update({
                'timestamp_utc': datetime.now(timezone.utc).isoformat(),
                'client_host': self.client_address[0],
                'method': 'POST', 'path': self.path,
                'received_bytes': len(raw),
                'received_sha256': hashlib.sha256(raw).hexdigest(),
            })
            reply = b'RECEIVED'
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(reply)))
            self.end_headers()
            self.wfile.write(reply)

        def log_message(self, *args):
            pass

    server = HTTPServer(('127.0.0.1', 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    connection = HTTPConnection('127.0.0.1', port, timeout=10)
    thread.start()
    try:
        # HTTPConnection goes directly to loopback; no proxy or public tunnel.
        connection.request('POST', '/receive', body=body,
                           headers={'Content-Type': 'application/json'})
        response = connection.getresponse()
        response_body = response.read().decode('utf-8')
        if response.status != 200 or response_body != 'RECEIVED':
            raise RuntimeError(f'Transfer failed: HTTP {response.status}: {response_body}')
        if receipt.get('received_sha256') != digest:
            raise RuntimeError('Server receipt does not match this request body.')
        result = {
            'provenance': 'New local verification run; not historical Colab evidence.',
            'destination': f'127.0.0.1:{port}',
            'status': response.status, 'response': response_body,
            'sent_sha256': digest, 'receipt': receipt,
            'same_runtime_only': True, 'model_sends_request': False,
        }
        (output / 'http_receipt.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(f'Loopback HTTP POST: {result["destination"]} | {result["status"]} {response_body}')
        print('Fixed fictional payload verified. No remote shell or off-host transfer.')
        return result
    finally:
        connection.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
