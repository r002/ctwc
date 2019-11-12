import cv2
import os
import numpy as np

class Engine(object):

    # Load our known templates
    template_root = "C:/code/ctwc/analyzer/templates"
    i = "I-Shape"
    j = "J-Shape"
    l = "L-Shape"
    o = "O-Shape"
    s = "S-Shape"
    t = "T-Shape"
    z = "Z-Shape"

    i_template = cv2.imread(f"{template_root}/i-template.jpg", 0), i
    j_template = cv2.imread(f"{template_root}/j-template.jpg", 0), j
    l_template = cv2.imread(f"{template_root}/l-template.jpg", 0), l
    o_template = cv2.imread(f"{template_root}/o-template.jpg", 0), o
    s_template = cv2.imread(f"{template_root}/s-template.jpg", 0), s
    t_template = cv2.imread(f"{template_root}/t-template.jpg", 0), t
    z_template = cv2.imread(f"{template_root}/z-template.jpg", 0), z

    templates = i_template, j_template, l_template, o_template, s_template, \
                t_template, z_template

    # Match against our known templates to identify the tetromino
    @staticmethod
    def identify_tetromino(src_img):
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

        # Now match the threshold of the Next Piece against our known templates.
        # Are there any matches?
        champ = None, 0
        for template in Engine.templates:
            res = cv2.matchTemplate(threshold, template[0], cv2.TM_CCOEFF_NORMED)
            print(f"Match % against {template[1]}: {res}")
            if res > champ[1]:
                champ = template[1], res
        print(f"\nMatch: {champ[0]} - {champ[1]}")


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

        output_dir = "C:/code/ctwc/analyzer/templates"
        cv2.imwrite(f"{output_dir}/z-template.jpg", threshold)

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

    @staticmethod
    def sample_video():  # video_source, output_dir

        ## TO-DO: Parameterize this later and make them relative
        video_source = "C:/code/ctwc/analyzer/part01.mp4"
        output_dir = "C:/code/ctwc/analyzer/frames"

        vidcap = cv2.VideoCapture(video_source)
        count = 0
        success = True
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        print(f"fps: {fps}")

        while success:
            success, image = vidcap.read()
            # print('read a new frame: ', success)

            if count % (10 * fps) == 0:
                 seconds = int(count / fps)
                 cv2.imwrite(f"{output_dir}/f-{count}__{seconds}-secs.jpg", image)
                 print(f"successfully written {count}th frame at {seconds} seconds")

                 # Run method to analyze the frame we just captured.
                 # 1. What Tetris piece was just dropped?
                 # 2. What is the current score?

            count += 1







    # @staticmethod
    # def video_to_frames(video, path_output_dir):
    #     # extract frames from a video and save to directory as 'x.png' where
    #     # x is the frame index
    #     vidcap = cv2.VideoCapture(video)
    #     count = 0
    #     while vidcap.isOpened():
    #         success, image = vidcap.read()
    #         if success:
    #             cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, image)
    #             count += 1
    #         else:
    #             break
    #     cv2.destroyAllWindows()
    #     vidcap.release()
