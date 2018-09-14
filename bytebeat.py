#import datetime
import numpy as np
from audio import Audio


class ByteBeat(Audio):
    """
    ByteBeat class, children of Audio
    let's enjoy bytebeat sound
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
        :return: bytes
            byte stream for audio
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

    def record(self, filename: str):
        """
        record bytebeat sound in wav
        :param filename: wav filename
        """
        # set a position of sampling points
        current_position = 0
        end_position = super().rate * self.duration

        # create a byte stream
        buffer = self.__compute_with_formula(current_position, end_position, chunk=False)

        # write sound in wav
        super()._write_wav(filename, buffer)


def argument_parser():
    """
    parse commandline arguments for ByteBeat class
    :return: namespace object
        parsed arguments
    """
    # create a parser
    import argparse
    import datetime
    parser = argparse.ArgumentParser()

    # set parsing arguments
    parser.add_argument("formula", type=str,
                        help="bytebeat formula")
    parser.add_argument("-r", "--rate", type=int, default=8000,
                        help="sampling rate[Hz] (default: 8000)")
    parser.add_argument("-t", "--time", type=int, default=30,
                        help="playback time[sec] (default: 30)")
    parser.add_argument("-s", "--score-name", type=str, nargs="?",
                        const="./scores/{0:%Y%m%d-%H%M%S}.wav".format(datetime.datetime.now()),
                        help="write a wav file (default: ./scores/[CURRENT_TIME].wav)")
    return parser.parse_args()


if __name__ == "__main__":
    from threading import Thread
    # get parsed arguments
    args = argument_parser()

    # instantiate ByteBeat
    b = ByteBeat(formula=args.formula, rate=args.rate, duration=args.time)
    try:
        print("Sampling rate: {} Hz, "
              "Playback time: {} sec".format(args.rate, args.time))

        # create and start new daemon thread for recording if score option
        if args.score:
            Thread(target=b.record, args=(args.score,), daemon=True).start()

        # start playback
        b.play()
    except KeyboardInterrupt:
        print("interrupting playback")
    finally:
        b.close()
