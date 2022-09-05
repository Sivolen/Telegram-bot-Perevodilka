import ffmpeg
from vosk import Model, KaldiRecognizer
from recasepunc.recasepunc import CasePuncPredictor, WordpieceTokenizer
import ffmpeg
from pydub import AudioSegment
import json
import os
from pathlib import Path
import speech_recognition as sr


def converter(file_name: str) -> str:
    """

    :param file_name: str
    :return: str
    """
    file_path = f"{Path(__file__).parent.parent}\\cache\\{file_name}"
    name = file_name.split(".")
    m4a_audio = AudioSegment.from_file(file_path, format="mp4")

    m4a_audio.export(
        f"{Path(__file__).parent.parent}\\cache\\{name[0]}.mp3", format="mp3"
    )
    return f"{Path(__file__).parent.parent}\\cache\\{name[0]}.mp3"


def converter_wav(file_name: str) -> str:
    """

    :param file_name: str
    :return: str
    """
    file_path = f"{Path(__file__).parent.parent}\\cache\\{file_name}"
    name = file_name.split(".")
    m4a_audio = AudioSegment.from_file(file_path, format="mp4")
    m4a_audio.export(
        f"{Path(__file__).parent.parent}\\cache\\{name[0]}.wav", format="wav"
    )
    audio_file = f"{Path(__file__).parent.parent}\\cache\\{name[0]}.wav"
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="ru")


def translate(file_name: str) -> str:
    """
    :param file_name: str
    :return: str
    """

    if not os.path.exists(f"{Path(__file__).parent.parent}/model"):
        print(
            "Please download the model from https://alphacephei.com/vosk/models "
            "and unpack as 'model' in the current folder."
        )
        exit(1)

    file_path = converter(file_name=file_name)
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
    # print(text)
    # cased = subprocess.check_output(
    #     f"python {Path(__file__).parent.parent}\\recasepunc\\recasepunc.py predict "
    #     f"{Path(__file__).parent.parent}\\recasepunc\\checkpoint",
    #     shell=True,
    #     text=True,
    #     input=text,
    # )

    # print(cased)

    if not os.path.exists(f"{Path(__file__).parent.parent}/recasepunc"):
        return text
    else:
        text = punctuation(text)
        return text


def punctuation(text: str) -> str:
    predictor = CasePuncPredictor(
        f"{Path(__file__).parent.parent}/recasepunc/checkpoint", lang="ru"
    )

    text = text
    tokens = list(enumerate(predictor.tokenize(text)))

    results = ""
    for token, case_label, punc_label in predictor.predict(tokens, lambda x: x[1]):
        prediction = predictor.map_punc_label(
            predictor.map_case_label(token[1], case_label), punc_label
        )
        if token[1][0] != "#":
            results = results + " " + prediction
        else:
            results = results + prediction
    return results


# print(translate("AUDIO-2022-08-31-09-32-19.m4a"))