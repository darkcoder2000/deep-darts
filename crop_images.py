import argparse
import multiprocessing as mp
from dataset.annotate import crop_board
import os
from pathlib import Path
import cv2
import pandas as pd


def crop(img_path, write_path, bbox, size=480, overwrite=False):
    #if osp.exists(write_path) and not overwrite:
    #replace using Path
    if Path(write_path).exists() and not overwrite:
        print(write_path, 'already exists')
        return

    os.makedirs(os.path.dirname(write_path), exist_ok=True)  # Create parent directory
    #bbox = [int(x) for x in bbox.strip("[]").split(",")]

    crop, _ = crop_board(img_path, bbox)
    if size != 'full':
        crop = cv2.resize(crop, (size, size))
    cv2.imwrite(write_path, crop)
    print('Wrote', write_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-lp', '--labels-path', default='dataset/labels.pkl')
    parser.add_argument('-ip', '--image-path', default='dataset/images')
    parser.add_argument('-s', '--size', nargs='+', default=['480'])
    args = parser.parse_args()

    for size in args.size:
        if size != 'full':
            size = int(size)

        data = pd.read_pickle(args.labels_path)

        read_prefix = args.image_path
        write_prefix = Path(Path(args.image_path).parent, 'cropped_images', str(size))

        print('Read path:', read_prefix)
        print('Write path:', write_prefix)

        img_paths = [str(Path(read_prefix, folder, name)) for (folder, name) in zip(data.img_folder, data.img_name)]
        write_paths = [str(Path(write_prefix, folder, name)) for (folder, name) in zip(data.img_folder, data.img_name)]
        bboxes = data.bbox.values
        sizes = [size for _ in range(len(bboxes))]

        p = mp.Pool(mp.cpu_count())
        p.starmap(crop, list(zip(img_paths, write_paths, bboxes, sizes)))

