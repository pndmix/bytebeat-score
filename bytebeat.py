import numpy as np
from audio import Audio


class ByteBeat(Audio):
    """
    ByteBeat class, children of Audio
    let's playing bytebeat sound
    """
    def __init__(self, formula: str, rate: int=8000, duration: int=30):
        """
        :param formula:  bytebeat formula
        :param rate:     sampling rate[Hz] (default: 8000)
        :param duration: playback time[seconds] (default: 30)
        """
        super().__init__(rate)
        self.formula = str(formula)
        self.duration = int(duration)

    def __compute_with_formula(self, current: int, end: int, chunk: bool=True):
        """
        compute with the bytebeat formula
        :param current: current position of sampling points
        :param end:     end position of sampling points
        :param chunk:   computing range is CHUNK (default: True)
        :return: 1D numpy array converted to byte stream for audio
        """
        # set a end position of computing range
        if chunk:
            target_end = current + super().CHUNK
        else:
            target_end = current + end

        # create a 1D numpy array as arguments
        if target_end <= end:
            data = np.arange(current, target_end)
        else:
            data = np.arange(current, end)

        # compute with the bytebeat formula
        result = np.vectorize(lambda t: int(eval(self.formula)) % 256)(data)

        # convert a 1D numpy array into a byte stream for audio
        return result.astype(np.int8).tostring()

    def play(self):
        """
        start playback
        """
        # initialize a position of sampling points
        current_position = 0
        end_position = super().rate * self.duration

        # playback loop
        while current_position < end_position:
            # create a byte stream
            buffer = self.__compute_with_formula(current_position, end_position)
            super()._write_stream(buffer)

            # increment a current position by CHUNK
            current_position += super().CHUNK

    def record(self):
        """
        record bytebeat
        """
        # set a position of sampling points
        current_position = 0
        end_position = super().rate * self.duration

        # create a byte stream
        buffer = self.__compute_with_formula(current_position, end_position, chunk=False)
        super()._write_wav(buffer)


def argument_parser():
    """
    parse commandline arguments for ByteBeat class
    :return: parsed arguments
    """
    # create a parser
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # set parsing arguments
    parser.add_argument("formula", type=str, help="set bytebeat formula")
    parser.add_argument("-r", "--rate", type=int, help="set sampling rate[Hz]", default=8000)
    parser.add_argument("-t", "--time", type=int, help="set playback time[sec]", default=30)
#    parser.add_argument("-s", "--score", type=int, help="set playback time[sec]", default=30)
    return parser.parse_args()


if __name__ == "__main__":
    # instantiate ByteBeat
    args = argument_parser()
    b = ByteBeat(formula=args.formula, rate=args.rate, duration=args.time)

    # start ByteBeat sound
    try:
        print("Sampling rate: {} Hz, "
              "Playback time: {} sec".format(args.rate, args.time))
        b.play()
        b.record()
    except KeyboardInterrupt:
        print("Interrupting playback")
    finally:
        b.close()
