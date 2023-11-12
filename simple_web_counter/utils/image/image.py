from typing import Iterable, Iterator

from PIL import Image  # type: ignore


def resize_image_to_height(image: Image.Image, height: int) -> Image.Image:
    return image.resize(size=(int(image.width * (height / image.height)), height))


def concat_paired_images(
    left_image: Image.Image, right_image: Image.Image, mode: str
) -> Image.Image:
    dest_image_width = left_image.width + right_image.width
    dest_image_height = max(left_image.height, right_image.height)

    dest_image = Image.new(mode=mode, size=(dest_image_width, dest_image_height))
    dest_image.paste(im=left_image, box=(0, 0))
    dest_image.paste(im=right_image, box=(left_image.width, 0))

    return dest_image


def concat_images(images: Iterable[Image.Image], mode: str) -> Image.Image:
    images_itr = iter(images)

    return _concat_images(next(images_itr), images_itr, mode=mode)


def _concat_images(
    first_image: Image.Image, rest_images_itr: Iterator[Image.Image], mode: str
) -> Image.Image:
    try:
        return concat_paired_images(
            left_image=first_image,
            right_image=_concat_images(
                first_image=next(rest_images_itr),
                rest_images_itr=rest_images_itr,
                mode=mode,
            ),
            mode=mode,
        )
    except StopIteration:
        return first_image
