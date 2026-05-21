valenia_hospital = {
    "hospital_taberna_valenia": {
        "nombre": "Hospital y Taberna",
        "descripcion": "Edificio conjunto: el hospital al norte y la taberna al sur, punto de encuentro.",
        "conexiones": [
            "entrada_oeste_valenia",
            "castillo_valenia",
            "residencia_norte_2_valenia",
            "residencia_sur_valenia"
        ],
        "acciones": ["hospital_valenia", "taberna_valenia"]
    },
    "hospital_valenia": {
        "nombre": "Hospital de Valenia",
        "descripcion": "Centro de curación y reposo para aventureros heridos.",
        "conexiones": ["hospital_taberna_valenia"],
        "acciones": ["curar"]
    },
    "taberna_valenia": {
        "nombre": "Taberna del Puerto",
        "descripcion": "Taberna ruidosa donde se cuentan historias y se contratan trabajos.",
        "conexiones": ["hospital_taberna_valenia"],
        "acciones": ["beber", "contratar_trabajo"]
    }
}
