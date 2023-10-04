import cv2
import imutils
import math
import numpy as np
from PIL import Image
from itertools import permutations
from pyzbar.pyzbar import decode


def combine_four():
    rotate("images/1-cropped.png")
    rotate("images/2-cropped.png")
    rotate("images/3-cropped.png")
    rotate("images/4-cropped.png")
    bound_image("rotated_1-cropped.png")
    bound_image("rotated_2-cropped.png")
    bound_image("rotated_3-cropped.png")
    bound_image("rotated_4-cropped.png")
    img1 = Image.open("bound_rotated_1-cropped.png")
    img2 = Image.open("bound_rotated_2-cropped.png")
    img3 = Image.open("bound_rotated_3-cropped.png")
    img4 = Image.open("bound_rotated_4-cropped.png")
    img_list = [img1, img2, img3, img4]
    p = permutations(img_list)
    for perm in p:
        # print(perm)
        try_all(perm)
    # try_one(img3, img4, img2, img1)


def rotate(image_name):
    img1 = cv2.imread(image_name)
    blur = cv2.GaussianBlur(img1, (3, 3), sigmaX=0, sigmaY=0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    (thresh, black_and_white) = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(black_and_white, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=20, minLineLength=5, maxLineGap=1)
    # print(lines)
    angles = np.empty(lines.shape[0])
    lengths_squared = np.empty(lines.shape[0])
    num_slopes = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # find slope of each line
        lengths_squared[num_slopes] = (x1 - x2) ** 2 + (y1 - y2) ** 2
        # checks if vertical
        if x1 - x2 == 0:
            angles[num_slopes] = 0
        # checks if horizontal
        elif y1 - y2 == 0:
            angles[num_slopes] = 0
        else:
            slope = max(-(y2 - y1) / (x2 - x1), (x2 - x1) / (y2 - y1))
            angle = abs(np.arctan(slope) * 180 / math.pi)
            if angle > 83:
                angles[num_slopes] = angle - 90
            else:
                angles[num_slopes] = angle
        num_slopes += 1
        # cv2.line(black_and_white, (x1, y1), (x2, y2), (0, 0, 255), 2)
    sorted_lengths_squared = np.array([x for _, x in sorted(zip(angles, lengths_squared))])
    angles = np.sort(angles)
    # print(angles)
    # print(sorted_lengths_squared)
    # remove first and last 10 percent
    five_percent = int(0.05 * angles.shape[0])
    avg_angle = np.dot(angles[five_percent: -five_percent],
                       sorted_lengths_squared[five_percent: -five_percent]) / np.sum(
        sorted_lengths_squared[five_percent: -five_percent])
    # print(np.sum(lengths_squared))
    # print(avg_angle)
    rotated_img1 = imutils.rotate(black_and_white, angle=-avg_angle)
    # cv2.imshow("Detected Lines", img1)
    # cv2.waitKey(2000)
    rotated_name = "rotated_" + image_name[7:]
    cv2.imwrite(rotated_name, rotated_img1)
    # cv2.imshow("Detected Lines", black_and_white)
    # cv2.waitKey(10)
    # cv2.imshow("Detected Lines", rotated_img1)
    # cv2.waitKey(10)


def bound_image(image_name):
    image = Image.open(image_name)
    image_box = image.getbbox()
    cropped = image.crop(image_box)
    cropped.save("bound_" + image_name)


def get_concat_h_resize(im1, im2, resample=Image.BICUBIC, resize_big_image=False):
    if im1.height == im2.height:
        _im1 = im1
        _im2 = im2
    elif (((im1.height > im2.height) and resize_big_image) or
          ((im1.height < im2.height) and not resize_big_image)):
        _im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((int(im2.width * im1.height / im2.height), im1.height), resample=resample)
    dst = Image.new('L', (_im1.width + _im2.width, _im1.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (_im1.width, 0))
    return dst


def get_concat_v_resize(im1, im2, resample=Image.BICUBIC, resize_big_image=False):
    if im1.width == im2.width:
        _im1 = im1
        _im2 = im2
    elif (((im1.width > im2.width) and resize_big_image) or
          ((im1.width < im2.width) and not resize_big_image)):
        _im1 = im1.resize((im2.width, int(im1.height * im2.width / im1.width)), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((im1.width, int(im2.height * im1.width / im2.width)), resample=resample)
    dst = Image.new('L', (_im1.width, _im1.height + _im2.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (0, _im1.height))
    return dst


def try_all(img_list):
    img1 = img_list[0]
    img2 = img_list[1]
    img3 = img_list[2]
    img4 = img_list[3]
    for a in range(4):
        img1 = img1.rotate(90, expand=True)
        for b in range(4):
            img2 = img2.rotate(90, expand=True)
            for c in range(4):
                img3 = img3.rotate(90, expand=True)
                for d in range(4):
                    img4 = img4.rotate(90, expand=True)
                    combined_img = get_concat_v_resize(get_concat_h_resize(img1, img2), get_concat_h_resize(img3, img4))
                    # combined_img.show()
                    decoded_objects = decode(combined_img)
                    if decoded_objects:
                        qr_code_contents = [obj.data.decode('utf-8') for obj in decoded_objects if obj.type == 'QRCODE']
                        return qr_code_contents
                    else:
                        return


def try_one(img1, img2, img3, img4):
    img2 = img2.rotate(180, expand=True)
    img3 = img3.rotate(90, expand=True)
    img4 = img4.rotate(180, expand=True)
    combined_img = get_concat_v_resize(get_concat_h_resize(img1, img2), get_concat_h_resize(img3, img4))
    for code in decode(combined_img):
        # print(code.data)
        all_possible_data.append(code.data.decode("utf-8"))
    combined_img.show()


# main method
all_possible_data = []
combine_four()
print("all possible QR codes:")
print(all_possible_data)