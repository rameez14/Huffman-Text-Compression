import array
import argparse
import time
import pickle
import sys

class Huffman_model:
    def __init__(self, model):
        self.model = model
        self.iterate_model = model

    def iteratation_(self, index):
        nodes = self.iterate_model[index]
        if isinstance(nodes, str):
            return nodes
        else:
            self.iterate_model = nodes

    def reset(self):
        self.iterate_model = self.model

#main
start = time.perf_counter()
parser = argparse.ArgumentParser()
parser.add_argument('bin', type=str, help="the compression file XXXX.bin")
args = parser.parse_args()

if 'bin' in args:
    bin_file = args.bin
    pkl_file = bin_file[:bin_file.find('.bin')] + '.pkl'
else:
    sys.exit()

pkl_file = bin_file[:bin_file.find('.bin')] + '-symbol-model.pkl'
out_file = bin_file[:bin_file.find('.bin')] + '-decompressed.txt'
length = 0
model = {}
with open(pkl_file, 'rb') as f:
    model = pickle.load(f)
length = model['length']
huffman = Huffman_model(model)

bytes = bytes();
data = array.array('B')
with open(bin_file, 'rb') as f:
    bytes = f.read()

length_r = 0
c_b = '00000000'
recover_file = ''
for ab in bytes:
    binstr = bin(ab)[2:]
    binstr = c_b[0:(8-len(binstr))] + binstr
    for b in binstr:
        r = huffman.iteratation_(b)
        length_r+=1
        if isinstance(r,str):
            recover_file += r
            huffman.reset()
        if length_r >=length:
            break
with open(out_file, 'w') as f:
    f.write(recover_file)

print('Decompress: %.2fs'%(time.clock()-start))
