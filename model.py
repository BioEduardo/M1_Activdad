from mesa import Model, DataCollector
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

from robot_limpieza import Robot, Basura


class LimpiezaDeHabitacion(Model):

    def __init__(self, TMax, N, width, height, porcentaje):
        self.largo = width
        self.ancho = height
        # Tiempo maximo de ejecucion
        self.max_time = TMax - 2 # El -2 es para ajustar el detenimiento del programa
        # Numero de robots
        self.num_robots = N
        # Cantidad de celdas con basura
        self.num_trash = round(width * height * porcentaje)
        # Agregar una cuadricula donde nuestro modelo ha de correr
        self.grid = MultiGrid(width, height, True)
        # Activates all the agents once per step, simultaneamente
        self.schedule = SimultaneousActivation(self)
        # Enables conditional shut off of the model once a condition is met
        self.running = True
        # Contador de tiempo (aumenta con los steps)
        self.cont_time = 0

        # Create agentes
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
    
    def check_cleaned(self):
        if self.num_trash == 0:
            print(f"Toda la basura ha sido limpiada en un tiempo de {self.cont_time}")
            self.running = False

    def step(self):
        self.check_steps()
        self.check_cleaned()
        self.schedule.step()
