# AI Movie Night Recommendation Tool 🎬

## 📌 Project Description
This project builds a movie recommendation system using various approaches: popularity-based filtering, collaborative filtering with user ratings, and semantic similarity using language model embeddings. It guides users through exploratory data analysis, building recommendation engines, and integrating all methods into a single unified tool.

Whether you're into action-packed blockbusters or indie dramas, this AI system can help you pick the perfect movie for your night based on data and AI-generated insights.

## 🧠 Skills & Techniques Used
- **Python (Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn)**
- **Recommender Systems** (popularity-based, collaborative filtering, embedding-based)
- **Natural Language Processing** (Sentence Transformers for text embeddings)
- **Exploratory Data Analysis (EDA)**
- **Data Merging, Filtering, and Pivoting**
- **Cosine Similarity for content-based recommendations**

## 🔍 Key Insights & Findings
- **Distribution analysis** revealed that most movies have mid-range ratings, with a few standout titles having significantly high vote counts or averages.
- **Popularity-based recommender** shows that movies like *Inception* and *The Dark Knight* consistently top the charts by both vote count and rating.
- **Collaborative filtering** uncovered nuanced recommendations like *Reservoir Dogs* for fans of *The Godfather*, emphasizing hidden user preference patterns.
- **Embedding-based recommendations** allow flexible user input in natural language, generating diverse suggestions based on themes or moods.

## 📊 Visualizations & Explanations

### 1. Distribution of `vote_average`
![Vote Average Distribution](example_plot.png)  
This histogram shows the frequency of vote averages across all movies. The majority of movies cluster between scores of 5 and 7, with fewer extremes.

### 2. Distribution of `vote_count`
This plot reveals that a small number of movies have very high vote counts. These are typically blockbusters or widely known films.

### 3. User Ratings Distribution
A histogram of user ratings shows that users tend to give mid to high ratings, with fewer low ratings.

> 💡 These visual insights helped design different filtering strategies and informed weighting when generating recommendations.

---

## 🔁 Recommendation Modes Included
- **Popularity-Based:** Recommends top movies by vote average or vote count.
- **Collaborative Filtering:** Suggests similar movies based on user rating behavior.
- **Semantic Search:** Uses sentence embeddings to recommend movies based on a user’s mood or text description (e.g., "a sci-fi thriller with emotional depth").

## 🧪 How to Use the Final Recommender
Use the `recommend_movies()` function with one of the following:
```python
recommend_movies(method='vote_average', top_n=5)
recommend_movies(method='similar_movies', movie_title='Inception', top_n=5)
recommend_movies(method='embedding', user_prompt=['The Matrix', 'Inception'], top_n=5)
