
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("students.json")
PASSING_SCORE = 70


def load_students():
    """Load student records from JSON, or start with an empty list."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Saved data is invalid. Starting with no records.")
            return []

        for student in data:
            if (
                not isinstance(student, dict)
                or not isinstance(student.get("name"), str)
                or not isinstance(student.get("score"), int)
                or isinstance(student.get("score"), bool)
                or not 0 <= student["score"] <= 100
            ):
                print("A saved record is invalid. Starting with no records.")
                return []

        return data

    except (json.JSONDecodeError, OSError):
        print("Could not read students.json. Starting with no records.")
        return []


def save_students():
    """Save all student records to JSON."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
        return True
    except OSError:
        print("Error: Could not save student records.")
        return False


def get_score():
    """Ask for a valid score between 0 and 100."""
    try:
        score = int(input("Enter score (0-100): ").strip())
    except ValueError:
        print("Please enter a whole number.")
        return None

    if not 0 <= score <= 100:
        print("Score must be between 0 and 100.")
        return None

    return score


def add_student():
    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    score = get_score()
    if score is None:
        return

    students.append({"name": name, "score": score})

    if save_students():
        print(f"{name} added successfully!")


def show_all():
    if not students:
        print("No student records found.")
        return

    print("\n--- All Students ---")
    for student in students:
        print(f"{student['name']} - {student['score']}")


def show_passed():
    passed = [
        student for student in students
        if student["score"] >= PASSING_SCORE
    ]

    if not passed:
        print("No students have passed.")
        return

    print("\n--- Passed Students ---")
    for student in passed:
        print(f"{student['name']} - {student['score']}")


def search_student():
    name = input("Enter student name to search: ").strip().casefold()

    if not name:
        print("Name cannot be empty.")
        return

    matches = [
        student for student in students
        if student["name"].casefold() == name
    ]

    if matches:
        for student in matches:
            print(f"Found: {student['name']} - {student['score']}")
    else:
        print("Student not found.")


def update_student():
    name = input("Enter the name to update: ").strip().casefold()

    matches = [
        student for student in students
        if student["name"].casefold() == name
    ]

    if not matches:
        print("Student not found.")
        return

    if len(matches) > 1:
        print("Multiple students have that name. Search by a unique name first.")
        return

    score = get_score()
    if score is None:
        return

    old_score = matches[0]["score"]
    matches[0]["score"] = score

    if save_students():
        print(f"{matches[0]['name']}'s score updated: {old_score} -> {score}")
    else:
        matches[0]["score"] = old_score


def delete_student():
    name = input("Enter the name to delete: ").strip().casefold()

    matches = [
        student for student in students
        if student["name"].casefold() == name
    ]

    if not matches:
        print("Student not found.")
        return

    if len(matches) > 1:
        print("Multiple students have that name. Cannot safely delete.")
        return

    student = matches[0]
    confirm = input(
        f"Delete {student['name']} (score {student['score']})? Type yes to confirm: "
    ).strip().casefold()

    if confirm != "yes":
        print("Deletion cancelled.")
        return

    students.remove(student)

    if save_students():
        print(f"{student['name']} deleted successfully!")
    else:
        students.append(student)


def main():
    while True:
        print("\n===== Student Records Manager =====")
        print("1. Add student")
        print("2. Show all students")
        print("3. Show passed students")
        print("4. Search student")
        print("5. Update student score")
        print("6. Delete student")
        print("7. Exit")

        choice = input("Choose (1-7): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            show_all()
        elif choice == "3":
            show_passed()
        elif choice == "4":
            search_student()
        elif choice == "5":
            update_student()
        elif choice == "6":
            delete_student()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 7.")


students = load_students()

if __name__ == "__main__":
    main()
