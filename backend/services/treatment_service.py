"""
Treatment recommendation logic.

No database is used. Recommendations are generated from a curated,
in-memory knowledge base plus sensible generic fallbacks.
"""

from typing import Any

# Keys are normalized to lowercase "crop|disease"
TREATMENT_KNOWLEDGE_BASE: dict[str, dict[str, list[str]]] = {
    "corn|common rust": {
        "treatment": [
            "Apply a fungicide containing azoxystrobin or propiconazole at first sign of rust pustules.",
            "Remove and destroy heavily infected leaves to reduce spore spread.",
            "Repeat fungicide application every 10-14 days if conditions remain humid.",
        ],
        "prevention": [
            "Plant rust-resistant corn hybrids where available.",
            "Avoid overhead irrigation late in the day to reduce leaf wetness.",
            "Practice crop rotation and remove crop debris after harvest.",
        ],
    },
    "tomato|early blight": {
        "treatment": [
            "Apply chlorothalonil or copper-based fungicide at early symptom onset.",
            "Prune and remove lower infected leaves to improve airflow.",
            "Ensure consistent watering to reduce plant stress.",
        ],
        "prevention": [
            "Use mulch to prevent soil splash onto lower leaves.",
            "Rotate crops and avoid planting tomatoes in the same soil each year.",
            "Space plants adequately for good air circulation.",
        ],
    },
    "potato|late blight": {
        "treatment": [
            "Apply a fungicide with mancozeb or chlorothalonil as soon as symptoms appear.",
            "Remove and destroy infected plants immediately to prevent spread.",
            "Avoid working in fields when foliage is wet.",
        ],
        "prevention": [
            "Use certified disease-free seed potatoes.",
            "Ensure good field drainage and avoid excess moisture.",
            "Destroy volunteer potato plants and cull piles.",
        ],
    },
}

DEFAULT_TREATMENT = [
    "Isolate or remove severely affected plant parts to limit spread.",
    "Apply a broad-spectrum fungicide or bactericide suited to the symptom type.",
    "Consult a local agricultural extension office for a targeted treatment plan.",
]

DEFAULT_PREVENTION = [
    "Practice crop rotation each season.",
    "Avoid overhead watering; water at the base of the plant.",
    "Maintain proper plant spacing for airflow and monitor regularly for early symptoms.",
]


def get_treatment_recommendation(crop: str, disease: str) -> dict[str, Any]:
    """Return treatment and prevention steps for a given crop/disease pair."""
    key = f"{crop.strip().lower()}|{disease.strip().lower()}"
    entry = TREATMENT_KNOWLEDGE_BASE.get(key)

    if entry:
        return {
            "treatment": entry["treatment"],
            "prevention": entry["prevention"],
        }

    return {
        "treatment": DEFAULT_TREATMENT,
        "prevention": DEFAULT_PREVENTION,
    }
