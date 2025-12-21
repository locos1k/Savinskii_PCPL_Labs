import unittest
from main import (
    University, Faculty, FacultyUniversity,
    get_faculties_starting_with,
    get_universities_with_min_students,
    get_faculties_and_universities_many_to_many
)


class TestFacultyUniversityLogic(unittest.TestCase):
    def setUp(self):
        self.universities = [
            University(1, "МГТУ им. Н. Э. Баумана"),
            University(2, "ВШЭ"),
            University(3, "МФТИ"),
        ]

        self.faculties = [
            Faculty(1, "Информатика и системы управления", 1800, 1),
            Faculty(2, "Компьютерные науки", 1500, 2),
            Faculty(3, "Прикладная математика и информатика", 1600, 3),
            Faculty(4, "Физика", 1400, 3),
            Faculty(5, "Радиотехника", 900, 1),
            Faculty(6, "Инженерный бизнес и менеджмент", 1200, 1),
        ]

        self.faculty_universities = [
            FacultyUniversity(4, 3),
            FacultyUniversity(4, 2),
            FacultyUniversity(5, 1),
            FacultyUniversity(5, 3),
            FacultyUniversity(1, 1),
            FacultyUniversity(2, 2),
            FacultyUniversity(3, 3),
            FacultyUniversity(6, 1),
        ]

    def test_faculties_starting_with_I(self):
        result = get_faculties_starting_with("И", self.faculties, self.universities)
        expected = [
            ("Информатика и системы управления", "МГТУ им. Н. Э. Баумана"),
            ("Инженерный бизнес и менеджмент", "МГТУ им. Н. Э. Баумана"),
        ]
        self.assertEqual(result, expected)

    def test_min_students_by_university(self):
        result = get_universities_with_min_students(self.faculties, self.universities)
        expected = [
            ("МГТУ им. Н. Э. Баумана", 900),
            ("МФТИ", 1400),
            ("ВШЭ", 1500),
        ]
        self.assertEqual(result, expected)

    def test_many_to_many_relationship(self):
        result = get_faculties_and_universities_many_to_many(
            self.faculties, self.universities, self.faculty_universities
        )
        expected = [
            ("Инженерный бизнес и менеджмент", "МГТУ им. Н. Э. Баумана"),
            ("Информатика и системы управления", "МГТУ им. Н. Э. Баумана"),
            ("Компьютерные науки", "ВШЭ"),
            ("Прикладная математика и информатика", "МФТИ"),
            ("Радиотехника", "МГТУ им. Н. Э. Баумана"),
            ("Радиотехника", "МФТИ"),
            ("Физика", "МФТИ"),
            ("Физика", "ВШЭ"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()