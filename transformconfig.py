import os
import pandas as pd
import yaml

# Load configuration
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

def transform_csv(file_path, transformed_path, cam_number):
    df = pd.read_csv(file_path)
    
    # Remove empty columns
    df = df.dropna(axis=1, how='all')
    
    # Convert wide format to long format
    columns_to_keep = config['csv']['columns_to_keep']
    snapshot_prefix = config['csv_transformation']['snapshot_prefix']
    time_suffix = config['csv_transformation']['time_suffix']
    
    snapshot_columns = [col for col in df.columns if col.startswith(snapshot_prefix) and not col.endswith(time_suffix)]
    time_columns = [col for col in df.columns if col.endswith(time_suffix)]
    
    long_df = pd.DataFrame()
    
    for snapshot_col in snapshot_columns:
        time_col = snapshot_col + time_suffix
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

def merge_transformed_csv(transformed_path, merged_file_path):
    merged_df = pd.DataFrame()
    
    for cam_number in range(1, len(config['cameras']) + 1):
        file_path = os.path.join(transformed_path, f'transformed_cam{cam_number}.csv')
        if os.path.exists(file_path):
            temp_df = pd.read_csv(file_path)
            temp_df['camera'] = f'transformed_cam{cam_number}.csv'
            merged_df = pd.concat([merged_df, temp_df], ignore_index=True)
        else:
            print(f'File not found: {file_path}')
    
    merged_df.to_csv(merged_file_path, index=False)

def main():
    base_path = config['paths']['snapshot_base_folder']
    transformed_path = config['paths']['transformed_result_folder']
    merged_file_path = config['paths']['merged_result_file']
    
    for cam_number in range(1, len(config['cameras']) + 1):
        cam_folder = os.path.join(base_path, f'camera{cam_number}')
        file_path = os.path.join(cam_folder, f'camera{cam_number}_res.csv')
        if os.path.exists(file_path):
            transform_csv(file_path, transformed_path, cam_number)
        else:
            print(f'File not found: {file_path}')
    
    merge_transformed_csv(transformed_path, merged_file_path)

if __name__ == "__main__":
    main()