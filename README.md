<h1 align="center"> AFusion: AlphaFold3 GUI(Graphical User Interface)</h1>

> Forked from [Hanziwww/AlphaFold3-GUI](https://github.com/Hanziwww/AlphaFold3-GUI)

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.10-blue.svg">
    <img src="https://img.shields.io/badge/Framework-Streamlit-green.svg">
    <img src="https://img.shields.io/badge/Model-AlphaFold3-orange.svg">
    <a href="https://pypi.org/project/afusion/">
        <img src="https://img.shields.io/badge/PyPI-afusion-purple.svg">
    </a>
    <a href='https://alphafold3-gui.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/alphafold3-gui/badge/?version=latest' alt='Documentation Status'>
    </a>
</p>

<p align="center">
    Transform your protein structure prediction workflow with AFusion - a sleek, intuitive graphical interface that makes AlphaFold3 accessible to everyone. Now with enhanced visualization capabilities!
</p>

**[Demo site](https://af3gui.streamlit.app/)** *(generate input JSON files ONLY)*

[**Usable visualization site**](https://af3vis.streamlit.app/) *(fully usable)*

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation and Running](#installation-and-running)
- [Usage](#usage)
  - [Launching AFusion](#launching-afusion)
  - [Using the GUI](#using-the-gui)
  - [Enhanced Visualization Features](#enhanced-visualization-features)
- [Documentation](#documentation)
- [ToDo](#todo)
- [Screenshots](#screenshots)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## ✨ Key Features

### Installation & Setup
- **GUI Installer**: Step-by-step visual installation wizard
- **Auto-Configuration**: Handles environment setup and dependencies

### Core Functionality
- **Visual Workflow**: Clean, modern interface for job configuration 
- **Multi-Entity Support**: Process proteins, RNA, DNA, and ligands
- **Advanced Options**: Customize MSA, templates, and modifications

### Execution & Control
- **🚀 Integrated Pipeline**: Direct AlphaFold3 execution from GUI
- **🖥️ Live Monitoring**: Real-time process tracking and console output
- **🧩 Batch Processing**: Python API for automated predictions

### **🌟 New Enhanced Visualization Features!**
- **Advanced 3D Visualization Styles**
  - Multiple view options (cartoon, stick, line, sphere)
  - Flexible coloring schemes (confidence, chain, secondary structure, rainbow)
  - Interactive residue selection and highlighting
  - Chain sequence viewer
- **Enhanced Export Capabilities**
  - Support for scientific formats (CIF, PDB)
  - 3D printing/CAD export (STL) with customizable resolution
  - Improved mesh generation
- **Improved Analysis Tools**
  - Enhanced PAE matrix visualization
  - Comprehensive confidence metrics display
  - Interactive chain analysis
  - Robust error handling and logging

[Previous sections remain the same through "Usage"]

### Enhanced Visualization Features

#### 1. Launch Visualization Interface
```bash
afusion visualization
```

#### 2. Visualization Controls
- **View Styles**: Choose between cartoon, stick, line, or sphere representations
- **Coloring Options**: 
  - Confidence-based coloring
  - Chain-based coloring
  - Secondary structure coloring
  - Rainbow coloring
  - Custom color selection
- **Selection Tools**:
  - Chain selection
  - Residue range selection
  - Interactive sequence viewer
  - Custom highlight colors

#### 3. Export Options
- **Scientific Formats**:
  - CIF format export
  - PDB format export
- **3D Printing/CAD**:
  - STL export with custom resolution
  - Optimized mesh generation
  - Multiple style options

#### 4. Analysis Features
- **Enhanced PAE Visualization**:
  - Interactive matrix display
  - Chain boundary visualization
  - Custom color schemes
- **Confidence Metrics**:
  - Comprehensive metric display
  - Interactive data tables
  - Visual representations

[Rest of the original content remains the same through "License"]

## Acknowledgements

- **Original Project**: Created by [Hanziwww](https://github.com/Hanziwww)
- **Enhanced Version**: Maintained by [Shivp1413](https://github.com/Shivp1413)
- **AlphaFold 3**: This GUI is designed to work with [AlphaFold 3](https://github.com/google-deepmind/alphafold3) by DeepMind
- **Streamlit**: AFusion is built using [Streamlit](https://streamlit.io/)
- **Contributors**: Thanks to all contributors to both the original and enhanced versions!

---

If you encounter any issues or have suggestions for improvements, please open an [issue](https://github.com/Shivp1413/AlphaFold3-GUI/issues) or submit a [pull request](https://github.com/Shivp1413/AlphaFold3-GUI/pulls).

Happy Folding! 🧬
