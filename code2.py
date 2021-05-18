import sys
import re

# corpus_path = "Health_English.txt"
# corpus_path = "technical_domain_corpus.txt"
if(len(sys.argv) < 3):
	print("Usage: python language_model.py <smoothing type> <path_corpus>")

smooth_model = sys.argv[1]
corpus_path = sys.argv[2] 


if(smooth_model == "k"):
	trainFileName = "20162083-brown-k-train-perplexity.txt"
	testFileName = "20162083-brown-k-test-perplexity.txt"
else:
	trainFileName = "20162083-brown-w-train-perplexity.txt"
	testFileName = "20162083-brown-w-test-perplexity.txt"


# inputStr = input("input sentence : ")

def find_perplexity(probValue, pp_n):
	return (1/probValue)**(1/float(pp_n))

def clean_data(tmp_data):
	tmp_data = re.sub(r'[0-9_]+', '', tmp_data)
	tmp_data = re.sub(r'n\'t', 'nt', tmp_data)
	tmp_data = re.sub(r'\'ll', ' will', tmp_data)
	tmp_data = re.sub(r'\'ve', ' have', tmp_data)
	tmp_data = re.sub(r'\'re', ' are', tmp_data)
	tmp_data = re.sub(r' i\'m ', ' i am ', tmp_data)
	tmp_data = re.sub(r'\'s', 's', tmp_data)
	tmp_data = re.sub(r'[^\w\s]', ' ', tmp_data)
	tmp_data = re.sub(r'[\s]+', ' ', tmp_data)
	tmp_data = re.sub(r'^ ', '', tmp_data)
	return tmp_data

def find_prob(findProbStr):
	probRes = 1
	inpList = findProbStr.split()
	if(smooth_model == 'k'):
		stInd = 0
		endInd = 3
		k_D = 0.75
		k_alpha = 1/len(inpList)
		cnt3 = 0
		cnt4 = 0
		if(endInd >= len(inpList)):
			for tmp in quadDict.keys():
				if tmp.startswith(findProbStr):
					cnt4 = cnt4 + 1
					cnt3 = cnt3 + quadDict[tmp]
			if cnt3 != 0 :
				probRes = probRes * (cnt4 - k_D) / cnt3
			else:
				probRes = probRes * k_alpha * len(quadDict.keys()) / sum(quadDict.values())
			return probRes

		while(endInd < len(inpList)) :
			triStr = " ".join(inpList[stInd:endInd])
			quadStr = " ".join(inpList[stInd:endInd+1])

			if(quadStr in quadDict.keys()):
				cnt4 = quadDict[quadStr]
				cnt3 = triDict[triStr]
				probRes = probRes * (cnt4 - k_D) / cnt3
			else:
				probRes = probRes * k_alpha * len(quadDict.keys()) / sum(quadDict.values())
			stInd = stInd + 1
			endInd = endInd + 1

		return probRes

	elif(smooth_model == 'w'):
		stInd = 0
		endInd = 3
		if(endInd >= len(inpList)):
			w_T = 0
			w_N = 0
			for tmp in quadDict.keys():
				if tmp.startswith(findProbStr):
					w_T = w_T + 1
					w_N = w_N + quadDict[tmp]
			if(w_N == 0):
				w_N = sum(quadDict.values())
				w_T = len(quadDict.keys())
			w_Z = len(inpList)
			probRes = probRes * w_T / (w_Z  * (w_N + w_T))
			return probRes

		while(endInd < len(inpList)) :
			triStr = " ".join(inpList[stInd:endInd])
			quadStr = " ".join(inpList[stInd:endInd+1])
			if quadStr in quadDict.keys():
				w_N = triDict[triStr]
				w_T = triDictType[triStr]
			else:
				w_N = sum(triDict.values())
				w_T = len(triDict.keys())
				w_Z = len(inpList)

			if(quadStr in quadDict.keys()):
				probRes = probRes * quadDict[quadStr] / (w_N + w_T)
			else:
				probRes = probRes * w_T / (w_Z  * (w_N + w_T))
			stInd = stInd + 1
			endInd = endInd + 1
		return probRes
	else:
		print("Invalid smoothing type")
		exit()

train_data = []
test_data = []
triDict = {}
quadDict = {}
triDictType = {}
test_triDict = {}
test_quadDict = {}
trainFlag = True

browntext = open(corpus_path, 'r').read()
browntext = re.sub(r'[\r\n]+', '', browntext)
browntext = browntext.split('.')

for line in browntext:
	line = re.sub(r'[^\x00-\x7F]+', '', line)
	if line.strip():
		if ( re.search(r'-', line) != None) :
			if ( re.search(r'[\w][ ]?-[ ]?[\w]', line) == None) :
				line = re.sub(r'-', '', line)
		line = clean_data (line)
		line = line.lower()

		if(trainFlag):
			tmpList = line.split()
			stInd = 0
			endInd = 3
			while(endInd < len(tmpList)) :
				tmpStr = " ".join(tmpList[stInd:endInd])
				if tmpStr in triDict.keys():
					triDict[tmpStr] = triDict[tmpStr] + 1
					tmpStr4 = tmpStr + " " + tmpList[endInd]
					if tmpStr4 in quadDict.keys():
						quadDict[tmpStr4] = quadDict[tmpStr4] + 1
					else:
						quadDict[tmpStr4] = 1
						triDictType[tmpStr] = triDictType[tmpStr] + 1
				else:
					triDict[tmpStr] = 1
					triDictType[tmpStr] = 1
					tmpStr = tmpStr + " " + tmpList[endInd]
					quadDict[tmpStr] = 1
					
				stInd = stInd + 1
				endInd = endInd + 1
			train_data.append(line)
			if(len(test_data) < 10000):
				trainFlag = False
		else:
			test_data.append(line)
			trainFlag = True

pp_sum = 0
filePtr = open(trainFileName, "w")
for inputStr in train_data:
	inputStr = re.sub(r'[^\x00-\x7F]+', '', inputStr)
	if inputStr.strip():
		if ( re.search(r'-', inputStr) != None) :
			if ( re.search(r'[\w][ ]?-[ ]?[\w]', inputStr) == None) :
				inputStr = re.sub(r'-', '', inputStr)
		inputStr = clean_data (inputStr)
		inputStr = inputStr.lower()
		inputStrProb = find_prob(inputStr)
		if(inputStrProb != 0):
			inputStrPP = find_perplexity(inputStrProb, len(inputStr.split()))
			pp_sum = pp_sum + inputStrPP
			filePtr.write(inputStr.strip() + "\t" + str(inputStrPP) + "\n")
		else:
			filePtr.write(inputStr.strip() + "\tinfinity\n")
pp_avg = pp_sum/len(train_data)
filePtr.write(str(pp_avg) + "\n")
filePtr.close()

pp_sum = 0
filePtr = open(testFileName, "w")
for inputStr in test_data:
	inputStr = re.sub(r'[^\x00-\x7F]+', '', inputStr)
	if inputStr.strip():
		if ( re.search(r'-', inputStr) != None) :
			if ( re.search(r'[\w][ ]?-[ ]?[\w]', inputStr) == None) :
				inputStr = re.sub(r'-', '', inputStr)
		inputStr = clean_data (inputStr)
		inputStr = inputStr.lower()
		inputStrProb = find_prob(inputStr)
		if(inputStrProb != 0):
			inputStrPP = find_perplexity(inputStrProb, len(inputStr.split()))
			pp_sum = pp_sum + inputStrPP
			filePtr.write(inputStr.strip() + "\t" + str(inputStrPP) + "\n")
		else:
			filePtr.write(inputStr.strip() + "\tinfinity\n")
pp_avg = pp_sum/len(test_data)
filePtr.write(str(pp_avg) + "\n")
filePtr.close()
# print(train_data)
# print(len(triDict))
# print(len(quadDict))
# print([(k, v) for k,v in quadDict.items() if v>10 ])
