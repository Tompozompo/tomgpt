import io
import sounddevice as sd
import soundfile as sf
from tomgpt.interfaces.cmd_assistant import CMDInterface
from tomgpt.interfaces.interface import Interface


class VoiceInterface(Interface):
    def __init__(self, client) -> None:
        super().__init__()
        self.file_path = "recorded_audio.wav"
        self.sample_rate = 44100  # Sample rate (number of samples per second)
        self.duration = 10 # The duration needs to be set beforehand... so hard limit on secs
        self.client = client
        
    def get_input(self):
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        input('Press Enter to start recording')
        recording = sd.rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=1, blocking=False)
        input("Press Enter to stop recording...")
        sd.stop()
        recording = recording[:sd.stop()]
        sf.write(self.file_path, recording, self.sample_rate)
        print("Recording saved to:", self.file_path)
        audio_file= open(self.file_path, "rb")
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        print(transcript)
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        return transcript.text
    
    def display(self, messages):
        CMDInterface().display(messages)
        m = list(messages)[-1].content[0].text.value
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="fable", # nova shimmer
            input=m,
        )
        response.stream_to_file("output.mp3")
        audio_byte_stream = io.BytesIO(response.content)
        audio_data, file_sample_rate = sf.read(audio_byte_stream)
        sd.play(audio_data, file_sample_rate)
        sd.wait()
