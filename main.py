from telegram.ext import Application
import os

from handlers.race_handlers import register_race_handlers
from handlers.start import register_start_handlers

TOKEN = os.getenv("BOT_TOKEN")


def main():
    app = Application.builder().token(TOKEN).build()

    # Registrar handlers
    register_start_handlers(app)
    register_race_handlers(app)

    print("MissiaM iniciado correctamente.")

    app.run_polling()


if __name__ == "__main__":
    main()
