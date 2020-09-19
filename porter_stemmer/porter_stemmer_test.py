# custom porter stemmer
from porter_stemmer import PorterStemmer

stemmer = PorterStemmer()
document = "day"
print(stemmer.stem_document(document))


# using the nltk library
# from nltk.stem import PorterStemmer
#
# stemmer = PorterStemmer()
# print(stemmer.stem('day'))
