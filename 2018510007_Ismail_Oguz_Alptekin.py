import requests
from bs4 import BeautifulSoup


def takingBook():
    flag = True #for checking the book is valid or not
    book_name = input("Please enter the name of the book: ")
    while flag:
        fix_name = book_name.replace(" ", "_")
        global book_name_txt
        book_name_txt = "{}.txt".format(book_name)

        #for checking possible url's
        url = "https://en.wikibooks.org/wiki/{}/Print_version".format(fix_name)
        url_2 = "https://en.wikibooks.org/wiki/{}/print_version".format(fix_name)
        url_3 = "https://en.wikibooks.org/wiki/{}/Printable_version".format(fix_name)
        url_4 = "https://en.wikibooks.org/wiki/{}/All_Chapters".format(fix_name)
        r = requests.get(url) 
        if(r.status_code != 200): #if the url is connected it returns 200
            r = requests.get(url_2) 
            if(r.status_code != 200):
                r = requests.get(url_3)
                if(r.status_code != 200):
                    r = requests.get(url_4)
                    if(r.status_code != 200): 
                        book_name = input("The book did not found!\nPlease enter a valid book name: ")
                    else:
                        flag = False
                else:
                    flag = False
            else:
                flag = False
        else:
            flag = False   
    soup = BeautifulSoup(r.content, "html.parser").get_text() #it parses the contnet of the webpage with html.parser
    global all_content
    all_content = soup # it keeps all the words in the book
    return book_name #to keep book name returns it

def writingTxt():     
    file = open(book_name_txt, "w+")
    for content in all_content:
        try:
            file.write(content)
        except(UnicodeEncodeError): #if there is a char that can not readable, skip this char.
            continue
    file.close()
        
def readingTxt():
    f = open(book_name_txt, "r+")
    global all_text
    all_text = f.read()
    marks = '''0123456789!#$%&'()*,+-./:;<=>?@[\]^_`{|}~"''' 
    for i in all_text:
        if i in marks: 
            all_text = all_text.replace(i, " ") #for deleting punctuation marks, and numbers
    all_text = all_text.lower()
    f.close()

def addingDict():
    global word_dict
    word_dict = {}
    wordlist_raw = all_text.split(" ")
    wordlist = []
    #stop words' list
    stopwords = ["front","page"," ", "<p>", "</p>","<a","</a>","<h1>","</h1>","<ul>","</ul>","<li>","</li>","<ol>","</ol>","<tr>","</tr>","<tbody>","</tbody>","<td","</td>","<table","<div",'class="',"<center>","</center>","<b>","<b>","<br>","</br>","<>","<>","<>","<>","<>","<>","<>","<>","<>","\t", "\n", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "v", "y", "z", "q", "w", "x","about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along","already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere","empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find","fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had","has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how","however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least","less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself","name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often","on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put","rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so","some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them","themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those","though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until","up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein","whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet","you", "your", "yours", "yourself", "yourselves", "the"]

    #writing the words to another list without stop words
    for i in wordlist_raw:
        for j in stopwords:
            flag = True
            if(i == j):
                flag = False
                break
        if(flag and i != "" and i != " " and i.find("\n") == -1):
            wordlist.append(i.strip()) #it deletes the spaces in the words

    #adding to words with their numbers to a dictionary            
    for i in wordlist:
        if(word_dict.get(i) == None):
            word_dict[i] = 0
        if(word_dict.get(i) != None):
            count = word_dict.get(i) +1
            word_dict[i] = (count)        

def mostWords(book_name):

    while True:
        how_many = int(input("\nHow many most common words to print: "))
        if(how_many < len(word_dict) and how_many >= 0):
            break;
        print("Please enter a valid number!")
        
    most_dict = {}
    #for choosing most used words
    for i in range(0,how_many):
        max_num = 0; 
        most_word = ""
        for x,y in word_dict.items():
            if(y > max_num): #if the number of the words are bigger than we keep 
                most_word = x 
                max_num = y
        most_dict[most_word] = max_num #at the end of the inner loop, add the word to the list
        word_dict[most_word] = 0; #zeroise the value of the word that we added already for prevent repeating
    print("\nBOOK: ", book_name)
    print("NO WORD\t    FREQ_1")
    no = 1
    #printing the frequency list
    for x, y in most_dict.items():
        print(no, f"{x:10} {y:<10}")
        no += 1
        

def mostCommon(book1, book2, book_name_1, book_name_2):
    common_words = []
    for x,y in book1.items(): #if the word is common it adds to the common words list
        for a,b in book2.items():
            if(x == a):
                common_words.append([x,y,b,y+b]) #x: word y: freq_1 b: freq_2 y+b: freq_sum

    while True:
        how_many = int(input("\nHow many most most common words to print: "))
        if(how_many < len(common_words) and how_many >= 0):
            break;
        print("Please enter a valid number!")
    
    most_common = []
    for i in range(0,how_many): #it is the similar with the above
        max_num = 0;
        most_word = ""
        for x in common_words:
            if(x != 0 and (x[3]) > (max_num) and x[0] != ""):
                index = common_words.index(x)
                freq1 = x[1] 
                freq2 = x[2]
                most_word = x[0]
                max_num = x[3]
        most_common.append([most_word,freq1,freq2,max_num])
        common_words[index] = ["",0,0,0]

    #printing the frequency list
    print("\nMOST COMMON WORDS: ")
    print("\nBOOK 1: ",book_name_1,"\nBOOK 2: ",book_name_2)
    print(f"NO WORD\tFREQ_1\tFREQ_2\tFREQ_SUM")
    no = 1
    for x in most_common:
        print(no, f"{x[0]:10}{x[1]:<5}{x[2]:>5}{x[3]:>10}")
        no += 1
   
    
def mostDistinct(book1, book2, book_name_1, book_name_2):
    distinct_words_1 = {}
    distinct_words_2 = {}
    for x,y in book1.items():
        for a,b in book2.items():
            flag = True
            if(x == a):
                flag = False
                break
        if(flag):
            distinct_words_1[x] = y

    for x,y in book2.items():
        for a,b in book1.items():
            flag = True
            if(x == a):
                flag = False
                break
        if(flag):
            distinct_words_2[x] = y

    while True:
        how_many = int(input("\nHow many most used distinct words to print: "))
        if(how_many < len(distinct_words_1) and how_many < len(distinct_words_2) and how_many >= 0):
            break;
        print("Please enter a valid number!")
    
    
    print("\nDISTINCT WORDS: \n")
    most_dict_1 = {} #for book 1
    most_dict_2 = {} #for book 2
    for i in range(0,how_many): #to find the distinct words in book 1
        max_num = 0;
        most_word = ""
        for x,y in distinct_words_1.items():
            if(y > max_num):
                most_word = x
                max_num = y
        most_dict_1[most_word] = max_num
        distinct_words_1[most_word] = 0;

    #printing the frequency list
    print("BOOK 1: ", book_name_1)
    print("NO WORD\t    FREQ_1")
    no = 1
    for x, y in most_dict_1.items():
        print(no, f"{x:10} {y:<10}")
        no += 1

    for i in range(0,how_many): #to find distinct words in book 2
        max_num = 0;
        most_word = ""
        for x,y in distinct_words_2.items():
            if(y > max_num):
                most_word = x
                max_num = y
        most_dict_2[most_word] = max_num
        distinct_words_2[most_word] = 0;
    #printing the frequency list
    print("\nBOOK 2: " + book_name_2)
    print("NO WORD\t    FREQ_1")
    no = 1
    for x, y in most_dict_2.items():
        print(no, f"{x:10} {y:<10}")
        no += 1
    
                

def optionFirst():
    book_name = takingBook()
    writingTxt()
    readingTxt()
    addingDict()
    mostWords(book_name)
def optionSecond():
    book_name_1 = takingBook()
    writingTxt()
    readingTxt()
    addingDict()
    book1 = word_dict
    book_name_2 = takingBook()
    writingTxt()
    readingTxt()
    addingDict()
    book2 = word_dict
    mostCommon(book1, book2, book_name_1, book_name_2)
    mostDistinct(book1, book2, book_name_1, book_name_2)
    
    
while True: 
    option = input("1. Most used words in one book\n2. Comparison of two books\nYour choice: ")
    if( not(option.isdigit())): #if the input is not an integer
        print("Please choose valid option!")
    elif(int(option) == 1):
        optionFirst()
        break
    elif(int(option) == 2):
        optionSecond()
        break
    else:
        print("Please choose valid option!")
