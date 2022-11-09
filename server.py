import mesa
from model import LimpiezaDeHabitacion
from robot_limpieza import *

# Drawing of each agent
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}
    
    if(isinstance(agent, Robot)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        portrayal["text_color"] = "white"
        portrayal["text"] = agent.movements
    
    if(isinstance(agent, Basura)):
        if (agent.state == 1):
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
            portrayal["r"] = 0.2
        else:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 0
            portrayal["r"] = 0.2

    return portrayal

# La cantidad de basura sera 10 veces la de los robots
numero_robots = 10 
ancho = 10
alto = 10
tiempoMaximo = 200

# Instantiate a canvas grid with its width and height in cells, and in pixels
grid = mesa.visualization.CanvasGrid(agent_portrayal, ancho, ancho, 500, 500)

server = mesa.visualization.ModularServer(LimpiezaDeHabitacion,
                       [grid],
                       "LimpiezaDeHabitacion",
                       {"N":numero_robots, "TMax":tiempoMaximo, "width":ancho, "height":alto})
server.port = 8521  # The default
server.launch()
