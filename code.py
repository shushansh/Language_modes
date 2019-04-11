import PyPDF4
import textract
import re
import nltk

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer

pst = PorterStemmer()

text = textract.process('C:/Users/vaibh/Desktop/2.pdf')
String = text.decode('utf-8').replace('\r\n','\n')
currencies_check = ['USD', 'EUR', 'RS', 'INR', 'ZAR']
string_check = ['round', 'deliveri', 'return']
String = sent_tokenize(String)
rqd_text = []

for line in String:
    processed_words = []
    line = line.replace(',','')
    line_words = word_tokenize(line)
    for words in line_words:
        try :
            processed_words.append(pst.stem(words))
        except:
            continue
    if string_check[0].lower() in processed_words and string_check[1].lower() in processed_words and string_check[2].lower() in processed_words:
        for wordl in processed_words:
            if re.search('usd(.+?)', str(wordl)):
                processed_words.append('usd')
            if re.search('eur(.+?)', str(wordl)):
                processed_words.append('eur')
            if re.search('rs(.+?)', str(wordl)):
                processed_words.append('rs')
            if re.search('zar(.+?)', str(wordl)):
                processed_words.append('zar')
        for curr in currencies_check:
            if curr.lower() in processed_words:
                rqd_text.append(line)
                currency = curr
                break

if len(rqd_text) < 1:
    print("Error! Data not found.")
    exit(1)

clean_text = rqd_text[0].replace(',','').replace(';','')
clean_text_split = word_tokenize(clean_text)

print(clean_text)

amount = re.findall(r'-?\d+\.?\d*', clean_text)
amount_matches = []
for intl in amount:
    if float(intl) > 10:
        amount_matches.append(float(intl))

if re.search('(.+?)elivery(.+?)and(.+?)eturn(.+?)', clean_text):
    m = re.search('(.+?)up(.+?)and', clean_text)
    if m:
        delivery_round = 'up'
        return_round = 'down'
    else:
        delivery_round = 'down'
        return_round = 'up'
else:
    if re.search('up(.+?)and(.+?)', clean_text):
        delivery_round = 'up'
        return_round = 'down'
    if re.search('down(.+?)eturn(.+?)up', clean_text):
        delivery_round = 'down'
        return_round = 'up'
    if 'up' in clean_text_split and 'down' not in clean_text_split:
        delivery_round = 'up'
        return_round = 'up'
    else:
        delivery_round = 'down'
        return_round = 'down'

if len(amount_matches) < 1:
    print('ERROR! File might be a scanned image, OCR error.')
    exit(1)

if len(amount_matches) > 1:
    delivery_amount = amount_matches[0]
    return_amount = amount_matches[1]
else:
    delivery_amount = amount_matches[0]
    return_amount = amount_matches[0]


print("Delivery Amount:\nCurrency: "+currency+"\nAmount: "+str(delivery_amount)+"\nRound: "+delivery_round+"\n")
print("Return Amount:\nCurrency: "+currency+"\nAmount: "+str(return_amount)+"\nRound: "+return_round+"\n")