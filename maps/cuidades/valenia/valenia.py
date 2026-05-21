from .valenia_castillo import valenia_castillo
from .valenia_residencias import valenia_residencias
from .valenia_murallas import valenia_murallas
from .valenia_hospital import valenia_hospital
from .valenia_mercado import valenia_mercado
from .valenia_puerto import valenia_puerto
from .valenia_gremio import valenia_gremio
from .valenia_establo import valenia_establo
from .valenia_banco import valenia_banco

valenia_submapas = {}
valenia_submapas.update(valenia_castillo)
valenia_submapas.update(valenia_residencias)
valenia_submapas.update(valenia_murallas)
valenia_submapas.update(valenia_hospital)
valenia_submapas.update(valenia_mercado)
valenia_submapas.update(valenia_puerto)
valenia_submapas.update(valenia_gremio)
valenia_submapas.update(valenia_establo)
valenia_submapas.update(valenia_banco)

ENTRADAS_CIUDADES = {
    "entrada_oeste": ("valenia", "entrada_oeste_valenia"),
    "entrada_sur": ("valenia", "entrada_sur_valenia"),
    "puerto": ("valenia", "puerto_valenia")
}
