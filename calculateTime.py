import math
from calculateAngle import calculateAngle

# Calculate time by determining the angles of the lines
# clockHands[0] - hour hand
# clockHands[1] - minute hand
# clockHands[2] - second hand (optional)
def calculateTime(clockHands):
    print()
    print()
    print('clockHands: ', clockHands)
    hasSeconds = len(clockHands) > 2

    hourAngle = calculateAngle(clockHands[0][0], clockHands[0][1], clockHands[0][2], clockHands[0][3])
    minuteAngle = calculateAngle(clockHands[1][0], clockHands[1][1], clockHands[1][2], clockHands[1][3])
    secondAngle = calculateAngle(clockHands[2][0], clockHands[2][1], clockHands[2][2], clockHands[2][3]) if hasSeconds else None

    #FOR DEBUGGING PURPOSES ONLY, DELETE LATER
    print("Hour angle: ", hourAngle)
    print("Minute angle: ", minuteAngle)
    print("Second angle: ", secondAngle)


    #Calculate the time from the clock hand angles, by first checking which quadrant each
    #clock hand is in, then calculating the time the hands are pointing to, accordingly
    #Hour Calculation
    if (((clockHands[0][3]-clockHands[0][1])<=0) and ((clockHands[0][2]-clockHands[0][0])>=0)):
        print("case 1")
        hoursCalculated = ((hourAngle//30)+3)%12
    elif (((clockHands[0][3]-clockHands[0][1])>=0) and ((clockHands[0][2]-clockHands[0][0])>=0)):
        print("case 2")
        hoursCalculated = ((hourAngle//30)-3)%12
    #Minute calculation
    if (((clockHands[1][3]-clockHands[1][1])<=0) and ((clockHands[1][2]-clockHands[1][0])>=0)):
        print("case 12")
        minutesCalculated = (math.floor(((minuteAngle/30)*5)+15))%60
    elif (((clockHands[1][3]-clockHands[1][1])>=0) and ((clockHands[1][2]-clockHands[1][0])>=0)):
        print("case 22")
        minutesCalculated = (math.floor(((minuteAngle/30)*5)-15))%60
    #Second calculation
    if (((clockHands[2][3]-clockHands[2][1])<=0) and ((clockHands[2][2]-clockHands[2][0])>=0)):
        print("case 13")
        secondsCalculated = (math.ceil(((secondAngle/30)*5)+15))%60 if hasSeconds else None
    elif (((clockHands[2][3]-clockHands[2][1])>=0) and ((clockHands[2][2]-clockHands[2][0])>=0)):
        print("case 23")
        secondsCalculated = (math.ceil(((secondAngle/30)*5)-15))%60 if hasSeconds else None

    #BACK-UP CODE, MIGHT BE DELETED LATER IF NOT NEEDED
    #    elif (((clockHands[0][3]-clockHands[0][1])>=0) and ((clockHands[0][2]-clockHands[0][0])<=0)):
    #        print ("case 3")
    #    elif (((clockHands[0][3]-clockHands[0][1])<=0) and ((clockHands[0][2]-clockHands[0][0])<=0)):
    #        print ("case 4")

    #FOR DEBUGGING PURPOSES ONLY
    print("Hours: ", hoursCalculated)
    print("Minutes: ", minutesCalculated,((minuteAngle/30))*5)
    if (hasSeconds): print("Seconds: ", secondsCalculated,((secondAngle/30))*5)
    else: print("Seconds: NA")

    timeTotal = str(hoursCalculated),":",str(minutesCalculated),":",str(secondsCalculated) if hasSeconds else str(hoursCalculated),":",str(minutesCalculated)
    return timeTotal