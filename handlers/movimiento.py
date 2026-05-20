# bot_handlers.py  (fragmento para pegar en bot.py)
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from mapas.mapa_global import mapa_global
from mapas.movimiento import calculartiempomovimiento, mover_jugador, puedemoverglobal
from mapas.bfs import bfs
from mapas.viajes import viaje_automatico
from mapas.accesos import chequear_acceso
from mapas.submapas import SUBMAPAS, ENTRADAS_CIUDADES

# Jugadores en memoria (asegúrate de usar la misma variable en todo el proyecto)
jugadores = {}

def get_player(user_id: int):
    """
    Crea o devuelve la ficha del jugador. Asegura que exista un asyncio.Lock por jugador.
    """
    import asyncio as _asyncio
    if user_id not in jugadores:
        jugadores[user_id] = {
            "ubicacion": "bosque",
            "en_ciudad": False,
            "sububicacion": None,
            "ciudad": None,
            "moviendo": False,
            "lock": _asyncio.Lock(),
            "montura_equipada": False,
            "tipo_montura": None,
            "pocion_velocidad": None,
            "peso_inventario": 0,
            "energia": 100,
            "oro": 0,
            "nivel": 1,
            "monturaguardadaen": None
        }
    return jugadores[user_id]

def botones_global(jugador):
    """
    Construye InlineKeyboardMarkup con destinos conectados al nodo global actual.
    callback_data: move_<destino>
    """
    botones = []
    origen = jugador["ubicacion"]
    for destino in mapa_global.get(origen, {}).get("conexiones", []):
        nombre = mapa_global.get(destino, {}).get("nombre", destino)
        botones.append([InlineKeyboardButton(nombre, callback_data=f"move_{destino}")])
    return InlineKeyboardMarkup(botones) if botones else None

def botones_ciudad(jugador, submapas):
    """
    Construye InlineKeyboardMarkup para movimientos dentro de la ciudad.
    callback_data: city_<destino>
    """
    botones = []
    ciudad = jugador["ciudad"]
    if not ciudad or ciudad not in submapas:
        return None
    actual = jugador["sububicacion"]
    for destino in submapas[ciudad][actual]["conexiones"]:
        nombre = submapas[ciudad].get(destino, {}).get("nombre", destino)
        botones.append([InlineKeyboardButton(nombre, callback_data=f"city_{destino}")])
    return InlineKeyboardMarkup(botones) if botones else None

# Movimiento global por botón (30s base)
async def mover_global(update: Update, context: ContextTypes.DEFAULT_TYPE, destino: str):
    query = update.callback_query
    await query.answer()
    jugador = get_player(query.from_user.id)

    async with jugador["lock"]:
        if jugador["moviendo"]:
            return
        jugador["moviendo"] = True

        # Validar que destino esté conectado desde la ubicación actual
        ok_conn, msg_conn = puedemoverglobal(jugador, destino)
        if not ok_conn:
            await query.edit_message_text(msg_conn)
            jugador["moviendo"] = False
            return

        # Validar acceso al destino
        ok, mensaje = chequear_acceso(jugador, mapa_global.get(destino, {}))
        if not ok:
            await query.edit_message_text(mensaje)
            jugador["moviendo"] = False
            return

        tiempo = calculartiempomovimiento(jugador, tiempo_base=30, duplicar=False)
        await query.edit_message_text(f"⏳ Viajando a {mapa_global.get(destino, {}).get('nombre', destino)}... ({tiempo}s)")
        await asyncio.sleep(tiempo)

        jugador["ubicacion"] = destino
        jugador["moviendo"] = False

        await query.edit_message_text(
            f"📍 {mapa_global.get(destino, {}).get('nombre', destino)}",
            reply_markup=botones_global(jugador)
        )

# Entrar a ciudad (5s base)
async def entrar_ciudad(update: Update, context: ContextTypes.DEFAULT_TYPE, puerta: str, submapas: dict):
    query = update.callback_query
    await query.answer()
    jugador = get_player(query.from_user.id)

    async with jugador["lock"]:
        if jugador["moviendo"]:
            return
        jugador["moviendo"] = True

        # Validar que la puerta tenga entrada definida
        entrada = ENTRADAS_CIUDADES.get(puerta)
        if not entrada:
            await query.edit_message_text("❌ Esta puerta no tiene entrada definida.")
            jugador["moviendo"] = False
            return

        tiempo = calculartiempomovimiento(jugador, tiempo_base=5, duplicar=False)
        await query.edit_message_text(f"⏳ Entrando a la ciudad... ({tiempo}s)")
        await asyncio.sleep(tiempo)

        jugador["en_ciudad"] = True
        jugador["ciudad"], jugador["sububicacion"] = entrada
        jugador["moviendo"] = False

        await query.edit_message_text(
            f"🏙️ {submapas[jugador['ciudad']][jugador['sububicacion']]['nombre']}",
            reply_markup=botones_ciudad(jugador, submapas)
        )

# Movimiento dentro de ciudad: validar conexiones y condiciones
async def mover_ciudad(update: Update, context: ContextTypes.DEFAULT_TYPE, destino: str, submapas: dict):
    query = update.callback_query
    await query.answer()
    jugador = get_player(query.from_user.id)

    ciudad = jugador.get("ciudad")
    actual = jugador.get("sububicacion")
    if not ciudad or not actual:
        await query.edit_message_text("❌ No estás en una ciudad.")
        return

    if destino not in submapas[ciudad][actual]["conexiones"]:
        await query.edit_message_text("❌ No puedes ir allí desde aquí.")
        return

    nodo_info = submapas[ciudad][destino]
    ok, mensaje = chequear_acceso(jugador, nodo_info)
    if not ok:
        await query.edit_message_text(mensaje)
        return

    jugador["sububicacion"] = destino
    await query.edit_message_text(
        f"📍 {submapas[ciudad][destino]['nombre']}",
        reply_markup=botones_ciudad(jugador, submapas)
    )

# /godirect command: ruta por BFS, tiempo = (saltos*60) modificado y duplicado
async def godirect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jugador = get_player(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Uso: /godirect destino_id")
        return
    destino = context.args[0]
    if destino not in mapa_global:
        await update.message.reply_text("❌ Destino inválido")
        return

    # Prohibir destinos especiales
    if destino in ["los7infiernos", "templo_celestial", "neridias"]:
        await update.message.reply_text("❌ Esta zona es especial, no accesible")
        return

    # Chequear acceso al destino final
    ok, mensaje = chequear_acceso(jugador, mapa_global.get(destino, {}))
    if not ok:
        await update.message.reply_text(mensaje)
        return

    # BFS pasando jugador para filtrar nodos inaccesibles
    ruta = bfs(jugador["ubicacion"], destino, jugador=jugador)
    if not ruta:
        await update.message.reply_text("❌ No hay ruta disponible")
        return

    tiempo_base = (len(ruta) - 1) * 60
    tiempo_final = calculartiempomovimiento(jugador, tiempo_base=tiempo_base, duplicar=True)

    nombres = " → ".join([mapa_global[n]["nombre"] for n in ruta])
    await update.message.reply_text(f"⏳ Viajando...\n🧭 {nombres}\n⌛ {tiempo_final}s")
    await asyncio.sleep(tiempo_final)

    jugador["ubicacion"] = destino
    await update.message.reply_text(f"📍 Has llegado a {mapa_global[destino]['nombre']}", reply_markup=botones_global(jugador))

# Callback handler para botones
async def botones_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    jugador = get_player(query.from_user.id)

    if data.startswith("move_"):
        destino = data.split("_", 1)[1]
        # Si es entrada a ciudad, llamar a entrar_ciudad con SUBMAPAS importado
        if destino in ENTRADAS_CIUDADES:
            await entrar_ciudad(update, context, destino, SUBMAPAS)
        else:
            await mover_global(update, context, destino)
    elif data.startswith("city_"):
        destino = data.split("_", 1)[1]
        await mover_ciudad(update, context, destino, SUBMAPAS)

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jugador = get_player(update.effective_user.id)
    await update.message.reply_text(
        f"📍 {mapa_global.get(jugador['ubicacion'], {}).get('nombre', jugador['ubicacion'])}",
        reply_markup=botones_global(jugador)
    )

# Ejemplo de registro de handlers en main (ajusta token y nombres de archivo)
def main():
    app = ApplicationBuilder().token("TUTOKENAQUI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("godirect", godirect))
    app.add_handler(CallbackQueryHandler(botones_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
