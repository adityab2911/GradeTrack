def calculate_attendance(attended, conducted):
    if conducted <= 0:
        return 0

    return (attended / conducted) * 100

def classes_needed_for_target(attended, conducted, target_percentage):
    target = target_percentage / 100

    if conducted <= 0:
        return 0

    if (attended / conducted) >= target:
        return 0

    required = (target * conducted - attended) / (1 - target)

    return int(required + 0.999999)

def projected_attendance(
    attended,
    conducted,
    future_classes,
    future_attended
):
    total_attended = attended + future_attended
    total_conducted = conducted + future_classes

    if total_conducted <= 0:
        return 0

    return (total_attended / total_conducted) * 100