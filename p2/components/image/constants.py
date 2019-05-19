"""p2 image component constants"""

# Taken from https://sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html
EXIF_IMAGE_WIDTH = 'ImageWidth'
EXIF_IMAGE_HEIGHT = 'ImageHeight'
EXIF_COMPRESSION = 'Compression'
EXIF_ORIENTATION = 'Orientation'
EXIF_MODEL = 'Model'
EXIF_SOFTWARE = 'Software'

DEFAULT_EXIF_TAGS = [
    EXIF_IMAGE_WIDTH,
    EXIF_IMAGE_HEIGHT,
    EXIF_COMPRESSION,
    EXIF_ORIENTATION,
    EXIF_MODEL,
    EXIF_SOFTWARE,
]

TAG_IMAGE_EXIF_TAGS = 'component.p2.io/image/exif_tags'
