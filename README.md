# Generali Data Challenge

Building an Insurance Recommendation System

The goal is to create an information retrieval system that benefits both users and the insurance company. Using real-world data, we aim to identify optional coverages to recommend to new users.

## Task

The challenge is fully described in ./slide/20250612_Data_challenge_TS - ENG.pdf.

## Implementation Approach

Our approach involves mapping users into a low-dimensional feature space using SVD.
This is conceptually similar to how LSI (Latent Semantic Indexing) works in information retrieval.

Once users are represented in this space, we can use KNN to find each new user's closest neighbors and leverage their coverage choices to generate personalized recommendations.

## Folder structures

**GeneraliDataChal**
├── **Data**
│ ├── garanzie.csv
│ └── merged_table.csv
├── Slide
│ └── 20250612_Data_challenge_TS - ENG.pdf
├── **Source**
│ ├── app.py
│ ├── dataloader.py
│ ├── engine.py
│ ├── enginee.py
│ ├── evaluation.py
│ └── svd.py
├── *LICENSE*
└── *README.md*
## Quick usage

> Insert here the snippet of code for the app usage.