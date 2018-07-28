import numpy as np
from PIL import Image


def downsampled_image(img, ds_ratio):
    '''Reduced the size of the image to be used in the NoteShrink'''
    new_w = max(int(img.shape[0]*ds_ratio), 100)
    new_h = max(int(img.shape[1]*ds_ratio), 100)

    downsampled_image = Image.fromarray(img).resize((new_w,new_h))
    return np.array(downsampled_image)


def quantize(image, bits_per_channel):
    '''Reduces the number of bits per channel in the given image.'''

    assert image.dtype == np.uint8

    shift = 8 - bits_per_channel
    halfbin = (1 << shift) >> 1

    return ((image.astype(int) >> shift) << shift) + halfbin


def unpack_rgb(packed):
    '''Unpacks a single integer or array of integers into one or more
24-bit RGB values.
    '''

    orig_shape = None

    if isinstance(packed, np.ndarray):
        assert packed.dtype == int
        orig_shape = packed.shape
        packed = packed.reshape((-1, 1))

    rgb = ((packed >> 16) & 0xff,
           (packed >> 8) & 0xff,
           (packed) & 0xff)

    if orig_shape is None:
        return rgb
    else:
        return np.hstack(rgb).reshape(orig_shape + (3,))


def pack_rgb(rgb):
    '''Packs a 24-bit RGB triples into a single integer,
    works on both arrays and tuples.'''

    orig_shape = None

    if isinstance(rgb, np.ndarray):
        assert rgb.shape[-1] == 3
        orig_shape = rgb.shape[:-1]
    else:
        assert len(rgb) == 3
        rgb = np.array(rgb)

    rgb = rgb.astype(int).reshape((-1, 3))

    packed = (rgb[:, 0] << 16 |
              rgb[:, 1] << 8 |
              rgb[:, 2])

    if orig_shape is None:
        return packed
    else:
        return packed.reshape(orig_shape)


def rgb_to_sv(rgb):
    '''Convert an RGB image or array of RGB colors to saturation and
    value, returning each one as a separate 32-bit floating point array or
    value.'''

    if not isinstance(rgb, np.ndarray):
        rgb = np.array(rgb)

    axis = len(rgb.shape) - 1
    cmax = rgb.max(axis=axis).astype(np.float32)
    cmin = rgb.min(axis=axis).astype(np.float32)
    delta = cmax - cmin

    saturation = delta.astype(np.float32) / cmax.astype(np.float32)
    saturation = np.where(cmax == 0, 0, saturation)

    value = cmax / 255.0

    return saturation, value


def get_bg_color(image, bits_per_channel=6):
    '''Obtains the background color from an image or array of RGB colors
    by grouping similar colors into bins and finding the most frequent
    one.'''

    assert image.shape[-1] == 3

    quantized = quantize(image, bits_per_channel).astype(int)
    packed = pack_rgb(quantized)

    unique, counts = np.unique(packed, return_counts=True)

    packed_mode = unique[counts.argmax()]

    return unpack_rgb(packed_mode)


def get_fg_mask(bg_color, samples, value_threshold, sat_threshold):
    '''Determine whether each pixel in a set of samples is foreground by
    comparing it to the background color. A pixel is classified as a
    foreground pixel if either its value or saturation differs from the
    background by a threshold.'''

    s_bg, v_bg = rgb_to_sv(bg_color)
    s_samples, v_samples = rgb_to_sv(samples)

    s_diff = np.abs(s_bg - s_samples)
    v_diff = np.abs(v_bg - v_samples)

    return ((v_diff >= value_threshold) |
            (s_diff >= sat_threshold))
