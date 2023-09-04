# Signatur-ITS-Case - Car Number Plate Location Analyzer

### Overview:

This code provides a solution to visualize the distribution of car number plate locations captured from different cameras. The tool leverages heatmaps to provide a graphical representation of the areas with the highest concentration of number plates. Each camera can have a different resolution, so it takes the camera ID to fetch its resolution and adjust the coordinate system accordingly.

### Data Requirements:

1. **readings.csv**: Contains the readings from the different cameras. Each reading should represent the location of a car number plate on a picture, formatted as 4 coordinates in [x, y] format, representing the four corners of the number plate. An associated camera ID should also be part of the reading.

2. **camera_config.csv**: Contains the configuration details of each camera. The data should include the camera ID and its resolution (height and width).

### Code Structure:

- **Constants**:
    - `FILE_PATH_READINGS`: File path for readings.
    - `FILE_PATH_CAMERA_CONFIG`: File path for camera configurations.
    - `AREA_INCREASE_FACTOR`: Factor by which the area showing the highest concentration of number plates is increased.
    - `SHOW_HIGH_LOW`: A boolean flag that controls whether to show color bar indications for heatmap intensity or not.

- **Functions**:
    1. `load_data()`: Loads readings and camera configurations from CSV files.
    2. `split_data_by_camera(data, camera_config)`: Splits the data based on unique camera IDs and returns each camera's data and its configuration.
    3. `extract_coordinates(data)`: Extracts the x and y coordinates from the data.
    4. `generate_heatmap(coordinates, height, width)`: Generates the heatmap for the given coordinates on the specified resolution.
    5. `display_heatmap(matrix, camera_id, show_bar=True)`: Displays the heatmap with a specified color bar.
    6. `get_center_of_mass(matrix)`: Identifies the center of the highest concentration of number plates on the heatmap.
    7. `compute_dimensions(coordinates)`: Computes the average dimensions (length and height) of the number plates.
    8. `get_area_of_interest(center, length, height, ratio, increment)`: Computes the area where the number plates are found at their highest concentration.
    9. `main()`: The main function that drives the processing, heatmap generation, and display.

- **Execution Point**:
    - The `if __name__ == '__main__':` block serves as the entry point to the script, triggering the `main()` function.

### Execution Steps:

1. Load readings and camera configurations.
2. Split data based on unique camera IDs.
3. For each camera:
    - Extract x and y coordinates for number plate locations.
    - Generate and display the heatmap of number plate locations.
    - Identify the center of the highest concentration.
    - Compute the average dimensions of the number plates.
    - Calculate and display the area of highest concentration.
    - Print the area coordinates to the console.

### Usage:

To run the program, ensure you have the required libraries installed (numpy, pandas, cv2, matplotlib) and run:

```bash
python <filename>.py
```

Replace `<filename>` with the name of the python file containing the code.

### Notes:

- Make sure the `readings.csv` and `camera_config.csv` files are available in the specified path.
- The code uses OpenCV (`cv2`) for image processing, `pandas` for data manipulation, and `matplotlib` for visualization.
- If there's a change in the data format or structure, adjustments may be required in the `load_data()` and `split_data_by_camera()` functions.
