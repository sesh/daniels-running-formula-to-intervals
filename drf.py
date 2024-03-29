from .intervals import upload_to_intervals
import os
import sys


PACES = {
    "ST": ("105", "130"),
    "L": ("59", "74"),
    "E": ("59", "74"),
    "M": ("75", "84"),
    "T": ("83", "88"),
    "I": ("95", "100"),
    "R": ("105", "110"),
}


def convert(workout, metric=False):
    # cleanup some funk
    workout = workout.replace("×", "x")

    converted = []
    steps = [s.strip() for s in workout.split("+")]

    for step in steps:
        repeats = 1

        if "x" in step:
            repeats, step = step.split("x", 1)
            repeats = int(repeats)
            step = step.replace("(", "").replace(")", "")

        if "ST" in step:
            repeats = int(step.split("ST")[0].strip())

        for k in PACES:
            if k in step:
                strides = "ST" in step
                recovery = None

                if "w/" in step:
                    step, recovery = step.split("w/", 1)
                elif strides:
                    recovery = "1 min rest"

                step = step.replace(k, "")
                step = step.strip()

                for _ in range(repeats):
                    if "min" in step:
                        mins = int(step.replace("min", "").strip())
                        converted.append(
                            f"- {mins}m00 {PACES[k][0]}-{PACES[k][1]}% Pace"
                        )
                    elif strides:
                        converted.append(f"- 0m20 {PACES[k][0]}-{PACES[k][1]}% Pace")
                    else:
                        dist = int(step)

                        if dist > 50:
                            # probably meters
                            km = dist / 1000
                        elif not metric:
                            km = dist * 1.6
                        else:
                            km = dist

                        converted.append(
                            f"- {km:.2f}km {PACES[k][0]}-{PACES[k][1]}% Pace"
                        )

                    if recovery:
                        if "min" in recovery:
                            minutes, recovery_type = recovery.split("min")
                            minutes = int(minutes)

                            if recovery_type.strip() in [
                                "rest",
                                "rests",
                                "recovery between",
                            ]:
                                converted.append(f"- {minutes}m00 Rest")

                            if recovery_type.strip() in ["jg recoveries", "jg"]:
                                converted.append(f"- {minutes}m00 50-70% Pace")
                        else:
                            dist, recovery_type = recovery.strip().split(" ", 1)

                            dist = int(dist)

                            if dist > 30:
                                # probably meters
                                dist = dist / 1000
                            elif not metric:
                                dist = dist * 1.6

                            converted.append(f"- {dist:.2f}km 50-70% Pace")

    return "\n".join(converted)


if __name__ == "__main__":
    athlete_id = os.environ.get("INTERVALS_ATHLETE_ID") or input(
        "Intervals Athlete ID: "
    )
    api_key = os.environ.get("INTERVALS_API_KEY") or input("Intervals API Key: ")

    workout_name = input("Workout name: ")
    workout_str = input("Workout (Daniels' Formula): ")

    if not all([athlete_id, api_key, workout_name, workout_str]):
        sys.exit("All fields are required.")

    intervals_str = convert(workout_str, metric="--metric" in sys.argv)
    print(intervals_str)

    upload = input("Upload [yN]?")
    if upload == "y":
        upload_to_intervals(
            intervals_str, workout_name, athlete_id, api_key, "Daniels 2Q"
        )
