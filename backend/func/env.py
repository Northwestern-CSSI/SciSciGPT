import os
import shutil
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib as mpl


def python_env_setup():
    # Set seaborn style, which is commonly used by Anthropic
    mpl_config_dir = mpl.get_configdir()
    style_dir = os.path.join(mpl_config_dir, 'stylelib')
    os.makedirs(style_dir, exist_ok=True)

    seaborn_style_map = {"seaborn-v0_8": "seaborn", "seaborn-v0_8": "seaborn-whitegrid", "seaborn-v0_8": "seaborn-white"}

    for k, v in seaborn_style_map.items():
        seaborn_style_path = os.path.join(style.core.BASE_LIBRARY_PATH, f'{k}.mplstyle')
        custom_style_path = os.path.join(style_dir, f'{v}.mplstyle')
        shutil.copy2(seaborn_style_path, custom_style_path)

    plt.style.reload_library()

    plt.style.use('seaborn')
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
python_env_setup()


python_env_setup_string = """
import os
import shutil
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib as mpl

def python_env_setup():
    # Set seaborn style, which is commonly used by Anthropic
    print("Setting seaborn style...")
    mpl_config_dir = mpl.get_configdir()
    style_dir = os.path.join(mpl_config_dir, 'stylelib')

    os.makedirs(style_dir, exist_ok=True)

    seaborn_style_path = os.path.join(style.core.BASE_LIBRARY_PATH, 'seaborn-v0_8.mplstyle')
    custom_style_path = os.path.join(style_dir, 'seaborn.mplstyle')

    shutil.copy2(seaborn_style_path, custom_style_path)
    plt.style.reload_library()
    print("\nUpdated available styles:", plt.style.available)

    plt.style.use('seaborn')
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
    print("Seaborn style set successfully.")
python_env_setup()
"""