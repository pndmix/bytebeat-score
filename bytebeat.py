import argparse
import struct
import numpy as np
import pyaudio


class ByteBeat:
    CHUNK = 1024
    FORMAT = pyaudio.paUInt8
    RATE = 8000
    CHANNELS = 1

    def __init__(self, formula, duration):
        self.formula = formula
        self.duration = int(duration)

    def __compute_with_formula(self, current, end):
        length = ByteBeat.CHUNK // 2
        if current + length <= end:
            data = np.arange(current, current + length)
        else:
            data = np.arange(current, end)
        return np.vectorize(lambda t: int(eval(self.formula)) % 256)(data)

    def play(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=ByteBeat.FORMAT,
            channels=ByteBeat.CHANNELS,
            rate=ByteBeat.RATE,
            frames_per_buffer=ByteBeat.CHUNK,
            output=True
        )
        try:
            current_sample = 0
            end_sample = self.duration * ByteBeat.RATE // 2
            while current_sample < end_sample:
                data = self.__compute_with_formula(current_sample, end_sample)
                buffer = struct.pack("h" * len(data), *data)
                stream.write(buffer)
                current_sample += len(data)
        except KeyboardInterrupt:
            pass
        finally:
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
