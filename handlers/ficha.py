# -------------------------
# Botón y handler: mostrar ficha del personaje
# -------------------------

def botones_ficha():
    """
    InlineKeyboardMarkup con un botón para ver la ficha.
    Puedes añadir este markup a cualquier mensaje (por ejemplo al menú principal).
    """
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Alma", callback_data="ficha")]
    ])

async def ficha_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    CallbackQuery handler que muestra nombre, género, raza y ubicación del jugador.
    Mantiene el botón para que pueda pulsarse repetidamente.
    """
    query = update.callback_query
    await query.answer()

    jugador = get_player(query.from_user.id)

    # Si la ficha usa lock (si la inicializaste), úsala para evitar condiciones de carrera
    lock = jugador.get("lock")
    if lock:
        async with lock:
            texto = (
                f"📋 FICHA\n\n"
                f"⚔️ Nombre: {jugador.get('nombre') or 'No asignado'}\n"
                f"👤 Género: {jugador.get('genero') or 'No asignado'}\n"
                f"🧬 Raza: {jugador.get('raza') or 'No asignada'}\n\n"
                f"📍 Ubicación: {jugador.get('ubicacion') or 'No asignada'}"
            )
    else:
        texto = (
            f"📋 FICHA\n\n"
            f"⚔️ Nombre: {jugador.get('nombre') or 'No asignado'}\n"
            f"👤 Género: {jugador.get('genero') or 'No asignado'}\n"
            f"🧬 Raza: {jugador.get('raza') or 'No asignada'}\n\n"
            f"📍 Ubicación: {jugador.get('ubicacion') or 'No asignada'}"
        )

    # Edita el mensaje original para mostrar la ficha y deja el botón para volver a pulsar
    try:
        await query.edit_message_text(texto, reply_markup=botones_ficha())
    except Exception:
        # Si no se puede editar (p. ej. el mensaje original no es editable), enviar un nuevo mensaje
        await query.message.reply_text(texto, reply_markup=botones_ficha())

# -------------------------
# Registro del handler (añádelo donde registras los demás handlers)
# -------------------------
# app.add_handler(CallbackQueryHandler(ficha_handler, pattern="^ficha$"))
