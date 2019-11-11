import cv2
import os

class Engine(object):

    @staticmethod
    def video_to_frames(video, path_output_dir):
        # extract frames from a video and save to directory as 'x.png' where
        # x is the frame index
        vidcap = cv2.VideoCapture(video)
        count = 0
        while vidcap.isOpened():
            success, image = vidcap.read()
            if success:
                cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, image)
                count += 1
            else:
                break
        cv2.destroyAllWindows()
        vidcap.release()

    ## This converts the video into frames
    # video_to_frames(video_source, output_dir)

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
                 cv2.imwrite(f"{output_dir}/frame-{count}__{seconds}-secs.jpg", image)
                 print(f"successfully written {count}th frame at {seconds} seconds")

                 # Run method to analyze the frame we just captured.
                 # 1. What Tetris piece was just dropped?
                 # 2. What is the current score?

            count += 1
