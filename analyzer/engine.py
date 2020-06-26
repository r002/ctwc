import cv2
import os
import numpy as np
from .vars import Vars as v
import sys

class Engine(object):

    # Load our known templates
    template_root = "C:/code/ctwc/analyzer/templates"

    i_template = cv2.imread(f"{template_root}/i-template.jpg", 0), v.i
    j_template = cv2.imread(f"{template_root}/j-template.jpg", 0), v.j
    l_template = cv2.imread(f"{template_root}/l-template.jpg", 0), v.l
    o_template = cv2.imread(f"{template_root}/o-template.jpg", 0), v.o
    s_template = cv2.imread(f"{template_root}/s-template.jpg", 0), v.s
    t_template = cv2.imread(f"{template_root}/t-template.jpg", 0), v.t
    z_template = cv2.imread(f"{template_root}/z-template.jpg", 0), v.z

    templates = i_template, j_template, l_template, o_template, s_template, \
                t_template, z_template

    video_source = "C:/code/ctwc/analyzer/part01.mp4"
    output_dir = "C:/code/ctwc/analyzer/frames"

    # Initialize the internal representation of the game board
    d = np.zeros((20,10))

    ## Accepts a video frame image and extracts Jeff's gameboard (upper left).
    ## Extracts the "board state" from the screenshot.
    @staticmethod
    def extract_board(image):
        # board = image[10:500, 710:910]  # Include name
        board = image[14:432, 716:928]    # Only the board

        # cv2.imshow(f"Testing board", board)
        # cv2.waitKey(0)

        x_start=716
        y_start=14
        b_width=21
        b_height=21

        # Iterate through the entire board to capture the state
        for y in range(20):
            for x in range(10):
                x1=x_start+x*b_width
                x2=x_start+(x+1)*b_width
                y1=y_start+y*b_height
                y2=y_start+(y+1)*b_height
                # print(f"{x1}, {x2} | {y1}, {y2}")
                square = image[y1:y2, x1:x2]
                m = int(np.mean(square))
                # print(f"\t m{x} val: {m}\n")
                Engine.d[y][x] = m
                # cv2.imshow(f"Testing square", square)
                # cv2.waitKey(0)

        # print(f"***internal board state:\n{Engine.d}", end="\r")
        print(f"{Engine.d}")

        sys.stdout.write('\x1b[1A'*21)  # Move cursor back up 21 lines

        # sys.stdout.flush()


        # x=0
        # y=0
        # x1=14+x*21
        # x2=14+(x+1)*21
        # y1=716+y*20
        # y2=716+(y+1)*20
        # # print(f"{x1}, {x2} | {y1}, {y2}")
        # square = image[x1:x2, y1:y2]
        # m = np.mean(square)
        # print(f"*** mean: {m}")
        # # print(f"***square mean: {np.mean(square)} | sum: {sum(square)}")
        # # pixel = image[x1, y1]
        # # print(f"***pixel: {pixel} | sum: {sum(pixel)}")
        # cv2.imshow(f"Testing square", square)

        # cv2.imshow(f"Testing extract_board", board)
        # cv2.waitKey(0)

    ## Match against our known templates to identify the tetromino
    @staticmethod
    def identify_tetromino(image):
        next_box = image[208:283, 615:703]  # These are the coordinates of the 'Next Box'

        # Enlarge the image
        scale_percent = 450
        width = int(next_box.shape[1] * scale_percent / 100)
        height = int(next_box.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_next_box = cv2.resize(next_box, dim, interpolation = cv2.INTER_AREA)
        next_box_gray = cv2.cvtColor(resized_next_box, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(next_box_gray, 20, 255, cv2.THRESH_BINARY_INV)

        # Now match the threshold of the Next Piece against our known templates.
        # Are there any matches?
        champ = None, 0
        for template in Engine.templates:
            res = cv2.matchTemplate(threshold, template[0], cv2.TM_CCOEFF_NORMED)
            print(f"Match % against {template[1]}: {res}")
            if res > champ[1]:
                champ = template[1], res
        print(f"\nMatch: {champ[0]} - {champ[1]}\n\n")


    ## This method analyzes a video and identifies what tetromino appears in
    ## the Next Box
    @staticmethod
    def process_video():
        vidcap = cv2.VideoCapture(Engine.video_source)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, 132000) # skip to the 2:12 mark (Start of first game)

        frame_no = 1
        success = True
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        print(f"fps: {fps}")

        while success:
            success, image = vidcap.read()
            # if count % (10 * fps) == 0:

            seconds = int(frame_no / fps)
            # cv2.imwrite(f"{Engine.output_dir}/f-{count}__{seconds}-secs.jpg", image)
            # print(f"successfully written {count}th frame at {seconds} seconds")

            # Run method to analyze the frame we just captured.
            # 1. What Tetris piece was just dropped?

            # os.system('cls')  # Will clear the entire console screen (Windows)

            print(f"Frame no: {frame_no}")  # UNCOMMENT to print frame no
            Engine.extract_board(image)


            # Engine.identify_tetromino(image)  # UNCOMMENT to Parse the next box

            # cv2.imshow(f"Frame no: {frame_no} | Seconds: {seconds}", image)
            # cv2.imshow(f"Frame no: x | Seconds: {seconds}", image)
            # cv2.waitKey(0)

             # 2. What is the current score?
             # TO-DO

            frame_no += 1

            # if success:
                # cv2.imwrite("C:/code/ctwc/analyzer/frame50sec.jpg", image)     # save frame as JPEG file
                # cv2.imshow("20sec", image)
                # cv2.waitKey(0)

    ## This method parses a single inputted frame to ascertain the next
    ## piece that is about to be dropped.
    @staticmethod
    def parse_image(src_img):
        image = cv2.imread(src_img)
        next_box = image[208:283, 615:703]  # These are the coordinates of the 'Next Box'

        # Enlarge the image
        scale_percent = 450
        width = int(next_box.shape[1] * scale_percent / 100)
        height = int(next_box.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_next_box = cv2.resize(next_box, dim, interpolation = cv2.INTER_AREA)

        next_box_gray = cv2.cvtColor(resized_next_box, cv2.COLOR_BGR2GRAY)

        _, threshold = cv2.threshold(next_box_gray, 20, 255, cv2.THRESH_BINARY_INV)

        ## Temp code to extract templates
        # output_dir = "C:/code/ctwc/analyzer/templates"
        # cv2.imwrite(f"{output_dir}/z-template.jpg", threshold)

        _, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        a = []
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.045 * cv2.arcLength(cnt, True), True)
            cv2.drawContours(resized_next_box, [approx], 0, (0, 0, 255), 2)
            # print(len(approx))
            a.append(len(approx))

        cv2.imshow('Next Box', resized_next_box)
        cv2.imshow('Threshold', threshold)
        cv2.waitKey(0)

        # edged = cv2.Canny(next_box, 30, 150)
        # cv2.imshow("Edged", edged)
        # cv2.waitKey(0)

        return a

    ## This method extracts a video frame every ten seconds and saves it
    ## to the /frames directory.
    @staticmethod
    def sample_video():  # video_source, output_dir
        vidcap = cv2.VideoCapture(Engine.video_source)
        count = 0
        success = True
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        print(f"fps: {fps}")

        while success:
            success, image = vidcap.read()
            # print('read a new frame: ', success)

            if count % (10 * fps) == 0:
                 seconds = int(count / fps)
                 cv2.imwrite(f"{Engine.output_dir}/f-{count}__{seconds}-secs.jpg", image)
                 print(f"successfully written {count}th frame at {seconds} seconds")

                 # Run method to analyze the frame we just captured.
                 # 1. What Tetris piece was just dropped?
                 # 2. What is the current score?

            count += 1
