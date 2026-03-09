# seqdepcov_plot

**seqdepcov_plot** is a lightweight Python utility for visualising per-base sequencing depth and coverage from short-read alignments mapped to a reference genome.

The tool is designed for **genome-wide inspection of sequencing depth**, and is particularly suitable for chloroplast genomes, mitochondrial genomes, and small bacterial genomes. It produces **publication-ready figures** (PDF, SVG, PNG) with editable text and consistent layout across all output formats.

Current stable version: **v0.1.5**

---

## Key Features

- Generate genome-wide sequencing depth plots from `samtools depth` output
- Clean, minimal dependencies — no GUI required
- Publication-ready vector outputs:
  - **PDF** — embedded TrueType fonts (fonttype 42), journal-ready
  - **SVG** — fully editable text (Adobe Illustrator / Inkscape compatible)
  - **PNG** — high-resolution raster preview (300 dpi)
- Statistics summary displayed below the x-axis:
  - Genome length · Mean depth · Minimum depth · Maximum depth
- Compatible with **BAM files from any source** — CLI aligners or GUI tools (e.g. Geneious Prime)

---

## Repository Contents

```
seqdepcov_plot/
├── BAM_to_seqdepcovv0.1.5.py   — Generate per-base depth file from BAM
├── seqdepcov_plotv0.1.5.py     — Plot sequencing depth from depth file
├── README.md
└── LICENSE
```

> Only the **stable version (v0.1.5)** is provided. Earlier development iterations (v0.1.0–v0.1.4) were used for internal debugging and layout tuning and are not released.

---

## Requirements

### Software
- Python ≥ 3.8
- samtools ≥ 1.10
- BWA ≥ 0.7.17 *(Pipeline A only — CLI workflow from raw reads)*

### Python packages
- `matplotlib`
- `numpy`

Install Python dependencies:
```bash
pip install matplotlib numpy
```

Or via conda:
```bash
conda install -c conda-forge matplotlib numpy
```

---

## Usage

The workflow consists of two steps:

1. Generate a per-base depth file from a BAM file
2. Plot the depth profile across the genome

---

### Pipeline A — Full CLI workflow (raw reads → BAM → plot)

This pipeline is recommended for users who perform all analyses in the command line, starting from raw FASTQ files. It ensures full transparency and reproducibility.

**Step 1. Index the reference genome**
```bash
bwa index reference.fasta
```

**Step 2. Map reads to the reference genome**
```bash
bwa mem -t 8 reference.fasta reads_R1.fastq reads_R2.fastq > alignment.sam
```
> `-t 8` specifies 8 threads. Adjust according to your system.

**Step 3. Convert SAM to BAM**
```bash
samtools view -bS alignment.sam > alignment.bam
```

**Step 4. Filter paired-end reads (both mates mapped)**
```bash
samtools view -bF 12 alignment.bam > alignment.filtered.bam
```
> `-F 12` excludes read pairs where either mate is unmapped.
> This step is optional but recommended for cleaner depth profiles.

**Step 5. Sort the BAM file**
```bash
samtools sort -@ 8 alignment.filtered.bam -o alignment.sorted.bam
```

**Step 6. Index the sorted BAM file**
```bash
samtools index alignment.sorted.bam
```

**Step 7. Generate per-base depth file**
```bash
python BAM_to_seqdepcovv0.1.5.py alignment.sorted.bam sample_prefix
```

Output: `sample_prefix.depth.txt`

**Step 8. Plot sequencing depth**
```bash
python seqdepcov_plotv0.1.5.py sample_prefix.depth.txt sample_prefix
```

Output:
```
sample_prefix.pdf
sample_prefix.svg
sample_prefix.png
```

---

### Pipeline B — BAM-only workflow (GUI tools → plot)

This pipeline is designed for users who have already generated a BAM file using GUI-based software such as **Geneious Prime**, and wish to generate a reproducible depth plot from the command line.

**Step 1. Export BAM from Geneious Prime**

- Map reads to the reference genome in Geneious Prime
- Export the alignment as a **BAM file**
- Ensure the exported BAM is **coordinate-sorted**

**Step 2. Generate per-base depth file**
```bash
python BAM_to_seqdepcovv0.1.5.py exported.bam sample_prefix
```

Output: `sample_prefix.depth.txt`

**Step 3. Plot sequencing depth**
```bash
python seqdepcov_plotv0.1.5.py sample_prefix.depth.txt sample_prefix
```

Output:
```
sample_prefix.pdf
sample_prefix.svg
sample_prefix.png
```

---

## Interpretation Notes

### How sequencing depth is calculated

All depth values in this tool are computed using:

```
samtools depth -a -q 0 -Q 0
```

| Flag | Meaning |
|------|---------|
| `-a` | Report all positions, including zero-depth positions |
| `-q 0` | No mapping quality filter — all reads are counted |
| `-Q 0` | No base quality filter — all bases are counted |

This reports **raw per-base read coverage** directly from the BAM alignment, with no filtering, smoothing, or normalisation applied.

### Why depth values may differ from Geneious Prime

Users may observe differences between depth statistics reported by this tool and those displayed in **Geneious Prime** or other GUI-based software.

These differences arise because Geneious Prime applies **internal, proprietary algorithms** that may include:

- Fragment-level merging of overlapping read pairs
- Additional filtering or normalisation
- Visualisation smoothing

Because these algorithms are not publicly documented, they **cannot be exactly replicated** using standard command-line tools.

This tool therefore prioritises **reproducibility, transparency, and community-standard definitions of sequencing depth**, rather than attempting to replicate proprietary behaviour.

> In practice, **mean depth** values are generally comparable between tools. **Minimum depth** values are most sensitive to differences in counting method, and may differ substantially in regions of uneven coverage.

---

## Known Limitations

- Sequencing depth is calculated on a **per-read basis** using `samtools depth`. Fragment-level depth (collapsed paired-end reads) is not applied.
- For paired-end short-read data, both mates contribute independently to coverage if they overlap the same genomic position. This may result in higher depth values compared to fragment-aware GUI tools.
- For long-read sequencing data (e.g. Oxford Nanopore or PacBio), low per-base depth values may reflect the intrinsic characteristics of long reads rather than insufficient sequencing coverage.
- This tool does not perform read collapsing, smoothing, normalisation, or bias correction. It is intended for transparent visualisation of raw per-base sequencing depth.
- Interpretation of coverage patterns should always consider the sequencing technology, library preparation strategy, and read mapping parameters used.

---

## Output Format Details

| Format | Description |
|--------|-------------|
| `.pdf` | Embedded TrueType fonts (fonttype 42). Suitable for direct submission to journals. |
| `.svg` | Fully editable vector. Text is selectable and editable in Adobe Illustrator and Inkscape. |
| `.png` | 300 dpi raster. Suitable for quick inspection, presentations, and sharing. |

---

## Versioning Policy

Only **stable versions** are released publicly. Development and debugging iterations are not included.

| Version | Status | Notes |
|---------|--------|-------|
| v0.1.5 | Stable | Initial public release |
| v0.1.0–v0.1.4 | Internal | Development and layout debugging — not released |

---

## Citation

If you use this tool in your research, please cite as:

> Bao-Ngoc Mach (Vanness). *seqdepcov_plot: A Python utility for sequencing depth and coverage visualisation from BAM files.* GitHub. Version v0.1.5. https://github.com/bearlab999/seqdepcov_plot

---

## Acknowledgements

The conceptual foundation of this tool was inspired by the protocol and supplementary script published by **Chang Liu and colleagues**:

> Chang Liu et al. (2023) *Generating Sequencing Depth and Coverage Map for Organelle Genomes.* protocols.io.

I first encountered this work at the **MAKDA Workshop 2024**. While the scripts in this repository were written independently and differ substantially in implementation, the original protocol provided the initial motivation for developing a reproducible, command-line-based depth visualisation workflow.

---

## License

This project is released under the **MIT License**.
You are free to use, modify, and redistribute it with appropriate attribution.
See [LICENSE](LICENSE) for full details.

---

## Author

**Bao-Ngoc Mach (Vanness)**

*This tool was developed through iterative testing on real sequencing datasets.*
