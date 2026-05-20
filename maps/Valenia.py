# mapas/ciudades/valenia.py
valenia_data = {
    "descripcion": (
        "Valenia, ciudad costera fortificada y corazón "
        "del comercio marítimo del continente."
    )
}

valenia_submapas = {
    "puerta_oeste": {
        "nombre": "Puerta Oeste",
        "tipo": "puerta",
        "conexiones": ["establo_oeste", "zona_residencial"],
        "salida": None
    },
    "puerta_suroeste": {
        "nombre": "Puerta Suroeste",
        "tipo": "puerta",
        "conexiones": ["establo_suroeste", "taberna"],
        "salida": None
    },
    "establo_oeste": {
        "nombre": "Establo Oeste",
        "tipo": "establo",
        "conexiones": ["puerta_oeste"]
    },
    "establo_suroeste": {
        "nombre": "Establo Suroeste",
        "tipo": "establo",
        "conexiones": ["puerta_suroeste"]
    },
    "zona_residencial": {
        "nombre": "Zona Residencial",
        "tipo": "residencial",
        "conexiones": [
            "puerta_oeste",
            "taberna",
            "castillo",
            "hospital",
            "torre_mago"
        ]
    },
    "taberna": {
        "nombre": "Taberna y Posadas",
        "tipo": "taberna",
        "conexiones": [
            "puerta_suroeste",
            "zona_residencial",
            "castillo",
            "gremio"
        ]
    },
    "castillo": {
        "nombre": "Castillo de Valenia",
        "tipo": "castillo",
        "conexiones": [
            "zona_residencial",
            "taberna",
            "hospital",
            "banco_almacenes",
            "casa_arden",
            "puerto",
            "calle_comercio",
            "gremio"
        ]
    },
    "hospital": {
        "nombre": "Hospital",
        "tipo": "hospital",
        "conexiones": ["zona_residencial", "castillo", "banco_almacenes"]
    },
    "torre_mago": {
        "nombre": "Torre del Mago",
        "tipo": "magia",
        "conexiones": ["zona_residencial"]
    },
    "banco_almacenes": {
        "nombre": "Banco y Almacenes",
        "tipo": "banco",
        "conexiones": ["hospital", "castillo", "casa_arden"]
    },
    "casa_arden": {
        "nombre": "Casa de Representación (Arden)",
        "tipo": "nobleza",
        "conexiones": ["banco_almacenes", "castillo", "puerto"]
    },
    "puerto": {
        "nombre": "Puerto",
        "tipo": "puerto",
        "conexiones": ["casa_arden", "castillo", "calle_comercio"]
    },
    "calle_comercio": {
        "nombre": "Calle del Comercio",
        "tipo": "comercio",
        "conexiones": ["puerto", "castillo", "gremio"]
    },
    "gremio": {
        "nombre": "Gremio",
        "tipo": "gremio",
        "conexiones": ["calle_comercio", "taberna", "castillo"]
    }
}
