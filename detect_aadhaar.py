import os
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from object_detection.utils import label_map_util, visualization_utils as vis_util

# Load Model and Label Map
MODEL_DIR = "models/inference_graph/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model"
LABEL_PATH = "label_map.pbtxt"

def load_model():
    print("Loading model from:", MODEL_DIR)
    return tf.saved_model.load(MODEL_DIR)

def load_image_into_numpy_array(path):
    return np.array(Image.open(path))

# Detect Aadhaar Features
def detect_features(img_path):
    detect_fn = load_model()
    category_index = label_map_util.create_category_index_from_labelmap(LABEL_PATH, use_display_name=True)

    image_np = load_image_into_numpy_array(img_path)
    input_tensor = tf.convert_to_tensor(image_np)[tf.newaxis, ...]

    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        detections['detection_boxes'],
        detections['detection_classes'],
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        line_thickness=3,
        min_score_thresh=0.5)

    return image_np, detections['detection_boxes'], detections['detection_scores'], detections['detection_classes']

# Run and visualize
if __name__ == "__main__":
    img_path = "data/pan_card.jpg"
    output_img, _, _, _ = detect_features(img_path)

    cv2.imshow("Detected Aadhaar Features", cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
