```markdown
# Cross‑Sections and Dimensions Tool
*A LiDAR‑based GIS tool for automated stream cross‑section extraction and bankfull width delineation.*

https://img.shields.io/badge/license-MIT-green
https://img.shields.io/badge/Python-ArcPy%20(ArcGIS%20Pro)-blue
https://img.shields.io/badge/status-Research%20Tool-blueviolet
https://img.shields.io/badge/GIS-ArcGIS%20Pro-orange

---

## Table of Contents
- #overview
- #key-features
- #method-summary
- #repository-structure
- #installation
- #how-to-run
- #parameters
- #outputs
- #example-workflow
- #performance--validation
- #limits-of-applicability
- #citation-giscience--remote-sensing
- #contact
- #license

---

## Overview
The **Cross‑Sections and Dimensions Tool** is a deterministic GIS workflow that:
1. Generates warped, perpendicular cross‑sections from a stream centreline  
2. Extracts elevation and slope from high‑resolution DEMs  
3. Applies a slope‑threshold method to identify bank edges  
4. Produces levelled bankfull width lines and polygons  
5. Saves all intermediate datasets to a structured geodatabase for transparency

Validation across **191 km** of streams in Greater Melbourne shows:
- **F1 Score:** 0.74  
- **Mean Absolute Error (bankfull elevation):** 0.6 m  
The tool performs best for streams of **Strahler order ≥ 5** with **<80% canopy cover**.

---

## Key Features
- Automated station points, 2D cross-sections, 3D profiles, and bankfull polygons  
- Warp‑based cross‑section construction avoids intersecting lines  
- Slope-threshold method is clear, deterministic, and reproducible  
- All intermediate datasets stored in a geodatabase  
- Modular functions make calibration easy (interval, half‑width, slope threshold)

---

## Method Summary

### Main Steps
1. Dissolve stream lines  
2. Generate evenly spaced station points  
3. Create warped 2D cross-sections  
4. Sample elevation and slope from DEM  
5. Detect high-gradient bank edges  
6. Level cross-sections using lower bank elevation  
7. Create bankfull lines and polygons  
8. Apply optional smoothing using linear regression (batch-based)

### Workflow Diagram
(Add these images in a `/docs` folder)
- `/docs/workflow.png`
- `/docs/xsections.png`
- `/docs/bank_detection.png`
- `/docs/bfw_polygons.png`

---

## Repository Structure

```

.
├─ JK\_KR\_x\_sections.py                  # Entry point script
├─ JK\_KR\_x\_sections\_functions.py        # Core functions
├─ /docs                                # Add diagrams/screenshots here
├─ LICENSE
└─ README.md

````

---

## Installation

### Requirements
- ArcGIS Pro (ArcPy)
- Python 3.x (ArcGIS Pro environment)
- LiDAR DEM (1 m recommended)
- Stream centreline polyline dataset  

### Steps
1. Clone the repository  
   ```bash
   git clone https://github.com/yourusername/CrossSectionsDimensionsTool.git
````

2.  Place the two Python files in your ArcGIS project folder
3.  (Optional) Add `JK_KR_x_sections.py` as a Script Tool in a `.tbx`
4.  Ensure DEM + stream layer use same CRS
5.  Choose projection when running (GDA94 or GDA2020 MGA Zone 55)

***

## How to Run

Run inside ArcGIS Pro's Python window, or as a Script Tool.

The script will ask for:

*   Function ID (1–4)
*   Project folder
*   Stream path
*   DEM path
*   Station spacing
*   Cross‑section width
*   Slope threshold
*   Projection

### Function IDs

*   **1** → Station points
*   **2** → + 2D cross-sections
*   **3** → + 3D cross-sections
*   **4** → + Bankfull width (final outputs)

***

## Parameters

| Parameter           | Description                                    |
| ------------------- | ---------------------------------------------- |
| Station interval    | 5–1000 m (default 25)                          |
| Cross-section width | 20–100 m (default 60; half-width = 30)         |
| Slope threshold     | 5–15° (default 7°; calibrated value often 11°) |
| Projection          | GDA94 or GDA2020 MGA55                         |

***

## Outputs

All outputs stored in:

    /x_sec_outputs.gdb/

Includes:

*   `station_points_<interval>`
*   `x_sec_i<interval>_w<halfwidth>`
*   `..._3D`
*   `..._3D_pts`
*   `..._s<slope>_levelled_pts`
*   `..._s<slope>_levelled_lines`
*   `..._s<slope>_levelled_poly`
*   `..._corrected` versions (after smoothing)

***

## Example Workflow

1.  Run Function ID **3**
2.  DEM sampled → 3D cross-sections created
3.  Test slope thresholds (7–13°) for calibration
4.  Choose best value (11° in Melbourne case study)
5.  Run Function ID **4** with final slope threshold
6.  Inspect bankfull polygons in GIS

***

## Performance & Validation

*   **F1 score:** 0.74
*   **Precision:** 0.72
*   **Recall:** 0.76
*   **MAE:** 0.6 m for bankfull elevation
*   Strongest performance in medium‑large streams with moderate canopy
*   Tool fails intentionally where bank edges cannot be detected

***

## Limits of Applicability

*   Sensitive to DEM quality, canopy, and very small channels (<5 m)
*   Cannot detect banks in piped, filled, or extremely shallow channels
*   Requires ArcGIS Pro (ArcPy); not yet compatible with QGIS

***

## Citation (GIScience & Remote Sensing)

> Kunapo, J., & Russell, K. (2026). *Cross-Sections and Dimensions: A LiDAR-Based GIS Tool for Bankfull Channel Mapping.* GIScience & Remote Sensing (under review).

***

## Contact

**Dr Joshphar Kunapo**  
Waterway Ecosystem Research Group  
University of Melbourne  
📧 <jkunapo@unimelb.edu.au>

***

## License

MIT License – See LICENSE file.

