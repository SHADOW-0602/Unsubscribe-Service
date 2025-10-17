import { createClient } from '@supabase/supabase-js'

export default async function handler(req, res) {
  const { email } = req.query
  
  if (!email) {
    return res.status(400).send(`
      <!DOCTYPE html>
      <html><body>
        <h2>Invalid Link</h2>
        <p>Missing email address</p>
      </body></html>
    `)
  }
  
  try {
    const supabase = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_ANON_KEY
    )
    
    await supabase
      .from('subscribers')
      .delete()
      .eq('email', email.toLowerCase().trim())
    
    res.status(200).send(`
      <!DOCTYPE html>
      <html>
      <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
      <body style="font-family:-apple-system,sans-serif;max-width:400px;margin:50px auto;padding:20px;text-align:center;background:#f8f9fa">
        <div style="background:white;padding:30px;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.1)">
          <div style="color:#27ae60;font-size:20px;margin-bottom:20px">✅ Unsubscribed</div>
          <p><strong>${email}</strong> removed from all updates</p>
        </div>
      </body>
      </html>
    `)
  } catch (error) {
    res.status(500).send(`
      <!DOCTYPE html>
      <html><body>
        <h2>Error</h2>
        <p>Please try again later</p>
      </body></html>
    `)
  }
}