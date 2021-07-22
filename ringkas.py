import re
import math
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

stopWordFactory = StopWordRemoverFactory()
stopwords = stopWordFactory.get_stop_words()

stemFactory = StemmerFactory()
stemmer = stemFactory.create_stemmer()

# method untuk melakukan tahap preprocessing terhadap dokumen teks
def preProcessing(berita):
    hasilPreprocessing = []

    # memecah teks berita menjadi beberapa kalimat
    temp = re.split("\n+", berita)
    teksBerita = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", temp[1])
    teks = []
    teks.append(temp[0])
    for kalimat in teksBerita:
        teks.append(kalimat)

    for kalimat in teks:
        stem = []
        # melakukan case folding pada dokumen
        lowerCase = kalimat.lower()
        # print(lowerCase)

        # melakukan data cleaning pada dokumen
        numRemove = re.sub(r'\d+', ' ', lowerCase)
        puncRemove = re.sub(r'[^\w\s]', ' ', numRemove)
        # puncRemove = numRemove.translate(punc)
        # print(puncRemove)

        # melakukan tokenisasi terhadap dokumen
        token = word_tokenize(puncRemove)
        # print(token)

        # melakukan stopword removal(filtering) pada dokumen
        filteredToken = [word for word in token if word not in stopwords]
        filteredToken = [word for word in filteredToken if len(word) > 2]
        # print(filteredToken)

        # melakukan stemming pada masing-masing token
        for word in filteredToken:
            stem.append(stemmer.stem(word))

        hasilPreprocessing.append(stem) 
    
    return hasilPreprocessing

# method untuk mencari nilai term frequency masing-masing token pada tiap dokumen
def getTF(token, wordSet):
    tfList = []
    logtfList = []
    
    # mencari nilai tf masing-masing token
    for kalimat in token:
        tfDict = dict.fromkeys(wordSet, 0)
        for kata in kalimat:
            tfDict[kata] += 1
        
        tfList.append(tfDict)
    
    # mencari log normalisasi dari nilai TF
    for kalimat in tfList:
        logtfDict = dict.fromkeys(wordSet, 0)
        for kata, val in kalimat.items():
            if val > 0:
                logtfDict[kata] = 1 + math.log10(float(val))
        
        logtfList.append(logtfDict)

    return logtfList

# method untuk mencari nilai inverse document frequency masing-masing token pada tiap dokumen
def getIDF(TF):
    idfDict = {}
    idfDict = dict.fromkeys(TF[0].keys(), 0)
    N = len(TF)

    # mencari nilai document frequency
    for dok in TF:
        for kata, val in dok.items():
            if val > 0:
                idfDict[kata] += 1
    
    # mencari nilai inverse document frequency
    for kata, val in idfDict.items():
        idfDict[kata] = math.log10(N / float(val))

    return idfDict

# method untuk mencari nilai TFIDF masing-masing token
def getTFIDF(TF, IDF):
    tfidfList = []

    for dok in TF:
        tfidfDict = {}
        tfidfDict = dict.fromkeys(TF[0].keys(), 0)

        for kata in dok:
            tfidfDict[kata] = dok[kata] * IDF[kata]

        tfidfList.append(tfidfDict)
    
    return tfidfList

# method untuk mencari nilai similarity antar dokumen
def getSIM(TFIDF, dnum):
    a = []
    aSum = []
    tfidfSum = []
    iscSim = []
    i = 0

    for dok in TFIDF:
        aDict = {}
        aDict = dict.fromkeys(TFIDF[0].keys(), 0)
        summary = 0

        for kata in dok:
            aDict[kata] = math.sqrt(TFIDF[dnum][kata]*dok[kata])
            summary += dok[kata]
        
        a.append(aDict)
        tfidfSum.append(summary)

    for dok in a:
        summary = 0

        for kata, val in dok.items():
            summary += val

        aSum.append(summary)
    
    for val in tfidfSum:
        iscSim.append(aSum[i]/(math.sqrt(tfidfSum[dnum])*math.sqrt(val)))
        i += 1
    
    return iscSim

# method untuk mencari nilai MMR masing-masing dokumen
def getMMR(SIM):
    i = 1
    maxSim = []
    mmrList = []
    k = 0.8

    # mencari nilai maximum similarity kecuali similarity dokumen target dengan query dan dokumen target dengan dokumen itu sendiri
    for dok in SIM:
        val = 0
        for kata in dok:
            if kata != dok[0] and kata != dok[i]:
                if kata > val:
                    val = kata
        maxSim.append(val)
        i += 1
    
    # menghitung nilai MMR
    j = 0
    for dok in SIM:
        mmrVal = k*dok[0]-(1-k)*maxSim[j]
        mmrList.append(mmrVal)
        j += 1

    return mmrList

# method untuk membentuk ringkasan
def getRingkasan(MMR, teks, persentase):
    jumlahKalimat = round((persentase*(len(teks)-1))/100)
    dokList = []
    for i in range(1, len(teks)):
        dokList.append(i)
    
    # membuat dictionary berisi nilai mmr
    mmrDict = {}
    mmrDict = dict.fromkeys(dokList, 0)
    for i in range(1, len(teks)):
        mmrDict[i] = MMR[i-1]

    # mengurutkan nilai mmr dari yang terbesar kemudian membuat ringkasan berdasarkan persentase yang ditentukan
    ringkasan = dict(sorted(mmrDict.items(), key=lambda x: x[1], reverse=True))
    ringkasanList = []
    i = 0
    for key, value in ringkasan.items():
        if i == jumlahKalimat:
            break
        ringkasanList.append(key)
        i += 1
    ringkasanList.sort()

    print("Ringkasan", persentase, "%")
    print("Query :", teks[0])

    f = open("ringkasan.txt", "w")
    ringkasan = ""
    for indeks in ringkasanList:
        f.write(teks[indeks] + " ")
        print(teks[indeks])
        ringkasan += teks[indeks] + " "
    f.close()

    print(ringkasanList)

    return ringkasan

# main method
def main(beritaKe, persentaseRingkasan):
    fileBerita = open("data/"+beritaKe+".txt", "r")
    berita = fileBerita.read()

    temp = re.split("\n+", berita)
    teksBerita = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", temp[1])
    teks = []
    teks.append(temp[0])
    for kalimat in teksBerita:
        teks.append(kalimat)

    token = preProcessing(berita)
    wordSet = set().union(*token)
    TF = getTF(token,wordSet)
    IDF = getIDF(TF)
    tfidf = getTFIDF(TF,IDF)
    iscSim = []
    for i in range(1,len(tfidf)):
        iscSim.append(getSIM(tfidf,i))
    mmr = getMMR(iscSim)

    print(berita, "\n")
    # print(len(teks))
    ringkasan = getRingkasan(mmr,teks,persentaseRingkasan)

    return ringkasan

if __name__== "__main__":
    fileName = "news7"
    persentase = 50
    f = open("ringkasan/"+fileName+"_"+str(persentase)+".txt", "w")
    f.write(main(fileName, persentase))