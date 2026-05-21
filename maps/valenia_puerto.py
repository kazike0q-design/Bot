valenia_puerto = {
    "puerto_valenia": {
        "nombre": "Puerto de Valenia",
        "descripcion": "Zona portuaria con comercio marítimo y muelles activos.",
        "conexiones": [
            "puerto_comercial_valenia",
            "muralla_este_valenia",
            "muelle_valenia",
            "mercado_valenia"
        ],
        "acciones": ["entrar_puerto"]
    },
    "puerto_comercial_valenia": {
        "nombre": "Puerto Comercial",
        "descripcion": "Área de carga y comercio internacional.",
        "conexiones": ["puerto_valenia"],
        "acciones": []
    },
    "muelle_valenia": {
        "nombre": "Muelle",
        "descripcion": "Muelle con acceso a barcos y zona pesquera.",
        "conexiones": ["entrada_fosas_marinas_valenia", "zona_pesquera_valenia", "barco_valenia", "puerto_valenia"],
        "acciones": ["embarcar"]
    },
    "zona_pesquera_valenia": {
        "nombre": "Zona Pesquera",
        "descripcion": "Área donde los pescadores trabajan y venden su captura.",
        "conexiones": ["muelle_valenia"],
        "acciones": ["pescar"]
    },
    "barco_valenia": {
        "nombre": "Barco",
        "descripcion": "Embarcación mercante lista para zarpar.",
        "conexiones": ["muelle_valenia"],
        "acciones": ["viajar_en_barco"]
    },
    "entrada_fosas_marinas_valenia": {
        "nombre": "Entrada a las Fosas Marinas",
        "descripcion": "Acceso a una zona peligrosa en el mar, solo para aventureros preparados.",
        "conexiones": ["muelle_valenia"],
        "acciones": ["explorar_fosas"]
    }
}
