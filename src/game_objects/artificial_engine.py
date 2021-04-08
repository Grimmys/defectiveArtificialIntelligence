import random
import statistics

from src.configuration import MIN_CELL_SIZE, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, MAX_CELL_SIZE, MAX_ACTION_FRAMES, \
    MIN_ACTION_FRAMES
from src.game_objects.action import Action
from src.game_objects.entity import Entity
from src.gui.tools import generate_random_position, format_size


def mutate_preferences(preferences):
    """This method takes a list of elements having each a specific weight (priority)
       and randomly changes these weights"""
    mutated_preferences = []
    deviations = []
    for preference in preferences:
        deviation = random.uniform(1, 8)
        deviations.append(deviation)
        mutated_preferences.append((preference[0], int(preference[1] * deviation)))
    if statistics.stdev(deviations) > 3:
        return mutated_preferences
    else:
        return mutate_preferences(preferences)


def pick_random_preference(preferences):
    total_weights = sum(map(lambda pref: pref[1], preferences))
    random_pick = random.randint(0, total_weights)
    for preference in preferences:
        random_pick -= preference[1]
        if random_pick <= 0:
            return preference[0]


class ArtificialEngine:

    @staticmethod
    def generate_artificial_engine():
        # Generate proportion of black points on the surface of the cell
        black_points_proportion = random.uniform(0.1, 0.4)

        # Generate median size
        standard_size = (
            random.randint(MIN_CELL_SIZE + 10, MAX_CELL_SIZE - 10),
            random.randint(MIN_CELL_SIZE + 10, MAX_CELL_SIZE - 10))

        # Generate median color
        theme_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Generate reactivity of the cell (i.e. determines if the execution of an action will be slow or fast)
        velocity = random.randint(MIN_ACTION_FRAMES, MAX_ACTION_FRAMES)

        # Generate movement direction preferences
        movement_direction_preferences = []
        for direction in Entity.directions:
            movement_direction_preferences.append((direction, random.randint(10, 100)))

        # Generate action preferences
        action_decision_preferences = [(Action.action_types.NOTHING, random.randint(50, 5000)),
                                       (Action.action_types.MOVE, random.randint(50, 5000)),
                                       (Action.action_types.TELEPORT, random.randint(20, 2000))]
        return black_points_proportion, standard_size, theme_color, velocity, movement_direction_preferences, action_decision_preferences

    @staticmethod
    def generate_defectuous_artificial_engine(original_engine, difficulty_level):
        # Generate slightly derivate proportion of black points from the original one
        deviation = 1 + (random.uniform(0.7, 0.8) - 1) / difficulty_level
        # Deviation coefficient could be decrease or increase
        deviation = deviation if random.random() < 0.5 else 1 / deviation
        black_points_proportion = original_engine.black_points_proportion * deviation

        # Generate standard size slightly different from the original one
        while True:
            standard_size = format_size(
                (random.randint(original_engine.standard_size[0] - 40, original_engine.standard_size[0] + 40),
                 random.randint(original_engine.standard_size[1] - 40, original_engine.standard_size[1] + 40)),
                MIN_CELL_SIZE,
                MAX_CELL_SIZE)
            size_difference = abs(standard_size[0] - original_engine.standard_size[0]) + abs(
                standard_size[1] - original_engine.standard_size[1])
            if 40 / difficulty_level < size_difference < 80 / difficulty_level:
                break

        # Mutate standard color until the deviation from the original one is enough
        while True:
            theme_color = []
            total_difference = 0
            for component in original_engine.theme_color:
                difference = random.randint(5, 60) * (-1 if random.random() < 0.5 else 1)
                defective_component = component + difference
                if defective_component < 0:
                    defective_component = 0
                if defective_component > 255:
                    defective_component = 255
                theme_color.append(defective_component)
                total_difference += abs(difference)
            if 60 / difficulty_level < total_difference < 120 / difficulty_level:
                break

        # Generate slightly different velocity from the original one
        deviation = random.uniform(0.5, 0.9)
        # Deviation coefficient could be decrease or increase
        deviation = deviation if random.random() < 0.5 else 1 / deviation
        velocity = int(original_engine.velocity * deviation)

        # Generate direction preferences slightly differents from the original ones
        movement_direction_preferences = mutate_preferences(original_engine.direction_preferences)

        # Mutate action preferences until the deviation from the original ones is enough
        action_decision_preferences = mutate_preferences(original_engine.action_preferences)

        return black_points_proportion, standard_size, theme_color, velocity, movement_direction_preferences, action_decision_preferences

    def __init__(self, level, original_engine=None):
        difficulty_level = 0.8 + level / 5
        self.black_points_proportion, self.standard_size, self.theme_color, \
        self.velocity, self.direction_preferences, self.action_preferences = (
            ArtificialEngine.generate_defectuous_artificial_engine(original_engine, difficulty_level)
            if original_engine else ArtificialEngine.generate_artificial_engine())

    def compute_pattern(self, image):
        image_with_pattern = image.copy()
        for x in range(0, image_with_pattern.get_width()):
            for y in range(0, image_with_pattern.get_height()):
                if image_with_pattern.get_at((x, y)) == (
                        255, 255, 255) and random.random() < self.black_points_proportion:
                    image_with_pattern.set_at((x, y), (0, 0, 0))

        return image_with_pattern

    def compute_size(self):
        size = random.randint(self.standard_size[0] - 10, self.standard_size[0] + 10), \
               random.randint(self.standard_size[1] - 10, self.standard_size[1] + 10)

        return format_size(size, MIN_CELL_SIZE, MAX_CELL_SIZE)

    def compute_color(self):
        generated_color = []
        for original_component in self.theme_color:
            generated_component = random.randint(original_component - 20, original_component + 20)
            if generated_component < 0:
                generated_component = 0
            if generated_component > 255:
                generated_component = 255
            generated_color.append(generated_component)
        return generated_color

    def compute_movement_direction(self):
        return pick_random_preference(self.direction_preferences)

    def compute_teleport_endpoint(self, entity_rect):
        endpoint = generate_random_position((MAIN_WINDOW_WIDTH - entity_rect.width,
                                             MAIN_WINDOW_HEIGHT - entity_rect.height))
        return endpoint

    def compute_action_decision(self):
        return pick_random_preference(self.action_preferences)
