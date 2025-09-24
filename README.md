# Document Verification System

This project automates the verification of Indian identity documents such as Aadhaar, PAN, and Driving License using computer vision and text extraction techniques. The system leverages OpenCV, TensorFlow Object Detection, and Streamlit for a user-friendly interface.

## Technologies Used / Tech Stack

- **Programming Language:** Python 3
- **Web Framework:** Streamlit (for interactive web UI)
- **Computer Vision:** OpenCV
- **Machine Learning / Deep Learning:** TensorFlow (Object Detection API, pre-trained models)
- **Optical Character Recognition (OCR):** pytesseract
- **Data Formats:** JSON (for document databases)
- **Environment Management:** Conda, virtualenv
- **Other Libraries:** numpy, pandas, Pillow, etc. (see `requirements.txt` for full details)

## Features

- **Aadhaar Detection & Verification**: Detects visual features of Aadhaar cards and verifies details using a database.
- **PAN Verification**: Extracts and verifies PAN card details.
- **Driving License Verification**: Extracts and verifies driving license details.
- **Text Extraction**: Uses OCR to extract text from document images.
- **Streamlit Web App**: Interactive UI for document upload and verification.
- **Database Support**: Sample JSON databases for Aadhaar, PAN, and Driving License.

## Project Structure

```
doc_verification/
├── data/                         # Directory for sample images and data
├── models/                       # TensorFlow models and research code
├── aadhaar_db.json               # Sample Aadhaar database
├── pan_db.json                   # Sample PAN database
├── driving_license_db.json       # Sample Driving License database
├── detect_aadhaar.py             # Visual feature detection for Aadhaar
├── verify_aadhaar.py             # Aadhaar verification logic
├── pan_verification.py           # PAN verification logic
├── verify_pan.py                 # PAN verification logic (alt)
├── driving_license_verification.py # Driving License verification logic
├── verify_dl.py                  # Driving License verification logic (alt)
├── extract_text.py               # OCR/Text extraction code
├── generate_tfrecord.py          # Generates TFRecord files for training
├── label_map.pbtxt               # Label map for object detection
├── requirements.txt              # Python dependencies
├── streamlit_app.py              # Streamlit web application
└── README.md                     # Project documentation
```

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/harshala334/doc_verification.git
    cd doc_verification
    ```

2. **Set up a Python virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate    # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **(Optional) Set PYTHONPATH for TensorFlow models**  
   If using TensorFlow object detection, set the PYTHONPATH:
    ```bash
    export PYTHONPATH=$PYTHONPATH:$(pwd)/models:$(pwd)/models/research:$(pwd)/models/research/slim
    ```

5. **(Optional) Install OpenCV via Conda**:
    ```bash
    conda install -c conda-forge opencv
    ```

## Usage

### Text Extraction

To extract text from an image:
```bash
python extract_text.py
```

### Aadhaar Detection & Verification

To detect Aadhaar features in an image:
```bash
python detect_aadhaar.py
```
To verify Aadhaar details:
```bash
python verify_aadhaar.py
```

### PAN Verification

To verify PAN details:
```bash
python pan_verification.py
```
or
```bash
python verify_pan.py
```

### Driving License Verification

To verify DL details:
```bash
python driving_license_verification.py
```
or
```bash
python verify_dl.py
```

### Run Streamlit Web App

To launch the web interface:
```bash
streamlit run streamlit_app.py
```

## Sample Databases

- `aadhaar_db.json`: Sample Aadhaar card data.
- `pan_db.json`: Sample PAN card data.
- `driving_license_db.json`: Sample driving license data.

## Model Files

- `ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz`  
  Pre-trained object detection model (required for Aadhaar detection).

## Notes

- You may need to adjust paths in scripts if running from a different directory.
- For TensorFlow Object Detection, ensure all dependencies are installed as specified in the [TensorFlow Object Detection API documentation](https://github.com/tensorflow/models/tree/master/research/object_detection).

## License

This repository is for educational and research purposes. Please check individual files for license details.

---

**Maintainer:** [harshala334](https://github.com/harshala334)
