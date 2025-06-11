import unittest
from organizador import Lesson, schedule_lessons

class TestScheduler(unittest.TestCase):
    def test_all_lessons_allocated(self):
        lines = [
            "Aula 1 - Prof. A 60min",
            "Aula 2 - Prof. B 45min",
            "Aula 3 - Prof. A 30min",
            "Aula 4 - Prof. C lightning",
            "Aula 5 - Prof. B 30min",
        ]
        lessons = [Lesson.from_string(line) for line in lines]
        schedule = schedule_lessons(lessons)
        self.assertTrue(all(l.allocated for l in lessons))

    def test_conflict_avoidance(self):
        # Duas aulas longas do mesmo professor: devem estar em sessões separadas
        lines = [
            "Aula A - Prof. A 180min",
            "Aula B - Prof. A 180min",
        ]
        lessons = [Lesson.from_string(line) for line in lines]
        schedule = schedule_lessons(lessons)

        prof_times = {}
        for day in schedule:
            for session in ["morning", "afternoon"]:
                for time_str, lesson in day[session]:
                    start = int(time_str[:2]) * 60 + int(time_str[3:])
                    end = start + lesson.duration
                    if lesson.professor not in prof_times:
                        prof_times[lesson.professor] = []
                    for s, e in prof_times[lesson.professor]:
                        self.assertTrue(end <= s or start >= e, "Conflito detectado")
                    prof_times[lesson.professor].append((start, end))

if __name__ == "__main__":
    unittest.main()
