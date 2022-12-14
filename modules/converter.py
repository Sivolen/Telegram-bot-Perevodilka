from pathlib import Path
from pydub import AudioSegment


def converter(file_name: str, format_file: str) -> str:
    """
    This function converts the original audio file into the formats needed for translation.
    :param format_file:
    :param file_name: str
    :return: str
    """

    file_path = Path(f"{Path(__file__).parent.parent}/cache/{file_name}")
    # file_path = Path(file_path)
    if (
        file_path.suffix == ".opus"
        or file_path.suffix == ".m4a"
        or file_path.suffix == ".ogg"
        or file_path.suffix == ".mp3"
        or file_path.suffix == ".wav"
        or file_path.suffix == ".mp4"
        or file_path.suffix == ".mkv"
    ):
        # name = file_name.split(".")
        name = file_path.stem

        audio = AudioSegment.from_file(file_path)

        audio.export(
            f"{Path(__file__).parent.parent}/cache/{name}.{format_file}",
            format=format_file,
        )
        return f"{Path(__file__).parent.parent}/cache/{name}.{format_file}"
