import gamecode as gamecode


class Animation:
    def __init__(self, frame_duration, keyframes):
        self.frame_duration = frame_duration
        self.keyframes = keyframes
        self.framelen = len(self.keyframes)

    def get_keyframe(self, statetime, mode):
        frame_number = int(statetime / self.frame_duration)
        # print(self.framelen-1, frame_number)
        # frame_number = self.framelen - 1 if self.framelen-1 < frame_number else frame_number

        if mode == gamecode.STATE_MOVING:
            frame_number = frame_number % len(self.keyframes)
            return self.keyframes[frame_number]
        return self.keyframes[0]

