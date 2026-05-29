from sklearn.cluster import KMeans
import numpy as np


def cluster_candidate(resume_score, match_score):
    # Create feature vector
    X = np.array([[resume_score, match_score]])

    # Dummy training data (simulate real clustering)
    training_data = np.array([
        [90, 85], [85, 80], [88, 82],   # strong
        [70, 60], [65, 55], [75, 65],   # moderate
        [40, 30], [50, 35], [45, 25]    # weak
    ])

    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(training_data)

    label = kmeans.predict(X)[0]

    if label == 0:
        return "Strong Fit"
    elif label == 1:
        return "Moderate Fit"
    else:
        return "Weak Fit"