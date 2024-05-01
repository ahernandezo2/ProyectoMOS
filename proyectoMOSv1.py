from pyomo.environ import *

# Crear una instancia de modelo concreto
modelo = ConcreteModel()

# Conjuntos
modelo.MATERIALES = Set(initialize=['Alcacelcer', 'Oximetazolina'])

# Parámetros
modelo.disponibilidad_maxima = {
    'Alcacelcer': 24,
    'Oximetazolina': 6
}
modelo.ganancia_por_tonelada = {
    'Alcacelcer': 5,
    'Oximetazolina': 4
}

# Variables de decisión
modelo.x = Var(modelo.MATERIALES, domain=NonNegativeReals)

# Función Objetivo
def funcion_objetivo(modelo):
    return sum(modelo.ganancia_por_tonelada[material] * modelo.x[material] for material in modelo.MATERIALES)
modelo.objetivo = Objective(rule=funcion_objetivo, sense=maximize)

# Restricciones
def restriccion_disponibilidad_maxima(modelo, material):
    return sum(modelo.x[material]) <= modelo.disponibilidad_maxima[material]
modelo.restriccion_disponibilidad_maxima = Constraint(modelo.MATERIALES, rule=restriccion_disponibilidad_maxima)


# Resolver el modelo
solver = SolverFactory('glpk')
resultado = solver.solve(modelo)

# Mostrar resultados
print("Cantidad óptima de Alcacelcer producida:", modelo.x['Alcacelcer'].value)
print("Cantidad óptima de Oximetazolina producida:", modelo.x['Oximetazolina'].value)
print("Ganancia máxima obtenida:", modelo.objetivo())
