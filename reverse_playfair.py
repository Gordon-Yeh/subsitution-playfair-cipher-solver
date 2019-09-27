import sys

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
        # case where a and b are vertically aligned (same col)
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

def main():
    if len(sys.argv) >= 3:
        ct = sys.argv[1]
        key = sys.argv[2]
        pt = reverse_playfair(ct, list(key))
        print('plaintext:', pt)
    else:
        print('error: did not provide a cipher text / key')

if __name__ == '__main__':
  main()
