valenia_gremio = {
    "gremio_valenia": {
        "nombre": "Gremio de Valenia",
        "descripcion": "Sede del gremio local: contratos, misiones y tablones de anuncios.",
        "conexiones": [
            "residencia_sur_2_valenia",
            "mercado_valenia",
            "muralla_este_valenia",
            "banco_almacen_valenia",
            "entrada_sur_valenia"
        ],
        "acciones": ["aceptar_mision", "consultar_tablon"]
    },
    "gremio_interior_valenia": {
        "nombre": "Interior del Gremio",
        "descripcion": "Oficinas y sala de reuniones del gremio.",
        "conexiones": ["gremio_valenia"],
        "acciones": []
    }
}
