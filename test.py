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

def parse_bbox(bbox_str):
  return [int(x) for x in bbox_str.strip('[]').split(',')]

def parse_xy(xy_str):
  xy_list = []
  
  #remove first and last square brackets
  xy_str = xy_str[1:]
  xy_str = xy_str[:-1]
  
  length = len(xy_str)
  if length == 0:
    return xy_list

  #remove all white spaces
  xy_str = xy_str.replace(" ", "")

  outer_list = xy_str.strip('[]').split('],[')
  for inner_list in outer_list:
    inner_float_list = []
    for val in inner_list.strip('[]').split(','):
      inner_float_list.append(float(val.strip()))
    xy_list.append(inner_float_list)
  return xy_list

def convert_csv_to_pkl(csv_file_path):
     
    # Get the folder path and file name
    folder_path = Path(csv_file_path).parent
    file_name = getFileName(csv_file_path)

    # Load the data from the csv file
    file_path = str(Path(folder_path, file_name))
    data = pd.read_csv(file_path, converters={'bbox': parse_bbox, 'xy': parse_xy})

    # Save the data to a pickle file
    file_name = getFileNameWithoutExtension(file_name)
    file_path = str(Path(folder_path, file_name))
    data.to_pickle(f"{file_path}.pkl")

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

def draw_annotation(pkl_file_path, base_folder):

    annotations = pd.read_pickle(pkl_file_path)

    for index, annotation in annotations.iterrows():
        print(annotation)
        
        #check if entry annotation["img_folder"] exist
        if "img_folder" in annotation:            
          image_folder = str(Path(base_folder, annotation["img_folder"]))
        else:
          image_folder = base_folder
        image_path = Path(image_folder, annotation["img_name"])
        image = cv2.imread(str(image_path))

        xy_points = annotation["xy"]        
        # Draw the points with a width of 3 pixels
        image_height, image_width, _ = image.shape
        index = 1
        for point_values in xy_points:            
            x_rel, y_rel = point_values
            x_abs = int(x_rel * image_width)
            y_abs = int(y_rel * image_height)            
            cv2.circle(image, (x_abs, y_abs), 3, (255, 0, 0), -1)

            #draw index on image
            cv2.putText(image, str(index), (x_abs, y_abs), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            index += 1

        #save the image
        image_name = getFileNameWithoutExtension(image_path)
        image_path = str(Path(image_folder, image_name))
        cv2.imwrite(f"{image_path}_annotated.jpg", image)



if __name__ == '__main__':

    #convert_pkl_to_csv(r".\dataset\annotations\images\myimages2.pkl")
    #draw_annotation(r".\dataset\annotations\utrecht_01_02_2023.pkl", r".\test")
    #draw_annotation(r".\dataset\labels.pkl", r".\dataset\cropped_images\800")
    
    convert_csv_to_pkl(r".\dataset\annotations\images\myimages2.csv")
    #draw_annotation(r".\dataset\images\myimages\labels.pkl", r".\dataset\cropped_images\800")
   
    