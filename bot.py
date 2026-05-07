# -*- coding: utf-8 -*-
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")

# =========================
# JUGADORES
# =========================
jugadores = {}

def get_player(user_id):
    if user_id not in jugadores:
        jugadores[user_id] = {
            "genero": None,
            "raza": None,
            "nombre": None,
            "nombre_temp": None,
            "nombre_temp_norm": None,
            "estado": "genero",
            "ui_message_id": None
        }
    return jugadores[user_id]

# =========================
# DESCRIPCIONES DE RAZAS
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

    "SemiBestia": """Las bestias han dominado el mundo durante miles de años y han evolucionado para mantener su dominio. En una brecha del tiempo antiguo, una trasgresión mutó a humanos con bestias poderosas, creando así a los mitad humanos y mitad bestias, mejor conocidos como Semi~Bestias. Sin embargo, este plan fracasó ante la ambición de la raza humana, que doblegó a la raza híbrida a la esclavitud y al dominio durante cientos de años. Hasta que llegó el día final de la guerra, cuando cientos de voluntarios Semi~Bestias dieron sus vidas por la causa.

~ Actualmente, el Reino Feralía vive en total libertad y al servicio del reino de MissiaM; su Casa Ragor representa la junta continental para la paz.

✍ Los Semi~Bestias poseen una diversidad de cualidades según el tipo de bestia que representan; algunos son más fuertes, otros más ágiles...""",

    "Gigante": """Una de las razas propias del continente y tan antiguas como los elfos, los gigantes han dominado las llanuras y las montañas del sur durante miles de años. Sin embargo, su naturaleza pacífica los llevó casi a la extinción, hasta que un milagro divino les permitió surgir. Los gigantes adoptan una forma humana intermedia para coexistir entre otras razas y volver a caminar por todo el continente. Debido a su tragedia, los gigantes nacen del milagro divino.

~ El reino Jotunheim es un territorio para la convivencia de los gigantes mismos; sin embargo, sigue en construcción. La Casa Bram representa la junta continental en el reino de MissiaM.

✍ Los gigantes tienen una fuerza increíble, aunque no les sirvió de mucho durante la guerra...""",

    "Sirena": """Una raza usurpadora y muy inteligente, a punto de la extinción, logró infiltrarse con sus cualidades hasta lo más alto del dominio humano, destruyendo la capital central que se encontraba en el océano en una isla, sumergiéndose hasta las profundidades del mismo y dominando el océano. Las sirenas se reprodujeron con las almas de los hombres humanos y multiplicaron sus filas; sin embargo, ante la amenaza de un nuevo enemigo en común, lograron adoptar forma humana para luchar en la gran guerra, proclamando así su nuevo reino en el cual viven en paz.

~ Ahora bien conocido, el reino Néridias es el hogar de estas sirenas y su casa Thal representa la junta continental del reino de MissiaM.

✍ Las sirenas son conocidas por tener un talento para la ilusión y el engaño para capturar a sus presas.""",

    "Draconiano": """Emergidos desde las profundidades del volcán, los hijos del fuego adoptaron la forma humana con aspectos de dragón. Fieles a un dragón milenario que reposa en el corazón del volcán, los Draconianos son criaturas con poco dialecto ante las demás razas, pero que han perdurado siglos dominando el oeste. Gracias al poder del Dragón, pudieron resistir su extinción y luchar en la Gran Guerra desde su trinchera.

~ El Valle del Dragón es una zona reinada por los Draconianos, y solo los más habilidosos pueden adentrarse en ella para demostrar su capacidad de superar sus pruebas. La Casa Fyrn habita a los más inteligentes entre ellos para representar la Junta Continental.

✍ Los Draconianos son inmunes al fuego, tienen una piel endurecida y algunos pueden volar.""",

    "Argoniano": """Una raza mítica, parientes de los Draconianos y adoradores del Dios del pantano. Poseen una variación similar a la humana con aspectos de reptil; son conocidos como shamanes y asesinos de las sombras. Los Argonianos han sobrevivido a los peligros del continente durante siglos. Aunque son ajenos a las costumbres de otras razas, contribuyeron a la paz del continente en la Gran Guerra con su magia ancestral.

~ Su inmenso reino es un pantano lleno de diversidad entre ellos, lo cual se convierte en un desafío para todos, y le dan el nombre de Saxhleel a su Dios Ancestral. La casa Valcor representa la junta continental del reino de MissiaM con su shaman más capacitado.

✍ Los Argonianos tienen una fuerte inmunidad al veneno, su regeneración es más avanzada y algunos pueden camuflajearse hasta tal punto de lograr la invisibilidad.""",

    "Necromano": """Malditos por la desgracia y la calamidad, los Necromanos son los magos oscuros de la muerte. En tiempos remotos, un grupo de magos se dedicó a descifrar los misterios de los seres divinos y, tras una traición, consiguieron una maldición que condenó a la raza humana. Sin embargo, al ser magos, su magia pudo sostener la maldición y convertirla en su nueva arma, dominando a los muertos; así, los Nigromantes se convirtieron en una nueva raza.

~ La maldición convirtió al valle divino en un contaminado y desgarrador escenario llamado Necropolis Mortaria. Sin participación alguna en la gran guerra, los Necromanos lograron, mediante la diplomacia, un asiento en la asamblea continental y su casa se llama Nox.

✍ Los Necromanos son magos de la muerte y, por ende, son inmunes a las maldiciones y alteraciones negativas. Tienen una habilidad pasiva que les permite tener un 50% más de vida, lo que les permite seguir luchando; invoca a lo que matan con iguales cualidades.""",

    "Skaldar": """Los Skaldars, antes conocidos como los Caídos en el Hielo, fueron una vez la Orden del Norte, comandantes que custodiaban las labores de los enanos con el propósito del Imperio Humano. Cayeron en la desgracia de la maldición causada por los magos que traicionaron lo divino. Sin embargo, uno entre ellos logró desprenderse de su humanidad y dejarse poseer por la maldición del Espíritu Helado para convertirse así en el Comandante del Norte Frío.

~ Esta raza surgió posteriormente a la Gran Guerra, reviviendo con el deseo de emerger nuevamente como comandantes de la Orden del Norte y tomando el dominio de las Tierras Blancas del Norte. También fundaron la Casa Frost para obtener un puesto en la junta continental del Reino de MissiaM.

✍ Los Skaldars tienen una alta resistencia al frío, no sufren hemorragias y, en algunos casos, se han detectado espacios que se han congelado por su magia.""",

    "Ángeles": """Los Ángeles, también conocidos como los Divinos, son una especie de otra dimensión que llegaron a presenciar el momento de la creación de las tierras, los mares y las criaturas. Compartieron con los espíritus y criaturas ancestrales y milenarias durante muchos siglos hasta su partida. Sin embargo, en una época, los humanos descubrieron los antiguos textos grabados en las piedras del Bosque Divino, los cuales se encontraban allí para llamar nuevamente a los Ángeles en caso de ser necesario. Al acudir al llamado, los Ángeles prestaron su voz y luz a los humanos para darles permiso de entrar en zonas y lugares donde solo los espíritus y las criaturas míticas se encontraban. Pero la codicia de la humanidad por más poder los llevó a la traición y, con ella, a la retirada de los Ángeles, dejándoles a la humanidad una gran maldición.

✍ Hasta la actualidad, jamás se ha vuelto a ver a un Ángel rondar por el continente.""",

    "Demonio": """La raza más peligrosa de todas se encuentra en otra dimensión, gobernando siete reinos en un ambiente posapocalíptico lleno de criaturas y seres diabólicos y malvados. Los siete jinetes o reyes del Inframundo lograron abrir una brecha en el Mar del Oeste, liberando toda su calamidad y poder, arrasando con todo a su paso. Los demonios buscan dominar todo el continente, destruyendo las razas simultáneamente en los 7 puntos cardinales. Así, casi al éxito de su conquista, fueron sucumbidos por un poder único, divino y ancestral que logró aniquilar a los siete jinetes, acabando con la gran guerra y dando inicio a la nueva era de paz con el reino de MissiaM.

✍ Hasta la actualidad, no se ha tenido avistamiento de ningún demonio en ninguna región."""
}

# =========================
# FUNCIONES AUXILIARES
# =========================
def normalizar_nombre(nombre):
    return " ".join(word.capitalize() for word in nombre.replace("_", " ").split())

def nombre_valido(nombre):
    if not 1 <= len(nombre) <= 20:
        return False

    for c in nombre:
        if not (c.isalpha() or c.isspace()):
            return False

    return True

# =========================
# BOTONES
# =========================
def botones_genero():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Masculino", callback_data="genero_M")],
        [InlineKeyboardButton("Femenino", callback_data="genero_F")]
    ])

def botones_confirmar_genero():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirmar", callback_data="confirmar_genero")],
        [InlineKeyboardButton("🔙 Volver", callback_data="volver_genero")]
    ])

# =========================
# BOTONES DE RAZAS
# =========================
def botones_razas(genero):

    gratis_base = [
        "Humano",
        "Elfo",
        "Enano",
        "SemiBestia"
    ]

    premium = [
        "Draconiano",
        "Argoniano",
        "Necromano",
        "Skaldar"
    ]

    if genero == "Masculino":
        gratis = gratis_base + ["Gigante"]
    else:
        gratis = gratis_base + ["Sirena"]

    botones = []

    max_len = max(len(gratis), len(premium))

    for i in range(max_len):
        fila = []

        if i < len(gratis):
            fila.append(
                InlineKeyboardButton(
                    f"🆓 {gratis[i]}",
                    callback_data=f"raza_{gratis[i]}"
                )
            )

        if i < len(premium):
            fila.append(
                InlineKeyboardButton(
                    f"💎 {premium[i]}",
                    callback_data=f"raza_{premium[i]}"
                )
            )

        botones.append(fila)

    botones.append([
        InlineKeyboardButton(" ", callback_data="ignore")
    ])

    botones.append([
        InlineKeyboardButton(
            "🪽 Ángeles",
            callback_data="raza_Ángeles"
        ),
        InlineKeyboardButton(
            "😈 Demonio",
            callback_data="raza_Demonio"
        )
    ])

    return InlineKeyboardMarkup(botones)

def botones_confirmar_raza():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirmar", callback_data="confirmar_raza")],
        [InlineKeyboardButton("🔙 Volver", callback_data="volver_raza")]
    ])

def botones_confirmar_nombre():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirmar", callback_data="confirmar_nombre")],
        [InlineKeyboardButton("❌ Cambiar", callback_data="cambiar_nombre")]
    ])

# =========================
# START / GENERO
# =========================
async def seleccionar_genero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jugador = get_player(update.effective_user.id)
    jugador["estado"] = "genero"

    msg = await update.message.reply_text(
        """🔥~Bienvenid@ a MissiaM~🔥

Un mundo de fantasía, ficción y misterios que encenderán tus cinco sentidos hasta un límite que te hará desear la ayuda de los dioses... Lleno de secretos, guerras y conspiraciones, MissiaM se convertirá en el centro de toda la discordia que lo rodea, mientras un Rey busca la paz, muchos otros conspiran para desestabilizar la corona y el legado que una vez los unió.

Descubre tu fortaleza en una de las 10 razas más prominentes del continente AeGedom y alcanza la cima de todo; conviértete en un salvador o en un destructor...

¡Los caminos están, pero la decisión es tuya!
Jóven Aventurer@ comenzarás una aventura única donde demostrarás de lo que estás hech@.

Selecciona tu género:""",
        reply_markup=botones_genero()
    )

    jugador["ui_message_id"] = msg.message_id

# =========================
# GENERO
# =========================
async def genero_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    jugador = get_player(query.from_user.id)
    data = query.data

    if data.startswith("genero_"):
        jugador["genero"] = "Masculino" if data == "genero_M" else "Femenino"

        await query.edit_message_text(
            f"Has seleccionado el género: {jugador['genero']}",
            reply_markup=botones_confirmar_genero()
        )

    elif data == "volver_genero":
        await query.edit_message_text(
            """🔥~Bienvenid@ a MissiaM~🔥

Un mundo de fantasía, ficción y misterios que encenderán tus cinco sentidos hasta un límite que te hará desear la ayuda de los dioses... Lleno de secretos, guerras y conspiraciones, MissiaM se convertirá en el centro de toda la discordia que lo rodea, mientras un Rey busca la paz, muchos otros conspiran para desestabilizar la corona y el legado que una vez los unió.

Descubre tu fortaleza en una de las 10 razas más prominentes del continente AeGedom y alcanza la cima de todo; conviértete en un salvador o en un destructor...

¡Los caminos están, pero la decisión es tuya!
Jóven Aventurer@ comenzarás una aventura única donde demostrarás de lo que estás hech@.

Selecciona tu género:""",
            reply_markup=botones_genero()
        )

    elif data == "confirmar_genero":
        await query.edit_message_text(
            "Selecciona tu raza:",
            reply_markup=botones_razas(jugador["genero"])
        )

# =========================
# RAZAS
# =========================
async def raza_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ignore":
        return

    jugador = get_player(query.from_user.id)
    data = query.data

    if data.startswith("raza_"):
        raza = data.replace("raza_", "")
        jugador["raza"] = raza

        await query.edit_message_text(
            f"⚔️ {raza}\n\n{descripciones[raza]}",
            reply_markup=botones_confirmar_raza()
        )

    elif data == "volver_raza":
        jugador["raza"] = None

        await query.edit_message_text(
            "Selecciona tu raza:",
            reply_markup=botones_razas(jugador["genero"])
        )

    elif data == "confirmar_raza":
        await query.edit_message_text(
            "✍️ Ahora escribe tu nombre usando:\n/name TuNombre"
        )

# =========================
# NOMBRE
# =========================
async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jugador = get_player(update.effective_user.id)

    if not context.args:
        await update.message.reply_text(
            "❌ Debes escribir un nombre.\nEjemplo:\n/name Arthas"
        )
        return

    nombre_temp = " ".join(context.args)
    nombre_norm = normalizar_nombre(nombre_temp)

    if not nombre_valido(nombre_norm):
        await update.message.reply_text(
            "❌ Nombre inválido.\nSolo letras y espacios.\nMáximo 20 caracteres."
        )
        return

    for u in jugadores.values():
        if u.get("nombre") == nombre_norm:
            await update.message.reply_text(
                "❌ Ese nombre ya está en uso."
            )
            return

    jugador["nombre_temp"] = nombre_temp
    jugador["nombre_temp_norm"] = nombre_norm

    await update.message.reply_text(
        f"Tu nombre será:\n\n⚔️ {nombre_norm}",
        reply_markup=botones_confirmar_nombre()
    )

# =========================
# CONFIRMAR NOMBRE
# =========================
async def confirmar_nombre_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    jugador = get_player(query.from_user.id)

    if query.data == "confirmar_nombre":
        jugador["nombre"] = jugador["nombre_temp_norm"]

        jugador["nombre_temp"] = None
        jugador["nombre_temp_norm"] = None

        await query.edit_message_text(
            f"""✅ PERSONAJE CREADO

⚔️ Nombre: {jugador['nombre']}
👤 Género: {jugador['genero']}
🧬 Raza: {jugador['raza']}"""
        )

    elif query.data == "cambiar_nombre":
        jugador["nombre_temp"] = None
        jugador["nombre_temp_norm"] = None

        await query.edit_message_text(
            "✍️ Escribe un nuevo nombre usando:\n/name TuNombre"
        )

# =========================
# MAIN
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", seleccionar_genero))
app.add_handler(
    CallbackQueryHandler(
        genero_handler,
        pattern="^(genero_|volver_genero|confirmar_genero)"
    )
)

app.add_handler(
    CallbackQueryHandler(
        raza_handler,
        pattern="^(raza_|volver_raza|confirmar_raza|ignore)"
    )
)

app.add_handler(CommandHandler("name", set_name))

app.add_handler(
    CallbackQueryHandler(
        confirmar_nombre_handler,
        pattern="^(confirmar_nombre|cambiar_nombre)"
    )
)

print("BOT ENCENDIDO")

app.run_polling()
