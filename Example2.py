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