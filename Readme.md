# bb_tags Repository

This repository contains tools and data for generating, managing, and decoding tags used in the BeesBook tracking system. The tags are represented in 12-bit or 16-bit formats, allowing for unique identification of individuals in the system.

---

## Repository Contents

### Files and Folders
- **Jupyter Notebooks**
- `BeesBookTagGenerator-PDF-multipage.ipynb`: Jupyter Notebook for interactively generating multi-page PDFs of BeesBook tags, suitable for printing.  Can set parameters of tag size, coding type (parity-based or hamming), parity type, and other drawing details.
- **Python Scripts**:
  - `BBTagGenFromList.py`: Script for generating tags from a provided list.
  - `Bee12bits.py`: Contains logic for 12-bit BeesBook tags, including parity-based separation of even and odd tags.
  - `Bee16bits.py`: Contains logic for handling 16-bit BeesBook tags.
  - `BeesBookTagGenerator.py`: Main script for generating BeesBook tags.
  - `BumbleBee12bits.py`: Script for working with Bumblebee-specific 12-bit tags.
- **testOutput**: Folder containing sample outputs and generated tag data for printing or testing purposes.

---

## Tag Encoding and Decoding in the BeesBook Pipeline

### 12-bit Tags
The 12-bit tag format supports **4096 unique tag IDs**, split based on parity:
1. **Even Tags**:
   - Binary numbers where `tag_number % 2 == 0`.
   - Mapped to the ID range **0 to 2047** in the decoding pipeline.

2. **Odd Tags**:
   - Binary numbers where `tag_number % 2 == 1`.
   - Mapped to the ID range **2048 to 4095** in the decoding pipeline.

### 16-bit Tags
Scripts in this repository also support generating and decoding 16-bit tags.