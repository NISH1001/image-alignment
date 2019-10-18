# image-alignment
A naive way to align a test image with a template one

## Usage
Run `aligner.py` with image name supplied as argument.  

```bash
python aligner.py images/test.jpg
```

The result will be stored as `res.jpg`

Random images can be tested by supplying `random` as an argument.  
```bash
python aligner.py random
```

## How?
The algorithm is very simple.  
- binarize/threshold the original image (with foreground color as white)
- take the coordinates of white pixels
- simply deduce a bounding box that enclosed these pixels along with the angle of alignment of the box.
- calculate angle of rotation/alignment
- align the origina image

The process is very naive (and simple). So, if the origina image if already rotated by 90 degrees perfectly, the alignment doesn't work.  
