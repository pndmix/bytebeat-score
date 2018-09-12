import pyaudio


class Audio:
    """
    Audio class with pyaudio for ByteBeat
    """
    FORMAT = pyaudio.paInt8
    CHANNELS = 1
    CHUNK = 1024

    def __init__(self, rate):
        """
        :param rate: sampling rate[Hz]
        """
        self.__rate = rate
        self.__pa = pyaudio.PyAudio()
        self.__stream = self.__pa.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.__rate,
            frames_per_buffer=self.CHUNK,
            output=True
        )

    @property
    def rate(self):
        return self.__rate

    def write_stream(self, buffer):
        """
        write audio stream
        :param buffer: byte strings
        """
        self.__stream.write(buffer)

    def close(self):
        """
        terminate audio stream
        """
        self.__stream.stop_stream()
        self.__stream.close()
        self.__pa.terminate()
