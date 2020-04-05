from PIL import Image
import os
import re

base_path = "LINEMOD/"
Synthetic_path  = base_path + "synthetic/"
synthetic_files = os.listdir(Synthetic_path)
a = re.compile(r".*img.*")
toConvert = list(filter(a.match, synthetic_files))
for curr_file in toConvert:
    im = Image.open(Synthetic_path + curr_file)
    rgb_im = im.convert('RGB')
    rgb_im.save(Synthetic_path + curr_file[:-3] + "jpg")
    os.remove(Synthetic_path + curr_file)