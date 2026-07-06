
from models.recommendation import PaperRecommendation


def top_k_similar(papers, similarity_matrix, paper_index, k=3):

    recommendations = []

    similarities = similarity_matrix[paper_index]

    for index, score in enumerate(similarities):

        if index == paper_index:
            continue

        recommendations.append(
            PaperRecommendation(
                title=papers[index].title,
                similarity=float(score),
                paper_index=index
            )
        )

    recommendations.sort(
        key=lambda x: x.similarity,
        reverse=True
    )

    return recommendations[:k]