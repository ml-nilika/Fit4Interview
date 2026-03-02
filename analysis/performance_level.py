def get_performance_label(score):
    if score < 40:
        return "Needs Significant Improvement"
    elif score < 60:
        return "Developing"
    elif score < 80:
        return "Strong Candidate"
    else:
        return "Excellent Performance"
