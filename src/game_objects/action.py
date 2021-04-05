from enum import Enum


class Action:
    action_types = Enum('ACTIONS', 'NOTHING MOVE TELEPORT EAT DIGEST')

    def __init__(self, nature, nb_frames, move_direction=None, endpoint=None):
        self.nature = nature
        self.nb_frames = nb_frames
        self.move_direction = move_direction
        self.endpoint = endpoint
        self.current_frame = 0

    def progress(self):
        self.current_frame += 1
        return self.current_frame == self.nb_frames
