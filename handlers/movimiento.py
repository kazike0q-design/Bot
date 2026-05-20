# bot_handlers.py  (fragmento integrado listo para pegar/reemplazar)
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
            # ubicación y estado
            "ubicacion": "bosque",   # nodo global por defecto
            "en_ciudad": False,
            "sububicacion": None,
            "ciudad": None,
            # control de movimiento / concurrencia
            "moviendo": False,
            "lock": _asyncio.Lock(),
            # atributos básicos
            "montura_equipada": False,
            "tipo_montura": None,
            "pocion_velocidad": None,
            "peso_inventario": 0,
            "energia": 100,
            "oro": 0,
            "nivel": 1,
            "monturaguardadaen": None,
            # campos de creación (si tu bot los usa)
            "genero": None,
            "raza": None,
            "nombre": None,
            "nombre_temp": None,
            "nombre_temp_norm": None,
            "estado": "genero"
        }
    return jugadores[user_id]

def botones_global(jugador):
    """
    Construye InlineKeyboardMarkup con destinos conectados al nodo global actual.
    Añade siempre el botón '🗺️ Ubicación' al final.
    """
    botones = []
    origen = jugador["ubicacion"]
    for destino in mapa_global.get(origen, {}).get("conexiones", []):
        nombre = mapa_global.get(destino, {}).get("nombre", destino)
        botones.append([InlineKeyboardButton(nombre, callback_data=f"move_{destino}")])

    # Botón permanente para ver la ubicación actual
    botones.append([InlineKeyboardButton("🗺️ Ubicación", callback_data="ubicacion")])

    return InlineKeyboardMarkup(botones) if botones else InlineKeyboardMarkup([[InlineKeyboardButton("🗺️ Ubicación", callback_data="ubicacion")]])

def botones_ciudad(jugador, submapas):
    """
    Construye InlineKeyboardMarkup para movimientos dentro de la ciudad.
    Añade siempre el botón '🗺️ Ubicación' al final.
    """
    botones = []
    ciudad = jugador["ciudad"]
    if not ciudad or ciudad not in submapas:
        # aun así devolvemos el botón de ubicación para poder consultarla
        return InlineKeyboardMarkup([[InlineKeyboardButton("🗺️ Ubicación", callback_data="ubicacion")]])

    actual = jugador["sububicacion"]
    for destino in submapas[ciudad][actual]["conexiones"]:
        nombre = submapas[ciudad].get(destino, {}).get("nombre", destino)
        botones.append([InlineKeyboardButton(nombre, callback_data=f"city_{destino}")])

    # Botón permanente para ver la ubicación actual dentro de la ciudad
    botones.append([InlineKeyboardButton("🗺️ Ubicación", callback_data="ubicacion")])

    return InlineKeyboardMarkup(botones) if botones else InlineKeyboardMarkup([[InlineKeyboardButton("🗺️ Ubicación", callback_data="ubicacion")]])

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

        # Mensaje al llegar: nombre + descripción si existe
        nombre = mapa_global.get(destino, {}).get("nombre", destino)
        descripcion = mapa_global.get(destino, {}).get("descripcion") or mapa_global.get(destino, {}).get("texto") or ""
        texto = f"📍 {nombre}"
        if descripcion:
            texto += f"\n\n{descripcion}"

        await query.edit_message_text(
            texto,
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

        # Mensaje al entrar: nombre + descripción si existe
        nodo = submapas[jugador['ciudad']][jugador['sububicacion']]
        nombre = nodo.get("nombre", jugador['sububicacion'])
        descripcion = nodo.get("descripcion") or nodo.get("texto") or ""
        texto = f"🏙️ {nombre}"
        if descripcion:
            texto += f"\n\n{descripcion}"

        await query.edit_message_text(
            texto,
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

    # Mensaje al moverse dentro de la ciudad
    nombre = submapas[ciudad][destino].get("nombre", destino)
    descripcion = submapas[ciudad][destino].get("descripcion") or submapas[ciudad][destino].get("texto") or ""
    texto = f"📍 {nombre}"
    if descripcion:
        texto += f"\n\n{descripcion}"

    await query.edit_message_text(
        texto,
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
    nombre = mapa_global[destino].get("nombre", destino)
    await update.message.reply_text(f"📍 Has llegado a {nombre}", reply_markup=botones_global(jugador))

# Mostrar la ubicación actual (reenvía el mensaje con nombre + descripción)
async def mostrar_ubicacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    jugador = get_player(query.from_user.id)

    # Si está dentro de una ciudad, mostrar submapa
    if jugador.get("en_ciudad"):
        ciudad = jugador.get("ciudad")
        sub = jugador.get("sububicacion")
        if ciudad and sub and ciudad in SUBMAPAS and sub in SUBMAPAS[ciudad]:
            nodo = SUBMAPAS[ciudad][sub]
            nombre = nodo.get("nombre", sub)
            descripcion = nodo.get("descripcion") or nodo.get("texto") or ""
            texto = f"📍 {nombre}"
            if descripcion:
                texto += f"\n\n{descripcion}"
            reply_markup = botones_ciudad(jugador, SUBMAPAS)
        else:
            texto = "❌ No se encontró la ubicación dentro de la ciudad."
            reply_markup = None
    else:
        # Ubicación global
        ubic = jugador.get("ubicacion")
        nodo = mapa_global.get(ubic, {}) if ubic else {}
        nombre = nodo.get("nombre", ubic or "No asignada")
        descripcion = nodo.get("descripcion") or nodo.get("texto") or ""
        texto = f"📍 {nombre}"
        if descripcion:
            texto += f"\n\n{descripcion}"
        reply_markup = botones_global(jugador)

    # Intentar editar el mensaje original; si falla, enviar un nuevo mensaje
    try:
        await query.edit_message_text(texto, reply_markup=reply_markup)
    except Exception:
        await query.message.reply_text(texto, reply_markup=reply_markup)

# Callback handler para botones (actualizado para 'ubicacion')
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
    elif data == "ubicacion":
        await mostrar_ubicacion(update, context)

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
