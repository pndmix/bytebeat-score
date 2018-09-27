import os
import numpy as np
from audio import Audio
from notation import infix, postfix


class ByteBeat:
    """
    ByteBeat class
    let's enjoy bytebeat sound
    """
    def __init__(self, formula: str,
                 rate: int=8000, duration: int=30, notation: str="infix"):
        """
        :param formula:  bytebeat formula
        :param rate:     sampling rate[Hz] (default: 8000)
        :param duration: playback time[seconds] (default: 30)
        :param notation: formula notation name (default: infix)
        """
        self.formula = str(formula)
        self.rate = int(rate)
        self.duration = int(duration)
        self.notation = eval(notation)  # infix or postfix function
        self.audio = Audio(self.rate)  # instantiate and open audio stream

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
            target_end = current + self.audio.CHUNK
        else:
            target_end = current + end

        # create a 1D numpy array as arguments
        if target_end <= end:
            data = np.arange(current, target_end, dtype=np.int64)
        else:
            data = np.arange(current, end, dtype=np.int64)

        # compute with the bytebeat formula
        result = np.vectorize(lambda t: self.notation(self.formula, t) % 256)(data)

        # convert a 1D numpy array into a byte stream for audio
        return result.astype(np.int8).tostring()

    def play(self):
        """
        start playback
        """
        # initialize a position of sampling points
        current_position = 0
        end_position = self.rate * self.duration

        # playback loop
        while current_position < end_position:
            # create a byte stream
            buffer = self.__compute_with_formula(current_position, end_position)
            self.audio.write_stream(buffer)

            # increment a current position by CHUNK
            current_position += self.audio.CHUNK

    def record(self, path: str):
        """
        record bytebeat sound in wav
        :param path: wav file path
        """
        # set a position of sampling points
        current_position = 0
        end_position = self.rate * self.duration

        # create a byte stream
        buffer = self.__compute_with_formula(current_position, end_position, chunk=False)

        # write sound in wav
        self.audio.write_wav(path, buffer)

    def write_score(self, path: str):
        """
        create and write a score file
        :param path: wav file path
        """
        # split path
        dir_path, filename = os.path.split(path)

        # create a new score file if not exist
        score_path = dir_path + "/scores.md"
        if not os.path.exists(score_path):
            text = "# ByteBeat Scores\n" \
                   "| NAME | FORMULA | RATE[Hz] | TIME[sec] |\n" \
                   "| :--- | :--- | :---: | :---: |\n"
            with open(score_path, "w") as f:
                f.write(text)

        # write a score file
        text = "| [{0}]({0}) | {1} | {2} | {3} |\n".format(
            filename,
            self.formula.replace("*", "\*").replace("|", "\|"),
            self.rate,
            self.duration
        )
        with open(score_path, "a") as f:
            f.write(text)


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
    parser.add_argument("-p", "--postfix", action="store_const", const="postfix", default="infix",
                        help="postfix notation")
    parser.add_argument("-r", "--rate", type=int, default=8000,
                        help="sampling rate[Hz] (default: 8000)")
    parser.add_argument("-t", "--time", type=int, default=30,
                        help="playback time[sec] (default: 30)")
    parser.add_argument("-s", "--score", type=str, nargs="?",
                        const="./scores/{0:%Y%m%d-%H%M%S}.wav".format(datetime.datetime.now()),
                        help="write a wav file (default: ./scores/[TIMESTAMP].wav)")
    return parser.parse_args()


def score(obj: ByteBeat, path: str):
    """
    optional score feature with commandline
    feature: writing score, recording sound in wav
    :param obj: ByteBeat instance
    :param path: wav file path
    """
    from sys import stderr
    from threading import Thread
    stderr.write("Scoring now ... ")
    stderr.flush()

    # create and start new threads
    threads = list()
    threads.append(Thread(target=obj.record, args=(path,), name="record"))
    threads.append(Thread(target=obj.write_score, args=(path,), name="write"))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    stderr.write("done.\n")
    stderr.flush()


if __name__ == "__main__":
    from threading import Thread

    # get parsed arguments
    args = argument_parser()

    # instantiate ByteBeat
    b = ByteBeat(formula=args.formula, rate=args.rate, duration=args.time, notation=args.postfix)
    try:
        print("Sampling rate: {} Hz, "
              "Playback time: {} sec".format(b.rate, b.duration))

        # create and start a new daemon thread if score option
        if args.score:
            Thread(target=score, args=(b, args.score,), name="score", daemon=True).start()

        # start playback
        b.play()
    except KeyboardInterrupt:
        print("interrupting")
    finally:
        b.audio.close()
