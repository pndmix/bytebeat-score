import pyaudio
import wave


class Audio:
    """
    Audio class with pyaudio, parent of ByteBeat
    """
    FORMAT = pyaudio.paInt8
    CHANNELS = 1
    CHUNK = 1024

    def __init__(self, rate):
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

    @property
    def rate(self):
        return self.__rate

    def _write_stream(self, buffer):
        """
        write audio stream
        :param buffer: byte strings
        """
        self.__stream.write(buffer)

    def _write_wav(self, buffer):
        """
        write wav file
        :param buffer: byte strings
        """
        with wave.open("/aaa.wav", "w") as w:
            w.setnchannels(self.CHANNELS)
            w.setsampwidth(1)
            w.setframerate(self.__rate)
            w.writeframes(buffer)
            w.close()

    def close(self):
        """
        terminate audio stream
        """
        self.__stream.stop_stream()
        self.__stream.close()
        self.__pa.terminate()
