![banner](https://github.com/yonwalone/nn-art-epoch-assignment/blob/main/banner.png?raw=true)

--------------------
  ![last-commit-shield](https://img.shields.io/github/last-commit/yonwalone/nn-art-epoch-assignment?style=flat-square)   ![repo-size](https://img.shields.io/github/repo-size/yonwalone/nn-art-epoch-assignment?style=flat-square)     ![top-language](https://img.shields.io/github/languages/top/yonwalone/nn-art-epoch-assignment?style=flat-square)

# nn-art-epoch-assignment

## Description
 'nn-art-epoch-assignment' is a deep learning project that aims to classify images of art into their respective art epochs, including Baroque, Expressionism, Modern, etc. The project involves the use of state-of-the-art deep neural networks, as well as various image preprocessing techniques, to create a highly accurate system for assigning art images to their correct epochs.

## Features
* Image Download: The system can automatically download art images from 'wikiart.org'.
* Image Analysis: The project includes a script to get properties of the images for each art epoch
* Custom Neural Network: The project includes a custom deep neural network architecture written in nearly plain python for image classification
* Model Training: 'nn-art-epoch-assignment' inludes scripts to train tensorflow models to classify images into epochs
* Deployment: The project includes a flask application to provide a website and a Flutter project to generate a mobile applications

## Technologies Used
* Conda
* Python
* TensorFlow
* Keras
* Numpy
* Cv2

## Getting Started
To get started with 'nn-art-epoch-assignment', users can simply clone the GitHub repository and follow these installation instructions:

### Virtual Environment Setup
The virtual environment specifies which versions of software and packages this project uses. For this we are using the software conda. Conda is both a package manager and a virtual environment for data science-centric Python.

You can install Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html).

And use the following commands to create and activate the conda environment:

```bash
conda env create -f environment.yml
conda activate py38-nn-art-epoch-assignment
```

The setup for the virtual environment is complete. To check if everything worked, run the following command and see if the version matches.

```bash
python --version
Python 3.8.16
```


### Project Structure

Filtered to show only important files and folders.
```
|-- custom_net
  |-- foundation
  |-- layer
  |-- model
|-- data
  |-- splits
  |-- baroque
    -- images.json
    -- log.txt
    -- painters.json
  ...
|-- deployment
  |-- epoch_check_app
  |-- flask
|-- results
  |-- custom_nets
  |-- graphs
  |-- log
  |-- models
|-- scripts
  |-- scripts
|-- src
 -- .gitignore
 -- config.py
 -- environment.yml
 -- README.md
 -- setup.py
```
* **custom_net**: Files to create and test the custom net
  * **foundation**: Basics to create the custom net
  * **layer**: Implementation of different types of layers
  * **model**: Custom model that can be created
* **data**: Includes the input data for the models
  * **splits**: Includes different splits of data, that include images splitted in train, test and validation data
  * **baroque**: There is a folder for each art epoch, that includes the images, the result of recieving the images (log.txt), a file with all painters, that produced an image in the specific art epoch, (painters.json) and an overview over the images (images.json)
* **deployment**: Includes different deployment approuches
  * **epoch_check_app**: Includes a flutter project to create a mobile app
  * **flask**: Includes code to create a website with flask app
  * **front_end_only**: Stopped approuch to create a website with running the model in front-end Javascript
* **results**: Results of training the models
  * **custom_nets**: Includes custom_models as json files
  * **graphs**: Includes graphs of accuracy and losse while training tensorflow models
  * **log**: Includes console outputs of training tensorflow models
  * **models**: Includes tensorflow models as .h5 files (Not synced because of size)
* **scripts**: All scripts for different purposes
  * **data_analysis**: Includes scripts for image analysis
  * **tf_model**: Includes scripts for training tensorflow models
* **src**: Reusable Python modules for the project. This is the kind of python code that you can import.

### Run scripts
Tell Python where to look for the library code to run own scripts. Once the package is locally installed, it can be easily used regardless of which directory you’re in. 
```bash
(py38-nn-art-epoch-assignment) pip install -e .
```
The '.' indicates that we’re installing the package in the current directory. The '-e' indicates that the package should be editable. That means that if you change the files inside the src folder, you don’t need to re-install the package for your changes to be picked up by Python.

For example, the following command can be used to call scripts from the src folder:
```bash
(py38-nn-art-epoch-assignment) python src/download.py
```

### Deployment

#### Flask Website
On Unix systems set enviornment variable FLASK_App.
```bash
export FLASK_APP=deployment/flask/app.py
```
Then its possible to start the flask application with the command:
```bash
flask run
```
In the response is a link to an url, where the website is available. 
It can be copied and pasted to a browser to visit the website.
The Flask-Server can be quit by pressing CTRL+C.

#### Flutter App
The flutter app was created with a device with Windows 11 as its operating system.
To build the app on a Windows device their are certain steps necessary:
1. Install the Flutter SDK
2. Run flutter doctor
3. Install Android Studio
4. Install Flutter PlugIn

The app can be started with:
```bash
flutter run
```
Use ADB to install the Android App on a real device.

The app is also provided as an apk for easier installation.

### Selenium Setup (Not necessary)
This sections contains the information needed for downloading the images from wikiart.org using Selenium.

1. Install Google Chrome
2. Check you Chrome Version
3. Download the Driver for your Chrome version [here](https://sites.google.com/chromium.org/driver/downloads).
4. Save the Unix Executable File 'chromedriver' in 'usr/local/bin'

## Contributing
Even if the repository is public, it is a private study project. Contributions are only permitted from Steffen, Benedikt and Lukas.
Therefore other contributions to 'nn-art-epoch-assignment' are currently not welcome and encouraged! Users can not contribute to the project by submitting bug reports, feature requests, or even code contributions. Pull requests will not be reviewed by the project maintainers and merged.

## License
'nn-art-epoch-assignment' is licensed under the MIT License, which allows for unrestricted use, modification, and redistribution of the code.