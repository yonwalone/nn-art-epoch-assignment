![banner](https://github.com/yonwalone/nn-art-epoch-assignment/blob/lz_readme/banner.png?raw=true)

--------------------
  ![last-commit-shield](https://img.shields.io/github/last-commit/yonwalone/nn-art-epoch-assignment?style=flat-square)   ![repo-size](https://img.shields.io/github/repo-size/yonwalone/nn-art-epoch-assignment?style=flat-square)     ![top-language](https://img.shields.io/github/languages/top/yonwalone/nn-art-epoch-assignment?style=flat-square)

# nn-art-epoch-assignment

## Description
 'nn-art-epoch-assignment' is a deep learning project that aims to classify images of art into their respective art epochs, including Baroque, Renaissance, Modern, etc. The project involves the use of state-of-the-art deep neural networks, as well as various image preprocessing techniques, to create a highly accurate system for assigning art images to their correct epochs.

## Features
* Image Download: The system can automatically download art images from various sources, including online art collections and public domain repositories.
* Image Preprocessing: ArtEpochNet uses advanced image preprocessing techniques to enhance image quality, remove noise, and normalize image features.
* Custom Neural Network: The project includes a custom deep neural network architecture designed specifically for the task of art epoch classification.
* Model Training: ArtEpochNet uses large-scale datasets to train and optimize the custom neural network.
* Evaluation Metrics: The system is evaluated using various performance metrics, including accuracy, precision, and recall.

## Technologies Used
* Conda
* Python
* TensorFlow
* Keras

## Getting Started
To get started with 'nn-art-epoch-assignment', users can simply clone the GitHub repository and follow these installation instructions:

### Virtual Environment Setup
The virtual environment specifies which versions of software and packages this project uses. For this we are using the software conda. Conda is both a package manager and a virtual environment for data science-centric Python.

You can install Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html).

And use the following commands to create and activate the conda environment:

```bash
~/Documents/nn-art-epoch-assignment$ conda env create -f environment.yml
~/Documents/nn-art-epoch-assignment$ conda activate py38-nn-art-epoch-assignment
```

The setup for the virtual environment is complete. To check if everything worked, run the following command and see if the version matches.

```bash
(py38-nn-art-epoch-assignment) SOK1USH@MacBook-Pro-von-Lukas nn-art-epoch-assignment % python --version
Python 3.8.16
```


### Project Structure
```
|-- data
|-- docs
|-- results
|-- scripts
|-- src
|-- tests
 -- .gitignore
 -- environment.yml
 -- README.md
 -- setup.py
```

* **data**: Raw data for the project. (No source control)
* **docs**: Documentation, including Markdown and reStructuredText (reST). Calling it docs makes it easy to publish documentation online through Github pages.
* **results**: Results, including checkpoints, hdf5 files, pickle files, as well as figures and tables. (No source control if heavy).
* **scripts**: All scripts - Python and bash alike - as well as .ipynb notebooks.
* **src**: Reusable Python modules for the project. This is the kind of python code that you can import.
* **tests**: Tests for the code.

### Run scripts
Tell Python where to look for the library code to run own scripts. Once the package is locally installed, it can be easily used regardless of which directory you’re in. 
```bash
(py38-nn-art-epoch-assignment) ~/Documents/nn-art-epoch-assignment $ pip install -e .
```
The '.' indicates that we’re installing the package in the current directory. The '-e' indicates that the package should be editable. That means that if you change the files inside the src folder, you don’t need to re-install the package for your changes to be picked up by Python.

## Contributing
Even if the repository is public, it is a private study project. Contributions are only permitted from Steffen, Benedikt and Lukas.
Therefore other contributions to 'nn-art-epoch-assignment' are currently not welcome and encouraged! Users can not contribute to the project by submitting bug reports, feature requests, or even code contributions. Pull requests will not be reviewed by the project maintainers and merged if they meet the project's quality standards.

## License
'nn-art-epoch-assignment' is licensed under the MIT License, which allows for unrestricted use, modification, and redistribution of the code.