'''
a decoder for a playfair cipher text

simply run the command
"python playfair_decoder.py PLAYFAIRCIPHERTEXT [log file name]"

based on the genetic evolution algorithm described in G. Negara's paper "n Evolutionary Approach for the Playfair Cipher Cryptanalysis"
https://pdfs.semanticscholar.org/fb4d/da978b245101f2e711ffe643e336747b8d7d.pdf?fbclid=IwAR18MzPTBIHXo0UbFO26bzI94P4zmt4Et1_SgfZEOyJfsa-NBPqooDQLpYE

the fitness function used was acquired from:
http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams
'''

import sys
import random
import ngram_score
import math

KEY_CHARS = ['A','B','C','D','E','F','G','H','I','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
KEY_SIZE = 25

with open('english_quadgrams.txt') as f:
    ngram = ngram_score.ngram_score(f)

def get_rand_pair(a, b):
    r1 = random.randint(a, b)
    r2 = random.randint(a, b)
    while r2 == r1:
        r2 = random.randint(a, b)
    return (r1, r2)

def swap(list, pos1, pos2): 
  list[pos1], list[pos2] = list[pos2], list[pos1] 
  return list

def reverse_playfair(ct, key):
    # build a mapping for O(1) access matrix positioning of each letter
    pos_mapping = {}
    pos_matrix = [[],[],[],[],[]]
    for row in range(0, 5):
        for col in range(0, 5):
            letter = key[row*5 + col]
            pos_matrix[row].append(letter)
            pos_mapping[letter] = (row, col)
    # print(pos_mapping)
    # print(pos_matrix)
    textList = list(ct)
    for i in range(0, len(textList), 2):
        a = textList[i]
        b = textList[i+1]
        a_pos = pos_mapping[a]
        b_pos = pos_mapping[b]

        # case where a and b are horizontally aligned (same row)
        if a_pos[0] == b_pos[0]:
            a_sub = pos_matrix[a_pos[0]][(a_pos[1]-1)%5]
            b_sub = pos_matrix[b_pos[0]][(b_pos[1]-1)%5]
        # case where a and b are horizontally aligned (same col)
        elif a_pos[1] == b_pos[1]:
            a_sub = pos_matrix[(a_pos[0]-1)%5][a_pos[1]]
            b_sub = pos_matrix[(b_pos[0]-1)%5][b_pos[1]]
        # case where a and b forms a square
        else:
            a_sub = pos_matrix[a_pos[0]][b_pos[1]]
            b_sub = pos_matrix[b_pos[0]][a_pos[1]]

        # handle translating to plaintext
        textList[i] = a_sub
        textList[i+1] = b_sub
    return ''.join(textList)

def get_rand_key():
    key = KEY_CHARS[:]
    random.shuffle(key)
    return key

def crossover(k1, k2):
    keyLen = len(k1)
    halfKeyLen = int(keyLen / 2)
    r1 = random.randint(0, halfKeyLen-1)
    r2 = random.randint(halfKeyLen, keyLen-1)
    return _crossover(k1, k2, r1, r2)

def _crossover(k1, k2, r1, r2):
    keyLen = len(k1)
    inherit1 = k1[r1:r2]
    inherit2 = k2[r1:r2]
    c1 = k1[:]
    c2 = k2[:]

    cInd = r2
    for pInd in range(r1,r1+keyLen):
        if k2[pInd%keyLen] not in inherit1:
            c1[cInd%keyLen] = k2[pInd%keyLen]
            cInd += 1
        pInd += 1

    cInd = r2
    for pInd in range(r1,r1+keyLen):
        if k1[pInd%keyLen] not in inherit2:
            c2[cInd%keyLen] = k1[pInd%keyLen]
            cInd += 1
        pInd += 1

    return (c1, c2)

def swap_mutate(k):
    rp = get_rand_pair(0,len(k)-1)
    swap(k, rp[0], rp[1])

def split_mutate(k):
    r = random.randint(0,len(k)-1)
    k.extend(k[:r])
    del k[:r]

def appendRandScoreKeyPairs(keySet, ct, n):
    for i in range(0, n):
        key = get_rand_key()
        pt = reverse_playfair(ct, key)
        score = scorePlainText(pt)
        keySet.append((score, key))

def scorePlainText(text):
    return ngram.score(text.replace('x', ''))

def toKeyString(key):
    return ''.join(key)

def decode(ct, saveFile, keySet=[], keyLen=25, keyNum=100, genNum=100, bestNum=0.33):
    # calculate the number of best keys to preserve
    # round it to the next even number so every key can be paired
    bestKeyNum = math.ceil(bestNum * keyNum / 2) * 2
    # generate a key set with keyNum keys
    appendRandScoreKeyPairs(keySet, ct, keyNum)
    global_best = keySet[0]

    for gen in range(0, genNum):
        # sort the key set by score
        keySet.sort(reverse=True)
        # save to file and print, if a new global best is found
        if keySet[0][0] > global_best[0]:
            global_best = keySet[0]
            print('gen[' + str(gen) + '] best key (' + str(global_best[0]) + ', ' + toKeyString(global_best[1]) + ')')
            saveFile.write('gen[' + str(gen) + '] best key (' + str(global_best[0]) + ', ' + toKeyString(global_best[1]) + ')\n')
        # eliminate the bad keys from the key set
        del keySet[len(keySet) - 2*bestKeyNum : len(keySet)]
        # randomly pair up and mate the best keys
        bestKeys = keySet[:bestKeyNum]
        random.shuffle(bestKeys)
        for i in range(0, bestKeyNum, 2):
            k1 = bestKeys[i]
            k2 = bestKeys[i+1]
            # cross over the 2 keys to produce children key pair
            cKeys = crossover(k1[1], k2[1])
            # mutate child at random
            r = random.randint(0,1)
            swap_mutate(cKeys[r])
            split_mutate(cKeys[int(not r)])
            cpt = (reverse_playfair(ct,cKeys[0]), reverse_playfair(ct,cKeys[1]))
            cscore = (scorePlainText(cpt[0]), scorePlainText(cpt[1]))
            # add the keys and their children into the keyset
            keySet.append((cscore[0], cKeys[0]))
            keySet.append((cscore[1], cKeys[1]))

        # generate bestNum random keys to refill the set
        appendRandScoreKeyPairs(keySet, ct, bestKeyNum)

    return sorted(keySet, reverse=True)[0]

def test_crossover():
    result = _crossover(list('abcdefg'), list('decgfba'), 2, 5)
    actual = (toKeyString(result[0]), toKeyString(result[1]))
    expected = ('bacdegf', 'abcgfde')
    if actual[0] == expected[0]:
        print('[result 1] test passed!')
    else:
        print('[result 1] failed: expected=' + expected[0] + ', actual=' + actual[0])
    if actual[1] == expected[1]:
        print('[result 2] test passed!')
    else:
        print('[result 2] failed: expected=' + expected[1] + ', actual=' + actual[1])

    result = crossover(list('IVFUMBAZKHXGSDRTWYELNOPCQ'), list('SATWDGNELKUVZQBFXOYHPMIRC'))
    actual = (toKeyString(result[0]), toKeyString(result[1]))
    if len(actual[0]) == len('IVFUMBAZKHXGSDRTWYELNOPCQ'):
        print('[result 1] test passed!')
    else:
        print('[result 1] failed: actual=' + actual[0])
    if len(actual[1]) == len('SATWDGNELKUVZQBFXOYHPMIRC'):
        print('[result 2] test passed!')
    else:
        print('[result 2] failed: actual=' + actual[1])

def main():
    if len(sys.argv) >= 2:
        ct = sys.argv[1]

        if len(sys.argv) >= 3:
            saveFileName = sys.argv[2]
        else:
            saveFileName = 'playfair.txt'

        with open(saveFileName, 'a+') as saveFile:
            seedKeySet = []
            result = decode(ct, saveFile, seedKeySet, keyLen=25, keyNum=2000, genNum=2000, bestNum=0.05)

        print('================================ COMPLETED ================================')
        print('key: ', str(result[1]))
        print('fitness: ', result[0])
        print('plaintext: ', reverse_playfair(ct, result[1]))
    else:
        print('error: did not provide a cipher text')

if __name__ == '__main__':
  main()
