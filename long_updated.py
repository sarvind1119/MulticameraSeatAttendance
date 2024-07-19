import os
import pandas as pd

def transform_csv(file_path, transformed_path, cam_number):
    df = pd.read_csv(file_path)

    # Remove empty columns
    df = df.dropna(axis=1, how='all')

    # Convert wide format to long format
    columns_to_keep = ['seat_number', 'seat_coordinates']
    snapshot_columns = [col for col in df.columns if col.startswith('snapshot_') and not col.endswith('_time')]
    time_columns = [col for col in df.columns if col.endswith('_time')]

    long_df = pd.DataFrame()

    for snapshot_col in snapshot_columns:
        time_col = snapshot_col + '_time'
        temp_df = df[columns_to_keep].copy()
        temp_df['snapshot'] = snapshot_col
        temp_df['Snapshot status'] = df[snapshot_col]
        temp_df['Snapshot Time'] = df[time_col]
        long_df = pd.concat([long_df, temp_df], ignore_index=True)

    # Save the transformed file
    if not os.path.exists(transformed_path):
        os.makedirs(transformed_path)
    output_file = os.path.join(transformed_path, f'transformed_cam{cam_number}.csv')
    long_df.to_csv(output_file, index=False)

def main():
    base_path = './snapshots'
    transformed_path = './transformed_result'

    for cam_number in range(1, 7):
        cam_folder = os.path.join(base_path, f'camera{cam_number}')
        file_path = os.path.join(cam_folder, f'camera{cam_number}_res.csv')
        if os.path.exists(file_path):
            transform_csv(file_path, transformed_path, cam_number)
        else:
            print(f'File not found: {file_path}')

if __name__ == "__main__":
    main()
