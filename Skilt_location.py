# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2

FILE_PATH_READINGS = r"readings.csv"
FILE_PATH_CAMERA_CONFIG = r"camera_config.csv"
AREA_INCREASE_FACTOR = 10
SHOW_HIGH_LOW = True


def load_data():
    readings = pd.read_csv(FILE_PATH_READINGS)
    camera_config = pd.read_csv(FILE_PATH_CAMERA_CONFIG)
    return readings, camera_config


def split_data_by_camera(data, camera_config):
    """
    Splits data by unique camera IDs.
    Returns: Cameras data, camera configurations, and unique camera IDs.
    """
    unique_camera_ids = sorted(data["camera_id"].unique().tolist())

    cameras = []
    camera_configurations = {}

    for cam_id in unique_camera_ids:
        camera_data = data[data["camera_id"] == cam_id].reset_index(drop=True)
        cameras.append(camera_data)

        camera_config_row = camera_config[camera_config["camera_id"] == cam_id].iloc[0]
        camera_configurations[cam_id] = [camera_config_row["height"], camera_config_row["width"]]

    return cameras, camera_configurations, unique_camera_ids


def extract_coordinates(data):
    flat_coords = [int(coord) for coord in data["coordinates"].str.extractall(r'(\d+)')[0].tolist()]
    reshaped = [flat_coords[i:i + 2] for i in range(0, len(flat_coords), 2)]
    reshaped = np.array(reshaped)
    end_shape = [reshaped[i:i + 4].reshape(4, 2) for i in range(0, len(reshaped), 4)]
    end_shape = list(end_shape)
    return end_shape



def generate_heatmap(coordinates, height, width):
    heatmap = np.zeros((height, width))
    #coordinates = np.array(coordinates)  # Convert list to numpy array
    #grouped_coords = [coordinates[i:i + 4].reshape(4, 2) for i in range(0, len(coordinates), 4)]
    for coord in coordinates:
        corners = np.asarray(coord).reshape(4, 2)
        mask = cv2.fillPoly(np.zeros_like(heatmap, dtype=np.uint8), [corners], 255).astype(bool)
        heatmap[mask] += 1
    return heatmap


def display_heatmap(matrix, camera_id, show_bar=True):
    if show_bar:
        max_val = matrix.max()
        mid_val = max_val / 2
        heatmap_display = plt.imshow(matrix, cmap='hot', interpolation='nearest')
        color_bar = plt.colorbar(heatmap_display, label="Probability", ticks=[0, mid_val, max_val])
        color_bar.ax.set_yticklabels(['Low', 'Average', 'High'])
    else:
        plt.imshow(matrix, cmap='hot', interpolation='nearest')

    plt.title(f'Number plate location heatmap camera: {camera_id}')
    plt.show()


def get_center_of_mass(matrix):
    points = np.where(matrix == matrix.max())
    return [points[0][0], points[1][0]]


def compute_dimensions(coordinates):
    lengths = [coord[1][0] - coord[0][0] for coord in coordinates]
    heights = [coord[3][1] - coord[1][1] for coord in coordinates]
    avg_length = sum(lengths) / len(coordinates)
    avg_height = sum(heights) / len(coordinates)
    return avg_length, avg_height, avg_length / avg_height


def get_area_of_interest(center, length, height, ratio, increment):
    half_length = int(length / 2)
    half_height = int(height / 2)
    adjusted_increment = int(increment * ratio)
    return [
        [center[1] - half_length - adjusted_increment, center[0] - half_height - increment],
        [center[1] + half_length + adjusted_increment, center[0] - half_height - increment],
        [center[1] + half_length + adjusted_increment, center[0] + half_height + increment],
        [center[1] - half_length - adjusted_increment, center[0] + half_height + increment]
    ]


def main():
    """
    Main execution function.
    """
    try:
        data, camera_config = load_data()
        cameras, camera_configs, camera_ids = split_data_by_camera(data, camera_config)

        for i, camera in enumerate(cameras):
            coordinates = extract_coordinates(camera)
            height, width = camera_configs[camera_ids[i]]
            heatmap = generate_heatmap(coordinates, height, width)

            display_heatmap(heatmap, camera_ids[i], SHOW_HIGH_LOW)

            center = get_center_of_mass(heatmap)
            avg_length, avg_height, ratio = compute_dimensions(coordinates)

            area = get_area_of_interest(center, avg_length, avg_height, ratio, AREA_INCREASE_FACTOR)
            area_heatmap = generate_heatmap([area], height, width)

            display_heatmap(area_heatmap, camera_ids[i], False)

            print(f"Most likely numberplate location for camera {camera_ids[i]}: {area}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
