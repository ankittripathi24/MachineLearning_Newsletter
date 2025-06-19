import json
from datetime import datetime

class MessageFormatter:
    def __init__(self):
        with open('lessons/lessons.json', 'r') as f:
            self.lessons = json.load(f)['lessons']

    def get_todays_lesson(self):
        # Calculate which lesson to send based on days since start
        start_date = datetime(2024, 1, 1)  # Project start date
        days_passed = (datetime.now() - start_date).days
        lesson_index = days_passed % len(self.lessons)
        
        lesson = self.lessons[lesson_index]
        
        message = f"""
        🤖 Daily ML Lesson #{lesson['day']}

        📚 {lesson['title']}

        {lesson['content']}

        💻 Code Example:
        ```python
        {lesson['code_example']}
        📌 Additional Resources:
        {chr(10).join(['• ' + r for r in lesson['resources']])}
        """
        return message
