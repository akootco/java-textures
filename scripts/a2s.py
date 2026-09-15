import cv2
import numpy as np

# Conversion instructions (x, y, w, h) - Used by alex_to_steve_stretch
CI = [
    [55, 16, 1, 32],  # right arm, last column, back
    [51, 16, 1, 4],  # right arm, last column, bottom, main layer
    [51, 32, 1, 4],  # right arm, last column, bottom, second layer
    [47, 16, 8, 32],  # right arm, big middle region
    [63, 48, 1, 16],  # left arm, last column, back, second layer
    [59, 48, 1, 4],  # left arm, last column, bottom, second layer
    [55, 48, 8, 16],  # left arm, big middle region, second layer
    [47, 48, 1, 16],  # left arm, last column, back, main layer
    [43, 48, 1, 4],  # left arm, last column, bottom, main layer
    [39, 48, 8, 16]  # left arm, big middle region, main layer
]

# Arm FBLR and TB regions (x, y, w, h) - Used by is_steve
FBLR = [
    [40, 20, 16, 12],  # right arm, main layer
    [40, 36, 16, 12],  # right arm, second layer
    [32, 52, 16, 12],  # left arm, main layer
    [48, 52, 16, 12]  # left arm, second layer
]

TB = [
    [44, 16, 8, 4],  # right arm, main layer
    [44, 32, 8, 4],  # right arm, second layer
    [36, 48, 8, 4],  # left arm, main layer
    [52, 48, 8, 4]  # left arm, second layer
]


class SkinConverter:
    def __init__(self):
        self._image = None

    def _get_ratio_to_base(self):
        h, w, c = self._image.shape
        return w / 64

    def _ratio_adjust(self, arr, ratio=-1):
        if ratio < 0:
            ratio = self._get_ratio_to_base()
        return list(map(lambda r: list(map(lambda e: e * ratio, r)), arr))

    def _clear_rect(self, x, y, w, h):
        x, y, w, h = int(x), int(y), int(w), int(h)
        self._image[y:y + h, x:x + w, :] = [0] * self._image.shape[2]

    def _draw_image(self, source_image, sx, sy, sw, sh, dx, dy, dw, dh, flip_horizontal=False):
        sx, sy, sw, sh, dx, dy, dw, dh = int(sx), int(sy), int(sw), int(sh), int(dx), int(dy), int(dw), int(dh)
        roi = source_image[sy:sy + sh, sx:sx + sw]
        resized_roi = cv2.resize(roi, (dw, dh), interpolation=cv2.INTER_AREA)
        if flip_horizontal:
            resized_roi = cv2.flip(resized_roi, 1)
        self._image[dy:dy + dh, dx:dx + dw] = resized_roi

    def _move_rect(self, sx, sy, sw, sh, x, y, w=-1, h=-1, copy_mode=False, flip_horizontal=False):
        old_image = self._image.copy()
        if not copy_mode:
            self._clear_rect(sx, sy, sw, sh)
        w = sw if w < 0 else w
        h = sh if h < 0 else h
        self._draw_image(old_image, sx, sy, sw, sh, x, y, w, h, flip_horizontal=flip_horizontal)

    def _shift_rect(self, x, y, w, h, pixels_to_move, copy_mode=False):
        self._move_rect(x, y, w, h, x + pixels_to_move, y, -1, -1, copy_mode)

    def _is_empty_rect(self, x, y, w, h):
        x, y, w, h = int(x), int(y), int(w), int(h)
        return np.mean(self._image[y:y + h, x:x + w, 3]) == 0

    def _common_shift(self, ins, dx, dw, pixels_to_move, copy_mode=False, reverse_order=False):
        if reverse_order:
            ins = ins[::-1]
        for v in ins:
            self._shift_rect(v[0] + dx, v[1], v[2] + dw, v[3], pixels_to_move, copy_mode)

    def set_image(self, image):
        self._image = image

    def get_image(self):
        return self._image.copy()

    def load_from_file(self, file_path):
        self.set_image(cv2.imread(file_path, cv2.IMREAD_UNCHANGED))

    def save_to_file(self, file_path):
        cv2.imwrite(file_path, self.get_image())

    def is_steve(self):
        ratio = self._get_ratio_to_base()
        for v in self._ratio_adjust(FBLR + TB, ratio):
            if not self._is_empty_rect(v[0] + v[2] - ratio, v[1], ratio, v[3]):
                return True
        return False

    def alex_to_steve_stretch(self):
        ratio = self._get_ratio_to_base()
        self._common_shift(CI, -2 * ratio, ratio, ratio, True, True)