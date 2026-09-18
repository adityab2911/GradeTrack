ALL_ACHIEVEMENTS = [
    {
        "icon": "🥉",
        "title": "Getting Started",
        "description": "You've started tracking your academic journey!",
        "rarity": "Common",
        "requirement": "Enter your CGPA"
    },
    {
        "icon": "📈",
        "title": "Rising Star",
        "description": "Your SGPA is improving!",
        "rarity": "Rare",
        "requirement": "Improve your SGPA between semesters"
    },
    {
        "icon": "🔥",
        "title": "Attendance Warrior",
        "description": "Your attendance is above 90%!",
        "rarity": "Rare",
        "requirement": "Reach 90% attendance"
    },
    {
        "icon": "💯",
        "title": "Perfect Attendance",
        "description": "100% attendance. Absolutely flawless!",
        "rarity": "Legendary",
        "requirement": "Reach 100% attendance"
    },
    {
        "icon": "🎯",
        "title": "Goal Crusher",
        "description": "You reached your CGPA target!",
        "rarity": "Epic",
        "requirement": "Reach your CGPA target"
    },
    {
        "icon": "🏆",
        "title": "Elite Performer",
        "description": "Your CGPA is 9.0 or higher!",
        "rarity": "Epic",
        "requirement": "Reach a CGPA of 9.0"
    },
    {
        "icon": "🎯",
        "title": "Attendance Target",
        "description": "You've reached your attendance goal!",
        "rarity": "Rare",
        "requirement": "Reach your attendance target"
    },
    {
        "icon": "🚀",
        "title": "Consistency King",
        "description": "You've maintained an SGPA of 8.0+!",
        "rarity": "Epic",
        "requirement": "Maintain 8.0+ SGPA in every semester"
    },
    {
        "icon": "⭐",
        "title": "Academic Comeback",
        "description": "Your SGPA improved by 1.0+ points!",
        "rarity": "Legendary",
        "requirement": "Improve SGPA by 1.0+ points"
    }
]


def get_achievements(
    cgpa=None,
    attendance=None,
    target_cgpa=None,
    target_attendance=None,
    semesters=None
):
    achievements = []

    # 🥉 Getting Started
    if cgpa is not None:
        achievements.append(ALL_ACHIEVEMENTS[0])

    # 📈 Rising Star
    if semesters and len(semesters) >= 2:

        first_sgpa = semesters[0]["sgpa"]
        latest_sgpa = semesters[-1]["sgpa"]

        if latest_sgpa > first_sgpa:
            achievements.append(ALL_ACHIEVEMENTS[1])

    # 🔥 Attendance Warrior
    if attendance is not None and attendance >= 90:
        achievements.append(ALL_ACHIEVEMENTS[2])

    # 💯 Perfect Attendance
    if attendance is not None and attendance >= 100:
        achievements.append(ALL_ACHIEVEMENTS[3])

    # 🎯 Goal Crusher
    if (
        cgpa is not None
        and target_cgpa is not None
        and cgpa >= target_cgpa
    ):
        achievements.append(ALL_ACHIEVEMENTS[4])

    # 🏆 Elite Performer
    if cgpa is not None and cgpa >= 9.0:
        achievements.append(ALL_ACHIEVEMENTS[5])

    # 🎯 Attendance Target
    if (
        attendance is not None
        and target_attendance is not None
        and attendance >= target_attendance
    ):
        achievements.append(ALL_ACHIEVEMENTS[6])

    # 🚀 Consistency King
    if semesters:

        all_strong = all(
            semester["sgpa"] >= 8.0
            for semester in semesters
        )

        if len(semesters) >= 2 and all_strong:
            achievements.append(ALL_ACHIEVEMENTS[7])

    # ⭐ Academic Comeback
    if semesters and len(semesters) >= 2:

        first_sgpa = semesters[0]["sgpa"]
        latest_sgpa = semesters[-1]["sgpa"]

        if latest_sgpa - first_sgpa >= 1.0:
            achievements.append(ALL_ACHIEVEMENTS[8])

    return achievements