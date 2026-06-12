import re
from pyspellchecker import SpellChecker
from typing import List, Dict

MAX_WORDS = 30

FILLER_WORDS = {
    "please", "kindly", "actually", "basically", "just", "really", "very",
    "if you don't mind", "kind of", "sort of", "i mean",
    "to be honest", "honestly", "frankly"
}

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
    r"\bthe reason why\b": "why",
    r"\bservice continuity\b": "uptime"
}

VERB_MAP = {
    r"\b(write|create|generate)\b.*\bpython\b.*\bhello\s*world\b": "Write Python code to print Hello World",
    r"\b(print|print out|display)\b.*\bhello\s*world\b": "Print Hello World",
    r"\b(write|create|generate)\b.*\bpython\b": "Write Python code",
    r"\b(write|create|generate)\b.*\bcode\b": "Write code",
    r"\b(write|create)\b.*\bsummary\b": "Summarize",
    r"\bsummarize\b": "Summarize",
    r"\bexplain\b": "Explain",
    r"\bdescribe\b": "Describe",
    r"\blist\b": "List",
    r"\bcompare\b": "Compare",
    r"\bdefine\b": "Define",
    r"\bdraft\b": "Draft"
}

# Initialize spell checker once at module level
spell = SpellChecker()

# Compile regex pattern for filler words for better performance
FILLER_PATTERN = r"\b(" + "|".join(re.escape(w) for w in FILLER_WORDS) + r")\b"


def _normalize(text: str) -> str:
    """Normalize text by replacing quotes, stripping whitespace, and collapsing spaces."""
    if not text:
        return ""
    text = text.replace("'", "'")
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _clean_punctuation(text: str) -> str:
    """Remove or replace special punctuation characters."""
    text = re.sub(r"[""\"`]", "", text)
    text = re.sub(r"[!?;:]+", ".", text)
    text = re.sub(r"[\(\)\[\]]", "", text)
    return text


def _remove_filler_words(text: str) -> str:
    """Remove common filler words from text."""
    return re.sub(FILLER_PATTERN, "", text, flags=re.IGNORECASE)


def _apply_replacements(text: str) -> str:
    """Apply predefined phrase replacements to optimize text."""
    for pat, repl in REPLACEMENTS.items():
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    return text


def _force_imperative(text: str) -> str:
    """Convert polite requests to imperative mood."""
    text = re.sub(r"^(could|can|would)\s+you\s+(please\s+)?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^please\s+(could|can|would)\s+you\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^please\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^i\s+(want|need)\s+(you\s+to\s+)?", "", text, flags=re.IGNORECASE)
    return text.strip()


def _map_to_canonical(text: str) -> str:
    """Map text to canonical verb forms."""
    lowered = text.lower()
    for pat, verb in VERB_MAP.items():
        if re.search(pat, lowered):
            if verb.endswith("Hello World") or verb.startswith("Write Python code to"):
                return verb
            new_text = re.sub(pat, "", text, flags=re.IGNORECASE).strip()
            new_text = re.sub(r"^(of|about|the)\s+", "", new_text, flags=re.IGNORECASE)
            if new_text:
                return f"{verb} {new_text}"
            return verb
    return text


def _correct_spelling(text: str) -> str:
    """Correct spelling errors in text using spell checker."""
    try:
        words = text.split()
        corrected = []
        for word in words:
            if word.lower() in spell:  # known word
                corrected.append(word)
            else:
                corrected_word = spell.correction(word)
                corrected.append(corrected_word if corrected_word else word)
        return " ".join(corrected)
    except Exception as e:
        print(f"Warning: Spell correction failed: {e}")
        return text


def _trim_words(text: str, max_words: int = MAX_WORDS) -> str:
    """Trim text to a maximum number of words."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words])


def _final_cleanup(text: str) -> str:
    """Perform final cleanup: normalize spaces, strip punctuation, capitalize."""
    text = re.sub(r"\s+", " ", text).strip()
    text = text.strip(" .,-")
    if text:
        text = text[0].upper() + text[1:]
    return text


def optimize_prompt(prompt: str) -> str:
    """
    Optimize a prompt by applying a series of transformations.
    
    Args:
        prompt: The input prompt text to optimize
        
    Returns:
        Optimized prompt text
    """
    text = _normalize(prompt)
    text = _correct_spelling(text)
    text = _clean_punctuation(text)
    text = _remove_filler_words(text)
    text = _apply_replacements(text)
    text = _force_imperative(text)
    text = _map_to_canonical(text)
    text = _apply_replacements(text)
    text = _trim_words(text)
    text = _final_cleanup(text)
    return text


def optimize_suggestions(prompt: str) -> List[Dict[str, str]]:
    """
    Generate multiple optimization suggestions for a prompt.
    
    Args:
        prompt: The input prompt text
        
    Returns:
        List of dictionaries with different optimization styles
    """
    base = optimize_prompt(prompt)
    short = " ".join(base.split()[:6])
    balanced = base
    formal = _normalize(prompt)
    formal = _correct_spelling(formal)
    formal = _clean_punctuation(formal)
    formal = _remove_filler_words(formal)
    formal = _apply_replacements(formal)
    formal = _force_imperative(formal)
    formal = _map_to_canonical(formal)
    formal = _apply_replacements(formal)
    formal = _trim_words(formal, max_words=40)
    formal = _final_cleanup(formal)
    return [
        {"style": "short", "text": short},
        {"style": "balanced", "text": balanced},
        {"style": "formal", "text": formal}
    ]
