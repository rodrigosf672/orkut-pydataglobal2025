# Text Mining Orkut’s Community Data with Python: Cultural Memory, Platform Neglect, and Digital Amnesia

![Orkut screenshot from the Wayback Machine](images/orkut-wayback.png)

---

# PyData Global 2025
**Time:** 11:00–11:30 EST | **Date:** Dec. 9, 2025 | **Location:** [https://pydata.org/global2025](https://pydata.org/global2025)

[![](images/pydata-global.png)](https://pydata.org/global2025)

## Objective

This repository contains the full code, data, and presentation materials for a study of 124,988 recovered Orkut community names. The project reconstructs a small surviving portion of Orkut’s deleted communities and analyzes them using Python-based stylometry, semantic embeddings, and clustering. The goal is to surface linguistic patterns, cultural themes, and expressive registers from early Brazilian internet culture, and to demonstrate how computational methods can help recover and interpret fragments of lost digital platforms.


## Tools Used

- BeautifulSoup (HTML parsing)  
- Pandas (data processing)  
- SentenceTransformers (multilingual embeddings)  
- UMAP, HDBSCAN, KMeans (clustering + projection)  
- BERTopic (topic modeling)  
- Plotly (visualization)
- Positron IDE (Python editing + integrated terminal)  
- Data Explorer (CSV inspection, previews, summaries)  
- Quarto Previewer (live slides + reproducible report)

## Repository Structure

```
.
├── README.md                   # Project overview, instructions, talk abstract
├── _quarto.yml                 # Quarto project configuration
├── requirements.txt            # Python dependencies for reproducibility
│
├── orkut_analysis.qmd          # Full analysis: scraping, stylometry, embeddings, clustering
├── orkut-presentation.qmd      # PyData Global 2025 talk slides (Reveal.js)
├── orkut_scraper.py            # Wayback Machine HTML scraper using requests + BeautifulSoup
├── orkut_communities.csv       # Cleaned dataset of 124,988 community names
├── pink.scss                   # Custom SCSS theme for slides (Orkut-inspired design)
│
└── images/                     # All images, figures, and plot outputs
    ├── orkut-logo.png          # Orkut logo for slides + README
    ├── orkut-profile1.jpg      # Early Orkut profile screenshot
    ├── orkut-profile2.jpeg     # Later Orkut profile (friend-provided)
    ├── orkut-wayback.png       # Wayback Machine interface screenshot
    ├── rodrigo-about_me.jpg    # Slide photo
    │
    ├── plot1.png               # Language distribution
    ├── plot2.png               # UMAP semantic map
    ├── plot3.png               # Caps lock stylometry
    ├── plot4.png               # Miguxês stylometry
    ├── plot5.png               # BERTopic micro-topic bars
    ├── plot6.png               # BERTopic intertopic map
    ├── plot7.png               # Additional analysis plot
    ├── plot8.png               # Additional analysis plot
    ├── plot9.png               # Additional analysis plot
    └── plot10.png              # Sentiment distribution map
```

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Render the analysis:

```bash
quarto render orkut_analysis.qmd
```

Preview the presentation slides:

```bash
quarto preview orkut-presentation.qmd
```

## Disclaimers

By accessing or using this repository, you agree to the following terms:

- The materials in this repository are provided on an “as is” and “as available” basis for research and educational purposes only.
- No guarantees are made regarding accuracy, completeness, or suitability for any specific use. 
- By using this repository, you agree that all use is at your own risk, and that the author assumes no responsibility or liability for any damages, losses, or legal issues arising from your use, modification, or distribution of this code or data.
- Users are solely responsible for ensuring that their use of the included code and data complies with all applicable laws, platform terms of service, and ethical guidelines.
- Nothing in this repository should be interpreted as legal advice.

## Contact

Rodrigo Silva Ferreira  
rodrigosf672@gmail.com  
[LinkedIn](https://www.linkedin.com/in/rsf309/) | [GitHub](https://github.com/rodrigosf672)