from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
from supabase import create_client

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        
        if url.path == '/unsubscribe' or 'email=' in url.query:
            params = parse_qs(url.query)
            email = params.get('email', [''])[0].strip().lower() if params.get('email') else ''
            
            if not email:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<!DOCTYPE html><html><body>Invalid Link</body></html>')
                return
            
            try:
                supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_ANON_KEY'])
                supabase.table('subscribers').delete().eq('email', email).execute()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html = f'<!DOCTYPE html><html><body>Unsubscribed: {email}</body></html>'
                self.wfile.write(html.encode())
                
            except Exception:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<!DOCTYPE html><html><body>Error</body></html>')
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<!DOCTYPE html><html><body><h1>Unsubscribe Service</h1><p>Add ?email=your@email.com to unsubscribe</p></body></html>')
