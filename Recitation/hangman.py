from random import randint ;

print("Welcome to hangman")

words = ['apple','desk','class','name']

Max_Wrong_Attempt = 5;

while True:
	num = randint(0, 3);
	word = words[num];

	empty_word= ['_' for i in word];

	wrong_attempts = 0;

	while wrong_attempts < Max_Wrong_Attempt:
		print("Word: "+str(empty_word)+"\n")		

		if not '_' in empty_word:
			break;
		
		c = input("Enter a character\n");
		if c in word:
			print("Great Job\n");
			for i, char in enumerate(word): 
				if char == c:
					empty_word[i]=c;
		else:
			print("Wrong letter..\n");
			wrong_attempts+=1;

	if '_' in empty_word:
		print("!!!!!!!! You lost. The word was "+word+" !!!!!!!!!\n")
	else:
		print("!!!!!!!!! You Won !!!!!!!!!\n")