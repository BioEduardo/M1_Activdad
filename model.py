#----------------------------------------------------------
# M1. Actividad
# Este programa representa al modela de limpieza de habitacion
# 
# Date: 11-Nov-2022
# Authors:
#           Eduardo Joel Cortez Valente A01746664
#           Paulo Ogando Gulias A01751587
#----------------------------------------------------------

from mesa import Model, DataCollector
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from robot_limpieza import Robot, Basura

class LimpiezaDeHabitacion(Model):

    # Inicializa el modelo. Agrega los agentes
    def __init__(self, tiempoMaximo, N, width, height, porcentaje):
        self.largo = width
        self.ancho = height
        self.max_time = tiempoMaximo - 2 
        self.num_robots = N
        self.num_trash = round(width * height * porcentaje)
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.cont_time = 0

        for i in range(self.num_trash):
            if i <= self.num_robots:
                robot = Robot(i, self)
                self.schedule.add(robot)
                self.grid.place_agent(robot, (1, 1))
            
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            basura = Basura(i+self.num_trash, self)            
            self.schedule.add(basura)
            self.grid.place_agent(basura, (x, y))

    # Checa si se ha alcanzado el limite de tiempo establecido
    def check_steps(self):
        if self.cont_time == self.max_time:
            print("Tiempo limite alcanzado")
            totalCeldas = self.largo * self.ancho
            celdasLimpias = (self.largo * self.ancho) - self.num_trash
            porcentajeCeldasLimpias = 100 * celdasLimpias / totalCeldas
            print(f"El porcentaje de celdas limpias es de {porcentajeCeldasLimpias}%s")
            # Imprimir la cantidad de basura que falta por limpiar
            self.running = False
        else:
            self.cont_time += 1
    
    # Checa si toda la basura ha sido limpiada
    def check_cleaned(self):
        if self.num_trash == 0:
            print(f"Toda la basura ha sido limpiada en un tiempo de {self.cont_time}")
            self.running = False

    # Representa un paso del modelo
    def step(self):
        self.check_steps()
        self.check_cleaned()
        self.schedule.step()
