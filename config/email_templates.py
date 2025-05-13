from datetime import datetime

def render_outlet_email_template(created=0, lacking=0, discounted=0, archived=0, attributes=0, errors=0, operation_logs=''):
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
        h2 {{
          color: #333;
          border-bottom: 1px solid #cccccc;
        }}
        .container p {{
          color: #555;
          font-size: 16px;
        }}
        .footer {{
          margin-top: 20px;
          font-size: 14px;
          color: #999;
        }}
        .logs p {{
          font-family: monospace;
          font-size: 12px;
          margin: 0.5rem 0;
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
        <p><strong>Liczba znalezionych błędów: {errors}</strong></p>
        <div class="footer">
          <em>Poniżej znajdują się logi operacji. Polecam w nie zajrzeć i zobaczyć, czy wszystko przebiegło pomyślnie, czy wystąpiły błędy.</em>
        </div>
        <div class="logs">
          <h2>Logi operacji</h2>
          {operation_logs}
        </div>
      </div>
    </body>
    </html>
    """