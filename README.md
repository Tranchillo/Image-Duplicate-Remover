
# Image Duplicate Remover

## Description
**Image Duplicate Remover** is a Python script designed to identify duplicate images in a folder, group them based on similarity, and produce a unique set of images. The script uses hashing algorithms and similarity calculations to compare images.

### Key Features:
- Groups similar images into dedicated folders.
- Extracts a representative image from each group and moves it to the non-similar images folder.
- Automatically removes group folders after extracting the representative images.

---

## Requirements
Ensure you have Python 3.7 or later installed. The following Python libraries are also required:

- `numpy`
- `Pillow`
- `scikit-image`
- `imagehash`

---

## Installing Dependencies
### Method 1: Using a Virtual Environment (Recommended)
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. Install the required dependencies:
   ```bash
   pip install numpy Pillow scikit-image imagehash
   ```
4. Run the script within the virtual environment.

### Method 2: Global Installation
Run the following command to install the dependencies globally:
```bash
pip install numpy Pillow scikit-image imagehash
```

---

## Usage
1. Place the images to be processed in the `input_images` folder. If the folder does not exist, it will be created on the first script run.
2. Run the script using the following command:
   ```bash
   python image_duplicate_remover.py
   ```
3. Once processing is complete:
   - All unique images will be saved in the `grouped_images/non_similar_images` folder.
   - The group folders (`group_`) will be automatically removed.

---

## Example Folder Structure
After processing, the folder structure will resemble the following:

```
input_images/
grouped_images/
    └── non_similar_images/
```

---

## Notes
- The script works with the following image formats: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`.
- Any name conflicts in the `non_similar_images` folder will be resolved automatically by appending a unique number.

---

## Support
For any issues or suggestions, feel free to contact the author.
