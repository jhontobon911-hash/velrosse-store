from flask import Flask, render_template_string, request, send_from_directory, make_response
from flask_mail import Mail, Message

app = Flask(__name__)

# --- CONFIGURACIÓN DE CORREO VELROSSE STORE ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'velrossestore@gmail.com' 
app.config['MAIL_PASSWORD'] = 'icdl jprr ztug mdpa' 
app.config['MAIL_DEFAULT_SENDER'] = 'velrossestore@gmail.com'
mail = Mail(app)

# Ruta local de sus imágenes
CARPETA_FAJAS = r'C:\Users\STEVEN\OneDrive\Escritorio\INGENIERIA DE SOFTWARE\Programas\FAJAS'

@app.route('/imagenes_fajas/<path:filename>')
def serve_fajas(filename):
    return send_from_directory(CARPETA_FAJAS, filename)

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Velrosse Store - Faja Moldeadora</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --gold: #b28d42; --pink: #e91e63; --black: #000; --light-gold: #fdf7eb; }
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
        .thumbs-list { display: flex; flex-direction: column; gap: 10px; }
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

        .sel-title { font-size: 13px; font-weight: 800; text-transform: uppercase; margin: 15px 0 10px; display: block; }
        .radio-flex { display: flex; gap: 10px; margin-bottom: 15px; }
        .radio-btn { flex: 1; border: 1px solid #ddd; padding: 12px; border-radius: 8px; text-align: center; cursor: pointer; font-weight: bold; position: relative; }
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

        .features-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 40px 0; }
        .feature-card { background: var(--light-gold); padding: 20px; text-align: center; border-radius: 10px; }
        .feature-card i { font-size: 24px; color: var(--gold); margin-bottom: 10px; display: block; }
        .feature-card span { font-size: 12px; font-weight: bold; line-height: 1.2; display: block; }

        .results-section { text-align: center; margin-top: 50px; }
        .results-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 25px; }
        .result-item { text-align: left; }
        .result-img-pair { display: flex; gap: 5px; margin-bottom: 10px; }
        .result-img-pair img { width: 50%; border-radius: 5px; }

        .footer-black { background: #000; color: #fff; padding: 40px 20px; margin-top: 60px; }
        .footer-grid { max-width: 1200px; margin: auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: center; }
        .footer-item i { font-size: 30px; color: var(--gold); margin-bottom: 15px; display: block; }

        #successModal { 
            display: {% if success %} flex {% else %} none {% endif %}; 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 10000; justify-content: center; align-items: center; 
        }
        .modal-content { background: #fff; padding: 40px; border-radius: 20px; text-align: center; max-width: 450px; border: 3px solid var(--gold); }
        .modal-content h2 { color: #28a745; margin-bottom: 15px; }
        .modal-content p { font-size: 17px; font-weight: bold; }
        .wa-btn { background: #25D366; color: white; padding: 15px 25px; border-radius: 50px; text-decoration: none; display: inline-block; margin-top: 20px; font-weight: 900; font-size: 20px; }
    </style>
</head>
<body>

    <div id="successModal">
        <div class="modal-content">
            <i class="fa-solid fa-circle-check" style="font-size: 60px; color: #28a745;"></i>
            <h2>¡GRACIAS POR TU COMPRA!</h2>
            <p>su pedido esta en proceso de alistamiento y envio</p>
            <p>en caso de tener alguna pregunta puedes escribirnos a nuestro whatsaap</p>
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
                    {% for i in range(1, 10) %}
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
                    <span class="sel-title">1. Selecciona el Color</span>
                    <div class="radio-flex">
                        <label class="radio-btn"><input type="radio" name="color" value="Negro" checked> <i class="fa-solid fa-circle" style="color:black;"></i> NEGRO</label>
                        <label class="radio-btn"><input type="radio" name="color" value="Beige"> <i class="fa-solid fa-circle" style="color:#f5f5dc;"></i> BEIGE</label>
                    </div>

                    <span class="sel-title">2. Selecciona tu Talla</span>
                    <div style="display:grid; grid-template-columns: repeat(3,1fr); gap:5px;">
                        {% for t in ['XS', 'S', 'M', 'L', 'XL', '2XL'] %}
                        <label class="radio-btn" style="padding:8px;"><input type="radio" name="talla" value="{{t}}" required> {{t}}</label>
                        {% endfor %}
                    </div>

                    <span class="sel-title">3. Completa tus Datos</span>
                    <div class="input-group"><i class="fa-solid fa-user"></i><input type="text" name="nombre" class="field" placeholder="Nombre completo" required></div>
                    <div class="input-group"><i class="fa-solid fa-phone"></i><input type="tel" name="celular" class="field" placeholder="Número de celular" required></div>
                    <div class="input-group"><i class="fa-solid fa-id-card"></i><input type="text" name="cedula" class="field" placeholder="Número de cédula" required></div>
                    <div class="input-group"><i class="fa-solid fa-location-dot"></i><input type="text" name="ciudad" class="field" placeholder="Ciudad" required></div>
                    <div class="input-group"><i class="fa-solid fa-map-pin"></i><input type="text" name="direccion" class="field" placeholder="Dirección de entrega" required></div>

                    <button type="submit" class="btn-submit">COMPRAR AHORA<br><small style="font-size:12px;">PAGA AL RECIBIR</small></button>
                </form>
            </div>
        </div>

        <div class="features-grid">
            <div class="feature-card"><i class="fa-solid fa-vest"></i><span>Moldea tu cintura<br>y reduce medidas</span></div>
            <div class="feature-card"><i class="fa-solid fa-person-rays"></i><span>Mejora tu postura<br>y alivia el dolor</span></div>
            <div class="feature-card"><i class="fa-solid fa-calendar-check"></i><span>Uso diario<br>y postparto</span></div>
            <div class="feature-card"><i class="fa-solid fa-gem"></i><span>Material premium<br>transpirable</span></div>
        </div>

        <div class="results-section">
            <h3 style="font-weight:900; font-size:24px;">RESULTADOS REALES</h3>
            <p>Mujeres reales, resultados reales</p>
            <div class="results-grid">
                {% set res = [("Camila R.","Desde que uso la faja mi cintura se ve mucho más definida."), ("Daniela M.","Me ayudó muchísimo después del parto, súper cómoda."), ("Valentina G.","La uso todos los días, es ligera y no se nota.")] %}
                {% for nombre, texto in res %}
                <div class="result-item">
                    <div class="result-img-pair">
                        <img src="/imagenes_fajas/faja (1).jpg">
                        <img src="/imagenes_fajas/faja (2).jpg">
                    </div>
                    <div style="color:var(--gold); font-size:12px;">★★★★★</div>
                    <p style="font-size:13px; font-style:italic; margin:5px 0;">"{{texto}}"</p>
                    <strong style="font-size:12px;">- {{nombre}}</strong>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <div class="footer-black">
        <div class="footer-grid">
            <div class="footer-item"><i class="fa-solid fa-box-open"></i><strong>ENVÍO GRATIS</strong><br><small>A toda Colombia de 2 a 4 días</small></div>
            <div class="footer-item"><i class="fa-solid fa-handshake"></i><strong>PAGA AL RECIBIR</strong><br><small>Cancela cuando recibas tu producto</small></div>
            <div class="footer-item"><i class="fa-solid fa-lock"></i><strong>COMPRA SEGURA</strong><br><small>Tus datos protegidos al 100%</small></div>
            <div class="footer-item"><i class="fa-solid fa-award"></i><strong>GARANTÍA</strong><br><small>7 días por defectos de fábrica</small></div>
        </div>
    </div>

    <script>
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
        color = request.form.get('color')
        talla = request.form.get('talla')

        try:
            msg = Message(subject=f"NUEVO PEDIDO: {nombre}",
                          recipients=['velrossestore@gmail.com'])
            
            msg.body = (
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"       NUEVA VENTA - VELROSSE STORE     \n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📦 DETALLES DEL PRODUCTO:\n"
                f"----------------------------------------\n"
                f"Producto:  Faja Moldeadora Velrosse\n"
                f"Talla:     {talla}\n"
                f"Color:     {color}\n\n"
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
                f"        PAGO AL RECIBIR EN CASA         \n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
            mail.send(msg)
            success = True
        except Exception as e:
            print(f"Error: {e}")
            success = True 

    # --- BYPASS DE NGROK ---
    response = make_response(render_template_string(HTML_LAYOUT, success=success))
    response.headers['ngrok-skip-browser-warning'] = '69420'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)