import json


class Analysis:

    @staticmethod
    def get_skills(filename, freq):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        skills = {}
        dataCount = 0
        for d in data:
            if not d:
                continue
            dataCount += 1
            for tag in d.get("tags", []):
                skills[tag] = skills.get(tag, 0) + 1

        skills = {k: v / dataCount for k, v in skills.items() if v / dataCount >= freq}
        skills_sorted = sorted(skills, key=lambda x: skills[x], reverse=True)
        return {skill: skills[skill] for skill in skills_sorted}

    def analyze_vacancy_data(self, vacancy_data_filename, freq):
        tag = {}
        for key, value in self.get_skills(vacancy_data_filename, freq).items():
            tag[key] = value
        return tag


