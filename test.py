import cv2
import pandas as pd
from pathlib import Path
from helper import getFileName, getFileNameWithoutExtension

def convert_pkl_to_csv(pkl_file_path):

    # Get the folder path and file name
    folder_path = Path(pkl_file_path).parent
    file_name = getFileName(pkl_file_path)

    # Load the data from the pickle file
    file_path = str(Path(folder_path, file_name))
    data = pd.read_pickle(file_path)

    # Save the data to a csv file
    file_name = getFileNameWithoutExtension(file_name)
    file_path = str(Path(folder_path, file_name))
    data.to_csv(f"{file_path}.csv")

def convert_to_absolute(image, annotations):

  # Get image height and width
  image_height, image_width, _ = image.shape

  # Parse the annotations list
  new_annotations = []
  for annotation in annotations:
    new_annotation = annotation.copy()
    xy_points = annotation[3]

    # Convert each relative xy point to absolute pixel value
    absolute_points = []
    for point in xy_points:
      point_values = [float(x) for x in point.strip("[]").split(",")]
      x_rel, y_rel = point_values
      x_abs = int(x_rel * image_width)
      y_abs = int(y_rel * image_height)
      absolute_points.append([x_abs, y_abs])

    # Update the xy points in the annotation with absolute values
    new_annotation[3] = absolute_points
    new_annotations.append(new_annotation)

  return new_annotations

def draw_annotation(pkl_file_path, image_folder):

    annotations = pd.read_pickle(pkl_file_path)
    print(annotations)

    for index, annotation in annotations.iterrows():
        print(annotation)
          
        image_path = Path(image_folder, annotation[0])
        image = cv2.imread(str(image_path))

        # Get the bounding box annotation (assuming format "[xmin, ymin, xmax, ymax]")        
        bbox_values = annotation[1]
        xmin, ymin, xmax, ymax = bbox_values

        # Draw the bounding box for the dartboard
        #cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)

        # Parse the xy points
        xy_points = annotation[2]
        
        # Draw the points with a width of 3 pixels
        image_height, image_width, _ = image.shape
        for point_values in xy_points:            
            x_rel, y_rel = point_values
            x_abs = int(x_rel * image_width)
            y_abs = int(y_rel * image_height)            
            cv2.circle(image, (x_abs, y_abs), 3, (255, 0, 0), -1)

        #save the image
        image_name = getFileNameWithoutExtension(image_path)
        image_path = str(Path(image_folder, image_name))
        cv2.imwrite(f"{image_path}_annotated.jpg", image)


if __name__ == '__main__':

    #convert_pkl_to_csv(r".\dataset\annotations\utrecht_01_02_2023.pkl")
    draw_annotation(r".\dataset\annotations\utrecht_01_02_2023.pkl", r".\data\test")
    