##
## This is the Runner for the CTWC Video Analyzer
## Created: Sunday - Nov 10, 2019
##

from .engine import Engine

## Set the source and destination directories
video_source = "./part01.mp4"
output_dir = "./frames"

## Instantiate what we need to use
engine = Engine()

def invoke_exit():
    print("Bye! Have a great day!")
    exit()


options = {1 : engine.sample_video,
           2 : invoke_exit
}

# Present an options menu to solicit the user's input
while True:
    prompt = """
Please input your command:

1) Sample video
2) Exit

$> """
    choice = input(prompt)
    print()
    options[int(choice)]()
