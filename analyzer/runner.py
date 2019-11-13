##
## This is the Runner for the CTWC Video Analyzer
## Created: Sunday - Nov 10, 2019
##

import cv2
from .engine import Engine
from .vars import Vars as v

## Set the source and destination directories - Currently unused
# video_source = "./part01.mp4"
# output_dir = "./frames"

## Instantiate what we need to use
engine = Engine()

def invoke_exit():
    print("Bye! Have a great day!")
    exit()

file_root = "C:/code/ctwc/analyzer/f_samples"

i1 = f"{file_root}/i1__frame-5100__170-secs.jpg", v.i, 1
i2 = f"{file_root}/i2__frame-7200__240-secs.jpg", v.i, 2
i3 = f"{file_root}/i3__frame-10800__360-secs.jpg", v.i, 3

j1 = f"{file_root}/j1__frame-11700__390-secs.jpg", v.j, 1
j2 = f"{file_root}/j2__frame-13800__460-secs.jpg", v.j, 2
j3 = f"{file_root}/j3__frame-15900__530-secs.jpg", v.j, 3

l1 = f"{file_root}/l1__frame-9300__310-secs.jpg", v.l, 1
l2 = f"{file_root}/l2__frame-10200__340-secs.jpg", v.l, 2
l3 = f"{file_root}/l3__frame-11100__370-secs.jpg", v.l, 3

o1 = f"{file_root}/o1__frame-4800__160-secs.jpg", v.o, 1
o2 = f"{file_root}/o2__frame-5400__180-secs.jpg", v.o, 2
o3 = f"{file_root}/o3__frame-5700__190-secs.jpg", v.o, 3

s1 = f"{file_root}/s1__frame-7500__250-secs.jpg", v.s, 1
s2 = f"{file_root}/s2__frame-9900__330-secs.jpg", v.s, 2
s3 = f"{file_root}/s3__frame-15600__520-secs.jpg", v.s, 3

t1 = f"{file_root}/t1__frame-4200__140-secs.jpg", v.t, 1
t2 = f"{file_root}/t2__frame-12300__410-secs.jpg", v.t, 2
t3 = f"{file_root}/t3__frame-13200__440-secs.jpg", v.t, 3

z1 = f"{file_root}/z1__frame-4500__150-secs.jpg", v.z, 1
z2 = f"{file_root}/z2__frame-6300__210-secs.jpg", v.z, 2
z3 = f"{file_root}/z3__frame-6900__230-secs.jpg", v.z, 3

tetrominos = i1, i2, i3, j1, j2, j3, l1, l2, l3, o1, o2, \
             o3, s1, s2, s3, t1, t2, t3, z1, z2, z3

def parse_images():
    for piece in tetrominos:
        a = engine.parse_image(piece[0])
        print(f"{piece[1]}{piece[2]} : {a}")

def parse_single_image():
    piece = z1
    a = engine.parse_image(piece[0])
    print(f"{piece[1]}{piece[2]} : {a}")

def identify_tetromino():
    piece = j3
    image = cv2.imread(piece[0])
    match_res = engine.identify_tetromino(image)

options = {1 : engine.sample_video,
           2 : parse_images,
           3 : parse_single_image,
           4 : identify_tetromino,
           5 : engine.process_video,
           0 : invoke_exit
}

# Present an options menu to solicit the user's input
while True:
    prompt = """
_______________________________

----- CTWC Video Analyzer -----
_______________________________

Please input your command:

1) Sample video
2) Parse images
3) Parse single image
4) Identify tetromino
5) Process video
0) Exit

$Command me, baby> """
    choice = input(prompt)
    print()
    options[int(choice)]()
