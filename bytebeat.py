import sys
import argparse
import struct
import pyaudio


class ByteBeat:
    FORMAT = pyaudio.paUInt8
    RATE = 8000
    CHANNELS = 1

    def __init__(self, formula, duration):
        self.formula = formula
        self.duration = int(duration)

    def __buffer(self):
        sample_count = self.duration * ByteBeat.RATE // 2
        data = [int(eval(self.formula)) % 256 for t in range(sample_count)]
        return struct.pack("h" * len(data), *data)

    def play(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=ByteBeat.FORMAT,
            channels=ByteBeat.CHANNELS,
            rate=ByteBeat.RATE,
            output=True
        )
        stream.write(self.__buffer())
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("formula", type=str, help="set bytebeat code")
    parser.add_argument("-t", "--time", type=int, help="set playing time[sec]", default=30)
    args = parser.parse_args()
    # play bytebeat
    ByteBeat(formula=args.formula, duration=args.time).play()
