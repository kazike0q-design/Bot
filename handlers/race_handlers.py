from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from game.races import RACES

async def race_intro_after_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    race = context.user_data.get("race", "Humano")

    if race == "Humano":
        race_text = "Los humanos son una raza estupenda, con un corazón muy noble."
    elif race == "Elfo":
        race_text = "Los elfos son una raza estupenda, con gran sabiduría acumulada gracias a su longeva vitalidad y cultura."
    else:
        race_text = "Los enanos son una raza estupenda, son muy buenos fabricando y construyendo gracias a sus hábiles manos."

    text = f"""
╔════════════════════════════╗
                         🔥『 MissiaM 』🔥
╚════════════════════════════╝

¡Excelente elección de la naturaleza! 🌿✨ *{race_text}* Me hace muy feliz que seas uno de ellos. 💖

—Se acerca flotando un poco más, hablando en un tono cómplice— 🌬️

¡Vaya cabeza la mía, se me pasaba decirte lo más importante! 🤦‍♀️ Ahora mismo nos encontramos en medio del bosque. 🌲 Los ancestros me trajeron hasta ti por un motivo misterioso... ¡pero no te preocupes, caminante! 🛡️ Puedo invocar un portal mágico que te deje sano y salvo en tu propio reino para que comiences tu viaje. 🌀🏰

—Te mira de reojo con una sonrisa traviesa y junta sus manos— 😉🤞

Solo... démonos un pequeño deseo de buena suerte, ¿sí? 🤞 Esperemos que mi energía mágica no decida tomarse una siesta a mitad del camino. 💤✨

Progreso : ██████▒▒▒▒ 60%
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "Entrar al Portal 🪞",
                callback_data="enter_portal"
            )
        ]
    ]

    await query.edit_message_caption(
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
  
async def enter_portal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_caption(
        caption="🌀 El portal se abre... comienzas tu aventura en MissiaM..."
    )

RACE_SELECTION_TEXT = """
╔════════════════════════════╗
                         🔥『 MissiaM 』🔥
╚════════════════════════════╝

¡¡Oh, maravilloso! Entonces perteneces a esa hermosa mitad que trae vida y continuidad al mundo 🌍✨. Es realmente interesante cómo se dividen los caminantes... 🚶‍♂️👣

—Te observa con ojos brillantes ✨, ladeando la cabeza con una sonrisa curiosa—

Dime, buen viajero... 🧭 En este rincón del mundo conviven muchísimas razas distintas, y muchas de ellas comparten tu misma forma de ser. Para poder guiarte mejor por sus senderos 🛤️, ¿me dirías a qué raza perteneces? Mi corazón tiene mucha intriga por conocer tus raíces 🌱💖.

Progreso : ███▒▒▒▒▒▒▒ 30%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


async def show_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    race_key = query.data.replace("race_", "")

    if race_key not in RACES:
        return

    race_data = RACES[race_key]

    keyboard = [
        [
            InlineKeyboardButton(
                race_data["confirm_text"],
                callback_data=race_data["confirm_callback"]
            )
        ],
        [
            InlineKeyboardButton(
                "⬅ Volver a Razas",
                callback_data="back_race_selection"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_caption(
        caption=race_data["description"],
        reply_markup=reply_markup
    )


async def back_to_race_selection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "Humanos 🧑‍💼",
                callback_data="race_human"
            )
        ],
        [
            InlineKeyboardButton(
                "Elfos 🧝",
                callback_data="race_elf"
            )
        ],
        [
            InlineKeyboardButton(
                "Enanos 👷‍♂",
                callback_data="race_dwarf"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_caption(
        caption=RACE_SELECTION_TEXT,
        reply_markup=reply_markup
    )


async def confirm_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    race_key = query.data.replace("confirm_race_", "")

    if race_key not in RACES:
        return

    context.user_data["race"] = RACES[race_key]["name"]

    await race_intro_after_confirm(update, context)
    return

def register_race_handlers(app):

    app.add_handler(
        CallbackQueryHandler(
            show_race,
            pattern="^race_(human|elf|dwarf)$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            confirm_race,
            pattern="^confirm_race_(human|elf|dwarf)$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            back_to_race_selection,
            pattern="^back_race_selection$"
        )
    )
    
    app.add_handler(
        CallbackQueryHandler(
            enter_portal,
            pattern="^enter_portal$"
        )
    )
