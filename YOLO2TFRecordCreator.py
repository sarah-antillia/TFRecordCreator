# 
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# YOLO2TFRecordCreator.py
# 
# 2021/11/08  sarah antillia.com

import os
import sys

import dataset_util

from PIL import Image
import tensorflow.compat.v1 as tf
import glob
import io
import argparse
import traceback

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  


class YOLO2TFRecordCreator:

  def __init__(self, images_dir, yolo_anno_dir, output_dir, 
               dataset="train", filename="foo.tfrecord"):
               
    self.images_dir    = images_dir
    self.yolo_anno_dir = yolo_anno_dir
    self.output_dir    = output_dir    #tfrecord/ foo.tfrecord
    self.dataset       = dataset
    self.filename      = filename
    self.class_map     = []
    classes_file       = os.path.join(yolo_anno_dir, "classes.txt")
    if os.path.exists(classes_file) == False:
      raise Exception("No found " + classes_file)
      
    with open(classes_file, "r") as f:
      for row in f.readlines():
        self.class_map.append(row.strip("\n"))
        
    print("class_map {}".format(self.class_map))


  def create_tf_example(self, image_file, source_id):
    image_filepath = os.path.join(self.images_dir, image_file)
    
    filename = os.path.basename(image_file)
    print("--- filename {}".format(filename))
    
    # 2021/11/07: Try to use filename as source_id. 
    try:
      # The following line will cause an exception if the filename were a string something 
      # like uuid based name: 'ff290a59-462c-47a1-8a99-017a1b30e550_0_9224.jpg'
      # See also: google/automl/efficientdet/dataloader.py: line 342.
      source_id = tf.strings.to_number(filename)
    except Exception as ex:
      print(ex)


    with tf.gfile.GFile(image_filepath, 'rb') as fid:
      encoded_jpg = fid.read()

      encoded_jpg_io = io.BytesIO(encoded_jpg)
      image = Image.open(encoded_jpg_io)
      width, height = image.size

      image_format = b'jpg'
      xmins = []
      xmaxs = []
      ymins = []
      ymaxs = []
      classes_text = []
      classes = []
       
      source_id = str(source_id)
      name     = filename.split('.')[0]
      anno_txt_file = name + ".txt"
      anno_txt_filepath = os.path.join(self.yolo_anno_dir, anno_txt_file)
      
      if os.path.exists(anno_txt_filepath) == False:
        print("Not found annotation file {}".format(anno_txt_filepath))
        return
              
      with open(anno_txt_filepath,"r") as file:

        for row in file.readlines():
            
            # YOLO row format: row= (class_id, xcen, ycen, w, h)
         
            print(row)
            items = row.split(" ")
            
            class_id = items[0]
            xcen     = float(items[1])
            ycen     = float(items[2])
            w        = float(items[3])
            h        = float(items[4])
            xmin     = xcen - w/2
            ymin     = ycen - h/2
            xmax     = xmin + w
            ymax     = ymin + h
            
            xmins.append(xmin)
            xmaxs.append(xmax)
            ymins.append(ymin)
            ymaxs.append(ymax)
            
            classes_text.append(class_id.encode('utf-8'))
           
            # class_id may begins with 0
            class_id  = int(class_id)
            class_name = self.class_map[class_id].encode('utf-8')
            print("--- class_id {} class_name {}".format(class_id, class_name))
            
            #2021/11/03: Adding 1 to class_id.
            classes.append(class_id + 1)
            

        tf_example = tf.train.Example(features=tf.train.Features(feature={
            'image/height':             dataset_util.int64_feature(height),
            'image/width':              dataset_util.int64_feature(width),
            'image/filename':           dataset_util.bytes_feature(filename.encode('utf-8')),
            'image/source_id':          dataset_util.bytes_feature(source_id.encode('utf-8')),
            'image/encoded':            dataset_util.bytes_feature(encoded_jpg),
            'image/format':             dataset_util.bytes_feature(image_format),
            'image/object/bbox/xmin':   dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax':   dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin':   dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax':   dataset_util.float_list_feature(ymaxs),
            'image/object/class/text':  dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(classes),
        }))
        return tf_example


  def generate(self):
    # self.dataset is "train", "valid", "test".
    
    tfrecord_dir = os.path.join(self.output_dir, self.dataset)
    if os.path.exists(tfrecord_dir) == False:
      os.makedirs(tfrecord_dir)
      
    tfrecord_path = os.path.join(tfrecord_dir, self.filename)

    image_files = os.listdir(self.images_dir)
    #print("--- {}".format(image_files))
   
    with tf.python_io.TFRecordWriter(tfrecord_path) as writer:
    
      source_id = 0    
      for image_file in image_files:
    
        if image_file.endswith(".jpg"):
           
          source_id += 1
          tf_example = self.create_tf_example(image_file, source_id)
          if tf_example != None:
            print("--- writing tf_example {}".format(image_file))
            
            writer.write(tf_example.SerializeToString())
          else:
            print("--- tf_example is None {}".format(image_file))

        if image_file.endswith(".png"):
          print("Sorry, png files not supported")

          
usage = "python YOLO2TFRecordCreator.py images_dir yolo_anno_dir output_dir dataset"

# python YOLO2TFRecordCreator.py ./YOLO/valid ./YOLO/valid ./tfrecord valid

# python YOLO2TFRecordCreator.py ./dataset/train ./dataset/train ./tfrecord train
# python YOLO2TFRecordCreator.py ./dataset/valid ./dataset/valid ./tfrecord valid


if __name__ == "__main__":

  images_dir     = ""
  yolo_anno_dir  = ""
  output_dir     = "./tfrecord"
  dataset        = "train"   
  try:
    if len(sys.argv) == 5:
      images_dir     = sys.argv[1]
      yolo_anno_dir  = sys.argv[2]
      output_dir     = sys.argv[3]
      dataset        = sys.argv[4]
    else:
      raise Exception(usage)
      
    if os.path.exists(images_dir) == False:
      raise Exception("Not found " + images_dir)
      
    if os.path.exists(yolo_anno_dir) == False:
      raise Exception("Not found " + yolo_anno_dir)
    
    if os.path.exists(output_dir) ==False:
      os.makedirs(output_dir)
       
    filename = dataset + ".tfrecord"
      
    creator = YOLO2TFRecordCreator(images_dir, 
                 yolo_anno_dir, 
                 output_dir, 
                 dataset  = dataset, 
                 filename = filename)
    creator.generate()
    
  except:
    traceback.print_exc()
    