# =========================================================
# 🧩 CREAR_PERSONAJE (VERSIÓN CORREGIDA REAL)
# =========================================================

import os
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Falta BOT_TOKEN")

# =========================
# 🧠 ESTADO
# =========================
jugadores = {}
nombres_usados = set()

def get_player(user_id):
    if user_id not in jugadores:
        jugadores[user_id] = {
            "genero": None,
            "raza": None,
            "nombre": None,
            "nombre_temp": None,
            "nombre_temp_norm": None,
            "ui_message_id": None,
            "estado": "inicio"
        }
    return jugadores[user_id]

# =========================
# 🎯 UI SEGURA
# =========================
async def ui_render(context, chat_id, message_id, text=None, image=None, keyboard=None):
    try:
        if image:
            await context.bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(media=image, caption=text),
                reply_markup=keyboard
            )
        else:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=keyboard
            )
    except Exception:
        try:
            await context.bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=text,
                reply_markup=keyboard
            )
        except:
            pass

# =========================
# 🧬 RAZAS
# =========================
razas = {
    "male": ["Humano", "Elfo", "Enano", "Semi Bestia", "Gigante"],
    "female": ["Humano", "Elfo", "Enano", "Semi Bestia", "Sirena"],
    "pago": ["Draconianos", "Argonianos", "Necromanos", "Skaldars"],
    "info": ["Ángeles", "Demonios"]
}

# =========================
# 📖 DESCRIPCIONES COMPLETAS
# =========================
descripciones = {

"Humano": """Durante cientos de años, la raza más temible y letal conocida en el continente AeGedom dominó gran parte de él: sus océanos, el norte frío y el noreste oscuro. Tomaron como esclavos a los enanos para forjar sus armas y armaduras, y a las semibestias para sus placeres y necesidades, amenazando constantemente los territorios de los elfos y librando guerras contra las razas del oeste. Hasta que la calamidad tocó las bases de su imperio, dejando a la humanidad con el reino más pequeño de todos.

~ En la actualidad, el Reino Valénia es gobernado por un linaje que proclamó el dominio de sus tierras, y en la actualidad sus miembros con mayor títulos representan la casa Arden en el Reino de MissiaM.

✍ La raza humana, debido a su corta vida, es considerada la raza de la supervivencia, adaptándose con mayor facilidad a los ambientes, profesiones y destrezas que se propongan.""",

"Elfo": """Siendo una de las razas más antiguas del mundo, los elfos son los seres más egoístas, tomando sus conocimientos, cultura y misterios más poderosos como un tesoro oculto jamás visto por otras razas. Durante cientos de años mantuvieron su distancia hasta que un punto en la historia los hizo unir fuerzas con otras razas. Posteriormente a la guerra, la raza volvió a tomar su posición cultural.

~ El Bosque Milenario, dominio de los elfos, es custodiado aún por ellos mismos y su casa Lorien es representada por sus guerreros más hábiles en el Reino de MissiaM.

✍ A través de los milenios, la raza ha dominado el control total del Maná, brindándoles capacidades extraordinarias para dominar más habilidades y destrezas.""",

"Enano": """Una raza formidable en conducta y disciplina, pero durante muchos siglos dominada por otras razas con el único fin para el cual son más hábiles: forjar y armar naciones enteras con las mejores armaduras y los equipos mágicos más avanzados. Tras la Gran Guerra, quedaron libres del yugo de cualquier raza y su castillo, Durnhall, prosperó.

~ Tanto su reino, Durnhall, como la casa Bron, prestan sus servicios de forma libre y diplomática en el reino de MissiaM, convirtiéndose en el reino comercial más importante.

✍ Los enanos tienen una excepcional capacidad para visualizar los mejores materiales en las cuevas, exploraciones y recolección.""",

"Semi Bestia": """Las bestias han dominado el mundo durante miles de años y han evolucionado para mantener su dominio. En una brecha del tiempo antiguo, una trasgresión mutó a humanos con bestias poderosas, creando así a los mitad humanos y mitad bestias, mejor conocidos como Semi~Bestias. Sin embargo, este plan fracasó ante la ambición de la raza humana, que doblegó a la raza híbrida a la esclavitud y al dominio durante cientos de años. Hasta que llegó el día final de la guerra, cuando cientos de voluntarios Semi~Bestias dieron sus vidas por la causa.

~ Actualmente, el Reino Feralía vive en total libertad y al servicio del reino de MissiaM; su Casa Ragor representa la junta continental para la paz.

✍ Los Semi~Bestias poseen una diversidad de cualidades según el tipo de bestia que representan; algunos son más fuertes, otros más ágiles...""",

"Gigante": """Una de las razas propias del continente y tan antiguas como los elfos, los gigantes han dominado las llanuras y las montañas del sur durante miles de años. Sin embargo, su naturaleza pacífica los llevó casi a la extinción, hasta que un milagro divino les permitió surgir. Los gigantes adoptan una forma humana intermedia para coexistir entre otras razas y volver a caminar por todo el continente. Debido a su tragedia, los gigantes nacen del milagro divino.

~ El reino Jotunheim es un territorio para la convivencia de los gigantes mismos; sin embargo, sigue en construcción. La Casa Bram representa la junta continental en el reino de MissiaM.

✍ Los gigantes tienen una fuerza increíble, aunque no les sirvió de mucho durante la guerra...""",

"Sirena": """Una raza usurpadora y muy inteligente, a punto de la extinción, logró infiltrarse con sus cualidades hasta lo más alto del dominio humano, destruyendo la capital central que se encontraba en el océano en una isla, sumergiéndose hasta las profundidades del mismo y dominando el océano. Las sirenas se reprodujeron con las almas de los hombres humanos y multiplicaron sus filas; sin embargo, ante la amenaza de un nuevo enemigo en común, lograron adoptar forma humana para luchar en la gran guerra, proclamando así su nuevo reino en el cual viven en paz.

~ Ahora bien conocido, el reino Néridias es el hogar de estas sirenas y su casa Thal representa la junta continental del reino de MissiaM.

✍ Las sirenas son conocidas por tener un talento para la ilusión y el engaño para capturar a sus presas.""",

"Draconianos": """Emergidos desde las profundidades del volcán, los hijos del fuego adoptaron la forma humana con aspectos de dragón. Fieles a un dragón milenario que reposa en el corazón del volcán, los Draconianos son criaturas con poco dialecto ante las demás razas, pero que han perdurado siglos dominando el oeste. Gracias al poder del Dragón, pudieron resistir su extinción y luchar en la Gran Guerra desde su trinchera.

~ El Valle del Dragón es una zona reinada por los Draconianos, y solo los más habilidosos pueden adentrarse en ella para demostrar su capacidad de superar sus pruebas. La Casa Fyrn habita a los más inteligentes entre ellos para representar la Junta Continental.

✍ Los Draconianos son inmunes al fuego, tienen una piel endurecida y algunos pueden volar.""",

"Argonianos": """Una raza mítica, parientes de los Draconianos y adoradores del Dios del pantano. Poseen una variación similar a la humana con aspectos de reptil; son conocidos como shamanes y asesinos de las sombras. Los Argonianos han sobrevivido a los peligros del continente durante siglos. Aunque son ajenos a las costumbres de otras razas, contribuyeron a la paz del continente en la Gran Guerra con su magia ancestral.

~ Su inmenso reino es un pantano lleno de diversidad entre ellos, lo cual se convierte en un desafío para todos, y le dan el nombre de Saxhleel a su Dios Ancestral. La casa Valcor representa la junta continental del reino de MissiaM con su shaman más capacitado.

✍ Los Argonianos tienen una fuerte inmunidad al veneno, su regeneración es más avanzada y algunos pueden camuflajearse hasta tal punto de lograr la invisibilidad.""",

"Necromanos": """Malditos por la desgracia y la calamidad, los Necromanos son los magos oscuros de la muerte. En tiempos remotos, un grupo de magos se dedicó a descifrar los misterios de los seres divinos y, tras una traición, consiguieron una maldición que condenó a la raza humana. Sin embargo, al ser magos, su magia pudo sostener la maldición y convertirla en su nueva arma, dominando a los muertos; así, los Nigromantes se convirtieron en una nueva raza.

~ La maldición convirtió al valle divino en un contaminado y desgarrador escenario llamado Necropolis Mortaria. Sin participación alguna en la gran guerra, los Necromanos lograron, mediante la diplomacia, un asiento en la asamblea continental y su casa se llama Nox.

✍ Los Necromanos son magos de la muerte y, por ende, son inmunes a las maldiciones y alteraciones negativas. Tienen una habilidad pasiva que les permite tener un 50% más de vida, lo que les permite seguir luchando; invoca a lo que matan con iguales cualidades.""",

"Skaldars": """Los Skaldars, antes conocidos como los Caídos en el Hielo, fueron una vez la Orden del Norte, comandantes que custodiaban las labores de los enanos con el propósito del Imperio Humano. Cayeron en la desgracia de la maldición causada por los magos que traicionaron lo divino. Sin embargo, uno entre ellos logró desprenderse de su humanidad y dejarse poseer por la maldición del Espíritu Helado para convertirse así en el Comandante del Norte Frío.

~ Esta raza surgió posteriormente a la Gran Guerra, reviviendo con el deseo de emerger nuevamente como comandantes de la Orden del Norte y tomando el dominio de las Tierras Blancas del Norte. También fundaron la Casa Frost para obtener un puesto en la junta continental del Reino de MissiaM.

✍ Los Skaldars tienen una alta resistencia al frío, no sufren hemorragias y, en algunos casos, se han detectado espacios que se han congelado por su magia.""",

"Ángeles": """Los Ángeles, también conocidos como los Divinos... (informativa)""",

"Demonios": """La raza más peligrosa de todas... (informativa)"""
}

imagenes_razas = {r: "https://via.placeholder.com/512" for r in descripciones}

# =========================
# ▶️ START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_player(update.effective_user.id)
    user["estado"] = "genero"

    msg = await context.bot.send_message(
        update.effective_chat.id,
        "🎉 Bienvenido a MissiaM\n\nSelecciona tu género:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Masculino", callback_data="gender_male")],
            [InlineKeyboardButton("Femenino", callback_data="gender_female")]
        ])
    )

    user["ui_message_id"] = msg.message_id

# =========================
# 🔘 CALLBACK GENERAL (CONTROLADO)
# =========================
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    user = get_player(q.from_user.id)
    data = q.data

    # -------- GENERO --------
    if data.startswith("gender_") and user["estado"] == "genero":
        user["genero"] = data.split("_")[1]
        user["estado"] = "razas"
        return await menu_razas(update, context)

    # -------- VOLVER --------
    if data == "volver_razas":
        return await menu_razas(update, context)

    # -------- MOSTRAR RAZA --------
    if data.startswith("raza_"):
        raza = data.replace("raza_", "")
        return await mostrar_raza(update, context, raza)

    # -------- CONFIRMAR RAZA --------
    if data.startswith("confirmar_raza_"):
        user["raza"] = data.replace("confirmar_raza_", "")
        user["estado"] = "nombre"

        return await ui_render(
            context,
            q.message.chat.id,
            user["ui_message_id"],
            f"✅ Has elegido: {user['raza']}\n\nAhora escribe tu nombre:\n\n/name Nombre_Apellido"
        )

    # -------- CAMBIAR NOMBRE --------
    if data == "cambiar_nombre":
        return await ui_render(
            context,
            q.message.chat.id,
            user["ui_message_id"],
            "✏️ Escribe tu nuevo nombre con /name Nombre_Apellido"
        )

    # -------- CONFIRMAR NOMBRE --------
    if data == "confirmar_nombre":
        user["nombre"] = user["nombre_temp"]
        nombres_usados.add(user["nombre_temp_norm"])

        return await ui_render(
            context,
            q.message.chat.id,
            user["ui_message_id"],
            f"🎉 Personaje creado:\n\n{user['nombre']} - {user['raza']}"
        )

# =========================
# 🧬 MENÚ RAZAS
# =========================
async def menu_razas(update, context):
    q = update.callback_query
    user = get_player(q.from_user.id)

    botones = []

    for r in razas[user["genero"]]:
        botones.append([InlineKeyboardButton(r, callback_data=f"raza_{r}")])

    for r in razas["pago"]:
        botones.append([InlineKeyboardButton(f"{r} 💰", callback_data=f"raza_{r}")])

    for r in razas["info"]:
        botones.append([InlineKeyboardButton(f"{r} 🔍", callback_data=f"raza_{r}")])

    await ui_render(context, q.message.chat.id, user["ui_message_id"], "🧬 Selecciona tu raza:", None, InlineKeyboardMarkup(botones))

# =========================
# 📖 MOSTRAR RAZA
# =========================
async def mostrar_raza(update, context, raza):
    q = update.callback_query
    user = get_player(q.from_user.id)

    es_pago = raza in razas["pago"]
    es_info = raza in razas["info"]

    botones = []

    if not es_info:
        if es_pago:
            botones.append([InlineKeyboardButton("💰 Próximamente", callback_data="noop")])
        else:
            botones.append([InlineKeyboardButton("✅ Elegir", callback_data=f"confirmar_raza_{raza}")])

    botones.append([InlineKeyboardButton("🔙 Volver", callback_data="volver_razas")])

    await ui_render(
        context,
        q.message.chat.id,
        user["ui_message_id"],
        f"🧬 {raza}\n\n{descripciones[raza]}",
        imagenes_razas[raza],
        InlineKeyboardMarkup(botones)
    )

# =========================
# ✍️ NOMBRE
# =========================
async def set_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_player(update.effective_user.id)

    if user["estado"] != "nombre":
        return await update.message.reply_text("⚠️ Primero selecciona tu raza.")

    nombre = " ".join(context.args).replace("_", " ").strip()
    nombre_norm = nombre.lower()

    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre):
        return await update.message.reply_text("❌ Solo letras y espacios.")

    if len(nombre) < 3 or len(nombre) > 20:
        return await update.message.reply_text("❌ Entre 3 y 20 caracteres.")

    if nombre_norm in nombres_usados:
        return await update.message.reply_text("❌ Nombre ya usado.")

    user["nombre_temp"] = nombre
    user["nombre_temp_norm"] = nombre_norm

    botones = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirmar", callback_data="confirmar_nombre")],
        [InlineKeyboardButton("✏️ Cambiar", callback_data="cambiar_nombre")]
    ])

    await ui_render(
        context,
        update.effective_chat.id,
        user["ui_message_id"],
        f"{nombre}\n\n¿Confirmar?",
        None,
        botones
    )

# =========================
# 🚀 MAIN
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("name", set_nombre))
app.add_handler(CallbackQueryHandler(callbacks))

app.run_polling()
