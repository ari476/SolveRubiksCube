import numpy as np
from cv2 import cv2
import imutils
from draw_solution import *

# import time

font = cv2.FONT_HERSHEY_SIMPLEX


def detect_color(detect_img):
    """
    :param detect_img: piece from the cube
    :return the color of this piece
    """
    dict_all_color = dict.fromkeys(['red', 'yellow', 'orange', 'white', 'green', 'blue'], 0)
    hsv = cv2.cvtColor(detect_img, cv2.COLOR_BGR2HSV)

    masks_list = [cv2.inRange(hsv, np.array([45, 0, 50]), np.array([180, i, 255])) for i in range(1, 256)]
    dict_all_color['white'] += np.sum(masks_list)

    masks_list = [cv2.inRange(hsv, np.array([90, x, 0]), np.array([130, 255, 255])) for x in range(1, 256)]
    dict_all_color['blue'] += np.sum(masks_list)

    masks_list = [cv2.inRange(hsv, np.array([165, x, 0]), np.array([180, 255, 255])) for x in range(1, 256)]
    dict_all_color['red'] += np.sum(masks_list)

    masks_list = [cv2.inRange(hsv, np.array([0, x, 0]), np.array([5, 255, 255])) for x in range(1, 256)]
    dict_all_color['red'] += np.sum(masks_list)

    masks_list = [cv2.inRange(hsv, np.array([5, x, 50]), np.array([22, 255, 255])) for x in range(1, 256)]
    dict_all_color['orange'] += np.sum(masks_list)

    masks_list = [cv2.inRange(hsv, np.array([0, x, 0]), np.array([5, 255, 100])) for x in range(1, 256)]
    dict_all_color['orange'] += np.sum(masks_list)

    dict_all_color['white'] = round(dict_all_color['white'] / 255)
    dict_all_color['blue'] = round(dict_all_color['blue'] / 255)
    dict_all_color['red'] = round(dict_all_color['red'] / 255)
    dict_all_color['orange'] = round(dict_all_color['orange'] / 255)

    # detect yellow color
    lower_yellow, upper_yellow = np.array([22, 0, 0]), np.array([45, 255, 255])
    masks_list = cv2.inRange(hsv, lower_yellow, upper_yellow)
    dict_all_color['yellow'] += np.sum(masks_list)

    # detect green color
    lower_green, upper_green = np.array([35, 25, 25]), np.array([88, 255, 255])
    masks_list = cv2.inRange(hsv, lower_green, upper_green)
    dict_all_color['green'] += np.sum(masks_list)

    # for color in dict_all_color:
    #     dict_all_color[color] = round(dict_all_color[color] / 255)
    # print(dict_all_color, end="\n")
    # print(max(dict_all_color, key=dict_all_color.get))
    return max(dict_all_color, key=dict_all_color.get)


def draw_rectangle_center(frame):
    """
    :param frame: frame to crop the image
    :return: draw rectangle to scan and return the crop img (pixels)
    """
    # Draws a rectangle to scan the cube and returns the pixels of the current scan
    length_diagonal = 100  # from center of frame to corner of rectangle
    height, width = frame.shape[:2]
    cv2.rectangle(frame,
                  pt1=(int(width / 2 - length_diagonal), int(height / 2 - length_diagonal)),
                  pt2=(int(width / 2 + length_diagonal), int(height / 2 + length_diagonal)),
                  color=(0, 0, 0), thickness=2)

    return frame[int(height / 2 - length_diagonal):int(height / 2 + length_diagonal),
           int(width / 2 - length_diagonal):int(width / 2 + length_diagonal)]


def fill_color_by_location(frame, start_pos_width, start_pos_height, list_color=None):
    """
    :param frame: frame to draw the result
    :param start_pos_width: x - coordinates
    :param start_pos_height: y - coordinates
    :param list_color: all colors of current side
    :return: void - draw the result on frame
    """
    if list_color is None:
        list_color = ['gray'] * 9

    dict_name_to_color = {'red': (0, 0, 255), 'yellow': (0, 255, 255), 'orange': (0, 165, 255),
                          'white': (255, 255, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0),
                          'gray': (79, 69, 54)}

    length_square = 15
    difference_x_y = length_square + 5
    start_pos_height = int(start_pos_height)
    start_pos_width = int(start_pos_width)
    piece = 0

    for y in range(start_pos_height, start_pos_height + 3 * difference_x_y, difference_x_y):
        for x in range(start_pos_width, start_pos_width + 3 * difference_x_y, difference_x_y):
            cv2.rectangle(frame,
                          pt1=(x, y),
                          pt2=(x + length_square, y + length_square),
                          color=dict_name_to_color[list_color[piece]], thickness=-1)
            piece += 1


def draw_rectangles_right_bottom(frame, side, list_color=None):
    """
    :param frame: frame to draw the result
    :param side: side to draw in screen
    :param list_color: each side is made up of 9 piece of colors, list_color is all this colors
    :return: void - draw on the frame
    """
    blank_space = 5
    length_square = 15
    difference_x_y = length_square + blank_space
    height, width = frame.shape[:2]
    start_pos_left = width * 2 / 3, height * 3 / 4

    dict_start_pos_by_side = {'L': (start_pos_left[0], start_pos_left[1]),
                              'F': (start_pos_left[0] + 3 * difference_x_y + blank_space, start_pos_left[1]),
                              'R': (start_pos_left[0] + 6 * difference_x_y + 2 * blank_space, start_pos_left[1]),
                              'B': (start_pos_left[0] + 9 * difference_x_y + 3 * blank_space, start_pos_left[1]),
                              'U': (start_pos_left[0] + 3 * difference_x_y + blank_space,
                                    start_pos_left[1] - (3 * difference_x_y + blank_space)),
                              'D': (start_pos_left[0] + 3 * difference_x_y + blank_space,
                                    start_pos_left[1] + 3 * difference_x_y + blank_space),
                              }

    start_pos_width = int(dict_start_pos_by_side[side][0])
    start_pos_height = int(dict_start_pos_by_side[side][1])
    fill_color_by_location(frame, start_pos_width, start_pos_height, list_color)


def put_text(frame, side):
    """
    :param frame: frame to put text on it
    :param side: the text is dependent by side param
    :return: void - draw on frame
    """
    dict_name_to_color = {'B': (0, 0, 255), 'L': (0, 255, 255), 'F': (0, 165, 255),
                          'R': (255, 255, 255), 'D': (0, 255, 0), 'U': (255, 0, 0), None: (0, 0, 0)}

    dict_text_side = {'R': "Show the white side facing the \n  camera and blue on top ",
                      'F': "Show the orange side facing the \n  camera and blue on top ",
                      'L': "Show the yellow side facing the \n  camera and blue on top ",
                      'B': "Show the red side facing the \n  camera and blue on top ",
                      'D': "Show the green side facing the \n  camera and orange on top ",
                      'U': "Show the blue side facing the \n  camera and red on top ", None: ""}

    for i in dict_text_side:
        dict_text_side[i] += "\n    and press enter to scan"

    if side is None:
        dict_text_side[None] = "press enter to solve the cube"

    y0, dy = 100, 40
    for i, line in enumerate(dict_text_side[side].split('\n')):
        y = y0 + i * dy
        cv2.putText(img=frame,
                    text=line,
                    org=(220, y),
                    fontFace=font, fontScale=1,
                    color=dict_name_to_color[side],
                    thickness=2)

    cv2.putText(img=frame,
                text="To rescan press r",
                org=(20, 35),
                fontFace=font, fontScale=1,
                color=(0, 0, 0), thickness=2)


def video_scan():
    """
    :return: all colors of each side in cube in dictionary
    """
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    width_frame = 900
    iterate = 0  # current side scan
    list_side = ['R', 'F', 'L', 'B', 'D', 'U', None]
    dict_side_colors = dict.fromkeys(list_side, None)

    # scan all side of cube
    while iterate <= 6:
        # open web camera
        while True:
            side = list_side[iterate]
            _, frame = cam.read()
            frame = imutils.resize(frame, width=width_frame)

            # Drawing the cubes in the figure below on the right in frame
            for s in dict_side_colors:
                if s is not None:
                    draw_rectangles_right_bottom(frame, s, dict_side_colors[s])

            all_pieces_pixels = []
            # Crop the image
            if side is not None:
                cropped_image = draw_rectangle_center(frame)
                height, _ = cropped_image.shape[:2]
                length = int(height / 3)
                # crop the crop image to nine pieces and save them in list
                for i in range(3):
                    for j in range(3):
                        all_pieces_pixels.append(
                            cropped_image[length * i: length * (i + 1), length * j: length * (j + 1)])

            # Identifies the colors of the sides and saves them in the list
            all_colors_pieces = []  # temp list to save the current colors of side
            k = cv2.waitKey(1)
            if k == 13:
                if side is not None:
                    # start = time.time()
                    for piece in all_pieces_pixels:
                        all_colors_pieces.append(detect_color(piece[12:-12, 12:-12]))
                    dict_side_colors[side] = all_colors_pieces
                    # print(time.time() - start)
                iterate += 1
                break

            # this for re-scanning
            elif (k == ord('r') or k == ord('R')) and iterate > 0:
                iterate -= 1
                side = list_side[iterate]
                dict_side_colors[side] = None

            cv2.putText(img=frame,
                        text="scanned sides: " + str(iterate) + "/6",
                        org=(20, frame.shape[0] - 20),
                        fontFace=font, fontScale=1,
                        color=(0, 0, 0), thickness=2)

            put_text(frame, side)
            cv2.imshow('frame', frame)

    cam.release()
    cv2.destroyAllWindows()
    return dict_side_colors


dict_all_side_colors = video_scan()
draw_solution(dict_all_side_colors)
