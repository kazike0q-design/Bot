valenia_mercado = {
    "mercado_valenia": {
        "nombre": "Mercado Central",
        "descripcion": "Plaza comercial con puestos de artesanos, herreros y alquimistas.",
        "conexiones": [
            "alquimista_valenia",
            "herrero_valenia",
            "armeria_valenia",
            "textiles_valenia",
            "casa_arden_valenia",
            "gremio_valenia",
            "castillo_valenia",
            "puerto_valenia"
        ],
        "acciones": ["comprar", "vender"]
    },
    "alquimista_valenia": {
        "nombre": "Alquimista",
        "descripcion": "Tienda de pociones y componentes raros.",
        "conexiones": ["mercado_valenia"],
        "acciones": ["comprar_pociones"]
    },
    "herrero_valenia": {
        "nombre": "Herrero",
        "descripcion": "Forja donde se reparan y mejoran armas y armaduras.",
        "conexiones": ["mercado_valenia"],
        "acciones": ["forjar", "reparar"]
    },
    "armeria_valenia": {
        "nombre": "Armería",
        "descripcion": "Venta especializada en armas finas y piezas únicas.",
        "conexiones": ["mercado_valenia"],
        "acciones": ["comprar_armas"]
    },
    "textiles_valenia": {
        "nombre": "Textiles",
        "descripcion": "Puesto de telas y ropa, desde ropajes comunes hasta trajes nobles.",
        "conexiones": ["mercado_valenia"],
        "acciones": ["comprar_ropa"]
    },
    "casa_arden_valenia": {
        "nombre": "Casa Arden",
        "descripcion": "Residencia noble con influencia en la política local.",
        "conexiones": ["mercado_valenia", "muralla_norte_valenia", "residencia_norte_valenia", "muralla_este_valenia"],
        "acciones": ["entrar_casa_arden"]
    }
}
