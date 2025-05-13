from datetime import datetime

def render_outlet_email_template(created=0, lacking=0, discounted=0, archived=0, attributes=0):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f9f9f9;
          padding: 20px;
        }}
        .container {{
          background-color: white;
          border-radius: 8px;
          padding: 30px;
          max-width: 600px;
          margin: auto;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
          color: #333;
          border-bottom: 1px solid #cccccc;
        }}
        p {{
          color: #555;
          font-size: 16px;
        }}
        .footer {{
          margin-top: 20px;
          font-size: 14px;
          color: #999;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Outlety {datetime.now().strftime("%d/%m/%Y, %H:%M")}</h1>
        <p>🎖️ Zaimportowano <strong>{created} produktów.</strong></p>
        <p>🔁 Przeniesiono <strong>{lacking} produktów.</strong> - <em>wymagają one wystawienia ręcznego.</em></p>
        <p>🏷️ Przeceniono <strong>{discounted} produktów.</strong></p>
        <p>📎 Zarchiwizowano i usunięto z Shopera <strong>{archived} produktów.</strong></p>
        <p>📜 Podpięto atrybuty do <strong>{attributes} produktów.</strong></p>
        <div class="footer">
          <em>Do wiadomości załączono logi operacji. Polecam w nie zajrzeć i zobaczyć, czy wszystko przebiegło pomyślnie.</em>
        </div>
      </div>
    </body>
    </html>
    """