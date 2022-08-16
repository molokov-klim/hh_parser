import json


class Analysis:



    def get_skills(self, filename, freq):
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

