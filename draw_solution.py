from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

from point import Point
from twophase import solve

right_side_points = ()
up_side_points = ()
front_side_points = ()
canvas = None


def flat_list(ls):
    return [item for tup in ls for item in tup]


def create_string_to_solve(all_colors_of_sides):
    """
    :param all_colors_of_sides: dict of all colors per side
    :return: string that represent the cube in model that api need to solve the cube
    """
    dict_color_to_side = {'blue': 'U', 'red': 'B', 'yellow': 'L', 'orange': 'F', 'white': 'R', 'green': 'D'}
    # U1-U9, R1-R9, F1-F9, D1-D9, L1-L9, B1-B9
    list_side_colors = all_colors_of_sides['U'] + all_colors_of_sides['R'] + all_colors_of_sides['F'] + \
                       all_colors_of_sides['D'] + all_colors_of_sides['L'] + all_colors_of_sides['B']

    st_side_letters = ""
    for i in list_side_colors:
        st_side_letters += dict_color_to_side[i]
    return st_side_letters


def points_of_hor_lines(side_points):
    """
    :param side_points: side points to draw the horizontal lines
    :return: 2 lines that produce from 2 points
    """
    # side_points : 4 points from top left to bottom right
    horizontal_line1_start_point = Point(side_points[0].x + (side_points[3].x - side_points[0].x) / 3,
                                         side_points[0].y + (side_points[3].y - side_points[0].y) / 3)
    horizontal_line1_end_point = Point(side_points[1].x + (side_points[2].x - side_points[1].x) / 3,
                                       side_points[1].y + (side_points[2].y - side_points[1].y) / 3)

    horizontal_line2_start_point = Point(side_points[0].x + (side_points[3].x - side_points[0].x) * 2 / 3,
                                         side_points[0].y + (side_points[3].y - side_points[0].y) * 2 / 3)

    horizontal_line2_end_point = Point(side_points[1].x + (side_points[2].x - side_points[1].x) * 2 / 3,
                                       side_points[1].y + (side_points[2].y - side_points[1].y) * 2 / 3)
    line1 = tuple(horizontal_line1_start_point) + tuple(horizontal_line1_end_point)
    line2 = tuple(horizontal_line2_start_point) + tuple(horizontal_line2_end_point)
    return line1, line2


def points_of_ver_lines(side_points):
    """
    :param side_points: side points to draw the vertical lines
    :return: 2 lines that produce from 2 points
    """
    # side_points : 4 points from top left to bottom right
    vertical_line1_start_point = Point(side_points[0].x + (side_points[1].x - side_points[0].x) / 3,
                                       side_points[0].y + (side_points[1].y - side_points[0].y) / 3)

    vertical_line1_end_point = Point(side_points[3].x + (side_points[2].x - side_points[3].x) / 3,
                                     side_points[3].y + (side_points[2].y - side_points[3].y) / 3)

    vertical_line2_start_point = Point(side_points[0].x + (side_points[1].x - side_points[0].x) * 2 / 3,
                                       side_points[0].y + (side_points[1].y - side_points[0].y) * 2 / 3)

    vertical_line2_end_point = Point(side_points[3].x + (side_points[2].x - side_points[3].x) * 2 / 3,
                                     side_points[3].y + (side_points[2].y - side_points[3].y) * 2 / 3)

    line1 = tuple(vertical_line1_start_point) + tuple(vertical_line1_end_point)
    line2 = tuple(vertical_line2_start_point) + tuple(vertical_line2_end_point)
    return line1, line2


def draw_side_and_lines(side_points):
    """
    :param side_points: specific side point of cube model
    :return: draw on canvas the side and the lines (like #) on the side
    """
    flat_ls = flat_list(side_points)
    points_line1_hor, points_line2_hor = points_of_hor_lines(side_points)
    points_line1_ver, points_line2_ver = points_of_ver_lines(side_points)

    # polygon side draw
    canvas.create_polygon(flat_ls, fill="white", outline='black', width=4)
    # Horizontal lines
    canvas.create_line(points_line1_hor, fill="black", width=4)
    canvas.create_line(points_line2_hor, fill="black", width=4)
    # Vertical lines
    canvas.create_line(points_line1_ver, fill="black", width=4)
    canvas.create_line(points_line2_ver, fill="black", width=4)


def padding(ls_points):
    """
    :param ls_points: list of points to decrease with padding one pixel
    :return: new list of points after padding
    """
    p = 1  # padding
    ls_pad = [p, p, -p, p, -p, -p, p, -p]
    zipped_lists = zip(ls_points, ls_pad)
    padding_ls = [x + y for (x, y) in zipped_lists]
    return padding_ls


def list_16_points_by_side(side_points):
    """
    :param side_points: side points of specific side
    :return: all 16 points that are on this side
    """
    points_line1_hor, points_line2_hor = points_of_hor_lines(side_points)
    points_line1_ver, points_line2_ver = points_of_ver_lines(side_points)
    point5 = ((points_line1_ver[2] + points_line1_ver[0] * 2) / 3, (points_line1_ver[3] + points_line1_ver[1] * 2) / 3)
    point6 = ((points_line2_ver[2] + points_line2_ver[0] * 2) / 3, (points_line2_ver[3] + points_line2_ver[1] * 2) / 3)
    point9 = ((points_line1_ver[2] * 2 + points_line1_ver[0]) / 3, (points_line1_ver[3] * 2 + points_line1_ver[1]) / 3)
    point10 = ((points_line2_ver[2] * 2 + points_line2_ver[0]) / 3, (points_line2_ver[3] * 2 + points_line2_ver[1]) / 3)

    list_16_points = [side_points[0].unpack(), points_line1_ver[:2], points_line2_ver[:2], side_points[1].unpack(),
                      points_line1_hor[:2], point5, point6, points_line1_hor[2:], points_line2_hor[:2], point9, point10,
                      points_line2_hor[2:], side_points[3].unpack(), points_line1_ver[2:], points_line2_ver[2:],
                      side_points[2].unpack()]
    return list_16_points


def fill_side_with_color(side_points, ls_side_color):
    """
    :param side_points: specific side point of cube model
    :param ls_side_color: list of color from top left to bottom right of side
    :return: fill the side with color on canvas according to the ls_side_color
    """
    list_16_points = list_16_points_by_side(side_points)
    for i in range(9):
        x = i + int(i / 3)
        ls = list_16_points[x] + list_16_points[x + 1] + list_16_points[x + 5] + list_16_points[x + 4]
        canvas.create_polygon(padding(ls), fill=ls_side_color[i], width=1)


def put_text_with_space_line(text, x, y, dy):
    """
    :param text: text to write on canvas
    :param x: x location to start write the text
    :param y: y location to start write the text
    :param dy: the diff between line of text in pixels
    :return: write the text on canvas
    """
    y0 = y
    for i, line in enumerate(text.split('\n')):
        y = y0 + i * dy
        canvas.create_text(x, y, fill='navy', font=('Helvetica', '15', 'bold'), anchor="nw", text=line)


def draw_solution(dict_side_colors=None):
    """
    :param dict_side_colors: dictionary of all colors of each side in cube
    :return: draw steps of solution
    """
    global front_side_points, up_side_points, right_side_points, canvas

    root = Tk()
    root.title('Solution')
    ico = Image.open('image.jpg')
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)
    root.state('zoomed')
    root.update()
    canvas = Canvas(root, height=root.winfo_height(), width=root.winfo_width(), bg="#C0C0C0")

    text = "U/D/F/B/R/L = turn Up / Down / Front / Back / Right \n/ Left clockwise (by the direction of the arrows)" \
           "\n\nU'/D'/F'/B'/R'/L' = turn Up / Down / Front / Back / \nRight / Left counterclockwise" \
           " (by the direction of\nthe arrows)\n\n" \
           "U2/D2/F2/B2/R2/L2 = turn Up / Down / Front / Back  \n/ Right / Left twice in the direction of the arrows"
    put_text_with_space_line(text, 5 * 205 + 20, 195 * 3, 20)

    # st_solution = 'F2 D'
    # st_solution = 'D ' * 24
    # st_solution += "Done!"

    st_represent_cube = create_string_to_solve(dict_side_colors)

    try:
        # solve is function from the api that output string represent the solution
        st_solution = solve(st_represent_cube)
    except ValueError as msg:
        messagebox.showinfo("Error", "Can't solve this cube - " + str(msg))
        return

    st_solution += ' Done!' if len(st_solution) > 0 else 'Done!'
    print(st_solution)

    # loop over the solution
    for num, move in enumerate(st_solution.split(' ')):
        x = (num % 7) * 205  # columns
        y = int(num / 7) * 195  # rows

        # all points to draw the cube model each one produce from 4 points
        # 4 points in origin of polygon
        front_side_points = [Point(60 + x, 60 + y), Point(140 + x, 90 + y), Point(140 + x, 190 + y),
                             Point(60 + x, 160 + y)]
        up_side_points = [Point(135 + x, 35 + y), Point(210 + x, 65 + y), Point(140 + x, 90 + y),
                          Point(60 + x, 60 + y)]
        right_side_points = [Point(140 + x, 90 + y), Point(210 + x, 65 + y), Point(210 + x, 160 + y),
                             Point(140 + x, 190 + y)]

        draw_side_and_lines(front_side_points)
        draw_side_and_lines(up_side_points)
        draw_side_and_lines(right_side_points)

        fill_side_with_color(front_side_points, dict_side_colors['F'])
        fill_side_with_color(up_side_points, dict_side_colors['U'])
        fill_side_with_color(right_side_points, dict_side_colors['R'])

        # draw the step number of solution
        text = str(num + 1) + ": " + move if move != 'Done!' else move
        canvas.create_text(up_side_points[3].x, (up_side_points[0].y - 5), fill='navy', text=text,
                           font=('Helvetica', '25', 'bold'))

        # draw 2x if need to rotate twice
        if len(move) > 1 and move[1] == "2":
            canvas.create_text(list_16_points_by_side(front_side_points)[5][0] + 13,
                               list_16_points_by_side(front_side_points)[5][1] + 20,
                               fill='navy', text="2x",
                               font=('Helvetica', '18', 'bold'))

        # not final step in solution
        if move != "Done!":
            draw_arrow(move)
            move_cube(dict_side_colors, move)
            draw_side_move(move[0])

    canvas.pack()
    root.mainloop()


def draw_arrow(move):
    """
    :param move: current move in solution
    :return: draw on canvas the direction of rotate according the move
    """

    def get_specific_points_by_specific_side(points, side):
        """
        :param points: 4 points of square that the triangle is blocked within it
        :param side: side to draw the arrow on it
        :return: draw arrow according the side and the points
        """
        ls_points_side = list_16_points_by_side(side)
        return ls_points_side[points[0]] + ls_points_side[points[1]] + \
               ls_points_side[points[2]] + ls_points_side[points[3]]

    def opposite_points(points):
        """
        :param points: 4 points of square that the triangle is blocked within it
        :return: 4 points in reverse order so that the triangle is exactly in the opposite direction
        """
        return points[3], points[2], points[1], points[0]

    # 4 points of square that the triangle is blocked within it
    dict_points_arrow = {"U": ((5, 1, 2, 6), (5, 1, 2, 6)),
                         "D": ((10, 14, 9, 13), (10, 14, 9, 13)),
                         "F": ((9, 8, 5, 4), (10, 14, 9, 13)),
                         "B": ((5, 1, 6, 2), (6, 7, 10, 11)),
                         "R": ((6, 7, 10, 11), (6, 7, 10, 11)),
                         "L": ((9, 8, 5, 4), (9, 8, 5, 4)),
                         }
    # 2 side to draw the triangle (arrow) according the move
    dict_side_to_draw = {'U': (right_side_points, front_side_points),
                         'D': (right_side_points, front_side_points),
                         'F': (right_side_points, up_side_points),
                         'B': (up_side_points, right_side_points),
                         'R': (up_side_points, front_side_points),
                         'L': (up_side_points, front_side_points)}

    side_move = move[0]
    if len(move) > 1 and move[1] == "'":
        arrow1 = get_specific_points_by_specific_side(opposite_points(dict_points_arrow[side_move][0]),
                                                      dict_side_to_draw[side_move][0])
        arrow2 = get_specific_points_by_specific_side(opposite_points(dict_points_arrow[side_move][1]),
                                                      dict_side_to_draw[side_move][1])
    else:
        arrow1 = get_specific_points_by_specific_side(dict_points_arrow[side_move][0], dict_side_to_draw[side_move][0])
        arrow2 = get_specific_points_by_specific_side(dict_points_arrow[side_move][1], dict_side_to_draw[side_move][1])

    draw_arrow_in_piece(arrow1)
    draw_arrow_in_piece(arrow2)


def draw_arrow_in_piece(ls_points):
    """
    :param ls_points: 4 points of square that the triangle is blocked within it
    :return: draw arrow in the square according the points
    """
    point1, point2, point3, point4 = Point(ls_points[0], ls_points[1]), Point(ls_points[2], ls_points[3]), \
                                     Point(ls_points[4], ls_points[5]), Point(ls_points[6], ls_points[7])

    # mid_point(head), left_corner_point, right_corner_point: mean endpoints of the triangle
    mid_point = ratio_div_point(point1, point2, 0.5)
    left_corner_point = ratio_div_point(point3, point1, 0.2)
    right_corner_point = ratio_div_point(point4, point2, 0.2)
    left_mid = ratio_div_point(left_corner_point, right_corner_point, 0.15)
    right_mid = ratio_div_point(right_corner_point, left_corner_point, 0.15)
    canvas.create_polygon(mid_point.unpack(), left_mid.unpack(), right_mid.unpack())


def ratio_div_point(p1, p2, r):
    """
    :param p1: point 1
    :param p2: point 2
    :param r: 0<=r<=1 ratio to finding a point between them (section formula)
    :return: point between them according to ratio
    """
    x = p1.x * (1 - r) + p2.x * r
    y = p1.y * (1 - r) + p2.y * r
    return Point(x, y)


def move_cube(dict_side_colors, move):
    """
    :param dict_side_colors: dictionary of all colors of each side in cube
    :param move: step move
    :return: change the dictionary according to move
    """
    if len(move) == 1:
        move_clockwise(dict_side_colors, move)
    elif len(move) == 2 and move[1] == '2':
        move_clockwise(dict_side_colors, move)
        move_clockwise(dict_side_colors, move)
    elif move[1] == "'":
        # move 1 counterclockwise = 3 times clockwise
        move_clockwise(dict_side_colors, move)
        move_clockwise(dict_side_colors, move)
        move_clockwise(dict_side_colors, move)


def move_clockwise(dict_side_colors, move):
    """
    :param dict_side_colors: dictionary of all colors of each side in cube
    :param move: step move
    :return: change the dictionary according to move
    """
    # change the dict by the move
    move = move[0]
    if move == 'U':
        dict_side_colors['L'][:3], dict_side_colors['B'][:3], dict_side_colors['R'][:3], dict_side_colors['F'][:3] = \
            dict_side_colors['F'][:3], dict_side_colors['L'][:3], dict_side_colors['B'][:3], dict_side_colors['R'][:3]

    elif move == 'D':
        dict_side_colors['L'][-3:], dict_side_colors['B'][-3:], dict_side_colors['R'][-3:], dict_side_colors['F'][-3:] = \
            dict_side_colors['B'][-3:], dict_side_colors['R'][-3:], dict_side_colors['F'][-3:], dict_side_colors['L'][
                                                                                                -3:]

    elif move == 'F':
        dict_side_colors['L'][2::3], dict_side_colors['U'][-3:], dict_side_colors['R'][::3], dict_side_colors['D'][:3] = \
            dict_side_colors['D'][:3], dict_side_colors['L'][-1::-3], dict_side_colors['U'][-3:], dict_side_colors['R'][
                                                                                                  -3::-3]

    elif move == 'B':
        dict_side_colors['L'][-3::-3], dict_side_colors['U'][:3], dict_side_colors['R'][-1::-3], dict_side_colors['D'][
                                                                                                 -3:] = \
            dict_side_colors['U'][:3], dict_side_colors['R'][2::3], dict_side_colors['D'][-3:], dict_side_colors['L'][
                                                                                                ::3]

    elif move == 'R':
        dict_side_colors['F'][2::3], dict_side_colors['U'][2::3], dict_side_colors['B'][::3], dict_side_colors['D'][
                                                                                              2::3] = \
            dict_side_colors['D'][2::3], dict_side_colors['F'][2::3], dict_side_colors['U'][-1::-3], dict_side_colors[
                                                                                                         'B'][-3::-3]

    elif move == 'L':
        dict_side_colors['F'][::3], dict_side_colors['U'][::3], dict_side_colors['B'][2::3], dict_side_colors['D'][
                                                                                             ::3] = \
            dict_side_colors['U'][::3], dict_side_colors['B'][-1::-3], dict_side_colors['D'][-3::-3], dict_side_colors[
                                                                                                          'F'][
                                                                                                      ::3]
    dict_side_colors[move][:3], dict_side_colors[move][3:6], dict_side_colors[move][6:] \
        = dict_side_colors[move][-3::-3], dict_side_colors[move][-2::-3], dict_side_colors[move][-1::-3]


def draw_side_move(move):
    """
    :param move: step move in solution
    :return: draw on canvas the part that needs to rotate in the cube
    """
    # each part produce form 6 lines
    dict_lines_move = {'U': [up_side_points[2].unpack() + up_side_points[3].unpack(),
                             points_of_hor_lines(front_side_points)[0],
                             points_of_hor_lines(right_side_points)[0],
                             up_side_points[1].unpack() + up_side_points[2].unpack(),
                             up_side_points[3].unpack() + points_of_hor_lines(front_side_points)[0][:2],
                             up_side_points[1].unpack() + points_of_hor_lines(right_side_points)[0][2:]],
                       'F': [points_of_hor_lines(up_side_points)[1],
                             points_of_ver_lines(right_side_points)[0],
                             up_side_points[2].unpack() + up_side_points[3].unpack(),
                             right_side_points[0].unpack() + right_side_points[3].unpack(),
                             up_side_points[3].unpack() + points_of_hor_lines(up_side_points)[1][:2],
                             right_side_points[3].unpack() + points_of_ver_lines(right_side_points)[0][2:]],
                       'B': [up_side_points[0].unpack() + up_side_points[1].unpack(),
                             right_side_points[1].unpack() + right_side_points[2].unpack(),
                             points_of_hor_lines(up_side_points)[0],
                             points_of_ver_lines(right_side_points)[1],
                             up_side_points[0].unpack() + points_of_hor_lines(up_side_points)[0][:2],
                             right_side_points[2].unpack() + points_of_ver_lines(right_side_points)[1][2:]],
                       'R': [front_side_points[1].unpack() + front_side_points[2].unpack(),
                             up_side_points[1].unpack() + up_side_points[2].unpack(),
                             points_of_ver_lines(up_side_points)[1],
                             points_of_ver_lines(front_side_points)[1],
                             front_side_points[2].unpack() + points_of_ver_lines(front_side_points)[1][2:],
                             up_side_points[1].unpack() + points_of_ver_lines(up_side_points)[1][:2]],
                       'D': [right_side_points[2].unpack() + right_side_points[3].unpack(),
                             front_side_points[2].unpack() + front_side_points[3].unpack(),
                             points_of_hor_lines(front_side_points)[1],
                             points_of_hor_lines(right_side_points)[1],
                             front_side_points[3].unpack() + points_of_hor_lines(front_side_points)[1][:2],
                             right_side_points[2].unpack() + points_of_hor_lines(right_side_points)[1][2:]],
                       'L': [front_side_points[0].unpack() + front_side_points[3].unpack(),
                             up_side_points[0].unpack() + up_side_points[3].unpack(),
                             points_of_ver_lines(up_side_points)[0],
                             points_of_ver_lines(front_side_points)[0],
                             front_side_points[3].unpack() + points_of_ver_lines(front_side_points)[0][2:],
                             up_side_points[0].unpack() + points_of_ver_lines(up_side_points)[0][:2]],
                       }

    for line in dict_lines_move[move[0]]:
        canvas.create_line(line, fill="#606060", width=4)
