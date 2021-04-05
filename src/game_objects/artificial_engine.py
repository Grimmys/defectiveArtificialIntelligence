import random
from enum import Enum

from src.configuration import MIN_CELL_SIZE, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, MAX_CELL_SIZE
from src.game_objects.action import Action
from src.game_objects.entity import Entity
from src.gui.tools import generate_random_position, format_size


class ArtificialEngine:
    @staticmethod
    def generate_artificial_engine():
        standard_size = (random.randint(MIN_CELL_SIZE + 10, MAX_CELL_SIZE - 10), random.randint(MIN_CELL_SIZE + 10, MAX_CELL_SIZE - 10))

        theme_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        movement_direction_preferences = []
        proportion_left = 100
        for direction in Entity.directions:
            priority = random.randint(5, proportion_left // 2)
            print(priority)
            movement_direction_preferences.extend([direction] * priority)
            proportion_left -= priority
        proportion_left //= 4
        for direction in Entity.directions:
            movement_direction_preferences.extend([direction] * proportion_left)
        print(movement_direction_preferences)

        action_decision_preferences = [Action.action_types.NOTHING] * random.randint(50, 5000) + \
                                      [Action.action_types.MOVE] * random.randint(50, 5000) + \
                                      [Action.action_types.TELEPORT] * random.randint(10, 50)
        return standard_size, theme_color, movement_direction_preferences, action_decision_preferences

    @staticmethod
    def generate_defectuous_artificial_engine(original_engine):
        size_insufficiently_different = True
        standard_size = original_engine.standard_size
        while size_insufficiently_different:
            standard_size = format_size((random.randint(original_engine.standard_size[0] - 40, original_engine.standard_size[0] + 40),
                             random.randint(original_engine.standard_size[1] - 40, original_engine.standard_size[1] + 40)),
                            MIN_CELL_SIZE,
                            MAX_CELL_SIZE)
            if abs(standard_size[0] - original_engine.standard_size[0]) + abs(standard_size[1] - original_engine.standard_size[1]) > 30:
                print(standard_size)
                size_insufficiently_different = False
        print("Original size :", original_engine.standard_size)
        print("Defective size :", standard_size)


        theme_color = []
        for composant in original_engine.theme_color:
            defectuous_commposant = composant + random.randint(30, 70) * (-1 if random.random() < 50 else 1)
            if defectuous_commposant < 0:
                defectuous_commposant = 0
            if defectuous_commposant > 255:
                defectuous_commposant = 255
            theme_color.append(defectuous_commposant)
        print("Original theme : ", original_engine.theme_color)
        print("Defective theme : ", theme_color)

        movement_direction_preferences = original_engine.direction_preferences
        for direction in Entity.directions:
            movement_direction_preferences.extend([direction] * random.randint(10, 50))

        action_decision_preferences = original_engine.action_preferences
        action_decision_preferences.extend([Action.action_types.NOTHING] * random.randint(10, 1000) + \
                                           [Action.action_types.MOVE] * random.randint(10, 1000) + \
                                           [Action.action_types.TELEPORT] * random.randint(1, 50))
        return standard_size, theme_color, movement_direction_preferences, action_decision_preferences

    def __init__(self, original_engine=None):
        self.standard_size, self.theme_color, self.direction_preferences, self.action_preferences = \
            ArtificialEngine.generate_defectuous_artificial_engine(original_engine) \
                if original_engine else ArtificialEngine.generate_artificial_engine()

    def compute_size(self):
        size = random.randint(self.standard_size[0] - 10, self.standard_size[0] + 10), \
               random.randint(self.standard_size[1] - 10, self.standard_size[1] + 10)

        return format_size(size, MIN_CELL_SIZE, MAX_CELL_SIZE)

    def compute_color(self):
        generated_color = []
        for original_composant in self.theme_color:
            generated_composant = random.randint(original_composant - 30, original_composant + 30)
            if generated_composant < 0:
                generated_composant = 0
            if generated_composant > 255:
                generated_composant = 255
            generated_color.append(generated_composant)
        return generated_color

    def compute_movement_direction(self):
        # For now, direction_priority is following the format " [DIRECTION, DIRECTION, DIRECTION, OTHER_DIRECTION] "
        return random.choice(self.direction_preferences)

    def compute_teleport_endpoint(self, entity_rect):
        endpoint = generate_random_position((MAIN_WINDOW_WIDTH - entity_rect.width,
                                             MAIN_WINDOW_HEIGHT - entity_rect.height))
        return endpoint

    def compute_action_decision(self):
        return random.choice(self.action_preferences)

