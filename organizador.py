import re
from datetime import datetime, timedelta
from collections import defaultdict

class Lesson:
    def __init__(self, title, professor, duration):
        self.title = title
        self.professor = professor
        self.duration = duration  # em minutos
        self.allocated = False

    @classmethod
    def from_string(cls, line):
        match = re.match(r"(.+?) - (Prof\. .+?) (.+)", line.strip())
        if match:
            title, professor, duration_str = match.groups()
            duration = 5 if "lightning" in duration_str else int(duration_str.replace("min", ""))
            return cls(title, professor, duration)
        return None

def schedule_lessons(lessons):
    schedule = []  # Lista de dias com sessões de manhã e tarde
    day_index = 0

    while any(not l.allocated for l in lessons):
        day = {
            "day_name": f"📅 {['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'][day_index % 5]}-feira",
            "morning": [],
            "afternoon": []
        }
        prof_schedule = defaultdict(list)

        def can_allocate(professor, start_time, duration):
            end_time = start_time + timedelta(minutes=duration)
            for s, e in prof_schedule[professor]:
                if not (end_time <= s or start_time >= e):
                    return False
            prof_schedule[professor].append((start_time, end_time))
            return True

        def fill_session(start_str, end_str, session_key):
            start = datetime.strptime(start_str, "%H:%M")
            end = datetime.strptime(end_str, "%H:%M")
            current = start
            while current < end:
                for lesson in lessons:
                    if not lesson.allocated and can_allocate(lesson.professor, current, lesson.duration):
                        if current + timedelta(minutes=lesson.duration) <= end:
                            day[session_key].append((current.strftime("%H:%M"), lesson))
                            current += timedelta(minutes=lesson.duration)
                            lesson.allocated = True
                            break
                        else:
                            prof_schedule[lesson.professor].pop()
                else:
                    break

        fill_session("09:00", "12:00", "morning")
        fill_session("13:00", "17:00", "afternoon")
        schedule.append(day)
        day_index += 1

    return schedule

def print_schedule(schedule):
    for day in schedule:
        print(day["day_name"] + ":")
        for time, lesson in day["morning"]:
            print(f"{time} {lesson.title} - {lesson.professor} {lesson.duration}min")
        print("12:00 Intervalo para Almoço\n")
        if day["afternoon"]:
            for time, lesson in day["afternoon"]:
                print(f"{time} {lesson.title} - {lesson.professor} {lesson.duration}min")
        else:
            print("13:00 (sem aulas disponíveis)")
        print("17:00 Reunião de Professores\n")

def main():
    try:
        with open("aulas.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Erro: arquivo 'aulas.txt' não encontrado.")
        return

    lessons = [Lesson.from_string(line) for line in lines if line.strip()]
    schedule = schedule_lessons(lessons)
    print_schedule(schedule)

if __name__ == "__main__":
    main()
