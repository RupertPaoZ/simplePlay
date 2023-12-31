import numpy as np
import cv2 as cv
import argparse
import os

def get_arucos(tag_num: int, tag_size: int, white=False):
    assert tag_size > 0
    _aruco_collector = []
    dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_50)
    for i in range(tag_num):
        if white:
            white_batch = tag_size // 8 * 10
            white_width = white_batch // 8
            markerImage = np.zeros((white_batch, white_batch), dtype=np.uint8)
            markerImage[white_width:tag_size+white_width, white_width:tag_size+white_width] = 255
            markerImage = markerImage.reshape((white_batch,white_batch,1))
            markerImage = np.tile(markerImage, (1,1,3))
            _aruco_collector.append(markerImage)
        else:
            white_batch = tag_size // 8 * 10
            white_width = white_batch // 8
            markerImage = np.ones((white_batch, white_batch), dtype=np.uint8)*255
            markerImage[white_width:tag_size+white_width, white_width:tag_size+white_width] = \
                cv.aruco.generateImageMarker(dictionary, i, tag_size, markerImage, 1)
            markerImage = markerImage.reshape((white_batch,white_batch,1))
            markerImage = np.tile(markerImage, (1,1,3))
            _aruco_collector.append(markerImage)
    return _aruco_collector

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pattern_root', type=str, default='')
    parser.add_argument('--save_root', type=str, default='')
    parser.add_argument('--pattern_num', type=int, default=1)
    parser.add_argument('--frame_num', type=int, default=1)
    parser.add_argument('--tag_size', type=int, default=80)
    parser.add_argument('--width', type=int, default=1024)
    parser.add_argument('--height', type=int, default=1080)
    

    args = parser.parse_args()
    
    pattern_root = args.pattern_root
    save_root = args.save_root
    pattern_num = args.pattern_num
    frame_num = args.frame_num
    tag_size = args.tag_size
    width = args.width
    height = args.height

    os.makedirs(save_root, exist_ok=True)

    fourcc = cv.VideoWriter_fourcc(*'H264')    
    out = cv.VideoWriter(f'{save_root}/patterns_video.mp4', fourcc, 240.0, (width, height), True)

    # artag
    tag_num = 2
    aruco_collector = get_arucos(tag_num, tag_size, white=False)
    white_batch = aruco_collector[0].shape[0]
    up = height - white_batch
    left = [256, width-white_batch-256]

    # font format for timestamp
    font = cv.FONT_HERSHEY_SIMPLEX
    org = (width//2 - white_batch//2, height - white_batch//4)
    fontScale = 1
    color = (255, 255, 255)
    thickness = 1

    # pos calibration
    for i in range(tag_num):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        pattern = cv.imread(f'{pattern_root}/{i}.png', 6)
        h, w, _ = pattern.shape
        frame[up:up+white_batch, left[i%tag_num]:left[i%tag_num]+white_batch] = aruco_collector[i%tag_num]
        cv.imwrite(f'{save_root}/T_{i}.png', frame)

    # brightness calibration
    aruco_collector = get_arucos(tag_num, tag_size, white=True)
    for i in range(tag_num):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        pattern = cv.imread(f'{pattern_root}/{i}.png', 6)
        h, w, _ = pattern.shape
        frame[up:up+white_batch, left[i%tag_num]:left[i%tag_num]+white_batch] = aruco_collector[i%tag_num]
        cv.imwrite(f'{save_root}/white_{i}.png', frame)
    cv.imwrite(f'{save_root}/black.png', np.zeros_like(frame))

    # gen video
    aruco_collector = get_arucos(tag_num, tag_size, white=True)
    for _ in range(frame_num):
        for i in range(pattern_num):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            pattern = cv.imread(f'{pattern_root}/{i}.png', 6)
            h, w, _ = pattern.shape
            delta_x0 = (width - w)//2
            frame[:h, delta_x0:w+delta_x0] = pattern
            frame[-white_batch:] = 0
            frame[up:up+white_batch, left[i%tag_num]:left[i%tag_num]+white_batch] = aruco_collector[i%tag_num]
            if i==0:
                # frame = cv.putText(frame, f'{i}', org, font, fontScale, color, thickness)
                frame[height-white_batch//4:, width//2-white_batch//8:width//2+white_batch//8] = (255,255,255)
            out.write(frame)
    out.release()