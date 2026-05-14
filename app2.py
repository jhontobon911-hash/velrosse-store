from flask import Flask, render_template_string, request, send_from_directory, make_response
from flask_mail import Mail, Message
import os
import threading

app = Flask(__name__)

# --- CONFIGURACIÓN DE CORREO VELROSSE STORE ---
# Usamos el puerto 465 con SSL para Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'velrossestore@gmail.com'
# Contraseña de aplicación (Limpia sin espacios invisibles)
app.config['MAIL_PASSWORD'] = 'yttpwcijszdjkdny' 
app.config['MAIL_DEFAULT_SENDER'] = ('Velrosse Store', 'velrossestore@gmail.com')

mail = Mail(app)

# Función para enviar el correo sin bloquear la carga de la página de éxito
def send_async_email(app_instance, msg):
    with app_instance.app_context():
        try:
            mail.send(msg)
            print("✅ [SERVER]: Correo enviado exitosamente a velrossestore@gmail.com")
        except Exception as e:
            print(f"❌ [SERVER] Error enviando correo: {str(e)}")

@app.route('/imagenes_fajas/<path:filename>')
def serve_fajas(filename):
    return send_from_directory('static', filename)

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Velrosse Store - Faja Moldeadora</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --gold: #b28d42; --pink: #e91e63; --black: #000; --light-gold: #fdf7eb; --dark-blue: #1a3a3a; }
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; background: #fff; color: #333; }
        
        .top-bar { background: #000; color: #fff; display: grid; grid-template-columns: repeat(3, 1fr); padding: 10px; font-size: 11px; text-align: center; border-bottom: 2px solid var(--gold); }
        .top-item { display: flex; align-items: center; justify-content: center; gap: 8px; }
        .top-item i { font-size: 18px; color: var(--gold); }

        .container { max-width: 1200px; margin: auto; padding: 20px; }

        .header-section { text-align: center; margin-bottom: 30px; }
        .brand-name { font-size: 40px; font-weight: 900; color: var(--gold); margin: 0; text-transform: uppercase; }
        .product-title { font-size: 32px; font-weight: 800; margin: 0; text-transform: uppercase; }
        .sub-desc { color: #666; font-size: 16px; margin-top: 5px; }
        .social-proof { background: #000; color: #fff; display: inline-block; padding: 5px 20px; border-radius: 50px; font-size: 12px; margin-top: 15px; font-weight: bold; }

        .main-grid { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 30px; margin-top: 20px; }

        .gallery-box { display: flex; gap: 15px; }
        .thumbs-list { display: flex; flex-direction: column; gap: 10px; max-height: 550px; overflow-y: auto; }
        .thumbs-list img { width: 70px; height: 95px; object-fit: cover; border-radius: 5px; cursor: pointer; border: 1px solid #ddd; }
        .main-img-box { flex-grow: 1; border: 1px solid #eee; border-radius: 10px; overflow: hidden; height: 550px; }
        .main-img-box img { width: 100%; height: 100%; object-fit: cover; }

        .purchase-box { border: 1px solid #eee; border-radius: 15px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
        .offer-timer { background: var(--light-gold); border: 1px dashed var(--gold); padding: 15px; text-align: center; border-radius: 10px; margin-bottom: 20px; }
        .timer-label { font-size: 14px; font-weight: bold; color: var(--gold); text-transform: uppercase; }
        .timer-clock { font-size: 35px; font-weight: 900; color: #000; }
        
        .price-row { display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }
        .price-now { font-size: 55px; font-weight: 900; color: var(--gold); }
        .discount-tag { background: var(--pink); color: #fff; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
        .payment-info { font-size: 14px; font-weight: bold; margin-bottom: 20px; display: flex; align-items: center; gap: 5px; }

        .sel-title { font-size: 13px; font-weight: 800; text-transform: uppercase; margin: 15px 0 10px; display: block; color: #000; }
        .qty-selector { width: 100%; padding: 12px; border-radius: 8px; border: 2px solid var(--gold); font-weight: bold; margin-bottom: 15px; }

        .item-selection-box { background: #fdfdfd; border: 1px solid #eee; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
        .radio-flex { display: flex; gap: 10px; margin-bottom: 10px; }
        .radio-btn { flex: 1; border: 1px solid #ddd; padding: 10px; border-radius: 8px; text-align: center; cursor: pointer; font-weight: bold; font-size: 13px; position: relative; }
        .radio-btn input { position: absolute; opacity: 0; }
        .radio-btn:has(input:checked) { border: 2px solid #000; background: #f9f9f9; }

        .input-group { position: relative; margin-bottom: 10px; }
        .input-group i { position: absolute; left: 15px; top: 15px; color: var(--gold); }
        .field { width: 100%; padding: 15px 15px 15px 45px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 15px; }

        .btn-submit { 
            background: var(--pink); color: #fff; border: none; width: 100%; padding: 25px; border-radius: 10px; 
            font-size: 24px; font-weight: 900; cursor: pointer; text-transform: uppercase; margin-top: 15px;
            animation: shake 0.5s infinite;
        }
        @keyframes shake {
            0% { transform: translate(1px, 1px) rotate(0deg); }
            10% { transform: translate(-1px, -2px) rotate(-1deg); }
            30% { transform: translate(3px, 2px) rotate(0deg); }
            50% { transform: translate(-1px, 2px) rotate(1deg); }
            70% { transform: translate(3px, 1px) rotate(-1deg); }
            90% { transform: translate(1px, 2px) rotate(0deg); }
            100% { transform: translate(1px, -2px) rotate(-1deg); }
        }

        .size-table-container { 
            margin: 50px auto; 
            max-width: 550px; 
            background: #fff;
            padding: 10px;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        }
        .size-table { 
            width: 100%; 
            border-collapse: separate; 
            border-spacing: 0;
            text-align: center; 
            font-size: 12px; 
            border: 1px solid #eee;
            border-radius: 8px;
            overflow: hidden;
        }
        .table-header-main { 
            background: var(--dark-blue) !important; 
            color: #fff !important; 
            font-size: 16px; 
            padding: 15px !important;
            letter-spacing: 3px;
            font-weight: 900;
        }
        .size-table thead tr:last-child th {
            background: #f8f9fa;
            color: var(--black);
            padding: 12px 5px;
            text-transform: uppercase;
            font-weight: 800;
            border-bottom: 2px solid var(--gold);
        }
        .size-table tbody tr:nth-child(even) { background: #fafafa; }
        .size-table tbody tr:hover { background: var(--light-gold); transition: 0.3s; }
        .size-table td { 
            padding: 12px 5px; 
            border-bottom: 1px solid #eee; 
            color: #444;
            font-weight: 600;
        }
        .size-table td:first-child { color: var(--pink); font-weight: 900; }

        .features-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 40px 0; }
        .feature-card { background: var(--light-gold); padding: 20px; text-align: center; border-radius: 10px; }
        .feature-card i { font-size: 24px; color: var(--gold); margin-bottom: 10px; display: block; }
        .feature-card span { font-size: 12px; font-weight: bold; line-height: 1.2; display: block; }

        .footer-black { background: #000; color: #fff; padding: 40px 20px; margin-top: 60px; }
        .footer-grid { max-width: 1200px; margin: auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: center; }
        .footer-item i { font-size: 30px; color: var(--gold); margin-bottom: 15px; display: block; }

        #successModal { 
            display: {% if success %} flex {% else %} none {% endif %}; 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 10000; justify-content: center; align-items: center;
        }
        .modal-content { background: #fff; padding: 40px; border-radius: 20px; text-align: center; max-width: 450px; border: 3px solid var(--gold); }
        .modal-content h2 { color: #28a745; margin-bottom: 15px; }
        .wa-btn { background: #25D366; color: white; padding: 15px 25px; border-radius: 50px; text-decoration: none; display: inline-block; margin-top: 20px; font-weight: 900; font-size: 20px; }
        
        @media (max-width: 768px) {
            .main-grid { grid-template-columns: 1fr; }
            .features-grid { grid-template-columns: repeat(2, 1fr); }
            .footer-grid { grid-template-columns: repeat(2, 1fr); }
            .brand-name { font-size: 30px; }
            .size-table-container { max-width: 95%; } 
        }
    </style>
</head>
<body>

    <div id="successModal">
        <div class="modal-content">
            <i class="fa-solid fa-circle-check" style="font-size: 60px; color: #28a745;"></i>
            <h2>¡GRACIAS POR TU COMPRA!</h2>
            <p>Su pedido está en proceso de alistamiento y envío.</p>
            <p>En caso de tener alguna pregunta puedes escribirnos a nuestro WhatsApp:</p>
            <a href="https://wa.me/573169641418" class="wa-btn"><i class="fa-brands fa-whatsapp"></i> +57 316 964 14 18</a>
            <br><br>
            <a href="/" style="color: #888; text-decoration: none; font-size: 12px;">VOLVER</a>
        </div>
    </div>

    <div class="top-bar">
        <div class="top-item"><i class="fa-solid fa-truck-fast"></i> <div>ENVÍO GRATIS<br><small>A TODA COLOMBIA</small></div></div>
        <div class="top-item"><i class="fa-solid fa-hand-holding-dollar"></i> <div>PAGA AL RECIBIR<br><small>SIN PAGOS ADELANTADOS</small></div></div>
        <div class="top-item"><i class="fa-solid fa-shield-halved"></i> <div>COMPRA SEGURA<br><small>DATOS PROTEGIDOS</small></div></div>
    </div>

    <div class="container">
        <div class="header-section">
            <h1 class="product-title">FAJA MOLDEADORA</h1>
            <h2 class="brand-name">VELROSSE STORE</h2>
            <p class="sub-desc">Moldea tu cintura, reduce medidas y mejora tu postura con máxima comodidad.</p>
            <div class="social-proof"><i class="fa-solid fa-star"></i> MILES DE MUJERES YA TRANSFORMARON SU CUERPO</div>
        </div>

        <div class="main-grid">
            <div class="gallery-box">
                <div class="thumbs-list">
                    {% for i in range(1, 8) %}
                    <img src="/imagenes_fajas/faja ({{i}}).jpg" onclick="document.getElementById('mainPhoto').src=this.src">
                    {% endfor %}
                </div>
                <div class="main-img-box">
                    <img src="/imagenes_fajas/faja (1).jpg" id="mainPhoto">
                </div>
            </div>

            <div class="purchase-box">
                <div class="offer-timer">
                    <div class="timer-label">¡Oferta por tiempo limitado!</div>
                    <div class="timer-clock" id="timer">02 : 47 : 35</div>
                </div>

                <div class="price-row">
                    <div style="display:flex; flex-direction:column;">
                        <span style="text-decoration:line-through; color:#999;">ANTES: $159.900</span>
                        <span class="price-now">$89.900</span>
                    </div>
                    <div class="discount-tag">45%<br>DTO.</div>
                </div>
                <div class="payment-info"><i class="fa-solid fa-house-chimney-check" style="color:var(--gold);"></i> PAGA AL RECIBIR EN LA PUERTA DE TU CASA</div>

                <form method="POST">
                    <span class="sel-title">¿Cuántas fajas deseas llevar?</span>
                    <select name="cantidad" id="qtySelect" class="qty-selector" onchange="generateSelectors()">
                        <option value="1">Llevar 1 Unidad - $89.900</option>
                        <option value="2">Llevar 2 Unidades - $179.800</option>
                        <option value="3">Llevar 3 Unidades - $269.700</option>
                    </select>

                    <div id="dynamicSelectors"></div>

                    <span class="sel-title">Datos de Envío</span>
                    <div class="input-group"><i class="fa-solid fa-user"></i><input type="text" name="nombre" class="field" placeholder="Nombre completo" required></div>
                    <div class="input-group"><i class="fa-solid fa-phone"></i><input type="tel" name="celular" class="field" placeholder="Número de celular" required></div>
                    <div class="input-group"><i class="fa-solid fa-id-card"></i><input type="text" name="cedula" class="field" placeholder="Número de cédula" required></div>
                    <div class="input-group"><i class="fa-solid fa-location-dot"></i><input type="text" name="ciudad" class="field" placeholder="Ciudad" required></div>
                    <div class="input-group"><i class="fa-solid fa-map-pin"></i><input type="text" name="direccion" class="field" placeholder="Dirección de entrega" required></div>

                    <button type="submit" class="btn-submit">COMPRAR AHORA<br><small style="font-size:12px;">PAGA AL RECIBIR</small></button>
                </form>
            </div>
        </div>

        <div class="size-table-container">
            <table class="size-table">
                <thead>
                    <tr><th colspan="4" class="table-header-main">TABLA DE MEDIDAS</th></tr>
                    <tr>
                        <th>Talla</th>
                        <th>Jeans</th>
                        <th>Cintura</th>
                        <th>Cadera</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>XS</td><td>6</td><td>60-67 CM</td><td>84-90 CM</td></tr>
                    <tr><td>S</td><td>8</td><td>68-75 CM</td><td>91-98 CM</td></tr>
                    <tr><td>M</td><td>10</td><td>76-83 CM</td><td>99-106 CM</td></tr>
                    <tr><td>L</td><td>12</td><td>84-91 CM</td><td>107-114 CM</td></tr>
                    <tr><td>XL</td><td>14</td><td>92-99 CM</td><td>115-122 CM</td></tr>
                    <tr><td>2XL</td><td>16-18</td><td>100-107 CM</td><td>123-130 CM</td></tr>
                </tbody>
            </table>
        </div>

        <div class="features-grid">
            <div class="feature-card"><i class="fa-solid fa-vest"></i><span>Moldea tu cintura<br>y reduce medidas</span></div>
            <div class="feature-card"><i class="fa-solid fa-person-rays"></i><span>Mejora tu postura<br>y alivia el dolor</span></div>
            <div class="feature-card"><i class="fa-solid fa-calendar-check"></i><span>Uso diario<br>y postparto</span></div>
            <div class="feature-card"><i class="fa-solid fa-gem"></i><span>Material premium<br>transpirable</span></div>
        </div>
    </div>

    <div class="footer-black">
        <div class="footer-grid">
            <div class="footer-item"><i class="fa-solid fa-box-open"></i><strong>ENVÍO GRATIS</strong><br><small>A toda Colombia</small></div>
            <div class="footer-item"><i class="fa-solid fa-handshake"></i><strong>PAGA AL RECIBIR</strong><br><small>Cancela al recibir</small></div>
            <div class="footer-item"><i class="fa-solid fa-lock"></i><strong>COMPRA SEGURA</strong><br><small>Datos protegidos</small></div>
            <div class="footer-item"><i class="fa-solid fa-award"></i><strong>GARANTÍA</strong><br><small>Por defectos de fábrica</small></div>
        </div>
    </div>

    <script>
        function generateSelectors() {
            const qty = document.getElementById('qtySelect').value;
            const container = document.getElementById('dynamicSelectors');
            container.innerHTML = '';
            for (let i = 1; i <= qty; i++) {
                container.innerHTML += `
                    <div class="item-selection-box">
                        <strong style="display:block; margin-bottom:10px; color:var(--pink);">Faja #${i}</strong>
                        <span class="sel-title">Color</span>
                        <div class="radio-flex">
                            <label class="radio-btn"><input type="radio" name="color_${i}" value="Negro" checked> NEGRO</label>
                            <label class="radio-btn"><input type="radio" name="color_${i}" value="Beige"> BEIGE</label>
                        </div>
                        <span class="sel-title">Talla</span>
                        <div style="display:grid; grid-template-columns: repeat(3,1fr); gap:5px;">
                            ${['XS', 'S', 'M', 'L', 'XL', '2XL'].map(t => `
                                <label class="radio-btn"><input type="radio" name="talla_${i}" value="${t}" required> ${t}</label>
                            `).join('')}
                        </div>
                    </div>
                `;
            }
        }
        window.onload = generateSelectors;

        let time = 10055;
        setInterval(() => {
            let h = Math.floor(time / 3600);
            let m = Math.floor((time % 3600) / 60);
            let s = time % 60;
            document.getElementById('timer').innerText = `${h<10?'0'+h:h} : ${m<10?'0'+m:m} : ${s<10?'0'+s:s}`;
            if(time > 0) time--;
        }, 1000);
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    success = False
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        celular = request.form.get('celular')
        cedula = request.form.get('cedula')
        ciudad = request.form.get('ciudad')
        direccion = request.form.get('direccion')
        cantidad = int(request.form.get('cantidad', 1))

        detalles_pedido = ""
        for i in range(1, cantidad + 1):
            color = request.form.get(f'color_{i}')
            talla = request.form.get(f'talla_{i}')
            detalles_pedido += f"• Faja #{i}: Talla {talla}, Color {color}\n"

        msg = Message(
            subject=f"NUEVA VENTA ({cantidad} UNID): {nombre}", 
            recipients=['velrossestore@gmail.com']
        )
        msg.body = (
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"        NUEVA VENTA - VELROSSE STORE     \n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📦 RESUMEN DEL PEDIDO:\n"
            f"----------------------------------------\n"
            f"Cantidad Total: {cantidad}\n"
            f"{detalles_pedido}\n"
            f"👤 DATOS DEL CLIENTE:\n"
            f"----------------------------------------\n"
            f"Nombre:    {nombre}\n"
            f"Celular:   {celular}\n"
            f"Cédula:    {cedula}\n\n"
            f"📍 DIRECCIÓN DE ENVÍO:\n"
            f"----------------------------------------\n"
            f"Ciudad:    {ciudad}\n"
            f"Dirección: {direccion}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"         PAGO AL RECIBIR EN CASA            \n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        
        # Enviar el correo en segundo plano
        threading.Thread(target=send_async_email, args=(app, msg)).start()
        success = True 

    response = make_response(render_template_string(HTML_LAYOUT, success=success))
    response.headers['ngrok-skip-browser-warning'] = '69420'
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # Para producción en Render o similares usar debug=False
    app.run(host='0.0.0.0', port=port, debug=False)
