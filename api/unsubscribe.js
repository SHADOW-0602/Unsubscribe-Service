const { createClient } = require('@supabase/supabase-js')

module.exports = async function handler(req, res) {
  // Handle both query params and URL path
  let email = req.query.email || req.query.e
  
  // Extract email from URL path if not in query
  if (!email && req.url) {
    const match = req.url.match(/[?&]email=([^&]+)/)
    if (match) email = decodeURIComponent(match[1])
  }
  
  if (!email) {
    return res.status(200).send(`
      <!DOCTYPE html>
      <html>
      <head><meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>body{font-family:-apple-system,sans-serif;max-width:400px;margin:50px auto;padding:20px;text-align:center}</style></head>
      <body>
        <h2>Unsubscribe Service</h2>
        <p>Please use the unsubscribe link from your email</p>
      </body></html>
    `)
  }
  
  try {
    const supabase = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_ANON_KEY
    )
    
    await supabase
      .from('email_subscriptions')
      .delete()
      .eq('email', email.toLowerCase().trim())
    
    res.status(200).send(`
      <!DOCTYPE html>
      <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta charset="UTF-8">
        <title>Unsubscribed Successfully</title>
        <style>
          body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin:0;padding:20px;background:#f8f9fa;color:#333}
          .container{max-width:400px;margin:50px auto;background:white;padding:40px 20px;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.1);text-align:center}
          .success{color:#27ae60;font-size:24px;margin-bottom:20px;font-weight:600}
          .email{color:#2c3e50;font-weight:bold;word-break:break-all}
          .message{color:#666;margin-top:20px;font-size:14px}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="success">✓ Successfully Unsubscribed</div>
          <p>The email address</p>
          <p class="email">${email}</p>
          <p>has been removed from all updates</p>
          <p class="message">You will no longer receive weekly market reports</p>
        </div>
      </body>
      </html>
    `)
  } catch (error) {
    res.status(500).send(`
      <!DOCTYPE html>
      <html>
      <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
      <body style="font-family:-apple-system,sans-serif;max-width:400px;margin:50px auto;padding:20px;text-align:center">
        <h2 style="color:#e74c3c">Error</h2>
        <p>Unable to process unsubscribe request</p>
        <p style="font-size:14px;color:#666">Please try again later or contact support</p>
      </body></html>
    `)
  }
}
