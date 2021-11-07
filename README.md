# TFRecordCreator
TFRecordCreator from other annotations 

<a href="./YOLO2TFRecordCreator.py">YOLO2TFRecordCreator</a> is a simple TFRecordCreator from YOLO annotations.<br>

Please run the following command on a command line prompt window.<br>

<pre>
>python YOLO2TFRecordCreator.py images_dir yolo_anno_dir output_dir dataset_name
</pre>
<br>
For example, run the command.<br>
<pre>
>python YOLO2TFRecordCreator.py ./dataset/valid ./dataset/valid ./tfrecord valid
</pre>
A <b>valid.tfrecord</b> file will be created in <b>./tfrecord</b> folder.<br>
<br>
<br>
If you would like to inspect the created tfrecord file, 
please run the following command.<br>
<pre>
>python TFRecordInspector.py ./tfrecord/valid/valid.tfrecord ./label_map.pbtxt ./output/valid
</pre>


