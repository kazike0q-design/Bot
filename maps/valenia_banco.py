valenia_banco = {
    "banco_almacen_valenia": {
        "nombre": "Banco y Almacén",
        "descripcion": "Institución financiera y almacén de mercancías.",
        "conexiones": [
            "castillo_valenia",
            "muralla_sur_valenia",
            "residencia_sur_valenia",
            "gremio_valenia"
        ],
        "acciones": ["depositar", "retirar", "acceder_almacen"]
    },
    "banco_valenia": {
        "nombre": "Banco",
        "descripcion": "Oficinas bancarias para transacciones y cofres.",
        "conexiones": ["banco_almacen_valenia"],
        "acciones": []
    },
    "almacen_valenia": {
        "nombre": "Almacén",
        "descripcion": "Granero y depósito de mercancías.",
        "conexiones": ["banco_almacen_valenia"],
        "acciones": []
    }
}
