"""
Project: Student Grade Tracker
Pre-Work Section C — Python Fundamentals
Estimated time: 45-60 minutes

Objective: Build a data processing script that reads student grades from
a CSV, calculates averages, assigns letter grades, and writes a summary report.

Your job: implement all the functions marked with # TODO.
Do NOT modify the function signatures or the main() function.
"""

import csv


# ============================================================
# FUNCTION 1: Load data from CSV
# ============================================================

def load_students(filepath: str) -> list[dict]:
    """
    Read student data from a CSV file.

    Each row becomes a dictionary. The CSV has columns:
    student_name, math, science, english, history

    Some cells may be empty strings (missing grades) — that's expected.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A list of dicts, one per student.
        Example: [{"student_name": "Alice", "math": "92", ...}, ...]

    Raises:
        FileNotFoundError: if the CSV file doesn't exist.
    """
    students = []               # Create an empty list to store the students

    try:
        with open(filepath, "r") as file:       # Read the students.csv and append the data to the empty students list
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)

        return students
    except FileNotFoundError:               # Handling the case that the program can't find the csv file
        print("Couldn't find that file. Please make sure the file is correct.")

        return []


# ============================================================
# FUNCTION 2: Calculate average, handling missing values
# ============================================================

def calculate_average(grades: list) -> float | None:
    """
    Calculate the average of a list of grade values.

    Grade values may be strings (from the CSV), empty strings, or numbers.
    Ignore any value that can't be converted to a float.

    Args:
        grades: A list of values (e.g., ["92", "88", "", "79"]).

    Returns:
        The average as a float, rounded to 1 decimal place.
        Returns None if there are no valid grades.
    """
    valid_grades = []               
    
    if not grades:                  # If there are no grades, return None
        return None

    for grade in grades:
        try:
            grade = float(grade)            
            valid_grades.append(grade)      # Try to append the grade to the valid_grades list
        except ValueError:                  # Skip over empty grade values
            continue

    if not valid_grades:                    # If there are no valid grades, return None
        return None
 
    return round(sum(valid_grades) / len(valid_grades), 1)  # Return the average of the grades
    


# ============================================================
# FUNCTION 3: Assign letter grade
# ============================================================

def get_letter_grade(average: float | None) -> str:
    """
    Convert a numeric average to a letter grade.

    Scale:
        90+  → "A"
        80-89 → "B"
        70-79 → "C"
        60-69 → "D"
        < 60  → "F"
        None  → "N/A" (no grades available)

    Args:
        average: The numeric average, or None.

    Returns:
        The letter grade as a string.
    """
    if average is None:                         
        return "N/A"      # Check to make sure average has a value, if not, return "N/A"
    
    if average >= 90:           # Take average and assign it to a letter grade
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"

# ============================================================
# FUNCTION 4: Generate summary report
# ============================================================

def generate_report(students: list[dict]) -> dict:
    """
    Generate a class summary report.

    Args:
        students: The list of student dicts from load_students().

    Returns:
        A dict with these keys:
            "total_students":   int — how many students
            "class_average":    float — average of all valid averages
            "highest_average":  float — the best average
            "lowest_average":   float — the lowest average
            "grade_distribution": dict — {"A": 3, "B": 5, ...}
            "students":         list of dicts, each with:
                                  name, average, grade
    """
        
    report = []                     # Create empty lists to store the values needed for the report
    averages = []
    total_students = len(students)
    grade_distribution = {          #Initialize a dictionary for the grades
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "F": 0,
        "N/A": 0
        }
    
    for student in students:        # Assign where to grab the grades from in the students.csv
        grades = [
            student["math"],
            student["science"],
            student["english"],
            student["history"]
        ]
        average = calculate_average(grades)         
        grade = get_letter_grade(average)
        if average is not None:
            averages.append(average)

        student_summary = {                     # Build the values for the report
            "name": student["student_name"],
            "average": average,
            "grade": grade
        }
        
        report.append(student_summary)


        if grade != "N/A":                      # If the student has a letter grade, increment it's count
            grade_distribution[grade] += 1



    if not averages:
        print("No value in averages.")
        class_average = None
        highest_average = None
        lowest_average = None
    else:
        class_average = round(sum(averages) / len(averages), 1)         # Calculating the values
        highest_average = max(averages)
        lowest_average = min(averages)

    return {
        "total_students": total_students,
        "class_average": class_average,
        "highest_average": highest_average,
        "lowest_average": lowest_average,
        "grade_distribution": grade_distribution,
        "students": report
    }

# ============================================================
# FUNCTION 5: Write report to a file
# ============================================================

def write_report(report: dict, filepath: str) -> None:
    """
    Write the summary report to a text file.

    Format example:
        ===========================
        STUDENT GRADE REPORT
        ===========================
        Total students: 15
        Class average:  81.3
        Highest average: 95.0
        Lowest average:  55.0

        Grade Distribution:
          A: 5
          B: 4
          ...

        Individual Results:
          Alice Johnson    Avg: 91.5  Grade: A
          ...

    Args:
        report:   The dict returned by generate_report().
        filepath: Path to write the report file.
    """
    with open(filepath, "w") as file:
        file.write("=" * 20 + "\n")                 # Writing formatting
        file.write("STUDENT GRADE REPORT\n")
        file.write("=" * 20 + "\n\n")

        file.write(f"Total students:  {report['total_students']}\n")        # Passing in values
        file.write(f"Class average: {report['class_average']}\n")
        file.write(f"Highest average: {report['highest_average']}\n")
        file.write(f"Lowest average: {report['lowest_average']}\n\n")

        file.write("Grade Distribution:\n") 
        for grade, count in report['grade_distribution'].items():
            file.write(f"{grade}: {count}\n")       # Pull the grade and the count from grade distribution and write it to the report

        file.write("\nIndividual Results:\n")
        for student in report['students']:
            file.write(f"{student['name']}   Avg: {student['average']}    Grade: {student['grade']}\n")             # Write the individual students and their information

# ============================================================
# MAIN — do not modify
# ============================================================

def main():
    print("Loading student data...")
    students = load_students("data/students.csv")
    print(f"Loaded {len(students)} students.")

    print("Generating report...")
    report = generate_report(students)

    print("\n--- Summary ---")
    print(f"Total students:   {report['total_students']}")
    print(f"Class average:    {report['class_average']}")
    print(f"Highest average:  {report['highest_average']}")
    print(f"Lowest average:   {report['lowest_average']}")

    print("\nGrade Distribution:")
    for grade, count in sorted(report["grade_distribution"].items()):
        print(f"  {grade}: {count}")

    print("\nTop 5 students:")
    sorted_students = sorted(
        [s for s in report["students"] if s["average"] is not None],
        key=lambda s: s["average"],
        reverse=True
    )
    for s in sorted_students[:5]:
        print(f"  {s['name']:<20} {s['average']:.1f}  ({s['grade']})")

    write_report(report, "grade_report.txt")
    print("\nReport written to grade_report.txt")


if __name__ == "__main__":
    main()
