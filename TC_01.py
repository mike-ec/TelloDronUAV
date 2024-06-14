import numpy as np
from djitellopy import Tello
import time


# Función para generar la curva parametrizada del arco
def arc(R, points):
    theta_arc = np.linspace(-np.pi/2,  np.pi/2, points)
    x_arc = R * np.sin(theta_arc)
    y_arc = np.zeros_like(theta_arc)
    z_arc = R * np.cos(theta_arc)
    x_arc += R  # Desplazar la curva para que el primer punto sea (0, 0, 0)
    return list(zip(x_arc, y_arc, z_arc))


# Parámetros del arco y la recta
R = 100
P = 10
S = 10

curva = arc(R, P)

# Posición inicial
xi, yi, zi = 0, 0, 0
altura_arco = []
altura_recta = []
x_values = []

# Inicializar el dron Tello
drone = Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")

drone.takeoff()
time.sleep(1)
print('Altura takeoff: {}'.format(drone.get_height()))

for i, (x, y, z) in enumerate(curva[1::]):

    dx = round(x - xi)
    dy = round(y - yi)
    dz = round(z - zi)

    # Actualizar la posición actual
    xi, yi, zi = x, y, z
    x_values += [dx]

    # Mover el dron a la nueva posición relativa
    drone.go_xyz_speed(dx, dy, dz, S)
    time.sleep(1)
    altura_arco += [drone.get_height()]

# Recta
drone.go_xyz_speed(0, R, 0, S)
#time.sleep(1)
altura_recta += [drone.get_height()]

# Arco
xi, yi, zi = 0, 0, 0

for i, (x, y, z) in enumerate(curva[1::]):
    dx = round(x - xi)
    dy = round(y - yi)
    dz = round(z - zi)

    # Actualizar la posición actual
    xi, yi, zi = x, y, z
    x_values += [dx]

    # Mover el dron a la nueva posición relativa

    drone.go_xyz_speed(-dx, dy, dz, S)
    time.sleep(1)
    altura_arco += [drone.get_height()]

# Recta
drone.go_xyz_speed(0, -R, 0, S)
#time.sleep(1)
altura_recta += [drone.get_height()]

# Aterrizar el dron
drone.land()

print('Altura arcos: ', altura_arco)
print('Altura rectas: ', altura_recta)
print('Valores en x: ', x_values)

# Area de las rectas (Rectangulos)
area_rec = 0

for i in altura_recta:

    area_rec += R * i

print(f'Area rectas : {area_rec}')

area_arc = 0

# Area de los arcos
for i, v in enumerate(altura_arco):

    area_arc += x_values[i] * v

print(f'Area arcos : {area_arc}')