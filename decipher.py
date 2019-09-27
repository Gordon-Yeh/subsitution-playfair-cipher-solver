import ngram_score
import random
import sys

ITERATION_TIMEOUT = 10000
upperCaseAlp = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];
with open('english_quadgrams.txt') as f:
    ngram = ngram_score.ngram_score(f)

def get_rand_pair(a, b):
    r1 = random.randint(a, b)
    r2 = random.randint(a, b)
    while r2 == r1:
        r2 = random.randint(a, b)
    return (r1, r2)

def apply_key(text, key):
  textList = list(ct);
  modified = [False for i in range(0, len(textList))]
  for i in range(0,len(key)):
    for ti in range(0, len(textList)):
      if textList[ti] == upperCaseAlp[i] and not modified[ti]:
        textList[ti] = key[i];
        modified[ti] = True
  return ''.join(textList);

def swap(list, pos1, pos2): 
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list

def decipher(ct, seedkey):
    candidate_text = apply_key(ct, seedkey)
    best_score = ngram.score(candidate_text)
    best_key = seedkey
    iterations = 0

    while iterations < ITERATION_TIMEOUT:
        r1 = get_rand_pair(0, 25)
        swap(best_key, r1[0], r1[1])
        candidate_text = apply_key(ct, best_key)
        score = ngram.score(candidate_text)
        if (score > best_score):
            best_score = score
        else:
            swap(best_key, r1[1], r1[0])

        iterations += 1
    
    return [best_key, best_score, apply_key(ct, best_key)]

def main():
  if len(sys.argv) >= 2:
    seedkey = ['O', 'G', 'K', 'I', 'D', 'T', 'C', 'Q', 'Z', 'A', 'P', 'X', 'J', 'H', 'F', 'E', 'Y', 'M', 'U', 'B', 'W', 'N', 'L', 'S', 'R', 'V']
    ct = sys.argv[1]
    print(decipher(ct, seedkey))
  else:
    print('error: did not provide a cipher text')

if __name__ == '__main__':
  main()
