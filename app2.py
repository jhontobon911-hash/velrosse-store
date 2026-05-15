from flask import Flask, render_template_string, request, send_from_directory, make_response
import os
import urllib.parse

app = Flask(__name__)

# --- CONFIGURACIÓN VELROSSE STORE ---
TELEFONO_VENTAS = "573169641418"

@app.route('/healthcheck')
def healthcheck():
    return "OK", 200

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

        /* --- BENEFICIOS --- */
        .benefits-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 25px 0; text-align: center; }
        .benefit-item { background: var(--light-gold); padding: 15px; border-radius: 10px; border: 1px solid #eee; }
        .benefit-item i { color: var(--gold); font-size: 24px; margin-bottom: 8px; }
        .benefit-item p { margin: 0; font-size: 13px; font-weight: bold; }

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
            background: #25D366; color: #fff; border: none; width: 100%; padding: 25px; border-radius: 10px; 
            font-size: 24px; font-weight: 900; cursor: pointer; text-transform: uppercase; margin-top: 15px;
            animation: shake 0.5s infinite;
        }

        .size-table-container { margin: 50px auto; max-width: 600px; background: #fff; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
        .size-table { width: 100%; border-collapse: collapse; text-align: center; }
        .table-header-main { background: var(--dark-blue); color: #fff; font-size: 18px; padding: 15px; text-transform: uppercase; font-weight: 900; }
        .size-table th { background: #f8f9fa; padding: 12px; border-bottom: 2px solid var(--gold); font-size: 13px; }
        .size-table td { padding: 12px; border-bottom: 1px solid #eee; font-weight: bold; }

        .reviews-section { margin-top: 60px; padding: 40px 0; background: #fafafa; border-radius: 20px; }
        .reviews-title { text-align: center; font-size: 28px; font-weight: 900; margin-bottom: 40px; color: var(--black); }
        .reviews-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; padding: 0 20px; }
        .review-card { background: #fff; border-radius: 15px; padding: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); border: 1px solid #eee; display: flex; flex-direction: column; }
        .review-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
        .review-avatar { width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 2px solid var(--gold); }
        .review-name { font-weight: 800; font-size: 16px; margin: 0; color: #222; }
        .verified-badge { color: #15b358; font-size: 11px; font-weight: bold; display: flex; align-items: center; gap: 4px; }
        .review-stars { color: #FFD700; font-size: 14px; margin: 10px 0; }
        .review-text { font-size: 14px; color: #444; line-height: 1.5; font-style: italic; margin-bottom: 15px; }
        .review-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f5f5f5; padding-top: 10px; }
        .review-product-img { width: 70px; height: 90px; object-fit: cover; border-radius: 8px; }

        .footer-black { background: #000; color: #fff; padding: 40px 20px; margin-top: 60px; }
        .footer-grid { max-width: 1200px; margin: auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: center; }
        .footer-item i { font-size: 30px; color: var(--gold); margin-bottom: 15px; display: block; }

        @keyframes shake { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }
        @media (max-width: 768px) { .main-grid { grid-template-columns: 1fr; } .footer-grid { grid-template-columns: repeat(2, 1fr); } }
        
        #redirectingModal { 
            display: {% if whatsapp_url %} flex {% else %} none {% endif %}; 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,0.95); z-index: 10000; justify-content: center; align-items: center; flex-direction: column; 
        }
        .loader { border: 8px solid #f3f3f3; border-top: 8px solid #25D366; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin-bottom: 20px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>

    <div id="redirectingModal">
        <div class="loader"></div>
        <h2 style="color: #25D366;">¡PROCESANDO TU PEDIDO!</h2>
        <p>Abriendo WhatsApp para confirmar...</p>
        {% if whatsapp_url %}<script>setTimeout(function(){ window.location.href = "{{ whatsapp_url|safe }}"; }, 1500);</script>{% endif %}
    </div>

    <div class="top-bar">
        <div class="top-item"><i class="fa-solid fa-truck-fast"></i> <div>ENVÍO GRATIS<br><small>A TODA COLOMBIA</small></div></div>
        <div class="top-item"><i class="fa-solid fa-hand-holding-dollar"></i> <div>PAGA AL RECIBIR<br><small>SIN PAGOS ADELANTADOS</small></div></div>
        <div class="top-item"><i class="fa-solid fa-shield-halved"></i> <div>COMPRA SEGURA<br><small>DATOS PROTEGIDOS</small></div></div>
    </div>

    <div class="container">
        <div class="header-section">
            <h1 class="product-title">FAJA MOLDEADORA PREMIUM</h1>
            <h2 class="brand-name">VELROSSE STORE</h2>
            <p class="sub-desc">La tecnología colombiana que define tu silueta al instante.</p>
            
            <div class="benefits-grid">
                <div class="benefit-item"><i class="fa-solid fa-wand-magic-sparkles"></i><p>EFECTO INVISIBLE</p></div>
                <div class="benefit-item"><i class="fa-solid fa-up-long"></i><p>LEVANTA COLA</p></div>
                <div class="benefit-item"><i class="fa-solid fa-compress"></i><p>REDUCE 2 TALLAS</p></div>
                <div class="benefit-item"><i class="fa-solid fa-leaf"></i><p>TELA TRANSPIRABLE</p></div>
            </div>
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
                    <div class="timer-label">Oferta finaliza en:</div>
                    <div class="timer-clock" id="timer">02 : 47 : 35</div>
                </div>

                <div class="price-row">
                    <div>
                        <span style="text-decoration:line-through; color:#999; font-size:18px;">ANTES: $159.900</span><br>
                        <span class="price-now">$89.900</span>
                    </div>
                    <div class="discount-tag">45%<br>DTO.</div>
                </div>

                <form method="POST">
                    <span class="sel-title">Cantidad</span>
                    <select name="cantidad" id="qtySelect" class="qty-selector" onchange="generateSelectors()">
                        <option value="1">Llevar 1 Unidad - $89.900</option>
                        <option value="2">Llevar 2 Unidades - $179.800</option>
                        <option value="3">Llevar 3 Unidades - $269.700</option>
                    </select>

                    <div id="dynamicSelectors"></div>

                    <span class="sel-title">Datos para la entrega</span>
                    <div class="input-group"><i class="fa-solid fa-user"></i><input type="text" name="nombre" class="field" placeholder="Nombre completo" required></div>
                    <div class="input-group"><i class="fa-solid fa-phone"></i><input type="tel" name="celular" class="field" placeholder="Número de celular" required></div>
                    <div class="input-group"><i class="fa-solid fa-id-card"></i><input type="text" name="cedula" class="field" placeholder="Número de cédula" required></div>
                    <div class="input-group"><i class="fa-solid fa-location-dot"></i><input type="text" name="ciudad" class="field" placeholder="Ciudad" required></div>
                    <div class="input-group"><i class="fa-solid fa-map-pin"></i><input type="text" name="direccion" class="field" placeholder="Dirección de entrega" required></div>

                    <button type="submit" class="btn-submit">
                        <i class="fa-brands fa-whatsapp"></i> PEDIR AHORA - PAGO AL RECIBIR
                    </button>
                </form>
            </div>
        </div>

        <div class="size-table-container">
            <table class="size-table">
                <thead>
                    <tr><th colspan="3" class="table-header-main">ENCUENTRA TU TALLA IDEAL</th></tr>
                    <tr><th>TALLA</th><th>CINTURA (CM)</th><th>CADERA (CM)</th></tr>
                </thead>
                <tbody>
                    <tr><td>XS</td><td>60 - 67</td><td>85 - 92</td></tr>
                    <tr><td>S</td><td>68 - 75</td><td>93 - 100</td></tr>
                    <tr><td>M</td><td>76 - 83</td><td>101 - 108</td></tr>
                    <tr><td>L</td><td>84 - 91</td><td>109 - 116</td></tr>
                    <tr><td>XL</td><td>92 - 99</td><td>117 - 124</td></tr>
                    <tr><td>2XL</td><td>100 - 107</td><td>125 - 132</td></tr>
                </tbody>
            </table>
            <p style="text-align:center; font-size:12px; color:#666; margin-top:10px;">* Si estás entre dos tallas, te recomendamos elegir la más grande.</p>
        </div>

        <div class="reviews-section">
            <h2 class="reviews-title">CLIENTES SATISFECHOS ⭐⭐⭐⭐⭐</h2>
            <div class="reviews-container">
                <div class="review-card">
                    <div class="review-header">
                        <img src="https://i.pravatar.cc/150?u=mariana_col" class="review-avatar">
                        <div>
                            <p class="review-name">Mariana Torres (Medellín)</p>
                            <span class="verified-badge"><i class="fa-solid fa-circle-check"></i> Comprador Verificado</span>
                        </div>
                    </div>
                    <div class="review-stars"><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i></div>
                    <p class="review-text">"Increíble calidad. Realmente moldea y no se nota bajo la ropa. El envío fue súper rápido."</p>
                    <div class="review-footer"><img src="/imagenes_fajas/faja (2).jpg" class="review-product-img"></div>
                </div>
                
                <div class="review-card">
                    <div class="review-header">
                        <img src="https://i.pravatar.cc/150?u=claudia_lat" class="review-avatar">
                        <div>
                            <p class="review-name">Claudia Ruiz (Cali)</p>
                            <span class="verified-badge"><i class="fa-solid fa-circle-check"></i> Comprador Verificado</span>
                        </div>
                    </div>
                    <div class="review-stars"><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i></div>
                    <p class="review-text">"Me encantó que pude pagar al recibir. La talla M me quedó perfecta siguiendo la tabla."</p>
                    <div class="review-footer"><img src="/imagenes_fajas/faja (4).jpg" class="review-product-img"></div>
                </div>

                <div class="review-card">
                    <div class="review-header">
                        <img src="https://i.pravatar.cc/150?u=sofia_barr" class="review-avatar">
                        <div>
                            <p class="review-name">Sofía Mendoza (B/quilla)</p>
                            <span class="verified-badge"><i class="fa-solid fa-circle-check"></i> Comprador Verificado</span>
                        </div>
                    </div>
                    <div class="review-stars"><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i></div>
                    <p class="review-text">"¡La mejor faja que he comprado! Recoge todo el abdomen y me siento súper segura."</p>
                    <div class="review-footer"><img src="/imagenes_fajas/faja (3).jpg" class="review-product-img"></div>
                </div>
            </div>
        </div>
    </div>

    <div class="footer-black">
        <div class="footer-grid">
            <div class="footer-item"><i class="fa-solid fa-box-open"></i><strong>ENVÍO GRATIS</strong><br><small>Todo Colombia</small></div>
            <div class="footer-item"><i class="fa-solid fa-handshake"></i><strong>PAGA AL RECIBIR</strong><br><small>Sin riesgos</small></div>
            <div class="footer-item"><i class="fa-solid fa-lock"></i><strong>PAGO SEGURO</strong><br><small>100% Protegido</small></div>
            <div class="footer-item"><i class="fa-solid fa-award"></i><strong>CALIDAD PREMIUM</strong><br><small>Garantizada</small></div>
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
    whatsapp_url = None
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
            detalles_pedido += f"• Faja {i}: Talla {talla}, Color {color}\\n"

        texto = (
            f"👑 *NUEVO PEDIDO - VELROSSE* 👑\\n\\n"
            f"👤 *Cliente:* {nombre}\\n"
            f"📞 *Celular:* {celular}\\n"
            f"🆔 *Cédula:* {cedula}\\n"
            f"📍 *Ciudad:* {ciudad}\\n"
            f"🏠 *Dirección:* {direccion}\\n\\n"
            f"📦 *PEDIDO:*\\n"
            f"{detalles_pedido}\\n"
            f"💰 *TOTAL A PAGAR:* ${89900 * cantidad:,}\\n\\n"
            f"🚚 *PAGO CONTRA ENTREGA*"
        )
        
        mensaje_final = urllib.parse.quote(texto.replace('\\n', '\n'))
        whatsapp_url = f"https://wa.me/{TELEFONO_VENTAS}?text={mensaje_final}"

    response = make_response(render_template_string(HTML_LAYOUT, whatsapp_url=whatsapp_url))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
