NoteShrink
==========

This Repo packages up the work from [Mark Zucker](https://github.com/mzucker/noteshrink) into a python module and cli script

Convert scans of handwritten notes to beautiful, compact *PDFs* [see full writeup](https://mzucker.github.io/2016/09/20/noteshrink.html)

Note this package does not convert to PDF as the original module relies on ImageMagick, this is very easy to implement yourself.


Requirements
------------

-  Python 2 or 3
-  NumPy 1.10 or later
-  SciPy
-  Image module from PIL or Pillow


Installation
-----

**Ensure you have Numpy, SciPy and PIL installed:**

```python
pip install numpy scipy pillow
```

```python
pip install NoteShrink
```

Usage
-----

**Commandline**
```bash
    note-shrink IMAGE1 [IMAGE2 ...]
```

**Integrating into your Python scripts**

```python
from NoteShrink import NoteShink

# Create a NoteShrink object full of images, either an array of filepaths, PIL images or numpy arrays
ns = NoteShrink(['test.png'], **args)

# Shrink the images by calling the shrink method, this returns an array of PIL images encoded as RGB
shrunk = ns.shrink()

# Carry on with your image processing...
for img in shrunk:
   img.save('example.png')
```


