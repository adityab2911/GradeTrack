def calculate_cgpa(semesters):
    total_points = 0
    total_credits = 0

    for semester in semesters:
        sgpa = semester["sgpa"]
        credits = semester["credits"]

        total_points += sgpa * credits
        total_credits += credits

    if total_credits == 0:
        return 0

    return total_points / total_credits

def required_future_sgpa(
    current_cgpa,
    completed_credits,
    target_cgpa,
    remaining_credits
):
    if remaining_credits <= 0:
        return 0

    required_sgpa = (
        target_cgpa * (completed_credits + remaining_credits)
        - current_cgpa * completed_credits
    ) / remaining_credits

    return required_sgpa


def maximum_possible_cgpa(
    current_cgpa,
    completed_credits,
    remaining_credits
):
    if completed_credits < 0 or remaining_credits <= 0:
        return current_cgpa

    maximum_cgpa = (
        current_cgpa * completed_credits
        + 10 * remaining_credits
    ) / (completed_credits + remaining_credits)

    return maximum_cgpa