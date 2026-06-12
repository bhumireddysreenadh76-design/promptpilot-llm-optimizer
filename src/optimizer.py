import re
from typing import List

# Filler words and short phrases to remove
FILLER_WORDS = {
    "please", "kindly", "actually", "basically", "just", "really", "very",
    "if you don’t mind", "if you don't mind", "kind of", "sort of", "i mean",
    "to be honest", "honestly", "frankly"
}

# Phrase replacements (verbose -> concise)
REPLACEMENTS = {
    r"\bin order to\b": "to",
    r"\bas soon as possible\b": "quickly",
    r"\ba large number of\b": "many",
    r"\bdue to the fact that\b": "because",
    r"\bprovide me with\b": "give",
    r"\bhelp me understand\b": "explain",
    r"\bi need it urgently\b": "urgent",
    r"\bwrite a summary of\b": "summarize",
    r"\bgive me details about\b": "describe",
    r"\bmake sure that\b": "ensure",
    r"\bvery important\b": "critical",
    r"\bfor the purpose of\b": "for",
    r"\bwith regard to\b": "about",
    r"\bthe reason why\b": "why"
}

# Verb mapping to canonical imperative verbs
VERB_MAP = {
    r"\bwrite (a )?summary\b": "Summarize",
    r"\bsummarize\b": "Summarize",
    r"\bexplain\b": "Explain",
    r"\bdescribe\b": "Describe",
    r"\blist\b": "List",
    r"\bcompare\b": "Compare",
    r"\bdefine\b": "Define",
    r"\bprovide\b": "Provide",
    r"\bcreate\b": "Create",
    r"\bdraft\b": "Draft"
}

MAX_WORDS = 25  # configurable token/word limit


def _normalize(text: str) -> str:
    text = text or ""
    text = text.strip()
    # normalize unicode apostrophes to ascii
    text = text.replace("’", "'")
    # collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text


def _remove_filler_words(text: str) -> str:
    # Remove filler words as whole words (case-insensitive)
    pattern = r"\b(" + "|".join(re.escape(w) for w in FILLER_WORDS) + r")\b"
    return re.sub(pattern, "", text, flags=re.IGNORECASE)


def _apply_replacements(text: str) -> str:
    for long_pat, short in REPLACEMENTS.items():
        text = re.sub(long_pat, short, text, flags=re.IGNORECASE)
    return text


def _force_imperative(text: str) -> str:
    """
    Convert polite/question forms into an imperative where possible.
    Examples:
      - "Could you explain X" -> "Explain X"
      - "Can you please summarize Y" -> "Summarize Y"
      - "I want a summary of Z" -> "Summarize Z"
    """
    # common polite patterns
    text = re.sub(r"^(could|can|would)\s+you\s+(please\s+)?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^please\s+(could|can|would)\s+you\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^i\s+want\s+(you\s+to\s+)?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^i\s+need\s+(you\s+to\s+)?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^please\s+", "", text, flags=re.IGNORECASE)
    return text


def _map_to_canonical_verb(text: str) -> str:
    """
    If the prompt contains a known verb phrase, rewrite the start to a canonical verb.
    Example: "please write a summary of AI" -> "Summarize AI"
    """
    lowered = text.lower()
    for pat, verb in VERB_MAP.items():
        if re.search(pat, lowered):
            # remove the matched verb phrase from text and prepend canonical verb
            new_text = re.sub(pat, "", text, flags=re.IGNORECASE).strip()
            # remove leading punctuation or 'of' connectors
            new_text = re.sub(r"^(of|about|the)\s+", "", new_text, flags=re.IGNORECASE)
            if new_text:
                return f"{verb} {new_text}"
            return verb
    return text


def _clean_punctuation(text: str) -> str:
    # Remove excessive punctuation but keep commas for lists and hyphens in words
    text = re.sub(r"[“”\"`]", "", text)
    # replace multiple punctuation with single space
    text = re.sub(r"[!?;:]+", ".", text)
    # remove stray parentheses but keep content
    text = re.sub(r"[\(\)

\[\]

]", "", text)
    return text


def optimize_prompt(prompt: str) -> str:
    """
    Main entry: returns a concise, imperative, token-efficient prompt string.
    Steps:
      1. Normalize whitespace and punctuation
      2. Remove filler words
      3. Apply dictionary replacements
      4. Force imperative style
      5. Map to canonical verb when possible
      6. Trim to MAX_WORDS and capitalize first word
    """
    if not prompt or not isinstance(prompt, str):
        return ""

    text = _normalize(prompt)
    text = _clean_punctuation(text)
    text = _remove_filler_words(text)
    text = _apply_replacements(text)
    text = _force_imperative(text)
    text = _map_to_canonical_verb(text)

    # collapse extra spaces again
    text = re.sub(r"\s+", " ", text).strip()

    # Trim to MAX_WORDS
    words: List[str] = text.split()
    if len(words) > MAX_WORDS:
        words = words[:MAX_WORDS]
        text = " ".join(words)

    # Capitalize first word (imperative style)
    if text:
        text = text[0].upper() + text[1:]

    return text
