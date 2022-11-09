from mesa import Agent

class Robot(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cleaned = 0
        self.movements = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def clean_trash(self, other):
        other.state = 1
        self.cleaned += 1
        self.model.num_trash -= 1
        self.movements -= 1

    def step(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        self.movements += 1
        if len(cellmates) > 0:
            for other in cellmates:
                if (isinstance(other, Basura)):
                    if (other.state == 0):
                        self.clean_trash(other)
                    else:
                        self.move()
                else:
                    self.move()
        else:
            self.move()

class Basura(Agent):

    UNCLEAN = 0
    CLEAN = 1

    def __init__(self, unique_id, model, init_state=UNCLEAN):
        super().__init__(unique_id, model)
        self.state = init_state

    def isClean(self):
        if self.state == self.CLEAN:
            return True
        else:
            return False

    def step(self):
        pass
