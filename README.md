# TFRecordCreator
TFRecordCreator from other annotations 

<a href="./YOLO2TFRecordCreator.py">YOLO2TFRecordCreator</a> is a simple TFRecordCreator from YOLO annotations.<br>

Please run the following command on a command line prompt window.<br>

<pre>
>python YOLO2TFRecordCreator.py input_images_dir input_yolo_anno_dir output_tfrecor_dir dataset_name
</pre>
For example, run the command.<br>
<pre>
>python YOLO2TFRecordCreator.py ./YOLO/valid ./YOLO/valid ./tfrecord valid
</pre>
A <b>valid.tfrecord</b> file will be created in <b>./tfrecord</b> folder.<br>
<br>

If you would like to inspect the created tfrecord file, please run the following command.<br>
<pre>
>python TFRecordInspector.py ./tfrecord/valid/valid.tfrecord ./label_map.pbtxt ./output/valid
</pre>

The following is the annotated images generated by the above command.<br>
<img src="./readme_ref/tfrecord_inspector_generated_folder.png"><br>

