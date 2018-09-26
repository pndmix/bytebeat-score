import pyaudio
import wave


class Audio:
    """
    Audio class with pyaudio
    """
    FORMAT = pyaudio.paInt8
    CHANNELS = 1
    CHUNK = 1024

    def __init__(self, rate: int):
        """
        :param rate: sampling rate[Hz]
        """
        self.__rate = int(rate)

        # start audio stream
        self.__pa = pyaudio.PyAudio()
        self.__stream = self.__pa.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.__rate,
            frames_per_buffer=self.CHUNK,
            output=True
        )

    def write_stream(self, buffer: bytes):
        """
        write audio stream
        :param buffer: byte stream for pyaudio
        """
        self.__stream.write(buffer)

    def write_wav(self, filename: str, buffer: bytes):
        """
        write wav file
        :param filename: wav filename
        :param buffer:   byte stream for pyaudio
        """
        with wave.open(filename, "w") as w:
            w.setnchannels(self.CHANNELS)
            w.setsampwidth(1)
            w.setframerate(self.__rate)
            w.writeframes(buffer)

    def close(self):
        """
        terminate audio stream
        """
        self.__stream.stop_stream()
        self.__stream.close()
        self.__pa.terminate()
