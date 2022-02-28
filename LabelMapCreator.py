# LabelMapCreator.py

import os
import sys
import traceback

class LabelMapCreator:

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
        print("{} {}".format(i, label))
        DISPLAY = "  display_name: "
        ID      = "  id: " 
        NAME    = "  name: "
        line = "item {" + NL + DISPLAY + label + NL  + ID  + str(i+1) + NL + NAME + label + NL + "}"  + NL
        f.write(line)
    
if __name__ == "__main__":
  classes_file = "./classes.txt"
  label_map_pbtxt = "./label_map.pbtxt"
  try:
    if os.path.exists(classes_file) == False:
      raise Exception("Not found "+ images_dir)
    bb = LabelMapCreator(classes_file)
    bb.create(label_map_pbtxt)
    #bb.run(images_dir, output_dir)
    
  except:
    traceback.print_exc()

