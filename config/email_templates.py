from datetime import datetime

def render_outlet_email_template(
        created=0,
        lacking=0,
        discounted=0,
        archived=0,
        activated=0,
        deactivated=0,
        attributes=0,
        category_attributes=0,
        errors=0,
        operation_logs=''):
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
        .logs {{
          background-color: white;
          border-radius: 8px;
          padding: 30px;
          max-width: 800px;
          margin: auto;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Outlety {datetime.now().strftime("%d/%m/%Y, %H:%M")}</h1>
        <p>🎖️ <strong>Zaimportowane produkty</strong>: <strong>{created}</strong></p>
        <p>🔁 <strong>Przeniesione</strong> produkty: <strong>{lacking}</strong> - <em>wymagają one wystawienia ręcznego.</em></p>
        <p>🏷️ <strong>Przecenione</strong> produkty: <strong>{discounted}</strong></p>
        <p>📎 <strong>Zarchiwizowane</strong> i usunięte z Shopera: <strong>{archived}</strong></p>
        <p>😇 <strong>Aktywowane</strong> na Shoperze: <strong>{activated}</strong></p>
        <p>💩 <strong>Deaktywowane</strong> na Shoperze: <strong>{deactivated}</strong></p>
        <p>📜 Liczba głównych produktów z <strong>podpiętymi atrybutami</strong> outletowymi: <strong>{attributes}</strong></p>
        <p>🗃️ Liczba kategorii z <strong>podpiętymi grupami atrybutów</strong>: <strong>{category_attributes}</strong></p>
        <p><strong>Liczba znalezionych błędów: {errors}</strong></p>
        <div class="footer">
          <em>Poniżej znajdują się logi operacji. Polecam w nie zajrzeć i zobaczyć, czy wszystko przebiegło pomyślnie, czy wystąpiły błędy.</em>
        </div>
      </div>
      <div class="logs">
        <h2>Logi operacji</h2>
        {operation_logs}
      </div>
    </body>
    </html>
    """