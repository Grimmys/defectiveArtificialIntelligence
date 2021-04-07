import random
import statistics

from src.configuration import MIN_CELL_SIZE, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, MAX_CELL_SIZE, MAX_ACTION_FRAMES, \
    MIN_ACTION_FRAMES
from src.game_objects.action import Action
from src.game_objects.entity import Entity
from src.gui.tools import generate_random_position, format_size


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
        proportion_left = 100
        for direction in Entity.directions:
            priority = random.randint(5, proportion_left // 2)
            movement_direction_preferences.extend([direction] * priority)
            proportion_left -= priority
        proportion_left //= 4
        for direction in Entity.directions:
            movement_direction_preferences.extend([direction] * proportion_left)

        # Generate action preferences
        action_decision_preferences = [(Action.action_types.NOTHING, random.randint(50, 5000)),
                                       (Action.action_types.MOVE, random.randint(50, 5000)),
                                       (Action.action_types.TELEPORT, random.randint(20, 2000))]
        print("Action decision preferences: ", action_decision_preferences)
        return black_points_proportion, standard_size, theme_color, velocity, movement_direction_preferences, action_decision_preferences

    @staticmethod
    def generate_defectuous_artificial_engine(original_engine, difficulty_level):
        # Generate slightly derivate proportion of black points from the original one
        deviation = 1 + (random.uniform(0.7, 0.8) - 1) / difficulty_level
        deviation = deviation if random.random() < 0.5 else 1 / deviation
        black_points_proportion = original_engine.black_points_proportion * deviation


        # Generate standard size slightly different from the original one
        while True:
            standard_size = format_size(
                (random.randint(original_engine.standard_size[0] - 40, original_engine.standard_size[0] + 40),
                 random.randint(original_engine.standard_size[1] - 40, original_engine.standard_size[1] + 40)),
                MIN_CELL_SIZE,
                MAX_CELL_SIZE)
            size_difference = abs(standard_size[0] - original_engine.standard_size[0]) + abs(standard_size[1] - original_engine.standard_size[1])
            if 40 / difficulty_level < size_difference < 80 / difficulty_level:
                break

        # Mutate standard color until the deviation from the original one is enough
        while True:
            theme_color = []
            total_difference = 0
            for composant in original_engine.theme_color:
                difference = random.randint(5, 60) * (-1 if random.random() < 0.5 else 1)
                defectuous_commposant = composant + difference
                if defectuous_commposant < 0:
                    defectuous_commposant = 0
                if defectuous_commposant > 255:
                    defectuous_commposant = 255
                theme_color.append(defectuous_commposant)
                total_difference += abs(difference)
            if 60 / difficulty_level < total_difference < 120 / difficulty_level:
                print("Total difference :", total_difference)
                break
        print("Old color theme :", original_engine.theme_color)
        print("New color theme :", theme_color)

        # Generate slightly different velocity from the original one
        deviation = random.uniform(0.5, 0.9)
        deviation = deviation if random.random() < 0.5 else 1 / deviation
        velocity = int(original_engine.velocity * deviation)

        # Generate direction preferences slightly differents from the original ones
        movement_direction_preferences = original_engine.direction_preferences
        for direction in Entity.directions:
            movement_direction_preferences.extend([direction] * random.randint(10, 50))

        # Mutate action preferences until the deviation from the original ones is enough
        while True:
            action_decision_preferences = []
            deviations = []
            for action_preference in original_engine.action_preferences:
                deviation = random.uniform(1, 8)
                deviations.append(deviation)
                action_decision_preferences.append((action_preference[0], int(action_preference[1] * deviation)))
            if statistics.stdev(deviations) > 3:
                break
        print("Defectuous decision preferences: ", action_decision_preferences)

        return black_points_proportion, standard_size, theme_color, velocity, movement_direction_preferences, action_decision_preferences

    def __init__(self, level, original_engine=None):
        difficulty_level = 0.8 + level / 5
        self.black_points_proportion, self.standard_size, self.theme_color, self.velocity, self.direction_preferences, self.action_preferences = (
            ArtificialEngine.generate_defectuous_artificial_engine(original_engine, difficulty_level)
            if original_engine else ArtificialEngine.generate_artificial_engine())

    def compute_pattern(self, image):
        image_with_pattern = image.copy()
        for x in range(0, image_with_pattern.get_width()):
            for y in range(0, image_with_pattern.get_height()):
                if image_with_pattern.get_at((x, y)) == (255, 255, 255) and random.random() < self.black_points_proportion:
                    image_with_pattern.set_at((x, y), (0, 0, 0))

        return image_with_pattern

    def compute_size(self):
        size = random.randint(self.standard_size[0] - 10, self.standard_size[0] + 10), \
               random.randint(self.standard_size[1] - 10, self.standard_size[1] + 10)

        return format_size(size, MIN_CELL_SIZE, MAX_CELL_SIZE)

    def compute_color(self):
        generated_color = []
        for original_composant in self.theme_color:
            generated_composant = random.randint(original_composant - 20, original_composant + 20)
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
        total_action_weights = sum(map(lambda act_pref: act_pref[1], self.action_preferences))
        random_pick = random.randint(0, total_action_weights)
        for action_preference in self.action_preferences:
            random_pick -= action_preference[1]
            if random_pick <= 0:
                return action_preference[0]
