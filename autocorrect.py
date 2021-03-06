import enchant
import nltk
import unicodedata
import bayes
from nltk import FreqDist
from nltk.corpus import brown
from nltk.corpus import twitter_samples
from enchant.tokenize import get_tokenizer


"""
Initializes the frequency distribution for nltk.corpus.brown
"""
def initialize():
    print 'Initializing...'

    # Get frequency list of brown
    print 'Getting frequency distribution of nltk.corpus.brown...'
    brown_list = [word.lower() for word in brown.words()]
    brown_freq_dist = FreqDist(brown_list)
    print 'Done with nltk.corpus.brown.'

    # Get frequency list of twitter
    print 'Getting frequency distribution of nltk.corpus.twitter_samples...'
    twitter_list = [uword.lower() for word in twitter_samples.strings() for uword in unicodedata.normalize('NFKD', word).encode('ascii','ignore')]
    twitter_freq_dist = FreqDist(twitter_list)
    print 'Done with nltk.corpus.twitter_samples.'

    # Get bayes
    print 'Getting best words from bayes...'
    best_bayes = bayes.import_bayes()
    print 'Done with bayes.'

    return brown_freq_dist, twitter_freq_dist, best_bayes

def tester():
    # Initialize lists
    freq_list, freq_list2, bayes_dict = initialize()
    testing_set = [('raning','raining'), ('rainning', 'raining'), ('writtings', 'writings'), ('loking', 'looking'), ('imature', 'immature'), ('haning', 'hanging'), ('furr', 'fur'), ('sxold', 'scold'), ('bacin', 'bacon'), ('thunder', 'thounder'), ('saled', 'sailed'), ('saild', 'sailed'), ('heroe', 'hero'), ('reporter', 'repoter'), ('heer', 'here')]
    cor = 0.0
    tot = 0.0
    print 'Done initializing.'

    for tup in testing_set:
        result = autocorrect(freq_list, freq_list, bayes_dict, "", tup[0])
        print tup[1] , ':' , result
        if tup[1] in result:
            cor += 1
        tot += 1

    print(cor/tot)

"""
Modified tester method that handles streams
"""
def streamer():
    # Initialize the two frequency lists
    freq_list, freq_list2, bayes_dict = initialize()
    pwl = enchant.request_pwl_dict("enchant_pwl.txt")
    curr, prev = "", ""
    print 'Done initalizing.'

    while True:
        letter = raw_input('Letter?  ')
        if letter in (' ', ''):
            print(autocorrect(freq_list, freq_list2, bayes_dict, prev, curr))
            prev = curr
            curr = ""
        else:
            curr += letter





def autocorrect(freq_list, freq_list2, bayes_dict, prev, word):
    d = enchant.Dict("en_US")
    words = d.suggest(word)
    for i in xrange(len(words)):
        words[i] = words[i].lower()

    if word not in words:
        words.append(word)

    scores = []


    for wordle in words:
        scores.append([wordle,(freq_list[wordle]+freq_list2[wordle])**0.7/(edit_distance(word, wordle) + 0.01)**1.8])
        if edit_distance(word, wordle) == 0 :
            scores[len(scores)-1][1] *= 6.0
            
            if d.check(wordle):
                scores[len(scores)-1][1] += 0.5
            else:
                scores[len(scores)-1][1] -= 0.5

        if prev in bayes_dict and wordle in bayes_dict[prev]:
            scores[len(scores)-1][1] *= 10.0

        if wordle == 'docker':
            scores[len(scores)-1][1] += 800.0

        if wordle == 'greylock':
            scores[len(scores)-1][1] += 150.0

        if wordle == 'hackfest':
            scores[len(scores)-1][1] += 150.0

        if wordle == 'invisiboard':
            scores[len(scores)-1][1] += 250.0



        
    scores = sorted(scores, key=lambda x: x[1])

    answer = scores[len(scores)-1][0]
    return answer




def edit_distance(word1, word2):
    
    word1 = word1.lower()
    word2 = word2.lower()

    dp = [[0 for x in range(len(word1)+1)] for x in range(len(word2)+1)]
    for let2 in range(len(word2) + 1):
        for let1 in range(len(word1) + 1):
            if let2==0:
                dp[let2][let1] = let1 * 2.0
            elif let1==0:
                dp[let2][let1] = let2 * 2.0
            elif word1[let1-1]==word2[let2-1]:
                dp[let2][let1] = dp[let2 - 1][let1 - 1]
            else:
                dp[let2][let1] = min(dp[let2 - 1][let1] + 1.2, dp[let2][let1 - 1] + 1.5, dp[let2 - 1][let1- 1 ] + mistype(word1[let1 - 1], word2[let2 - 1]))
    return dp[len(word2)][len(word1)]




def mistype(str1, str2):
    answer = 0
    assoc = [['q','z'], ['v', 'n', 'g', 'h'], ['x', 'd', 'f', 'v'], ['e', 's', 'w', 'r', 'f', 'c', 'x'], ['w', 's', 'd', 'f', 'r'], ['d', 'e', 'r', 't', 'g', 'v', 'c'], ['f', 't', 'h' ,'v', 'b'], ['g', 't', 'y', 'u', 'j', 'n', 'b'], ['u', 'j', 'k', 'l', 'o'], ['u', 'y', 'h', 'n', 'm', 'k'], ['j', 'm', 'u', 'i', 'l', 'o'], ['k', 'i', 'o', 'p', 'm'], ['n', 'j','k', 'l'], ['b', 'h', 'j', 'k', 'm'], ['i', 'k', 'l', 'p'], ['o', 'l'], ['w', 's', 'a'], ['e', 'd', 'f', 'g', 't'], ['q', 'a', 'z', 'x', 'd', 'c', 'e', 'w'], ['r', 'f', 'g', 'h', 'y'], ['y', 'h', 'j', 'k', 'i'], ['c', 'f' ,'g','b'], ['q', 'a', 's', 'd', 'e'], ['z', 'a', 's', 'd', 'c'], ['t', 'g', 'h', 'j', 'u'], ['a','s','x']]
    str1 = str1.lower()
    str2 = str2.lower()
    if str2 in assoc[ord(str1) - 97]:
        answer = 1
    else:
        answer = 2
    if str1 in ['a', 'q', 'w', 's', 'z', 'x'] or str2 in ['a', 'q', 'z', 'x', 's', 'w']:
        answer -= 0.5

    return answer


    

if __name__ == '__main__':
    #autocorrect(raw_input('Input a string: '))
    #edit_distance(raw_input('Input a string: '), raw_input('Input a string: '))
    #tester()
    streamer()





