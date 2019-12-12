while(1):
    frequency = float(input("enter Number: "))
    MCs = ((1/frequency)/2)/0.0000000625
    print("1024: " + str(MCs/1024))
    print("256: " + str(MCs/256))
    print("64: " + str(MCs/64))
