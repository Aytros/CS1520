import webapp2
import os
import random

from google.appengine.ext.webapp import template

class Question() :
  id = ''
  text = ''
  answers = []
  
def loadQuestions() :
  path = os.path.join(os.path.split(__file__)[0], 'text/questions.txt')
  q = dict()
  
  for line in file(path, 'r') :
    parts = line.split('\t')
    if len(parts) > 3 :
      question = Question()
      question.id = parts[0]
      question.text = parts[1]
      question.answers = parts[2:]
      q[question.id] = question
  return q
  
def getTemplatePath(templatename) :
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  return path
    
questions = loadQuestions()

class MainPage(webapp2.RequestHandler) :
  def get(self) :
    myQuestions = []
    for q in questions :
      myQuestion = Question()
      myQuestion.id = questions[q].id
      myQuestion.text = questions[q].text
      myQuestion.answers = list(questions[q].answers)
      random.shuffle(myQuestion.answers)
      myQuestions.append(myQuestion)
    
    random.shuffle(myQuestions)
    
    template_values = {
      'questions' : myQuestions
    }
    path = getTemplatePath('index.html')
    
    self.response.out.write(template.render(path, template_values))

    
app = webapp2.WSGIApplication([
  ('/', MainPage)
], debug=True)





