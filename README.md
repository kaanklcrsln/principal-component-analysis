# TIFF Image PCA Analysis Tool

A graphical user interface (GUI) application that analyzes TIFF images using PCA (Principal Component Analysis).

<img width="864" height="755" alt="Screenshot 2026-01-28 at 14 37 56" src="https://github.com/user-attachments/assets/6e8cf6e2-6d9a-4c73-bb86-e27fd0bbaccc" />

## Features

- **TIFF Image Support**: Load multi-band and single-band TIFF files
- **PCA Analysis**: Perform principal component analysis on image bands
- **Visualization**: 
  - Original image preview (RGB/grayscale)
  - First principal component (PC1) map
  - Value visualization with color scale
- **Statistics Table**: For each component:
  - Explained variance (Eigenvalue)
  - Variance ratio (%)
  - Standard deviation

## Installation

### Requirements

- Python 3.7+
- Virtual environment (recommended)

### Steps

1. Clone or download the project
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

3. Install required libraries:
```bash
pip install numpy scikit-learn pillow matplotlib tifffile
```

## Usage

Start the application:
```bash
python main.py
```

### Step-by-Step Usage

1. When the application opens, click the "Load TIFF Image" button
2. Select a TIFF file (.tif or .tiff)
3. PCA analysis is performed automatically
4. Results are displayed visually and in a table:
   - **Left panel**: Original image
   - **Right panel**: PC1 component
   - **Bottom table**: Statistics for each component

## Technical Details

### Supported Formats

- TIFF (.tif, .tiff)
- Single-band (grayscale) images
- Multi-band (multi-band/hyperspectral) images

### PCA Process

1. Image is flattened (H×W×C → (H×W)×C)
2. Maximum 10 components are calculated
3. First component (highest variance) is visualized
4. Statistics for all components are displayed in the table

### Libraries

- **tkinter**: GUI framework
- **numpy**: Numerical operations
- **scikit-learn**: PCA algorithm
- **PIL/Pillow**: Image processing
- **matplotlib**: Data visualization
- **tifffile**: Advanced TIFF file support

## Project Structure

```
PCA/
├── main.py              # Main application file
├── README.md            # This file
└── venv/                # Virtual environment (optional)
```

## Troubleshooting

### "Cannot identify image file" error

This error may be caused by PIL's limitations with certain TIFF formats. The code automatically switches to using the `tifffile` library in such cases.

### Warning on grayscale images

PCA provides limited information on single-band images. It is recommended to use multi-band images.

## License

This project was developed for educational purposes.

## Contributing

You can open pull requests for suggestions and improvements.
