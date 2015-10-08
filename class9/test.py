import webapp2
import os
from google.appengine.ext.webapp import template

class GradeQuiz(webapp2.RequestHandler) :
  def post(self) :
    answer1 = self.request.get('q1')
    answer2 = self.request.get('q2')
    answer3 = self.request.get('q3')
    myHtml = '''
<html>
  <head>
    <link rel="stylesheet" href="css/style.css">
	<script src="scripts/script.js">
	</script>
  </head>
  <body>
    <h1>QUIZ TIME!</h1>
'''

    if (answer1 == 'q1a2') :
      myHtml += 'Question 1 is correct.<br>'
    else :
      myHtml += 'Question 1 is not correct.<br>'
 
    if (answer2 == 'q2a1') :
      myHtml += 'Question 2 is correct.<br>'
    else :
      myHtml += 'Question 2 is not correct.<br>'

    if (answer3 == 'q3a3') :
      myHtml += 'Question 3 is correct.<br>'
    else :
      myHtml += 'Question 3 is not correct.<br>'

    myHtml += '</body></html>'
    self.response.out.write(myHtml)
    
    
class MainPage(webapp2.RequestHandler) :
  def get(self) :
    myHtml = '''
<html>
  <head>
    <link rel="stylesheet" href="css/style.css">
	<script src="scripts/script.js">
	</script>
  </head>
  <body>
    <h1>QUIZ TIME!</h1>
	<form method="post" action="submitquiz">
	  <input type="hidden" name="q1" id="q1">
	  <div class="Question">What is your name?</div><br>
	  <div onclick="chooseAnswer(this.id);" class="Answer" id="q1a1">Sir Robin</div>
	  <div onclick="chooseAnswer(this.id);" class="Answer" id="q1a2">Sir Lancelot</div>
	  <div onclick="chooseAnswer(this.id);" class="Answer" id="q1a3">Sir Galahad</div>
	  <br><br><br>
	  <input type="hidden" name="q2" id="q2">
	  <div class="Question">What is your quest?</div><br>
	  <div onclick="chooseAnswer(this.id);" class="Answer" id="q2a1">I seek the grail.</div>
	  <div onclick="chooseAnswer(this.id);" class="Answer" id="q2a2">I seek the swallow.</div>
	  <div onclick="chooseAnswer(this.id);" class="Answer" id="q2a3">I don't know.</div>
	  <br><br><br>
	  <input type="hidden" name="q3" id="q3">
	  <div class="Question">What is the airspeed of an unladen swallow?</div><br>
	  <div onclick="chooseAnswer(this.id);" class="Answer" id="q3a1">22mph.</div>
	  <div onclick="chooseAnswer(this.id);" class="Answer" id="q3a2">3 knots.</div>
	  <div onclick="chooseAnswer(this.id);" class="Answer" id="q3a3">An African or European swallow?</div>
	  <br><br><br>
	  <input type="submit">
	</form>
  </body>
</html>
'''

    self.response.out.write(myHtml)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/submitquiz', GradeQuiz)
], debug=True)

app.run()