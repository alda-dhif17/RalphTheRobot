#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor, TouchSensor, GyroSensor
from pybricks.parameters import Port, Direction, SoundFile, Stop, Color, ImageFile
from pybricks.robotics import DriveBase
from pybricks.tools import wait, print

import threading

class Status():
    WAIT = 0
    SEARCHING = 1
    CARRYING_LUGGAGE = 2
    PICKING_UP = 3
    DEPOSITING = 4
    COMPUTING = 5

brick_state = Status.SEARCHING
blocks_delivered = 0

def gameLoop(blocks_to_deliver):
    global brick_state


    leftMotor = Motor(Port.B)
    rightMotor = Motor(Port.C)
    wheels = DriveBase(Motor(Port.B), Motor(Port.C), 56, 114)
    uSensor = UltrasonicSensor(Port.S4)
    cSensor = ColorSensor(Port.S3)
    gSensor = GyroSensor(Port.S2)

    ts = TouchSensor(Port.S1)
    while not ts.pressed():
        # brick.sound.file(SoundFile.MOTOR_IDLE, 1000)

        if blocks_delivered >= blocks_to_deliver:
            brick_state = Status.WAIT
        
        if brick_state == Status.WAIT:
            return
        elif brick_state == Status.SEARCHING:
            print('STATE: SEARCHING')
            t = threading.Thread(target=searchLuggage, args=(wheels, cSensor, gSensor))
            t.start()
            brick_state = Status.COMPUTING
        elif brick_state == Status.CARRYING_LUGGAGE:
            print('STATE: CARRYING_LUGGAGE')
            t = threading.Thread(target=deliverLuggage, args=(wheels, cSensor, ))
            t.start()
            brick_state = Status.COMPUTING
        elif brick_state == Status.PICKING_UP:
            print('STATE: PICKING_UP')
            t = threading.Thread(target=doLuggage, args=(wheels, cSensor, True, ))
            t.start()
            brick_state = Status.COMPUTING
        elif brick_state == Status.DEPOSITING:
            print('STATE: DEPOSITING')
            t = threading.Thread(target=doLuggage, args=(wheels, cSensor,False, ))
            t.start()
            brick_state = Status.COMPUTING

def searchLuggage(wheels, cSensor, gSensor):
    global brick_state

    # while not slightly red ... 
    while cSensor.color() != Color.RED:
        print('Searching:', cSensor.rgb())

        if not (cSensor.color() in [Color.BLUE, Color.WHITE]) and (cSensor.color() != Color.RED):
            wheels.drive_time(50, 45, 1000)
        else:
            wheels.drive(-160, 0)

    wheels.stop(Stop.BRAKE)

    You_spin_me_right_round_baby_Right_round_like_a_record_baby_Right_round_round_round(wheels, 190)
    wheels.drive_time(65, 0, 1000)
    brick_state = Status.PICKING_UP

def You_spin_me_right_round_baby_Right_round_like_a_record_baby_Right_round_round_round(wheels, angle):
    wheels.drive_time(0, angle, 1000)

def doLuggage(wheels, cSensor, pickup=True):
    global brick_state, blocks_delivered
    
    if pickup:
        stapler = Motor(Port.A, Direction.CLOCKWISE)
        stapler.run_until_stalled(20, Stop.BRAKE)
        brick.sound.file(SoundFile.HORN_1,1000)
        brick_state = Status.CARRYING_LUGGAGE
    else:
        stapler = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        
        You_spin_me_right_round_baby_Right_round_like_a_record_baby_Right_round_round_round(wheels, 180)

        stapler.run_angle(50, 100, Stop.BRAKE)
        wheels.drive_time(-50, 0, 1000)
        stapler.run_angle(50, 25, Stop.BRAKE)
        
        wheels.drive_time(-113/3, 45/3, 1000*3)
        wheels.drive_time(0,45/3,1000*3)

        blocks_delivered += 1
        brick_state = Status.SEARCHING

def deliverLuggage(wheels, cSensor):
    global brick_state
    
    # while not slightly green
    while cSensor.color() != Color.GREEN:
        print('Deliver:', cSensor.rgb())

        if cSensor.color() != Color.BLUE:
            wheels.drive_time(50, 45, 1000)
        else:
            wheels.drive(-160, 0)
    wheels.stop(Stop.BRAKE)

    brick_state = Status.DEPOSITING

def main():
    # Play a sound (1000Hz, 1000ms)
    brick.sound.file(SoundFile.SNORING, 1000)
    brick.sound.file(SoundFile.ERROR_ALARM, 1000)
    brick.display.image(ImageFile.UP)
    brick.sound.file(SoundFile.HELLO, 1000)

    # countodwn 
    brick.sound.file(SoundFile.THREE, 1000)
    brick.sound.file(SoundFile.TWO, 1000)
    brick.sound.file(SoundFile.ONE, 1000)

    brick.sound.file(SoundFile.MOTOR_START, 1000)

    brick.light(Color.RED)

    gameLoop(2)

    # END
    brick.sound.file(SoundFile.MOTOR_STOP, 1000)

    # brick.sound.file(SoundFile.SNEEZING, 1000)
    # brick.sound.file(SoundFile.SMACK, 1000)
    # brick.sound.file(SoundFile.OUCH, 1000)
    # brick.sound.file(SoundFile.CRYING, 1000)
    
    brick.sound.file(SoundFile.GAME_OVER, 1000)
    
if __name__ == '__main__':
    main()