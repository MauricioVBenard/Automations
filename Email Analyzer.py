import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import re

# --- Estilos CSS mejorados ---
STYLE = """<style>
    .header {
        background-color: #3498db;
        color: white;
        text-align: center;
        padding: 15px;
        border-radius: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .result-box {
        background-color: #2c3e50;
        color: white;
        padding: 15px;
        border-radius: 5px;
        font-size: 1.1em;
        line-height: 1.5;
        margin-top: 15px;
    }
    .key-points {
        font-weight: bold;
        color: #f1c40f;
        margin-bottom: 5px;
    }
    .spam-alert {
        color: red;
        font-weight: bold;
    }
</style>"""

# --- Campos de entrada ---
email_info_input = widgets.Textarea(
    placeholder="Pega aquí el remitente y el título del correo electrónico",
    layout=widgets.Layout(width='99%')
)

email_body_input = widgets.Textarea(
    placeholder="Pega aquí el contenido crudo del correo electrónico",
    layout=widgets.Layout(width='99%')
)

analyze_button = widgets.Button(
    description="Analizar Correo",
    button_style='success',
    icon='search'
)

results_output = widgets.Output()

# --- Función para determinar la importancia del correo ---
def determine_importance(text):
    keywords_high = ["urgente", "importante", "inmediato", "acción requerida"]
    keywords_medium = ["recordatorio", "aviso", "pendiente", "favor revisar"]
    
    if any(word in text.lower() for word in keywords_high):
        return "🔴 Alta"
    elif any(word in text.lower() for word in keywords_medium):
        return "🟠 Media"
    else:
        return "🟢 Baja"

# --- Función para detectar posible spam o correo malicioso ---
def detect_spam(text):
    spam_keywords = ["ganador", "premio", "transferencia", "hacer clic", "suscripción", "no solicitado", "urgente", "gratis", "felicidades"]
    excessive_links = len(re.findall(r"https?://\S+", text)) > 2
    
    if any(word in text.lower() for word in spam_keywords) or excessive_links:
        return "<span class='spam-alert'>⚠️ Posible spam o correo fraudulento</span>"
    return "✅ No parece ser spam"

# --- Función de análisis de correos ---
def extract_key_info(text):
    sentences = text.split(". ")
    
    # Categorizar el tipo de correo
    if "curso" in text.lower() or "certificación" in text.lower():
        category = "📚 Educación / Formación"
    elif "descuento" in text.lower() or "promoción" in text.lower():
        category = "💰 Oferta / Promoción"
    elif "error" in text.lower() or "problema" in text.lower():
        category = "⚠️ Alerta / Reporte de Problema"
    elif "urgente" in text.lower() or "atención" in text.lower():
        category = "🚨 Urgente / Acción Requerida"
    else:
        category = "📩 General"

    # Extraer frases clave
    keywords = ["importante", "atención", "aviso", "oferta", "descuento", "error", "problema"]
    key_points = [sent.strip() for sent in sentences if any(word in sent.lower() for word in keywords)]
    
    return category, key_points[:3] if key_points else sentences[:3]

def analyze_email(b):
    with results_output:
        clear_output(wait=True)
        email_info = email_info_input.value
        email_body = email_body_input.value

        # Procesar la información del correo
        category, key_points = extract_key_info(email_body)
        importance = determine_importance(email_body)
        spam_status = detect_spam(email_body)
        
        # Mostrar resultados con formato mejorado
        display(HTML(f"""
        <div class='result-box'>
            <p class='key-points'>📌 <b>Remitente y Asunto:</b> {email_info}</p>
            <p class='key-points'>🧐 <b>Tipo de correo:</b> {category}</p>
            <p class='key-points'>🔥 <b>Importancia:</b> {importance}</p>
            <p class='key-points'>🚨 <b>Spam / Seguridad:</b> {spam_status}</p>
            <p class='key-points'>🔍 <b>Puntos clave:</b></p>
            <ul>
                {"".join(f"<li>{point}</li>" for point in key_points)}
            </ul>
        </div>
        """))

analyze_button.on_click(analyze_email)

# --- Construcción de la interfaz ---
ui = widgets.VBox([
    widgets.HTML("<div class='header'>Analizador de Correos Electrónicos</div>"),
    email_info_input,
    email_body_input,
    analyze_button,
    results_output
])

display(HTML(STYLE))
display(ui)
