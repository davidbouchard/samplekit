# Creates a set of drum samples for the Erica Sample Drum (or other sampler
# with cv controllable sample index) to be used with Ornament and Crime's
# Hemisphere Binary counter.
# inputs to the binary counter are triggers from a sequencer
# output is the correct pre-mix of samples to select

# eg with 4 input files:

# 01.wav 	0 0 0 1 = A
# 02.wav    0 0 1 0 = B
# 03.wav	0 0 1 1 = A + B
# 04.wav 	0 1 0 0 = C
# 05.wav	0 1 0 1 = C + A
# 06.wav 	0 1 1 0 = C + B
# 07.wav	0 1 1 1 = C + A + B
# 08.wav	1 0 0 0 = D
# 09.wav	1 0 0 1 = D
# 10.wav	1 0 1 0 = D + B
# 11.wav	1 0 1 1 = D + A + B
# 12.wav	1 1 0 0 = D + C
# 13.wav	1 1 0 1 = D + C + A
# 14.wav 	0 1 1 0 = D + C + B
# 15.wav	1 1 1 1 = D + C + A + B

import os
import sys

#default values for testing
sounds = ['A.wav', 'B.wav', 'C.wav', 'D.wav']

if __name__ == "__main__":

    if (len(sys.argv) <= 1):
        print("Usage: python3 genKit.py <soundfiles>")
        exit()

    # create the output folder
    os.makedirs("kit",exist_ok=True)

    sounds = sys.argv[1:]

    numSounds = len(sounds)

    for i in range(1, pow(2, numSounds)):
        output = ""
        count = 0
        binNum = bin(i)
        for j in range(0, numSounds):
            if i & 1 << j:
                count += 1
                output += sounds[j] + " "
        cmd = "sox -V1 "

        # preserve volume of individual hits when mixed
        # there is a slight risk of clipping here if the source samples are
        # too hot
        if (count > 1): cmd += "--combine mix-power "

        cmd += output

        # 16bit 48khz mono wav files
        cmd += "-c 1 -b 16 -r 48k kit/%02d.wav" % i

        print(cmd)
        os.system(cmd)
