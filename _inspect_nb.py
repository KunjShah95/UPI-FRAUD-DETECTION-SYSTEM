import json
import pathlib

nb_path = pathlib.Path(r'c:\UPI-FRAUD-DETECTION-SYSTEM-main\UPI-FRAUD-DETECTION-SYSTEM-main\Data_Analysis_for_UPI_Payment_System.ipynb')
nb = json.loads(nb_path.read_text(encoding='utf-8'))
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'code':
        src = ''.join(cell.get('source', ''))
        if any(key in src for key in ['ml_data =', 'ml_data_encoded', 'feature_columns', 'StandardScaler()', "drop('fraud'"]):
            print(f'\n--- CELL {i} ---')
            print(src[:5000])
