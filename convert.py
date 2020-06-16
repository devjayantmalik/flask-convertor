
from converter import Converter

def convert_file(filename):
    c = Converter()

    conv = c.convert(f'./static/{filename}.mp4', f'./static/output-{filename}.mkv', {
    'format': 'mkv',
    'audio': {
        'codec': 'mp3',
        'samplerate': 11025,
        'channels': 2
    },
    'video': {
        'codec': 'h264',
        'width': 480,
        'height': 360,
        'fps': 30
    }})


    global PROGRESS
    PROGRESS.append({"filename": filename, "progress": 0})

    for percent in conv:
        for item in PROGRESS:
            if item['filename'] == filename:
                item['progress'] = percent