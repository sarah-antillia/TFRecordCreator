# LabelMapCreator.py

import os
import sys
import traceback

class LabelMapYamlCreator:

  def __init__(self, classes_file):
    self.classes = []
    with open(classes_file, "r") as file:
      for i in file.read().splitlines():
        print(i)
        self.classes.append(i)  
    print(self.classes)
    
           
  def qt(self, label):
    line = "'" + label + "'"
    return line

  def create(self, label_map_pbtxt):
    NL = "\n"
    with open(label_map_pbtxt, "w") as f:
      for i in range(len(self.classes)):
        label   = self.classes[i]
        label   = self.qt(label)
        DISPLAY = "  display_name: "
        ID      = "  id: " 
        NAME    = "  name: "
        line = str(i+1) + ": " + label
        print(line)
        f.write(line + NL)
    
# python LabelMapCreator.py RoadSigns_v3_TFRecord 
if __name__ == "__main__":
  folder       = ""
  classes_file = "./classes.txt"
  label_map_pbtxt = "./label_map.yaml"
  output_dir     = ""
  try:
    if len(sys.argv) == 2:
      output_dir = sys.argv[1]
    else:
      raise Exception("Invalid argment ")

    classes_path = os.path.join(output_dir, classes_file)
    label_map_path = os.path.join(output_dir, label_map_pbtxt)
    if os.path.exists(output_dir) == False:
      os.makedirs(output_dir)
    if os.path.exists(classes_path) == False:
      raise Exception("Not found "+ classes_path)

    bb = LabelMapYamlCreator(classes_path)
    bb.create(label_map_path)
    #bb.run(images_dir, output_dir)
    
  except:
    traceback.print_exc()

