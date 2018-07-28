NoteShrinker
==========

![GitHub stars](https://img.shields.io/github/stars/ghandic/NoteShrinker.svg?style=social&label=Stars)
![Docker build](https://img.shields.io/docker/automated/challisa/noteshrinker.svg)
![Package version](https://img.shields.io/pypi/v/NoteShrinker.svg)
![License](https://img.shields.io/github/license/ghandic/NoteShrinker.svg)

This Repo packages up the work from [Mark Zucker](https://github.com/mzucker/noteshrink) into a python module and cli script

Convert scans of handwritten notes to beautiful, compact *PDFs* [see full writeup](https://mzucker.github.io/2016/09/20/noteshrink.html)

Note this package does not convert to PDF as the original module relies on ImageMagick, this is very easy to implement yourself.


Examples
------------
These examples use the default settings in the Python module.

Original            |  NoteShrunk
:-------------------------:|:-------------------------:
**Size: 1.4MB**![Original example 1](Examples/Input/us_tax_form_1937.jpg?raw=true "Original US Tax return form from 1937")  |  **Size: 516KB**![NoteShunk example 1](Examples/Output/us_tax_form_1937.png?raw=true "NoteShrunk US Tax return form from 1937")
**Size: 73KB**![Original example 2](Examples/Input/winston_churchhill_letter.jpg?raw=true "Original letter from Winston Churchhill")  |  **Size: 51KB**![NoteShunk example 2](Examples/Output/winston_churchhill_letter.png?raw=true "NoteShrunk letter from Winston Churchhill")
**Size: 132KB**![Original example 3](Examples/Input/Restraint_of_domestic_animals.jpg?raw=true "Original page from 'Restraint of domestic animals'")| **Size: 109KB**![NoteShunk example 3](Examples/Output/Restraint_of_domestic_animals.png?raw=true "NoteShrunk page from 'Restraint of domestic animals'")


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
pip install NoteShrinker
```

Usage
-----

**Docker**
```bash
docker run -v $PWD/Examples/Input:/imgs challisa/noteshrinker /imgs/us_tax_form_1937.jpg -w
```

**Command line**
```bash
    note-shrinker IMAGE1 [IMAGE2 ...]
```

**Integrating into your Python scripts**

```python
from NoteShrinker import NoteShrinker

# Create a NoteShrink object full of images, either an array of filepaths, PIL images or numpy arrays
ns = NoteShrinker(['test.png'], **args)

# Shrink the images by calling the shrink method, this returns an array of PIL images encoded as RGB
shrunk = ns.shrink()

# Carry on with your image processing...
for img in shrunk:
   img.save('example.png')
```
