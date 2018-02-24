"""Starter"""
import cv2
import numpy as np

import time
import random

import adb_utils
import img_proc


def main():
    """Main function"""
    i = 0
    while True:
        out = adb_utils.adb_sc()  # screenshots
        if out:
            print("Wait...")
            # platform_position = 0
            img, edge_img = img_proc.edge_detection()

        avatar_position, top_left, bottom_right = img_proc.find_avatar(img, edge_img)
        if avatar_position:
            if avatar_position[1] < img.shape[1] / 2:
                # if avatar on the left, scanning right
                platform_position = img_proc.find_platform(img, edge_img, left=avatar_position[1] + img.shape[1] * 0.045)
            else:
                # if avatar on the right, scanning left
                platform_position = img_proc.find_platform(img, edge_img, right=avatar_position[1] - img.shape[1] * 0.045)

            img[avatar_position[0], avatar_position[1]] = (255, 0, 0)
            img[platform_position[0], platform_position[1]] = (225, 0, 0)
            img[top_left[0], top_left[1]] = (0, 255, 0)  # green
            img[bottom_right[0], bottom_right[1]] = (0, 0, 255)  # red
            # mark the position in the image
            cv2.imwrite('images/center_{}.png'.format(i), img)
            i += 1
            dis = np.sqrt((avatar_position[0] - platform_position[0]) ** 2 + (avatar_position[1] - platform_position[1]) ** 2)
            adb_utils.adb_touch(int(1.33 * dis))
            time.sleep(random.uniform(1.0, 1.2))


if __name__ == '__main__':
    main()
