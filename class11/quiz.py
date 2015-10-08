import webapp2
import os
import random

from google.appengine.ext.webapp import template


# This question object will let us store our results.
class Question() :
  id = ''
  text = ''
  answers = []


# We'll use this function to load the questions and answers into an object.
def loadQuestions() :
  # This statement is used to split the current file's path into a directory and filename.
  pathparts = os.path.split(__file__);
  
  # We use this to create a full path to our questions file.
  path = os.path.join(pathparts[0], 'text/questions.txt')
  
  # q will hold the results we return.
  q = dict()
  
  # We'll iterate through the lines in the file...
  for line in file(path, 'r') :
    # ... and we'll split each line apart by tabs.
    parts = line.split('\t')
    if len(parts) > 3 :
      # Make sure there are at least 4 parts: an id, a question, a correct answer, and a wrong one.
      question = Question()
      question.id = parts[0]
      question.text = parts[1]
      question.answers = parts[2:]
      
      # Save the question object back to our result.
      q[question.id] = question
  return q


# We'll just use this convenience function to retrieve and render a template.
def renderTemplate(templatename, templatevalues) :
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  return template.render(path, templatevalues)
    
class MainPage(webapp2.RequestHandler) :
  def get(self) :
  
    # We'll assemble a set of questions from the ones saved in memory.
    myQuestions = []
    for q in questions :
      myQuestion = Question()
      myQuestion.id = questions[q].id
      myQuestion.text = questions[q].text
      myQuestion.answers = list(questions[q].answers)
      
      # This will shuffle the order of the answers so all users don't see the same thing.
      random.shuffle(myQuestion.answers)
      myQuestions.append(myQuestion)
    
    # After we're done, we'll shuffle the ordering.
    random.shuffle(myQuestions)
    
    template_values = {
      'questions' : myQuestions
    }
   
    self.response.out.write(renderTemplate('index.html', template_values))


class Grader(webapp2.RequestHandler) :
  def post(self) :
  
    # We'll collect our answers in a dictionary
    answers = dict()
    for i in range(1, 6) :
      # Note the call to .strip() below - this removes any trailing and leading whitespace.
      answers[str(i)] = self.request.get('q' + str(i)).strip()
    
    results = []
    
    # For every one of our answer IDs, we'll compare it against our original answer.
    for answerId in answers :
      if questions[answerId].answers[0] == answers[answerId] :
        results.append("Correct")
      else :
        results.append("Incorrect - '" + answers[answerId] + "'")
        
    template_values = {
      'results' : results
    }

    self.response.out.write(renderTemplate('results.html', template_values))
    
questions = loadQuestions()

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/submitquiz', Grader)
], debug=True)


















