# EduChain-AI

# Smart Education Recommendation System Using AI and Blockchain

An intelligent educational recommendation platform built using Python,
Streamlit, Machine Learning and blockchain-inspired technology.

## Features

- AI-powered personalized course recommendations.
- Student profile input.
- TF-IDF text vectorization.
- Cosine similarity matching.
- Course catalogue and search.
- SHA-256 blockchain hash-chain ledger.
- Blockchain integrity verification.
- Interactive Streamlit dashboard.

## Technologies

- Python
- Streamlit
- Pandas
- Scikit-learn
- SHA-256
- JSON

## Project Structure

```text
smart-education-recommendation-system/
│
├── app.py
├── recommender.py
├── blockchain.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── courses.csv
```

## Run Locally or in GitHub Codespaces

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start Streamlit

```bash
streamlit run app.py
```

### Step 3: Open the application

Streamlit will start on port 8501.

In GitHub Codespaces, open the Ports tab and select port 8501.

## How It Works

1. Students enter their academic profile.
2. The AI engine analyzes interests, skills and career goals.
3. TF-IDF converts course descriptions into numerical vectors.
4. Cosine similarity identifies relevant courses.
5. The system generates personalized recommendations.
6. Recommendation IDs are recorded in a SHA-256 hash-linked ledger.
7. The blockchain explorer verifies record integrity.

## Important Technical Note

This project implements a local blockchain-inspired hash-chain ledger.
It is not a decentralized blockchain, and local JSON storage does not
provide independent immutability or consensus.

The recommendation matching scores are similarity scores, not
predictions of student success.

## Future Scope

- Deep learning recommendation models.
- Student performance prediction.
- Smart contract integration.
- Certificate verification.
- Decentralized blockchain storage.
- Institution administration panel.

## License

MIT License.
