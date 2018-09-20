import os
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
            data = np.arange(current, target_end, dtype=np.int64)
        else:
            data = np.arange(current, end, dtype=np.int64)

        # compute with the bytebeat formula
        formula = self.formula.replace("/", "//")  # replace division operator for integer
        result = np.vectorize(lambda t: eval(formula) % 256)(data)

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

    def record(self, path: str):
        """
        record bytebeat sound in wav
        :param path: wav file path
        """
        # set a position of sampling points
        current_position = 0
        end_position = super().rate * self.duration

        # create a byte stream
        buffer = self.__compute_with_formula(current_position, end_position, chunk=False)

        # write sound in wav
        super()._write_wav(path, buffer)

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
            filename, self.formula, self.rate, self.duration
        )
        with open(score_path, "a") as f:
            f.write(text)


if __name__ == "__main__":
    from threading import Thread

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

    # get parsed arguments
    args = argument_parser()

    # instantiate ByteBeat
    b = ByteBeat(formula=args.formula, rate=args.rate, duration=args.time)
    try:
        print("Sampling rate: {} Hz, "
              "Playback time: {} sec".format(b.rate, b.duration))

        # create and start a new thread if score option
        if args.score:
            Thread(target=score, args=(b, args.score,), name="score").start()

        # start playback
        b.play()
    except KeyboardInterrupt:
        print("interrupting playback")
    finally:
        b.close()
