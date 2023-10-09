"""
This Python file contains code to run all the individual visualisation scripts for
https://datacommons.morrisanimalfoundation.org/

The files that are imported to power the visualisations are:
1. demo_viz.py
2. medical_viz.py
3. endpoints_viz.py
4. behavior_viz.py
5. lifestyle_viz.py

Author: Neha Bhomia
Created Date: October 9th, 2023
"""

from demo_viz import *

if __name__ == "__main__":
    age_vis(df_profile)
    sex_vis(df_tuple)
