from datetime import datetime

EMAIL_STYLING = """
      <style>
        body {
          font-family: Arial, sans-serif;
          background-color: #f9f9f9;
          padding: 20px;
        }
        .container {
          background-color: white;
          border-radius: 8px;
          padding: 30px;
          max-width: 600px;
          margin: auto;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
          color: #333;
          border-bottom: 1px solid #cccccc;
        }
        h2 {
          color: #333;
          border-bottom: 1px solid #cccccc;
        }
        .container p {
          color: #555;
          font-size: 16px;
        }
        .footer {
          margin-top: 20px;
          font-size: 14px;
          color: #999;
        }
        .logs p {
          font-family: monospace;
          font-size: 12px;
          margin: 0.5rem 0;
        }
        .logs {
          background-color: white;
          border-radius: 8px;
          padding: 30px;
          max-width: 800px;
          margin: auto;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
      </style>
"""

def render_outlet_email_template(
        created,
        lacking,
        discounted,
        redirects_removed,
        archived,
        activated,
        deactivated,
        attributes,
        category_attributes,
        errors,
        operation_logs=''):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      {EMAIL_STYLING}
    </head>
    <body>
      <div class="container">
        <h1>Outlety {datetime.now().strftime("%d/%m/%Y, %H:%M")}</h1>
        <p>🎖️ <strong>Zaimportowane</strong> produkty: <strong>{created}</strong></p>
        <p>💾 <strong>Przeniesione</strong> produkty: <strong>{lacking}</strong> - <em>wymagają one wystawienia ręcznego.</em></p>
        <p>🏷️ <strong>Przecenione</strong> produkty: <strong>{discounted}</strong></p>
        <p>🔁 <strong>Usunięte</strong> przekierowania: <strong>{redirects_removed}</strong></p>
        <p>📎 <strong>Zarchiwizowane</strong> i usunięte z Shopera: <strong>{archived}</strong></p>
        <p>😇 <strong>Aktywowane</strong> na Shoperze: <strong>{activated}</strong></p>
        <p>💩 <strong>Deaktywowane</strong> na Shoperze: <strong>{deactivated}</strong></p>
        <p>📜 Liczba głównych produktów z <strong>podpiętymi atrybutami</strong> outletowymi: <strong>{attributes}</strong></p>
        <p>🗃️ Liczba kategorii z <strong>podpiętymi grupami atrybutów</strong>: <strong>{category_attributes}</strong></p>
        <p><strong>Liczba znalezionych błędów: {errors}</strong></p>
        <div class="footer">
          <em>Poniżej znajdują się logi operacji. Polecam w nie zajrzeć jeżeli wystąpiły błędy.</em>
        </div>
      </div>
      <div class="logs">
        <h2>Logi operacji</h2>
        {operation_logs}
      </div>
    </body>
    </html>
    """

def render_promo_email_template(
        created_promo_allegro=0,
        ommited_promo_allegro=0,
        removed_promo_allegro=0,
        ommited_promo_allegro_early=0,
        errors=0,
        operation_logs=''):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      {EMAIL_STYLING}
    </head>
    <body>
      <div class="container">
        <h1>Promocje {datetime.now().strftime("%d/%m/%Y, %H:%M")}</h1>
        <p>🎖️ <strong>Zaimportowane</strong> promocje: <strong>{created_promo_allegro}</strong></p>
        <p>🔁 <strong>Pominięte</strong> promocje: <strong>{ommited_promo_allegro}</strong> - <em>produkt już posiada promocję.</em></p>
        <p>📅 <strong>Pominięte</strong> promocje: <strong>{ommited_promo_allegro_early}</strong> - <em>za wcześnie na promocję.</em></p>
        <p>🏷️ <strong>Usunięte</strong> promocje: <strong>{removed_promo_allegro}</strong></p>
        <p><strong>Liczba znalezionych błędów: {errors}</strong></p>
        <div class="footer">
          <em>Poniżej znajdują się logi operacji. Polecam w nie zajrzeć jeżeli wystąpiły błędy</em>
        </div>
      </div>
      <div class="logs">
        <h2>Logi operacji</h2>
        {operation_logs}
      </div>
    </body>
    </html>
    """