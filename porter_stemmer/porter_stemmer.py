class PorterStemmer:
    def __init__(self):
        """The word is a buffer holding a word to be stemmed. The letters are in the range
        [start, offset ... offset + 1) ... ending at end."""

        self.vowels = ('a', 'e', 'i', 'o', 'u')
        self.word = ''
        self.end = 0
        self.start = 0
        self.offset = 0

    def is_vowel(self, letter):
        return letter in self.vowels

    def is_consonant(self, index):
        """:returns True if word[index] is a consonant."""
        if self.is_vowel(self.word[index]):
            return False
        if self.word[index] == 'y':
            if index == self.start:
                return True
            else:
                return not self.is_consonant(index - 1)
        return True

    def m(self):
        """m() measures the number of consonant sequences between start and offset.
        if c is a consonant sequence and v a vowel sequence, and <..>
        indicates arbitrary presence,
           <c><v>       gives 0
           <c>vc<v>     gives 1
           <c>vcvc<v>   gives 2
           <c>vcvcvc<v> gives 3
           ....
        """
        n = 0
        i = self.start
        while True:
            if i > self.offset:
                return n
            if not self.is_consonant(i):
                break
            i += 1
        i += 1
        while True:
            while True:
                if i > self.offset:
                    return n
                if self.is_consonant(i):
                    break
                i += 1
            i += 1
            n += 1
            while True:
                if i > self.offset:
                    return n
                if not self.is_consonant(i):
                    break
                i += 1
            i += 1

    def contains_vowel(self):
        """:returns TRUE if the word contains a vowel in the range [start, offset]"""
        for i in range(self.start, self.offset + 1):
            if not self.is_consonant(i):
                return True
        return False

    def contains_double_consonant(self, j):
        """:returns TRUE if the word contain a double consonant in the range [offset, start]"""
        if j < (self.start + 1):
            return False
        if self.word[j] != self.word[j - 1]:
            return False
        return self.is_consonant(j)

    def is_of_form_cvc(self, i):
        """:returns TRUE for indices set {i-2, i-1, i} has the form consonant - vowel - consonant
        and also if the second c is not w,x or y. this is used when trying to
        restore an e at the end of a short  e.g.
           cav(e), lov(e), hop(e), crim(e), but
           snow, box, tray.
        """
        if i < (self.start + 2) or not self.is_consonant(i) or self.is_consonant(i - 1) or not self.is_consonant(i - 2):
            return 0
        ch = self.word[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends_with(self, s):
        """:returns TRUE when {start...end} ends with the string s."""
        length = len(s)
        if s[length - 1] != self.word[self.end]:  # tiny speed-up
            return False
        if length > (self.end - self.start + 1):
            return False
        if self.word[self.end - length + 1: self.end + 1] != s:
            return False
        self.offset = self.end - length
        return True

    def set_to(self, s):
        """sets [offset + 1, end] to the characters in the string s, readjusting end."""
        length = len(s)
        self.word = self.word[:self.offset + 1] + s + self.word[self.offset + length + 1:]
        self.end = self.offset + length

    def replace_morpheme(self, s):
        """is a mapping function to change morphemes"""
        if self.m() > 0:
            self.set_to(s)

    def remove_plurals(self):
        """This is step 1 ab and gets rid of plurals and -ed or -ing. e.g.
           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat
           feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable
           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess
           meetings  ->  meet
        """
        if self.word[self.end] == 's':
            if self.ends_with("sses"):
                self.end = self.end - 2
            elif self.ends_with("ies"):
                self.set_to("i")
            elif self.word[self.end - 1] != 's':
                self.end = self.end - 1
        if self.ends_with("eed"):
            if self.m() > 0:
                self.end = self.end - 1
        elif (self.ends_with("ed") or self.ends_with("ing")) and self.contains_vowel():
            self.end = self.offset
            if self.ends_with("at"):
                self.set_to("ate")
            elif self.ends_with("bl"):
                self.set_to("ble")
            elif self.ends_with("iz"):
                self.set_to("ize")
            elif self.contains_double_consonant(self.end):
                self.end = self.end - 1
                ch = self.word[self.end]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.end = self.end + 1
            elif self.m() == 1 and self.is_of_form_cvc(self.end):
                self.set_to("e")

    def terminal_y_to_i(self):
        """This defines step 1 c which turns terminal y to i when there is another vowel in the stem."""
        if self.ends_with('y') and self.contains_vowel():
            self.word = self.word[:self.end] + 'i' + self.word[self.end + 1:]

    def map_double_to_single_suffix(self):
        """Defines step 2 and maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """
        if self.word[self.end - 1] == 'a':
            if self.ends_with("ational"):
                self.replace_morpheme("ate")
            elif self.ends_with("tional"):
                self.replace_morpheme("tion")
        elif self.word[self.end - 1] == 'c':
            if self.ends_with("enci"):
                self.replace_morpheme("ence")
            elif self.ends_with("anci"):
                self.replace_morpheme("ance")
        elif self.word[self.end - 1] == 'e':
            if self.ends_with("izer"):      self.replace_morpheme("ize")
        elif self.word[self.end - 1] == 'l':
            if self.ends_with("bli"):
                self.replace_morpheme("ble")  # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends_with("alli"):
                self.replace_morpheme("al")
            elif self.ends_with("entli"):
                self.replace_morpheme("ent")
            elif self.ends_with("eli"):
                self.replace_morpheme("e")
            elif self.ends_with("ousli"):
                self.replace_morpheme("ous")
        elif self.word[self.end - 1] == 'o':
            if self.ends_with("ization"):
                self.replace_morpheme("ize")
            elif self.ends_with("ation"):
                self.replace_morpheme("ate")
            elif self.ends_with("ator"):
                self.replace_morpheme("ate")
        elif self.word[self.end - 1] == 's':
            if self.ends_with("alism"):
                self.replace_morpheme("al")
            elif self.ends_with("iveness"):
                self.replace_morpheme("ive")
            elif self.ends_with("fulness"):
                self.replace_morpheme("ful")
            elif self.ends_with("ousness"):
                self.replace_morpheme("ous")
        elif self.word[self.end - 1] == 't':
            if self.ends_with("aliti"):
                self.replace_morpheme("al")
            elif self.ends_with("iviti"):
                self.replace_morpheme("ive")
            elif self.ends_with("biliti"):
                self.replace_morpheme("ble")
        elif self.word[self.end - 1] == 'g':
            if self.ends_with("logi"):      self.replace_morpheme("log")

    def step3(self):
        """step3() deals with -ic-, -full, -ness etc."""
        if self.word[self.end] == 'e':
            if self.ends_with("icate"):
                self.replace_morpheme("ic")
            elif self.ends_with("ative"):
                self.replace_morpheme("")
            elif self.ends_with("alize"):
                self.replace_morpheme("al")
        elif self.word[self.end] == 'i':
            if self.ends_with("iciti"):     self.replace_morpheme("ic")
        elif self.word[self.end] == 'l':
            if self.ends_with("ical"):
                self.replace_morpheme("ic")
            elif self.ends_with("ful"):
                self.replace_morpheme("")
        elif self.word[self.end] == 's':
            if self.ends_with("ness"):      self.replace_morpheme("")

    def step4(self):
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
        if self.word[self.end - 1] == 'a':
            if self.ends_with("al"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'c':
            if self.ends_with("ance"):
                pass
            elif self.ends_with("ence"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'e':
            if self.ends_with("er"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'i':
            if self.ends_with("ic"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'l':
            if self.ends_with("able"):
                pass
            elif self.ends_with("ible"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'n':
            if self.ends_with("ant"):
                pass
            elif self.ends_with("ement"):
                pass
            elif self.ends_with("ment"):
                pass
            elif self.ends_with("ent"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'o':
            if self.ends_with("ion") and (self.word[self.offset] == 's' or self.word[self.offset] == 't'):
                pass
            elif self.ends_with("ou"):
                pass
            # takes care of -ous
            else:
                return
        elif self.word[self.end - 1] == 's':
            if self.ends_with("ism"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 't':
            if self.ends_with("ate"):
                pass
            elif self.ends_with("iti"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'u':
            if self.ends_with("ous"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'v':
            if self.ends_with("ive"):
                pass
            else:
                return
        elif self.word[self.end - 1] == 'z':
            if self.ends_with("ize"):
                pass
            else:
                return
        else:
            return
        if self.m() > 1:
            self.end = self.offset

    def step5(self):
        """step5() removes a final -e if m() > 1, and changes -ll to -l if m > 1."""
        self.offset = self.end
        if self.word[self.end] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.is_of_form_cvc(self.end - 1)):
                self.end = self.end - 1
        if self.word[self.end] == 'l' and self.contains_double_consonant(self.end) and self.m() > 1:
            self.end = self.end - 1

    def stem_document(self, document):
        result = []
        for line in document.split('\n'):
            result.append(self.stem_sentence(line))
        return '\n'.join(result)

    def alphabetic(self, word):
        return ''.join([letter if letter.isalpha() else '' for letter in word])

    def stem_sentence(self, sentence):
        result = []
        for word in sentence.split():
            result.append(self.stem_word(word))
        return ' '.join(result)

    def stem_word(self, word):
        if word == '':
            return ''

        self.word = word
        self.end = len(word) - 1
        self.start = 0

        self.remove_plurals()
        self.terminal_y_to_i()
        self.map_double_to_single_suffix()
        self.step3()
        self.step4()
        self.step5()
        return self.word[self.start: self.end + 1]
