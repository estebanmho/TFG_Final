import mouse

import pyautogui


class ActionController (object):


    '''def __init__(self):
        self.screenWidth, self.screenHeight = ptg.size()'''

    def click(self):
        mouse.click()

    def right_click(self):
        mouse.right_click()

    def move(self, coord_current, coord_previous):
        coord_x = int(coord_current[0]) - int(coord_previous[0])
        if abs(coord_x) < 20:
            coord_x = 0
        elif abs(coord_x) > 170:
            coord_x = 170
        coord_y = int(coord_current[1]) - int(coord_previous[1])
        if abs(coord_y) < 20:
            coord_y = 0
        elif abs(coord_y) > 170:
            coord_y = 170
        if coord_y == 0 and coord_x == 0:
            return
        '''coord = numpy.array([coord_x, coord_y])
        normalized_v = coord / np.sqrt(np.sum(coord ** 2))'''
        mouse.move(-coord_x*2.1, coord_y*2.1, absolute=False, duration=0.1)

    def wheel(self,  coord_current, coord_previous):
        if abs(coord_previous[1] - coord_current[1]) > 20:

            if coord_previous[1] < coord_current[1]:
                delta = 1
            else:
                delta = -1
            mouse.wheel(delta)

    def zoom_in(self):
        pyautogui.hotkey('ctrl', 'add')

    def zoom_out(self):
        pyautogui.hotkey('ctrl', 'subtract')

    list_functions = [move, None, click, right_click, zoom_in, zoom_out, wheel]

    def take_action(self, action_number, coord=[1, 1], coord_previous=[1, 1]):
        funcion_actual = self.list_functions[action_number]
        if action_number in [0, 6]:
            funcion_actual(self, coord, coord_previous)

        else:
            funcion_actual(self)



