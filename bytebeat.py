import sys
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

        buffer = self.__buffer()
        stream.write(buffer)
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    _, f, dur = sys.argv
    ByteBeat(formula=f, duration=dur).play()
