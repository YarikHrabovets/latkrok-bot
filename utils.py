import os.path

import aiogram.types
from aiogram.types import MediaGroup, InputFile


def logo_media() -> aiogram.types.MediaGroup:
    media = MediaGroup()
    for i in range(1, 7):
        media.attach_photo(InputFile(os.path.abspath(f'src/logo_{i}.jpeg')))

    return media
