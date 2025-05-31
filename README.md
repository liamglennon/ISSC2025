# ISSC2025: Code for Performance Evaluation of a Metal-Coated Headlamp Reflector Antenna for V2X Applications

This repository contains the code and data analysis tools supporting the paper:

**"Performance Evaluation of a Metal-Coated Headlamp Reflector Antenna for V2X Applications"**  
*Liam James Glennon, Luis Eduardo Partichelli Potrich, John Dooley*  
Maynooth University, ISSC 2025

## 📖 Overview
This project demonstrates a low-cost approach for rapid prototyping of antennas using 3D printing and metal coating. It includes:
- Measurement acquisition scripts
- S-parameter and radiation pattern processing
- Polar plot generation
- Performance evaluation of commercial vs. 3D-printed antenna configurations

## 🛠️ Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/liamglennon/ISSC2025.git
    cd ISSC2025
    ```
2. Install required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage
- Run measurement scripts:
    ```bash
    python acquire_measurements.py
    ```
- Process S-parameter data:
    ```bash
    python process_sparams.py
    ```
- Generate polar plots:
    ```bash
    python plot_polar.py
    ```
- Access example data files and documentation in the `/data` and `/docs` directories.

## 📊 Results
Results from the experiments confirm that:
- The 3D-printed reflector narrows the performance gap with COTS antennas (within 2–3 dB).
- Return loss and polar patterns are suitable for exploratory V2X and 5G antenna studies.

For more details, see the full paper in the `/docs` directory.

## 📬 Contact
For questions or contributions, please contact:  
📧 LiamJGlennon@gmail.com

---

© 2025 Liam James Glennon and contributors. Licensed under the [MIT License](LICENSE).
