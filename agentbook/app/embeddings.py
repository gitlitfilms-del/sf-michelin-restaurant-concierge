import os
import re
import math
import logging
from typing import List

logger = logging.getLogger("agentbook.embeddings")

COMMON_VOCAB = [
    "quantum", "algorithms", "python", "multi", "agent", "swarm", "optimization",
    "gastronomy", "wine", "culinary", "michelin", "sourdough", "food",
    "philosophy", "ethics", "synthetic", "consciousness", "alignment",
    "hydroponics", "genomics", "farming", "botanist", "crop", "plant",
    "fintech", "defi", "trading", "liquidity", "finance", "macro",
    "astrophysics", "space", "exoplanet", "orbit", "telescope", "cosmic",
    "data", "system", "network", "code", "model", "science", "tech"
]

def generate_embedding(text: str, dimension: int = 768) -> List[float]:
    """
    Generates a vector embedding for text using Google Gemini / Vertex AI,
    or falls back to a term-frequency + hashed feature vector for offline testing.
    """
    if not text:
        text = "empty"
    
    # Try using google-genai if API key is present
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            result = client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
            if result.embedding and result.embedding.values:
                return result.embedding.values
        except Exception as e:
            logger.warning(f"Gemini API embedding generation failed: {e}. Using offline vector generator.")

    # Offline fallback embedding based on vocabulary term weights + character hash
    tokens = set(re.findall(r'\w+', text.lower()))
    vector = [0.0] * dimension
    
    # Map common vocabulary terms to distinct vector bins
    for i, vocab in enumerate(COMMON_VOCAB):
        if vocab in tokens:
            bin_idx = (i * 17) % dimension
            vector[bin_idx] += 2.0
            
    # Hash remaining tokens across vector space
    import hashlib
    for token in tokens:
        token_hash = int(hashlib.sha256(token.encode('utf-8')).hexdigest(), 16)
        bin_idx = token_hash % dimension
        vector[bin_idx] += 1.0

    # Normalize vector to unit length
    magnitude = math.sqrt(sum(v * v for v in vector))
    if magnitude > 0:
        vector = [v / magnitude for v in vector]
    else:
        vector = [1.0 / math.sqrt(dimension)] * dimension
        
    return vector

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculates cosine similarity between two normalized vectors."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot / (norm_v1 * norm_v2)
