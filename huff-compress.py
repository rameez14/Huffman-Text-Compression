import array
import argparse
import re
import time
import pickle 
import sys
import copy

def huffman(words):
    outcome = {}
   
    def iteration(makecode, tree):
        if isinstance(tree,str):
            outcome[tree] = makecode
            return
        iteration(makecode+'0',tree['0'])
        iteration(makecode+'1',tree['1'])

    while (len(words) !=10) :
        l1 = words[0]
        l2 = words[1]
        i = 0
        new_term = ({'0':copy.deepcopy(l1[0]),'1':copy.deepcopy(l2[0])}, l1[1]+l2[1])
        for w in words:
            if new_term[1] < w[1]:
                words.insert(i,new_term)
                break
            i+=1
        words.remove(l1)
        words.remove(l2)

    while (len(words) !=1) :
        l1 = words[0]
        l2 = words[1]
        del words[0]
        del words[0]
        new_term = ({'0':copy.deepcopy(l1[0]),'1':copy.deepcopy(l2[0])}, l1[1]+l2[1])
        words.append(new_term)
        words = sorted(words, key=lambda x:x[1])
    iteration('',words[0][0])
    return outcome, words[0][0]

def term(letters, insert):
    letters_ = letters
    for i in range(len(letters_)):
        if letters_[i][1] >= insert[1]:
            letters_.insert(i, insert)
            break
    return letters_

def binary_conversion(huffman_str):
    info = array.array('B')
    c_b = '00000000'
    size = len(huffman_str)
    huffman_str += c_b[:(8-len(huffman_str)%8)]
    for i in range(0,len(huffman_str), 8):
        bytes = int(huffman_str[i:i+8],2)
        info.append(bytes)
    return info,size


def storing(huffman_str, huff_model):
    info, size = binary_conversion(huffman_str)
    with open(bin_path,"wb") as f:
        info.tofile(f)
    with open(pkl_path, "wb") as f:
        huff_model['size'] = size
        pickle.dump(huff_model,f)
    return


def data(init_data):
    word_array = {}
    for d in init_data:
        if d not in word_array:
            word_array[d] = 1
        else:
            word_array[d] += 1
    return word_array


#main
start = time.perf_counter()
parser = argparse.ArgumentParser()
parser.add_argument('-s', type=str, help='Symbol')
parser.add_argument('input', type=str, help="Input file")
args = parser.parse_args()

if "s" in args and "input" in args:
    character = args.s if args.s else 'word'
    record_path  = args.input if args.input else 'infile.txt'
    bin_path = record_path[:record_path.find('.')] + 'infile.bin'
    pkl_path = record_path[:record_path.find('.')] + '-infile-symbol-model.pkl'
    wording = ""
else:
        sys.exit()

with open(record_path) as f:
    wording = f.read()
wording_array = None

if character == "char":
    wording_array = data(wording)
if character == 'word':
    w_pattern = re.compile(r'([a-z]+)', re.I)
    s_symbol = re.compile(r'[^a-z]{1}',re.I)
    word_ = w_pattern.findall(wording)
    symbol_p = s_symbol.findall(wording)
    wording_array = data(word_+symbol_p)

wording_array = sorted(wording_array.items(), key=lambda d: d[1])
letters_huffman, huffman_model = huffman(wording_array)

print("Building huffman_model:  %.2fs" %  (time.perf_counter()-start))
start = time.perf_counter()

huffman_str = ""
if character == "char":
    for d in wording:
        huffman_str+=letters_huffman[d]

if character == "word":
    letters = ''
    pattern = re.compile(r'([a-z])', re.I)
    for d in wording:      
        if pattern.match(d):
            letters+=d
        else:
            if len(letters)!=0:
                huffman_str+=(letters_huffman[letters]+letters_huffman[d])
                letters = ''
            else:
                huffman_str += letters_huffman[d]
print('Encoding: %.2fs'%(time.perf_counter()-start))
storing(huffman_str, huffman_model)
