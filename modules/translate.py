from vosk import Model, KaldiRecognizer

# from recasepunc.recasepunc import CasePuncPredictor, WordpieceTokenizer
from pydub import AudioSegment
import json
from pathlib import Path
import speech_recognition as sr
from modules.converter import converter


def translate_sr(file_name: str) -> str:
    """
    This feature converts audio to text using speech recognition using the free Google API.
    :return: str
    """
    file_path = Path(f"{Path(__file__).parent.parent}/cache/{file_name}")
    if not file_path.suffix == ".wav":
        file_path = converter(file_name=file_name, format_file="wav")

    audio_file = file_path
    r = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    Path(audio_file).unlink()
    return r.recognize_google(audio, language="ru")


def translate_vosk(file_name: str) -> str:
    """
    :param file_name: str
    :return: str
    """
    model_path = Path(f"{Path(__file__).parent.parent}/model-small")
    if not model_path.exists():
        return (
            "Please download the model from https://alphacephei.com/vosk/models "
            "and unpack as 'model' in the current folder."
        )
    file_path = Path(f"{Path(__file__).parent.parent}/cache/{file_name}")
    if not file_path.suffix == ".mp3":
        file_path = converter(file_name=file_name, format_file="mp3")
    frame_rate = 16000
    channels = 1

    model = Model(f"{Path(__file__).parent.parent}/model-small")
    rec = KaldiRecognizer(model, frame_rate)
    rec.SetWords(True)

    mp3 = AudioSegment.from_mp3(file_path)
    mp3 = mp3.set_channels(channels)
    mp3 = mp3.set_frame_rate(frame_rate)

    rec.AcceptWaveform(mp3.raw_data)
    result = rec.Result()
    text = json.loads(result)["text"]

    Path(file_path).unlink()
    # if not os.path.exists(f"{Path(__file__).parent.parent}/recasepunc"):
    #     return text
    # else:
    #     text = punctuation(text)
    #     return text
    return text


# def punctuation(text: str) -> str:
#     predictor = CasePuncPredictor(
#         f"{Path(__file__).parent.parent}/recasepunc/checkpoint", lang="ru"
#     )
#
#     text = text
#     tokens = list(enumerate(predictor.tokenize(text)))
#
#     results = ""
#     for token, case_label, punc_label in predictor.predict(tokens, lambda x: x[1]):
#         prediction = predictor.map_punc_label(
#             predictor.map_case_label(token[1], case_label), punc_label
#         )
#         if token[1][0] != "#":
#             results = results + " " + prediction
#         else:
#             results = results + prediction
#     return results


# print(converter("PTT-20220906-WA0003.opus", format_file="mp3"))
