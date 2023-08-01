import cvzone
import cv2
import numpy as np
import time


class PID:
    def __init__(self, pidVals, targetVal, axis=0, limit=None):
        self.pidVals = pidVals
        self.targetVal = targetVal
        self.axis = axis
        self.pError = 0
        self.limit = limit
        self.I = 0
        self.pTime = 0

    def update(self, cVal):
        # Current Value - Target Value
        t = time.time() - self.pTime
        error = cVal - self.targetVal
        P = self.pidVals[0] * error
        self.I = self.I + (self.pidVals[1] * error * t)
        D = (self.pidVals[2] * (error - self.pError)) / t

        result = P + self.I + D

        if self.limit is not None:
            result = float(np.clip(result, self.limit[0], self.limit[1]))
        self.pError = error
        self.ptime = time.time()

        return result



def main():
    # For a 640x480 image center target is 320 and 240
    xPID = PID([1, 0.000000000001, 1], 640 // 2)
    yPID = PID([1, 0.000000000001, 1], 480 // 2, axis=1, limit=[-100, 100])

    while True:

        xVal = int(xPID.update(cx))
        yVal = int(yPID.update(cy))



if __name__ == "__main__":
    main()
