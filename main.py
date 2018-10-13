import pyaudio
import wave
import random
import string
import time
import sys
import os
from threading import Thread
from pydub import AudioSegment

def randstr(count):
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set * count, count))


class Recorder(object):
    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.fname = randstr(6) + ".wav"
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, mode='wb'):
        self.fname = "audio/" + randstr(6) + ".wav"
        return RecordingFile(self.fname, mode, self.channels, self.rate,
                             self.frames_per_buffer)


class RecordingFile(object):
    def __init__(self, fname, mode, channels, rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer,
                                     stream_callback=self.get_callback())

        print "Start recording"
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue

        return callback

    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile

    def export(self):
        if os.path.isfile(self.fname):
            song = AudioSegment.from_wav(self.fname)
            song.export(self.fname, format="wav")
            print "[Exported] Normal audio file"

    def export_reverse(self):
        fname = "reverse_" + self.fname
        if os.path.isfile(self.fname):
            song = AudioSegment.from_wav(self.fname)
            song = song.reverse()
            song.export(fname, format="wav")
            print "[Exported] Reverse version of audio file"

    def get_name_normal(self):
        return self.fname

    def get_name_reverse(self):
        return "reverse_" + self.fname


def main():
    r = Recorder()
    rf = r.open()
    rf.start_recording()
    time.sleep(5)
    rf.stop_recording()
    rf.export_reverse()
    pass


if __name__ == '__main__':
    main()
