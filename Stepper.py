from machine import Pin
import time

class Stepper:
    def __init__(self, steps_per_rev=200, pins=None, step_pin=None, dir_pin=None):
        self.steps_per_rev = steps_per_rev
        self.last_step_time = 0
        self.mode = None
        if pins is not None:
            self.mode = "direct"
            self.pins = [Pin(p, Pin.OUT) for p in pins]
            self.seq = [
                [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1]
            ]
        elif step_pin is not None and dir_pin is not None:
            self.mode = "driver"
            self.step_pin = Pin(step_pin, Pin.OUT)
            self.dir_pin = Pin(dir_pin, Pin.OUT)
        
        else:
            raise ValueError("pins=[...] or step_pin, dir_pin")
        
    def setSpeed(self, rpm):
        self.step_delay = int((60_000_000 / self.steps_per_rev) / rpm)

    def step(self, steps_to_move):
        direction = 1 if steps_to_move > 0 else -1
        steps_left = abs(steps_to_move)
        if not hasattr(self, "_seq_pos"):
            self._seq_pos = 0
        if self.mode == "direct":
            while steps_left > 0:
                now = time.ticks_us()
                if time.ticks_diff(now, self.last_step_time) >= self.step_delay:
                    self.last_step_time = now
                    for i in range(4):
                        self.pins[i].value(self.seq[self._seq_pos][i])
                    self._seq_pos = (self._seq_pos + direction) % len(self.seq)
                    steps_left -= 1
                else:
                    time.sleep_us(50)
        elif self.mode == "driver":
            self.dir_pin.value(1 if direction > 0 else 0)
            while steps_left > 0:
                now = time.ticks_us()
                if time.ticks_diff(now, self.last_step_time) >= self.step_delay:
                    self.last_step_time = now
                    self.step_pin.value(1)
                    time.sleep_us(5)
                    self.step_pin.value(0)
                    steps_left -= 1
                else:
                    time.sleep_us(50)        
    def moveDegrees(self, deg):
        steps = int((deg / 360.0) * self.steps_per_rev)
        self.step(steps)
    def moveRounds(self, n):
        steps = int(n * self.steps_per_rev)
        self.step(steps)
    def disable(self):
        for pin in self.pins:
            pin.value(0)