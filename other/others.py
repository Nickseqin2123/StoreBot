import pymorphy2


morph = pymorphy2.MorphAnalyzer()

def add_ending(sentence: str, word_replace: str):
    words = sentence.split()
    for i, word in enumerate(words):
        parsed = morph.parse(word)
        
        if word.lower() == word_replace.lower():
            # Выбираем нужную форму (родительный падеж, единственное число)
            new_word = parsed[0].inflect({'gent'}).word  # gen - родительный падеж
            words[i] = new_word
           
    return ' '.join(words)