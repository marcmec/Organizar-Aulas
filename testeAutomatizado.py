import unittest
from organizador import Lesson, schedule_lessons

class TestScheduler(unittest.TestCase):
    def test_all_lessons_allocated(self):
        lines = [
            "Fundamentos de Robótica - Prof. Lucas 60min",
            "Classificação de Dados - Prof. Beatriz 45min",
            "Sensores Autônomos - Prof. Lucas 30min",
            "Impacto Ético da IA - Prof. Marina lightning",
            "Estruturas de Código - Prof. Beatriz 30min",
        ]
        lessons = [Lesson.from_string(line) for line in lines]
        schedule = schedule_lessons(lessons)
        self.assertTrue(all(l.allocated for l in lessons))

    def test_conflict_avoidance(self):
        lines = [
            "Processamento de Imagens - Prof. Lucas 180min",
            "Sistemas Autônomos - Prof. Lucas 180min",
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
