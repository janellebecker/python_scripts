# -*- coding: utf-8 -*-
#This variable tells you my name
name = 'janelle' #can i comment here? yes 
z= ' is awesome'
print (name + z)

print (2/3) #yields 0.666
print (2//3) #yields 0

#########################TASK 2########################################
x = 5 + 4
y = x/10

print (x)
print (y)

string1 = 'this is a test'
string2 = " let's see if it works"

combo = string1 + string2

print combo

combo_length = len(combo)

print "the length of combo is " + str(len(combo)) + "characters long"

a = [1,2, 3]
b=[4, 5, 6]
c= a + b

print c

dict1 = {first:janelle, last:becker}
list1 = [0, 1, dict1


##########################TASK 3###################################
favfood = ['pork chops', 'cake', 'indian']

print len(favfood[1])

dict_pet = {'name': 'marty', 'species': 'cat', 'num_legs': '4'}

# You can change items in dictionaries
# You can add items to dictionaries 
dict_pet['name'] = 'dakota' 
dict_pet['adopt'] = 'pending'

print dict_pet

################################TASK 4###############################

scores = {'duke': 90, 'unc': 70, 'syracuse': 60, 'cal': 100}

if scores['duke'] > scores['unc']:
    print "Duke won!"
elif scores['duke'] < scores['unc']:
    print "UNC won!"
else:
    print "They tied!"




a_list = [1, 2, 3, 4]

for item in a_list:
    for item2 in a_list:
        print item2


###############################################################
#Goal: print each letter in a string on a new line
    #My attempt:
string3 = 'janelle'

for i in range(0, len(string3)):
    print string3[i]

#Cleaner version!
string3 = 'janelle'
for letter in string3:
    print letter


#Goal: print out all even numbers between 1-100

i=0
while i<101:
    print i
    i +=2
    
#ANother way:
for number in range(0,100):
    if number % 2 == 0:
        print number
#############################################################################

#didnt do this one:
# Make a dictionary and print out the values (hint - use .keys() to get a list of keys!).

###############################################################################

def add_two_numbers(a, b):
    return a+b

c = add_two_numbers(1, 2)
print c

def is_short_word(w):
    if len(w) < 8:
        return True
    else:
        False

word_list = ['janelle', 'becker']

for w in word_list:
    if is_short_word(w):
        print '&s is a short word!' % w
    else:
        print '%s is a long word.' % w

###################################################
#Goal: take two strings and return the longer one 

#My attempt:
def longer_string(first, last):
    a = len('first')
    b = len('last')
    if a > b:
        return first
        print "The longer word is " + str(first)
    elif a < b:
        return last
        print "The longer word is " + str(last)
    else: 
        return False
        print "The words are of equal length."

longer_string('janelle', 'becker')


list_of_strings = ['cat', 'dog', 'lizard']

###Fun and Games #2
def longest_string(list_of_strings):
    longest = ''
    for s in list_of_strings:
        longest = longer_string(s, longest):



###"HW": Fizz and buzz ---------------------------------------
#Print out the numbers between 1 and 100. 
#For every number divisible by 3, print out ‘fizz’ instead. 
#For every number divisible by 5, print out ‘buzz’ instead.

for i in range(0,100):
    if i %3==0:
        print 'fizz'
    elif i %5==0:
        print 'buzz'
    else:
        print i

#15 is divisible by both 3 and 5. i'm printing buzz

