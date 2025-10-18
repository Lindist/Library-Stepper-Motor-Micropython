# Library-Stepper-Motor-Micropython

```python
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
```

## Download Library
<a href="/Stepper.py'" download > Download Stepper.py</a>

## Expain Code

```python
# import Python Libraries
from machine import Pin # Add Pin from machine for control Board Pin
import time # Add time for delay algorithm program
```

Class
: in class Stepper

```python
'''
Add parameter in constructure
1. steps_per_rev is number cycle of motor's rotation.
2. pins is controller pin for 4 pin driver.
3. step_pin is step pin for driver movement control.
4. dir_pin is direction pin for driver direction control.

** 2 order use to 4 pin driver such as ULN2003, L298N.
** 3,4 order use to 3 pin driver(en,pul,dir) such as A4988, DRV8825, TB6600.
'''
    def __init__(self, steps_per_rev=200, pins=None, step_pin=None, dir_pin=None):
        self.steps_per_rev = steps_per_rev # bring steps_per_rev parameter value assign in self.steps_per_rev
        self.last_step_time = 0 # Add lasttime
        self.mode = None # Add mode be 4 pin driver(direct) or 3 pin driver(driver) 
        if pins is not None: # check if there is pins, is not it?
            self.mode = "direct" # assign mode is direct
            self.pins = [Pin(p, Pin.OUT) for p in pins] # assign pins is all output
            self.seq = [
                [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1]
            ] # specรfy is half sequence
        elif step_pin is not None and dir_pin is not None: # check if  there are step_pin and dir_pin ,are not they?
            self.mode = "driver" # assign mode is driver
            self.step_pin = Pin(step_pin, Pin.OUT) # assign step_pin is output
            self.dir_pin = Pin(dir_pin, Pin.OUT) # assign dir_pin is output
        
        else:
            raise ValueError("pins=[...] or step_pin, dir_pin") # error exception
```

```python
    def setSpeed(self, rpm): # set parameter speed rpm(round per minute)
        self.step_delay = int((60_000_000 / self.steps_per_rev) / rpm) # set speed motor
```

```python
    def step(self, steps_to_move): # Add pulse per step perameter
        direction = 1 if steps_to_move > 0 else -1 # add diff directon if steps_to_move more than zero
        steps_left = abs(steps_to_move) # only pulse positive value
        if not hasattr(self, "_seq_pos"): # check if there is _seq_pos variable, is not it?
            self._seq_pos = 0 # add _seq_pos
        if self.mode == "direct": # check mode is direct
            while steps_left > 0: # if step > 0
                now = time.ticks_us() # timer us
                if time.ticks_diff(now, self.last_step_time) >= self.step_delay: # check time passed if time more than speed
                    self.last_step_time = now # reset time
                    for i in range(4): # loop 
                        self.pins[i].value(self.seq[self._seq_pos][i]) # set pin
                    self._seq_pos = (self._seq_pos + direction) % len(self.seq) # current element passed
                    steps_left -= 1 # minus step down 1
                else:
                    time.sleep_us(50) #delay
        elif self.mode == "driver": # check mode is driver
            self.dir_pin.value(1 if direction > 0 else 0) # add diff directon if steps_to_move more than 
            while steps_left > 0:# if step > 0
                now = time.ticks_us() # timer us
                if time.ticks_diff(now, self.last_step_time) >= self.step_delay: # check time passed if time more than speed
                    self.last_step_time = now # reset time
                    self.step_pin.value(1) # set high pin
                    time.sleep_us(5) # delay
                    self.step_pin.value(0) # set low pin
                    steps_left -= 1 # minus step down 1
                else:
                    time.sleep_us(50) #delay
```

```python
    def moveDegrees(self, deg): # degree parameter
        steps = int((deg / 360.0) * self.steps_per_rev) # convert deg to pul
        self.step(steps) # callback funtion step
```

```python
    def moveRounds(self, n): # round parameter
        steps = int(n * self.steps_per_rev) # round step
        self.step(steps) # callback funtion step
```

```python
    def disable(self):
        for pin in self.pins:
            pin.value(0) # low pin for disable pin
```

## Example used to extra case

```python
from Stepper import Stepper # import Class Stepper
from machine import Pin # import Pin
import time # import time

accumulated_remainder = 0.0 # Add accumulated_remainder variable
PULSES_PER_REV = 1600 # Add PULSES_PER_REV variable
SLOTS = 29 # Add SLOTS variable
STEP_PER_SLOT = PULSES_PER_REV / SLOTS # Add STEP_PER_SLOT variable
motor = Stepper(steps_per_rev=200, pins=[5,6,9,11]) # Add instance motor for 4 pin
motor.setSpeed(30)   # 30 RPM
i = 1
def rotate_slotSD(remainder=0.0): # this function used to coincidental rotation in each slot
    steps_needed = STEP_PER_SLOT + remainder # find step need by STEP_PER_SLOT + remainder
    full_steps = int(steps_needed) # Decimal truncation
    motor.step(full_steps) # motor movement control as step need
    new_remainder = steps_needed - full_steps # minus with step need for decimal need return back

    return new_remainder # return new_remainder
time.sleep_ms(1500) # delay millisecon

while True: # loop always true
    accumulated_remainder = rotate_slotSD(accumulated_remainder) # call function rotate_slotSD and assign to accumulated_remainder
    motor.step(int(STEP_PER_SLOT)) # motor movement control as step need
    motor.step(2000) # motor movement control as step need
    time.sleep_ms(2000) # delay millisecon
    motor.moveRounds(-42) # move rounds need
    motor.moveDegrees(90)   # 90° rotation forward
    motor.moveDegrees(-180) # 180° rotation backward
    time.sleep_ms(1000) # delay millisecon
    motor.moveRounds(-38) # move rounds need
    time.sleep_ms(1000) # delay millisecon
    print(f"rev: {i}") # display revolution
    i+=1 # plus 1 revolution
    motor.disable()# disable all motor pins
```

```python
from Stepper import Stepper # import Class Stepper
from machine import Pin # import Pin
import time # import time

accumulated_remainder = 0.0 # Add accumulated_remainder variable
PULSES_PER_REV = 1600 # Add PULSES_PER_REV variable
SLOTS = 29 # Add SLOTS variable
STEP_PER_SLOT = PULSES_PER_REV / SLOTS # Add STEP_PER_SLOT variable
ena_pin = Pin(22,Pin.OUT) # enable 22 pin
ena_pin.value(1)  # disable motor(lock)
motor = Stepper(steps_per_rev=PULSES_PER_REV, step_pin=17, dir_pin=21) # Add instance motor for 3 pin
motor.setSpeed(11)   # 30 RPM
i = 1
def rotate_slotSD(remainder=0.0): # this function used to coincidental rotation in each slot
    steps_needed = STEP_PER_SLOT + remainder # find step need by STEP_PER_SLOT + remainder
    full_steps = int(steps_needed) # Decimal truncation
    motor.step(full_steps) # motor movement control as step need
    new_remainder = steps_needed - full_steps # minus with step need for decimal need return back

    return new_remainder # return new_remainder
time.sleep_ms(1500) # delay millisecon
ena_pin.value(0) # enable motor(unlock)
while True: # loop always true
    accumulated_remainder = rotate_slotSD(accumulated_remainder) # call function rotate_slotSD and assign to accumulated_remainder
    motor.step(int(STEP_PER_SLOT)) # motor movement control as step need
    motor.step(2000) # motor movement control as step need
    time.sleep_ms(2000) # delay millisecon
    motor.moveRounds(-42) # move rounds need
    motor.moveDegrees(90)   # 90° rotation forward
    motor.moveDegrees(-180) # 180° rotation backward
    time.sleep_ms(1000) # delay millisecon
    motor.moveRounds(-38) # move rounds need
    time.sleep_ms(1000) # delay millisecon
    print(f"rev: {i}") # display revolution
    i+=1 # plus 1 revolution
```

## Download Example

<a href="/Example1.py'" download > Download Example1.py</a><br>
<a href="/Example2.py" download > Download Example2.py</a>

