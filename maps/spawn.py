# mapas/spawn.py
import random
import importlib
from typing import Optional, Tuple

# Intento de importar get_player desde el bot; si no está disponible, el llamador debe pasar jugador_obj
try:
    from bot import get_player
except Exception:
    get_player = None

# Mapeo de raza -> nombre del módulo/reino (archivo en mapas/ciudades/<reino>.py)
RAZA_A_REINO = {
    "Humano": "valenia",
    "Elfo": "bosque_milenario",
    "Enano": "durnhall",
    "SemiBestia": "feralia",
    "Gigante": "jotunheim",
    "Sirena": "neridias",
    "Draconiano": "missiam",
    "Argoniano": "missiam",
    "Necromano": "missiam",
    "Skaldar": "missiam",
    "Ángeles": "missiam",
    "Demonio": "missiam"
}

def _cargar_submapa_reino(reino: str) -> Optional[dict]:
    """
    Intenta importar mapas.ciudades.<reino> y devolver <reino>_submapas o submapas.
    """
    module_name = f"mapas.ciudades.{reino}"
    try:
        mod = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None

    var_name = f"{reino}_submapas"
    if hasattr(mod, var_name):
        return getattr(mod, var_name)
    if hasattr(mod, "submapas"):
        return getattr(mod, "submapas")
    # Si el módulo exporta directamente un dict con el mismo nombre del reino
    if hasattr(mod, reino):
        return getattr(mod, reino)
    return None

def _obtener_puertas(submapa: dict) -> list:
    return [k for k, v in submapa.items() if v.get("tipo") == "puerta"]

def _obtener_establos(submapa: dict) -> list:
    return [k for k, v in submapa.items() if v.get("tipo") == "establo"]

def _elegir_nodo_spawn(submapa: dict) -> str:
    """
    Elige un nodo para spawn dentro del submapa:
    1) puerta aleatoria
    2) establo aleatorio
    3) cualquier nodo aleatorio
    """
    puertas = _obtener_puertas(submapa)
    if puertas:
        return random.choice(puertas)
    establos = _obtener_establos(submapa)
    if establos:
        return random.choice(establos)
    claves = list(submapa.keys())
    if not claves:
        raise ValueError("Submapa vacío: no hay nodos donde spawnear.")
    return random.choice(claves)

def spawn_player_by_race(user_id: Optional[int] = None, jugador_obj: Optional[dict] = None) -> Tuple[bool, dict]:
    """
    Asigna spawn al jugador según su raza.
    - Si get_player está disponible y se pasa user_id, obtiene la ficha.
    - Alternativamente acepta jugador_obj (diccionario) y lo modifica in-place.
    Retorna (ok, info) donde info contiene 'ubicacion', 'ciudad', 'sububicacion', 'mensaje'.
    """
    if jugador_obj is None:
        if user_id is None or get_player is None:
            return False, {"error": "No se proporcionó jugador ni get_player disponible."}
        jugador = get_player(user_id)
    else:
        jugador = jugador_obj

    raza = jugador.get("raza") or "Humano"
    reino = RAZA_A_REINO.get(raza, "missiam")

    # Cargar submapa desde mapas/ciudades/<reino>.py
    submapa = _cargar_submapa_reino(reino)
    if not submapa:
        # fallback a missiam
        submapa = _cargar_submapa_reino("missiam")
        reino = "missiam"
        if not submapa:
            return False, {"error": f"No existe submapa para la raza {raza} ni 'missiam'."}

    # Elegir una sububicación (preferencia: puerta)
    nodo_sub = _elegir_nodo_spawn(submapa)

    # Actualizar ficha del jugador: colocarlo en la puerta elegida (clave del submapa)
    # Nota: asumimos que la clave del submapa coincide con el nodo global de la puerta
    jugador["ubicacion"] = nodo_sub
    jugador["en_ciudad"] = True
    jugador["ciudad"] = reino
    jugador["sububicacion"] = nodo_sub

    mensaje = f"Spawn asignado: raza={raza} → reino={reino} → puerta={nodo_sub}"
    return True, {
        "ubicacion": nodo_sub,
        "ciudad": reino,
        "sububicacion": nodo_sub,
        "mensaje": mensaje
    }

# Ejemplo de uso desde un handler (adaptar a tu bot)
def spawn_handler_example(update, context):
    user_id = update.effective_user.id
    ok, info = spawn_player_by_race(user_id=user_id)
    if not ok:
        update.message.reply_text(f"Error al spawnear: {info.get('error')}")
    else:
        update.message.reply_text(info["mensaje"])
