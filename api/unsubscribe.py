from urllib.parse import urlparse, parse_qs
import os
from supabase import create_client

def handler(request):
    if request.method != 'GET':
        return {'statusCode': 405, 'body': 'Method not allowed'}
    
    url = urlparse(request.url)
    params = parse_qs(url.query)
    email = params.get('email', [''])[0].strip().lower()
    
    if not email:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'text/html'},
            'body': '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>body{font-family:-apple-system,sans-serif;max-width:400px;margin:50px auto;padding:20px;text-align:center}.error{color:#e74c3c;font-size:20px;margin-bottom:20px}</style></head><body><div class="error">Invalid Link</div><p>Missing email address</p></body></html>'
        }
    
    try:
        supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_ANON_KEY'])
        supabase.table('subscribers').delete().eq('email', email).execute()
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>body{{font-family:-apple-system,sans-serif;max-width:400px;margin:50px auto;padding:20px;text-align:center;background:#f8f9fa}}.container{{background:white;padding:30px;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.1)}}.success{{color:#27ae60;font-size:20px;margin-bottom:20px}}</style></head><body><div class="container"><div class="success">Unsubscribed</div><p><strong>{email}</strong> removed from all updates</p></div></body></html>'
        }
        
    except Exception:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/html'},
            'body': '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>body{font-family:-apple-system,sans-serif;max-width:400px;margin:50px auto;padding:20px;text-align:center}.error{color:#e74c3c;font-size:20px;margin-bottom:20px}</style></head><body><div class="error">Error</div><p>Please try again later</p></body></html>'
        }
