# =========================================================
# 馃З SISTEMA_CREACION_PERSONAJE_ULTRA_PRO (FINAL COMPLETO)
# =========================================================

# =========================
# 馃摝 IMPORTS
# =========================
import os
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# =========================
# 馃攼 TOKEN
# =========================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("No se encontr贸 BOT_TOKEN en variables de entorno")

# =========================
# 馃 ESTADO
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
        }
    return jugadores[user_id]

# =========================
# 馃幆 UI
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
    except:
        await context.bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message_id,
            caption=text,
            reply_markup=keyboard
        )

# =========================
# 馃К RAZAS
# =========================
razas = {
    "male": ["Humano", "Elfo", "Enano", "Semi Bestia", "Gigante"],
    "female": ["Humano", "Elfo", "Enano", "Semi Bestia", "Sirena"],
    "pago": ["Drac贸nido", "Argoniano", "Necr贸mano", "Skaldar"],
    "informativa": ["脕ngel", "Demonio"]
}

# =========================
# 馃摉 DESCRIPCIONES COMPLETAS
# =========================
descripciones = {

"Humano": """Durante cientos de a帽os, la raza m谩s temible y letal conocida en el continente AeGedom domin贸 gran parte de 茅l: sus oc茅anos, el norte fr铆o y el noreste oscuro. Tomaron como esclavos a los enanos para forjar sus armas y armaduras, y a las semibestias para sus placeres y necesidades, amenazando constantemente los territorios de los elfos y librando guerras contra las razas del oeste. Hasta que la calamidad toc贸 las bases de su imperio, dejando a la humanidad con el reino m谩s peque帽o de todos.

~ En la actualidad, el Reino Val茅nia es gobernado por un linaje que proclam贸 el dominio de sus tierras, y en la actualidad sus miembros con mayor t铆tulos representan la casa Arden en el Reino de MissiaM.

鉁� La raza humana, debido a su corta vida, es considerada la raza de la supervivencia, adapt谩ndose con mayor facilidad a los ambientes, profesiones y destrezas que se propongan.""",

"Elfo": """Siendo una de las razas m谩s antiguas del mundo, los elfos son los seres m谩s ego铆stas, tomando sus conocimientos, cultura y misterios m谩s poderosos como un tesoro oculto jam谩s visto por otras razas. Durante cientos de a帽os mantuvieron su distancia hasta que un punto en la historia los hizo unir fuerzas con otras razas. Posteriormente a la guerra, la raza volvi贸 a tomar su posici贸n cultural.

~ El Bosque Milenario, dominio de los elfos, es custodiado a煤n por ellos mismos y su casa Lorien es representada por sus guerreros m谩s h谩biles en el Reino de MissiaM.

鉁� A trav茅s de los milenios, la raza ha dominado el control total del Man谩, brind谩ndoles capacidades extraordinarias para dominar m谩s habilidades y destrezas.""",

"Enano": """Una raza formidable en conducta y disciplina, pero durante muchos siglos dominada por otras razas con el 煤nico fin para el cual son m谩s h谩biles: forjar y armar naciones enteras con las mejores armaduras y los equipos m谩gicos m谩s avanzados. Tras la Gran Guerra, quedaron libres del yugo de cualquier raza y su castillo, Durnhall, prosper贸.

~ Tanto su reino, Durnhall, como la casa Bron, prestan sus servicios de forma libre y diplom谩tica en el reino de MissiaM, convirti茅ndose en el reino comercial m谩s importante.

鉁� Los enanos tienen una excepcional capacidad para visualizar los mejores materiales en las cuevas, exploraciones y recolecci贸n.""",

"Semi Bestia": """Las bestias han dominado el mundo durante miles de a帽os y han evolucionado para mantener su dominio. En una brecha del tiempo antiguo, una trasgresi贸n mut贸 a humanos con bestias poderosas, creando as铆 a los mitad humanos y mitad bestias, mejor conocidos como Semi~Bestias. Sin embargo, este plan fracas贸 ante la ambici贸n de la raza humana, que dobleg贸 a la raza h铆brida a la esclavitud y al dominio durante cientos de a帽os. Hasta que lleg贸 el d铆a final de la guerra, cuando cientos de voluntarios Semi~Bestias dieron sus vidas por la causa.

~ Actualmente, el Reino Feral铆a vive en total libertad y al servicio del reino de MissiaM; su Casa Ragor representa la junta continental para la paz.

鉁� Los Semi~Bestias poseen una diversidad de cualidades seg煤n el tipo de bestia que representan; algunos son m谩s fuertes, otros m谩s 谩giles...""",

"Gigante": """Una de las razas propias del continente y tan antiguas como los elfos, los gigantes han dominado las llanuras y las monta帽as del sur durante miles de a帽os. Sin embargo, su naturaleza pac铆fica los llev贸 casi a la extinci贸n, hasta que un milagro divino les permiti贸 surgir. Los gigantes adoptan una forma humana intermedia para coexistir entre otras razas y volver a caminar por todo el continente. Debido a su tragedia, los gigantes nacen del milagro divino.

~ El reino Jotunheim es un territorio para la convivencia de los gigantes mismos; sin embargo, sigue en construcci贸n. La Casa Bram representa la junta continental en el reino de MissiaM.

鉁� Los gigantes tienen una fuerza incre铆ble, aunque no les sirvi贸 de mucho durante la guerra...""",

"Sirena": """Una raza usurpadora y muy inteligente, a punto de la extinci贸n, logr贸 infiltrarse con sus cualidades hasta lo m谩s alto del dominio humano, destruyendo la capital central que se encontraba en el oc茅ano en una isla, sumergi茅ndose hasta las profundidades del mismo y dominando el oc茅ano. Las sirenas se reprodujeron con las almas de los hombres humanos y multiplicaron sus filas; sin embargo, ante la amenaza de un nuevo enemigo en com煤n, lograron adoptar forma humana para luchar en la gran guerra, proclamando as铆 su nuevo reino en el cual viven en paz.

~ Ahora bien conocido, el reino N茅ridias es el hogar de estas sirenas y su casa Thal representa la junta continental del reino de MissiaM.

鉁� Las sirenas son conocidas por tener un talento para la ilusi贸n y el enga帽o para capturar a sus presas.""",

"Drac贸nido": """Emergidos desde las profundidades del volc谩n, los hijos del fuego adoptaron la forma humana con aspectos de drag贸n. Fieles a un drag贸n milenario que reposa en el coraz贸n del volc谩n, los Draconianos son criaturas con poco dialecto ante las dem谩s razas, pero que han perdurado siglos dominando el oeste. Gracias al poder del Drag贸n, pudieron resistir su extinci贸n y luchar en la Gran Guerra desde su trinchera.

~ El Valle del Drag贸n es una zona reinada por los Draconianos, y solo los m谩s habilidosos pueden adentrarse en ella para demostrar su capacidad de superar sus pruebas. La Casa Fyrn habita a los m谩s inteligentes entre ellos para representar la Junta Continental.

鉁� Los Draconianos son inmunes al fuego, tienen una piel endurecida y algunos pueden volar.""",

"Argoniano": """Una raza m铆tica, parientes de los Draconianos y adoradores del Dios del pantano. Poseen una variaci贸n similar a la humana con aspectos de reptil; son conocidos como shamanes y asesinos de las sombras. Los Argonianos han sobrevivido a los peligros del continente durante siglos. Aunque son ajenos a las costumbres de otras razas, contribuyeron a la paz del continente en la Gran Guerra con su magia ancestral.

~ Su inmenso reino es un pantano lleno de diversidad entre ellos, lo cual se convierte en un desaf铆o para todos, y le dan el nombre de Saxhleel a su Dios Ancestral. La casa Valcor representa la junta continental del reino de MissiaM con su shaman m谩s capacitado.

鉁� Los Argonianos tienen una fuerte inmunidad al veneno, su regeneraci贸n es m谩s avanzada y algunos pueden camuflajearse hasta tal punto de lograr la invisibilidad.""",

"Necr贸mano": """Malditos por la desgracia y la calamidad, los Necromanos son los magos oscuros de la muerte. En tiempos remotos, un grupo de magos se dedic贸 a descifrar los misterios de los seres divinos y, tras una traici贸n, consiguieron una maldici贸n que conden贸 a la raza humana. Sin embargo, al ser magos, su magia pudo sostener la maldici贸n y convertirla en su nueva arma, dominando a los muertos; as铆, los Nigromantes se convirtieron en una nueva raza.

~ La maldici贸n convirti贸 al valle divino en un contaminado y desgarrador escenario llamado Necropolis Mortaria. Sin participaci贸n alguna en la gran guerra, los Necromanos lograron, mediante la diplomacia, un asiento en la asamblea continental y su casa se llama Nox.

鉁� Los Necromanos son magos de la muerte y, por ende, son inmunes a las maldiciones y alteraciones negativas. Tienen una habilidad pasiva que les permite tener un 50% m谩s de vida, lo que les permite seguir luchando; invoca a lo que matan con iguales cualidades.""",

"Skaldar": """Los Skaldars, antes conocidos como los Ca铆dos en el Hielo, fueron una vez la Orden del Norte, comandantes que custodiaban las labores de los enanos con el prop贸sito del Imperio Humano. Cayeron en la desgracia de la maldici贸n causada por los magos que traicionaron lo divino. Sin embargo, uno entre ellos logr贸 desprenderse de su humanidad y dejarse poseer por la maldici贸n del Esp铆ritu Helado para convertirse as铆 en el Comandante del Norte Fr铆o.

~ Esta raza surgi贸 posteriormente a la Gran Guerra, reviviendo con el deseo de emerger nuevamente como comandantes de la Orden del Norte y tomando el dominio de las Tierras Blancas del Norte. Tambi茅n fundaron la Casa Frost para obtener un puesto en la junta continental del Reino de MissiaM.

鉁� Los Skaldars tienen una alta resistencia al fr铆o, no sufren hemorragias y, en algunos casos, se han detectado espacios que se han congelado por su magia.""",

"脕ngel": """Los 脕ngeles, tambi茅n conocidos como los Divinos, son una especie de otra dimensi贸n que llegaron a presenciar el momento de la creaci贸n de las tierras, los mares y las criaturas. Compartieron con los esp铆ritus y criaturas ancestrales y milenarias durante muchos siglos hasta su partida. Sin embargo, en una 茅poca, los humanos descubrieron los antiguos textos grabados en las piedras del Bosque Divino, los cuales se encontraban all铆 para llamar nuevamente a los 脕ngeles en caso de ser necesario. Al acudir al llamado, los 脕ngeles prestaron su voz y luz a los humanos para darles permiso de entrar en zonas y lugares donde solo los esp铆ritus y las criaturas m铆ticas se encontraban. Pero la codicia de la humanidad por m谩s poder los llev贸 a la traici贸n y, con ella, a la retirada de los 脕ngeles, dej谩ndoles a la humanidad una gran maldici贸n.

鉁� Hasta la actualidad, jam谩s se ha vuelto a ver a un 脕ngel rondar por el continente.""",

"Demonio": """La raza m谩s peligrosa de todas se encuentra en otra dimensi贸n, gobernando siete reinos en un ambiente posapocal铆ptico lleno de criaturas y seres diab贸licos y malvados. Los siete jinetes o reyes del Inframundo lograron abrir una brecha en el Mar del Oeste, liberando toda su calamidad y poder, arrasando con todo a su paso. Los demonios buscan dominar todo el continente, destruyendo las razas simult谩neamente en los 7 puntos cardinales. As铆, casi al 茅xito de su conquista, fueron sucumbidos por un poder 煤nico, divino y ancestral que logr贸 aniquilar a los siete jinetes, acabando con la gran guerra y dando inicio a la nueva era de paz con el reino de MissiaM.

鉁� Hasta la actualidad, no se ha tenido avistamiento de ning煤n demonio en ninguna regi贸n."""
}

# =========================
# 馃柤锔� IM脕GENES
# =========================
imagenes_razas = {r: "URL_IMAGEN" for r in descripciones}
IMG_MALE = "URL_MALE"
IMG_FEMALE = "URL_FEMALE"

# =========================
# 鈻讹笍 START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    jugador = get_player(user_id)

    botones = InlineKeyboardMarkup([
        [InlineKeyboardButton("Masculino", callback_data="gender_male")],
        [InlineKeyboardButton("Femenino", callback_data="gender_female")]
    ])

    msg = await context.bot.send_message(
        chat_id,
        "馃帀 Bienvenido a MissiaM\n\nSelecciona tu g茅nero:",
        reply_markup=botones
    )

    jugador["ui_message_id"] = msg.message_id

# =========================
# 鈿э笍 G脡NERO
# =========================
async def gender_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    user_id = q.from_user.id
    chat_id = q.message.chat.id
    jugador = get_player(user_id)

    if q.data == "gender_male":
        jugador["genero"] = "male"
        img = IMG_MALE
    else:
        jugador["genero"] = "female"
        img = IMG_FEMALE

    await ui_render(context, chat_id, jugador["ui_message_id"], "Seleccionando g茅nero...", img)
    await menu_razas(update, context)

# =========================
# 馃К MEN脷 RAZAS
# =========================
async def menu_razas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    user_id = q.from_user.id
    chat_id = q.message.chat.id
    jugador = get_player(user_id)

    botones = []

    for r in razas[jugador["genero"]]:
        botones.append([InlineKeyboardButton(r, callback_data=f"raza_{r}")])

    for r in razas["pago"]:
        botones.append([InlineKeyboardButton(f"{r} 馃挵", callback_data=f"raza_{r}")])

    for r in razas["informativa"]:
        botones.append([InlineKeyboardButton(f"{r} 馃攳", callback_data=f"raza_{r}")])

    await ui_render(context, chat_id, jugador["ui_message_id"], "馃К Selecciona tu raza:", None, InlineKeyboardMarkup(botones))

# =========================
# 馃摉 MOSTRAR RAZA
# =========================
async def mostrar_raza(update: Update, context: ContextTypes.DEFAULT_TYPE, raza):
    q = update.callback_query
    await q.answer()

    user_id = q.from_user.id
    chat_id = q.message.chat.id
    jugador = get_player(user_id)

    es_pago = raza in razas["pago"]
    es_info = raza in razas["informativa"]

    texto = f"馃К {raza}\n\n{descripciones[raza]}"

    if es_pago:
        texto += "\n\n馃挵 Esta es una raza premium."

    botones = []
    if not es_info:
        if es_pago:
            botones.append([InlineKeyboardButton("馃挵 Desbloquear", callback_data=f"pagar_{raza}")])
        else:
            botones.append([InlineKeyboardButton("鉁� Elegir", callback_data=f"confirmar_raza_{raza}")])

    botones.append([InlineKeyboardButton("馃敊 Volver", callback_data="volver_razas")])

    await ui_render(context, chat_id, jugador["ui_message_id"], texto, imagenes_razas[raza], InlineKeyboardMarkup(botones))

# =========================
# 馃敇 HANDLER GENERAL
# =========================
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    data = q.data

    if data.startswith("raza_"):
        await mostrar_raza(update, context, data.replace("raza_", ""))

    elif data == "volver_razas":
        await menu_razas(update, context)

    elif data.startswith("confirmar_raza_"):
        jugador = get_player(q.from_user.id)
        jugador["raza"] = data.replace("confirmar_raza_", "")

        await ui_render(
            context,
            q.message.chat.id,
            jugador["ui_message_id"],
            "[Ahora debes dar un nombre]\n\nUsa: /name Nombre_Apellido"
        )

# =========================
# 鉁嶏笍 NOMBRE
# =========================
async def set_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    jugador = get_player(user_id)

    nombre = " ".join(context.args).replace("_", " ").strip()
    nombre_norm = nombre.lower()

    if not re.fullmatch(r"[A-Za-z脕脡脥脫脷谩茅铆贸煤脩帽 ]+", nombre):
        return
    if len(nombre) < 3 or len(nombre) > 20:
        return
    if nombre_norm in nombres_usados:
        return

    jugador["nombre_temp"] = nombre
    jugador["nombre_temp_norm"] = nombre_norm

    botones = InlineKeyboardMarkup([
        [InlineKeyboardButton("鉁� Confirmar", callback_data="confirmar_nombre")],
        [InlineKeyboardButton("鉁忥笍 Cambiar", callback_data="cambiar_nombre")]
    ])

    await ui_render(context, chat_id, jugador["ui_message_id"], f"{nombre}\n\n驴Confirmar?", None, botones)

# =========================
# 馃敇 NOMBRE HANDLER
# =========================
async def nombre_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    jugador = get_player(q.from_user.id)

    if q.data == "confirmar_nombre":
        jugador["nombre"] = jugador["nombre_temp"]
        nombres_usados.add(jugador["nombre_temp_norm"])

    elif q.data == "cambiar_nombre":
        await q.answer("Usa /name nuevo_nombre")

# =========================
# 馃殌 MAIN
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("name", set_nombre))
app.add_handler(CallbackQueryHandler(gender_handler, pattern="gender_"))
app.add_handler(CallbackQueryHandler(handler))
app.add_handler(CallbackQueryHandler(nombre_handler, pattern="confirmar_nombre|cambiar_nombre"))

app.run_polling()
