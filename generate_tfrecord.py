# generate_tfrecord.py
import os
import glob
import pandas as pd
import tensorflow as tf
from xml.etree import ElementTree
from object_detection.utils import dataset_util

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ElementTree.parse(xml_file)
        root = tree.getroot()
        filename = root.find('filename').text
        for member in root.findall('object'):
            value = (
                filename,
                int(root.find('size')[0].text),
                int(root.find('size')[1].text),
                member[0].text,
                int(member[4][0].text),
                int(member[4][1].text),
                int(member[4][2].text),
                int(member[4][3].text)
            )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height',
                   'class', 'xmin', 'ymin', 'xmax', 'ymax']
    return pd.DataFrame(xml_list, columns=column_name)

def class_text_to_int(row_label):
    if row_label == 'aadhaar_no':
        return 1
    elif row_label == 'name':
        return 2
    elif row_label == 'dob':
        return 3
    elif row_label == 'photo':
        return 4
    else:
        return None

def create_tf_example(group, path):
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_image_data = fid.read()

    width = int(group.width)
    height = int(group.height)

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = [group.xmin / width]
    xmaxs = [group.xmax / width]
    ymins = [group.ymin / height]
    ymaxs = [group.ymax / height]
    classes_text = [group['class'].encode('utf8')]
    classes = [class_text_to_int(group['class'])]

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_image_data),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example

def main():
    image_dir = 'data/train_data'
    csv_input = xml_to_csv(image_dir)
    writer = tf.io.TFRecordWriter('data/train.record')

    for index, row in csv_input.iterrows():
        tf_example = create_tf_example(row, image_dir)
        writer.write(tf_example.SerializeToString())

    writer.close()
    print('✅ Successfully created TFRecord at data/train.record')

if __name__ == '__main__':
    main()
