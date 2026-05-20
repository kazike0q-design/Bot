# mapas/bfs.py
from collections import deque
from mapas.mapa_global import mapa_global
from mapas.accesos import chequear_acceso

PROHIBIDOS = {"los7infiernos", "templo_celestial", "neridias"}

def bfs(inicio, destino, jugador=None):
    """
    BFS que respeta:
      - nodos prohibidos
      - nodos con 'viaje_directo' == False
      - nodos con 'requisitos' (placeholder)
      - condiciones de acceso (si se pasa jugador)
    Devuelve la lista de nodos (camino) o None si no hay ruta.
    """
    if inicio not in mapa_global or destino not in mapa_global:
        return None

    cola = deque([(inicio, [inicio])])
    visitados = set()

    while cola:
        actual, camino = cola.popleft()

        if actual == destino:
            return camino

        if actual in visitados:
            continue
        visitados.add(actual)

        for vecino in mapa_global.get(actual, {}).get("conexiones", []):
            if vecino in visitados:
                continue
            if vecino in PROHIBIDOS:
                continue

            nodo_info = mapa_global.get(vecino, {})

            # Si se pasó jugador, chequear acceso al vecino
            if jugador:
                ok, mensaje = chequear_acceso(jugador, nodo_info)
                if not ok:
                    continue

            # Filtrar por viaje_directo (clave: 'viaje_directo') y requisitos
            if not nodo_info.get("viaje_directo", True):
                continue
            if nodo_info.get("requisitos"):
                continue

            cola.append((vecino, camino + [vecino]))

    return None
