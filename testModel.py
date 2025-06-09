from model import AiModel
aiModel = AiModel()

correctLessonName = ['拉康思想']

lesson = aiModel.genLesson(correctLessonName)

session = aiModel.genSession(lesson['content'][2]['session'][0], '拉康思想')

test = aiModel.genTest('拉康思想', lesson['content'][2])

print(lesson)
print(session)
print(test)
