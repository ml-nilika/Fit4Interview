def calculate_final_score(text_score, voice_score):
    final = (0.7 * text_score) + (0.3 * voice_score)
    return int(final)