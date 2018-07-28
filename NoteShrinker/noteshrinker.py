from PIL import Image
import numpy as np
from scipy.cluster.vq import kmeans, vq

from .noteshrinker_helpers import get_bg_color, get_fg_mask

class NoteImageTypeException(Exception):
    pass

class Note(object):

    def __init__(self, image, sample_fraction, num_colors,
                 saturate, white_bg, value_threshold, sat_threshold):

        if isinstance(image, str):
            self.image = np.array(Image.open(image))
        elif isinstance(image, Image.Image):
            self.image = np.array(image)
        elif isinstance(image, np.ndarray):
            self.image = image
        else:
            raise NoteImageTypeException('image must be supplied as a PIL Image, a filepath or numpy array')

        # PNG can have 4 color channels, for now just remove alpha
        if self.image.shape[2] == 4:
            self.image = self.image[...,: 3]

        self.image_shape = self.image.shape

        self.sample_fraction = sample_fraction
        self.num_colors = num_colors
        self.saturate = saturate
        self.white_bg = white_bg
        self.value_threshold = value_threshold
        self.sat_threshold = sat_threshold

        self.samples = self.sample_pixels()
        self.palette = None
        self.bg_color = None
        self.fg_color = None


    def sample_pixels(self):
        '''Pick a fixed percentage of pixels in the image, returned in random order.'''

        pixels = self.image.reshape((-1, 3))
        num_pixels = pixels.shape[0]
        num_samples = int(num_pixels * self.sample_fraction)

        idx = np.arange(num_pixels)
        np.random.shuffle(idx)

        return pixels[idx[:num_samples]]


    def set_palette(self, samples, kmeans_iter=40):
        '''Extract the palette for the set of sampled RGB values. The first
        palette entry is always the background color; the rest are determined
        from foreground pixels by running K-means clustering. Returns the
        palette, as well as a mask corresponding to the foreground pixels.'''

        self.bg_color = get_bg_color(samples)

        self.fg_mask = get_fg_mask(self.bg_color, samples, self.value_threshold, self.sat_threshold)

        self.centers, _ = kmeans(self.samples[self.fg_mask].astype(np.float32),
                            self.num_colors - 1,
                            iter=kmeans_iter)

        self.palette = np.vstack((self.bg_color, self.centers)).astype(np.uint8)


    def apply_palette(self):

        bg_color = self.palette[0]
        fg_mask = get_fg_mask(bg_color, self.image, self.value_threshold, self.sat_threshold)

        pixels = self.image.reshape((-1, 3))
        fg_mask = fg_mask.flatten()

        num_pixels = pixels.shape[0]
        labels = np.zeros(num_pixels, dtype=np.uint8)

        labels[fg_mask], _ = vq(pixels[fg_mask], self.palette)

        self.labels = labels.reshape(self.image_shape[:-1])


    def shrink(self):

        self.apply_palette()

        if self.saturate:
            self.palette = self.palette.astype(np.float32)
            pmin = self.palette.min()
            pmax = self.palette.max()
            self.palette = 255 * (self.palette - pmin) / (pmax - pmin)
            self.palette = self.palette.astype(np.uint8)

        if self.white_bg:
            self.palette = self.palette.copy()
            self.palette[0] = (255, 255, 255)

        self.shrunk = Image.fromarray(self.labels, 'P')
        self.shrunk.putpalette(self.palette.flatten())
        self.shrunk = self.shrunk.convert('RGB')


class NoteShrinker(object):


    def __init__(self, images, global_palette=True, sample_fraction=5,
                 num_colors=8, saturate=True, white_bg=True,
                 value_threshold=0.15, sat_threshold=0.2):

        if not isinstance(images, list):
            images = [images]

        self.global_palette = global_palette

        self.notes = [Note(img, sample_fraction, num_colors, saturate,
                           white_bg, value_threshold, sat_threshold) for img in images]

        self.num_inputs = len(images)


    def get_global_palette(self):

        all_samples = [note.samples for note in self.notes]
        all_samples = [s[:int(round(s.shape[0] / self.num_inputs))] for s in all_samples]
        global_samples = np.vstack(tuple(all_samples))

        [note.set_palette(global_samples) for note in self.notes]


    def shrink(self):

        if self.global_palette:
            self.get_global_palette()
        else:
            [note.set_palette(note.samples) for note in self.notes]

        [note.shrink() for note in self.notes]

        return [note.shrunk for note in self.notes]
