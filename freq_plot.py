import matplotlib.pyplot as plt
import numpy as np
import sys

upperCaseAlp = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];

def get_letter_freq(text):
  charFreq = {}
  for alp in upperCaseAlp:
    charFreq[alp] = 0;
  for c in text:
    if c in charFreq:
      charFreq[c] += 1
    else:
      charFreq[c] = 1
  return charFreq

def get_bigram_freq(text):
  dic = {}
  for i in range(0,len(text),2):
    bigram = text[i:i+2]
    if bigram in dic:
      dic[bigram] += 1
    else:
      dic[bigram] = 1
  return dic

def plot_dictionary(dic, xlabel, ylabel):
  items = sorted(dic.keys())
  values = [dic[i] for i in items]
  index = np.arange(len(items))
  plt.bar(index, values)
  plt.xlabel(xlabel, fontsize=5)
  plt.ylabel(ylabel, fontsize=5)
  plt.xticks(index, items, fontsize=5, rotation=30)
  plt.show()

def letter_freq_plot(text):
  freq = get_letter_freq(text)
  plot_dictionary(freq, 'letters', 'frequency')

def digram_freq_plot(text):
  freq = get_bigram_freq(text)
  plot_dictionary(freq, 'letters', 'frequency')

def main():
  if len(sys.argv) >= 2:
    ct = sys.argv[1]
    digram_freq_plot(ct)
  else:
    print('error: did not provide a cipher text')

if __name__ == '__main__':
  main()