from django import template


class CensorException(Exception):
    def __init__(self, message="Фильтр censor должен использоваться только со строковым типом данных!"):
        self.message = message
        super().__init__(self.message)


register = template.Library()


# Изобрел велосипед)
@register.filter()
def censor(value: str):
    if type(value) != str:
        raise CensorException(f"Значение принимает не допустимый тип ({type(value)})!")
    censored_words = ('редиска', 'баклажан', 'кабачок', 'огурец', 'редька')
    words = value.split(' ')
    idx = 0

    for word in words:
        if len(word) > 2:

            punctuation_flag = None
            if word[-1] in [',', '.', ':', ';', '!', '?']:
                punctuation_flag = word[-1]
                word = word[:-1]

            register_flag = None
            if word[0].isupper():
                register_flag = word[0]
                word = (word[0].lower() + word[1:])

            if word in censored_words:
                clean_word = word[0] + ('*' * (len(word) - 1))
                clean_word = clean_word + punctuation_flag if punctuation_flag else clean_word
                clean_word = register_flag + clean_word[1:] if register_flag else clean_word
                words[idx] = clean_word

            idx += 1
        else:
            idx += 1
    censored_value = ' '.join(words)

    return censored_value
