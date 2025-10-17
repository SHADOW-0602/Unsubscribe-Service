from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
from supabase import create_client

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        params = parse_qs(url.query)
        email = params.get('email', [''])[0].strip().lower()
        
        if not email:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>body{font-family:-apple-system,sans-serif;max-width:400px;margin:50px auto;padding:20px;text-align:center}.error{color:#e74c3c;font-size:20px;margin-bottom:20px}</style></head><body><div class="error">Invalid Link</div><p>Missing email address</p></body></html>')
            return
        
        try:
            supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_ANON_KEY'])
            supabase.table('subscribers').delete().eq('email', email).execute()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>body{{font-family:-apple-system,sans-serif;max-width:400px;margin:50px auto;padding:20px;text-align:center;background:#f8f9fa}}.container{{background:white;padding:30px;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.1)}}.success{{color:#27ae60;font-size:20px;margin-bottom:20px}}</style></head><body><div class="container"><div class="success">Unsubscribed</div><p><strong>{email}</strong> removed from all updates</p></div></body></html>'
            self.wfile.write(html.encode())
            
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>body{font-family:-apple-system,sans-serif;max-width:400px;margin:50px auto;padding:20px;text-align:center}.error{color:#e74c3c;font-size:20px;margin-bottom:20px}</style></head><body><div class="error">Error</div><p>Please try again later</p></body></html>')
