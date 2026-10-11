"""
Fertilizer / nutrient recommendation logic.

No database is used. Recommendations are generated from a curated,
in-memory knowledge base plus sensible generic fallbacks.
"""

from typing import Any

FERTILIZER_KNOWLEDGE_BASE: dict[str, dict[str, list[str]]] = {
    "corn|common rust": {
        "recommended_fertilizers": [
            "Balanced NPK fertilizer (e.g. 10-10-10) applied at recommended field rates.",
            "Potassium-rich fertilizer to strengthen plant resistance to fungal stress.",
        ],
        "nutrient_notes": [
            "Avoid excess nitrogen, as lush growth can worsen fungal disease severity.",
            "Ensure adequate potassium and phosphorus for overall plant vigor.",
        ],
    },
    "tomato|early blight": {
        "recommended_fertilizers": [
            "Calcium-enriched fertilizer to strengthen cell walls.",
            "Balanced NPK fertilizer with moderate nitrogen levels.",
        ],
        "nutrient_notes": [
            "Excess nitrogen promotes soft, disease-prone foliage; keep it moderate.",
            "Maintain consistent calcium and potassium levels through the growing season.",
        ],
    },
    "potato|late blight": {
        "recommended_fertilizers": [
            "Balanced NPK fertilizer with adequate potassium for tuber development.",
            "Avoid high-nitrogen fertilizers during active blight outbreaks.",
        ],
        "nutrient_notes": [
            "High nitrogen encourages dense canopy growth, which raises humidity and blight risk.",
            "Potassium supports overall plant resilience and tuber quality.",
        ],
    },
}

DEFAULT_FERTILIZERS = [
    "Balanced NPK fertilizer (10-10-10 or similar) at standard field application rates.",
    "Organic compost or well-rotted manure to improve soil health.",
]

DEFAULT_NUTRIENT_NOTES = [
    "Avoid excess nitrogen when disease symptoms are present, as it can promote pathogen-friendly growth.",
    "Ensure balanced potassium and phosphorus levels to support plant recovery and resilience.",
]


def get_fertilizer_recommendation(crop: str, disease: str) -> dict[str, Any]:
    """Return fertilizer and nutrient guidance for a given crop/disease pair."""
    key = f"{crop.strip().lower()}|{disease.strip().lower()}"
    entry = FERTILIZER_KNOWLEDGE_BASE.get(key)

    if entry:
        return {
            "recommended_fertilizers": entry["recommended_fertilizers"],
            "nutrient_notes": entry["nutrient_notes"],
        }

    return {
        "recommended_fertilizers": DEFAULT_FERTILIZERS,
        "nutrient_notes": DEFAULT_NUTRIENT_NOTES,
    }
