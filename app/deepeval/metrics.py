import re


def tokenize(text):
    return set(re.findall(r"\b[a-z0-9]+\b", text.lower()))


def check_answer_relevancy(question, actual_output):
    question_words = tokenize(question)
    answer_words = tokenize(actual_output)

    stop_words = {
        "what", "is", "the", "a", "an", "of",
        "in", "to", "for", "and", "how"
    }

    question_words -= stop_words
    answer_words -= stop_words

    if not question_words:
        score = 0.0
    else:
        matching_words = question_words.intersection(answer_words)
        score = len(matching_words) / len(question_words)

    return {
        "metric": "Answer Relevancy",
        "score": round(score, 2),
        "passed": score >= 0.5
    }