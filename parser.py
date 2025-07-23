import json
import numpy as np
import os
from collections import Counter


def parse_json(json_str):
    """Parse a JSON string into a Python dictionary.

    Args:
        json_str (str): The JSON string to parse.

    Returns:
        dict: The parsed JSON object.
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e


FOLDES = ["mesh_converg"]
for FOLDER in FOLDES:
    print(f'Parsing {FOLDER}')
    syms = []
    files = os.listdir(FOLDER)
    files = [os.path.join(FOLDER, file) for file in files]
    for file in files:
        if file.endswith('.json'):
            with open(file, 'r') as f:
                json_str = f.read()
                try:
                    parsed_json = parse_json(json_str)
                    parsed_json['properties']['material'] = file.split('_')[0]
                    parsed_json['filename'] = file
                    syms.append(parsed_json)
                except ValueError as e:
                    print(e)
        elif file.endswith('.npy'):
            data = np.load(file, allow_pickle=True)
            print(f"Loaded numpy array from {file}: {data}")
        else:
            print(f"Unsupported file type: {file}")

    n_etas = 6
    header = ['rho', 'l', 'E1', 'E2', 'G12', 'v12', 'duration', 'name', 'material',
              'R', 'z1', 'l/R', "ne"] + [f'eta{i+1}' for i in range(n_etas)] + \
        [f'count_eta{i+1}' for i in range(n_etas)] + ['link']
    with open(f'{FOLDER}.csv', 'w') as f:
        f.write(
            f"{','.join(header)}\n")
        for sym in syms:
            ne = len(sym['dictionary'])
            rho = sym['properties']['rho'][0]
            l = sym['properties']['l']
            E1 = sym['properties']['E1'][0]
            E2 = sym['properties']['E2'][0]
            G12 = sym['properties']['G12'][0]
            v12 = sym['properties']['v12'][0]
            duration = sym['properties']['duration']
            name = sym['properties']['name']
            material = 'Unknown'
            L = float(name.split('_')[1])
            z1 = sym['properties']['z1']
            b = L/10
            h = L/10
            inertia = b*h**3/12
            area = b*h
            R = L
            l_R = l/R
            etas = []
            m0 = area * rho
            for solution in sym['solutions']:
                eigv = solution['info']['eigv']
                omega = eigv**0.5
                eta = omega*L**2*(m0/E1/inertia)**0.5
                if eigv > 1e-2 and len(np.unique(etas)) < n_etas:
                    etas.append(round(eta, 8))
            counts = Counter(etas)
            etas = np.unique(etas)
            counts = [f"{counts[k]}" for k in etas]
            if len(counts) < n_etas:
                counts += ['-'] * (n_etas - len(counts))
            etas = [str(i) for i in etas]
            if len(etas) < n_etas:
                etas += ['-'] * (n_etas - len(etas))
            etas = ','.join(etas)
            counts = ','.join(counts)
            link = f"https://zibramax.github.io/FEMViewer/?mesh=https://raw.githubusercontent.com/ZibraMax/non-local-frequencies-nanostructures-2/refs/heads/main/{sym['filename']}&mode=1&magnif=6"
            f.write(
                f"{rho},{l},{E1},{E2},{G12},{v12},{duration},{name},{material},"
                f"{R},{z1},{l_R},{ne},{etas},{counts},{link}\n"
            )
