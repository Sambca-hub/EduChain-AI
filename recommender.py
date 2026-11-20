
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EducationRecommender:

    def __init__(self, csv_path="data/courses.csv"):
        self.csv_path = csv_path
        self.courses = pd.read_csv(csv_path)

        self.courses = self.courses.fillna("")

        required_columns = [
            "course_id",
            "course_name",
            "category",
            "skills",
            "level",
            "description",
            "career"
        ]

        missing = set(required_columns) - set(self.courses.columns)

        if missing:
            raise ValueError(
                f"Missing course columns: {', '.join(sorted(missing))}"
            )

        self.courses["combined_text"] = (
            self.courses["course_name"].astype(str) + " " +
            self.courses["category"].astype(str) + " " +
            self.courses["skills"].astype(str) + " " +
            self.courses["description"].astype(str) + " " +
            self.courses["career"].astype(str)
        )

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.course_vectors = self.vectorizer.fit_transform(
            self.courses["combined_text"]
        )

    def recommend(
        self,
        interests,
        skills,
        career_goal,
        level="Beginner",
        top_n=5
    ):

        student_profile = " ".join([
            str(interests),
            str(skills),
            str(career_goal)
        ])

        if not student_profile.strip():
            return pd.DataFrame()

        student_vector = self.vectorizer.transform(
            [student_profile]
        )

        similarity_scores = cosine_similarity(
            student_vector,
            self.course_vectors
        ).flatten()

        results = self.courses.copy()
        results["similarity"] = similarity_scores

        level_map = {
            "Beginner": ["Beginner", "All Levels"],
            "Intermediate": [
                "Beginner",
                "Intermediate",
                "All Levels"
            ],
            "Advanced": [
                "Beginner",
                "Intermediate",
                "Advanced",
                "All Levels"
            ],
            "All Levels": [
                "Beginner",
                "Intermediate",
                "Advanced",
                "All Levels"
            ]
        }

        allowed_levels = level_map.get(
            level,
            ["Beginner", "All Levels"]
        )

        results = results[
            results["level"].isin(allowed_levels)
        ].copy()

        results = results.sort_values(
            by="similarity",
            ascending=False
        )

        results = results.head(top_n)

        results["match_percentage"] = (
            results["similarity"] * 100
        ).round(2)

        return results.reset_index(drop=True)
