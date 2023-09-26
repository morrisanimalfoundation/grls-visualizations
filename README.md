# Golden Retriever Lifetime Study Data Visualisations
This GitHub project provides a set of scripts to create visualisations for the Golden Retriever Lifetime Study data, which is available on the Morris Animal Foundation's Data Commons website.
The project aims to help researchers and enthusiasts gain insights from this valuable dataset through visual representations.

## Table of Contents
* [Introduction](#introduction)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Contributing](#contributing)
* [License](#license)

## Introduction
The Morris Animal Foundation's Golden Retriever Lifetime Study is a comprehensive dataset that contains valuable information about the health, behavior, diet, and lifestyle of Golden Retrievers. This project provides a set of scripts to create visualisations for six major categories of data within the study:

1. Demographic Data
2. Medical Conditions Data
3. Primary Study Endpoints
4. Diet Data
5. Behavior Data
6. Lifestyle Data

The project is designed to be easy to use and customizable. You can run the provided scripts to generate visualisations for any specific category of interest.

## Getting Started
### Prerequisites
Before you begin, ensure you have met the following requirements:
* Python 3.x installed on your system.
* Access to the Golden Retriever Lifetime Study data on the Morris Animal Foundation's Data Commons website.
  * You can register for data access here: https://datacommons.morrisanimalfoundation.org/
* Access to the Fonts directory (Bunday Sans Complete)
* Three variables:
  * __`dirpath`__: The path to the directory containing all the study data.
  * __`vizpath`__: The path for the directory where the visualisation outputs will be saved as PNG files.
  * __`fontpath`__: The path for the directory containing the font files.

### Installation
1. Clone this GitHub repository to your local machine:
    ```
   git clone https://github.com/morrisanimalfoundation/grls-visualizations.git
    ```
2. Install the required Python packages by running the following command in the project's root directory:
    ```
   pip install -r requirements.txt
   ```

### Usage
To create visualisations for a specific category of data, follow these steps:

1. Set the __`dirpath`__, __`vizpath`__ and __`fontpath`__ variables in the __`py_secrets.py`__ file to specify the directory paths for the data and visualisation outputs. 
2. Run the corresponding script for the desired data category:
 * Demographic Data: __`demo_viz.py`__
 * Medical Conditions Data: __`med_viz.py`__
 * Primary Study Endpoints: __`endpoint_viz.py`__
 * Diet Data: __`diet_viz.py`__
 * Behavior Data: __`behavior_viz.py`__
 * Lifestyle Data: __`lifestyle_viz.py`__

For example, to create visualisations for Demographic Data, run:
 ```
 python3 demo_viz.py
 ```
3. The script will generate visualisations and save them in the specified __`vizpath`__ directory along with the data required for the graphics on the respective webpage.

### Project Structure
The project structure is organized as follows:
```
grls-visualizations/
│
├── main.py               # Script for running all of the visualisation scripts listed below
├── demo_viz.py           # Script for Demographic Data visualisation
├── medical_viz.py        # Script for Medical Conditions Data visualisation
├── endpoints_viz.py      # Script for Primary Study Endpoints visualisation
├── diet_viz.py           # Script for Diet Data visualisation
├── behavior_viz.py       # Script for Behavior Data visualisation
├── lifestyle_viz.py      # Script for Lifestyle Data visualisation
├── py_secrets.py         # Store your secret variables (dirpath, vizpath, fontpath) here
├── .gitignore            # Gitignore file to exclude sensitive data and outputs
├── requirements.txt      # List of Python packages required for this project
│
└── README.md             # This README file
```

### Contributing
Contributions to this project are welcome! Feel free to open issues, submit pull requests, or provide feedback to help improve the project.

### License
This project is licensed under [---]