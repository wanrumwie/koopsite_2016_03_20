import string

map = {
        'А': 'A',
        'Б': 'B',
        'В': 'V',
        'Г': 'H',
        'Д': 'D',
        'Е': 'E',
        'Ж': 'Zh',
        'З': 'Z',
        'И': 'Y',
        'Й': 'I',
        'К': 'K',
        'Л': 'L',
        'М': 'M',
        'Н': 'N',
        'О': 'O',
        'П': 'P',
        'Р': 'R',
        'С': 'S',
        'Т': 'T',
        'У': 'U',
        'Ф': 'F',
        'Х': 'Kh',
        'Ц': 'Ts',
        'Ч': 'Ch',
        'Ш': 'Sh',
        'Щ': 'Shch',
        'Ь': '',
        'Ю': 'Iu',
        'Я': 'Ia',
        'Є': 'Ie',
        'І': 'I',
        'Ї': 'I',
        'Ґ': 'G',
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'h',
        'д': 'd',
        'е': 'e',
        'ж': 'zh',
        'з': 'z',
        'и': 'y',
        'й': 'i',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'kh',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'shch',
        'ь': '',
        'ю': 'iu',
        'я': 'ia',
        'є': 'ie',
        'і': 'i',
        'ї': 'i',
        'ґ': 'g',
}
word_start_map = {
        'Й': 'Y',
        'Ю': 'Yu',
        'Я': 'Ya',
        'Є': 'Ye',
        'Ї': 'Yi',
        'й': 'y',
        'ю': 'yu',
        'я': 'ya',
        'є': 'ye',
        'ї': 'yi',
}
diphthong_map = {
        'ЗГ': 'ZGh',
        'Зг': 'Zgh',
        'зг': 'zgh',
}

def transliterate(s, lang_from='uk', lang_to='en'):
    if lang_from == 'uk' and lang_to == 'en':
        for a in diphthong_map:
            s = s.replace(a, diphthong_map[a])
        words = s.split()
        for i in range(len(words)):
            word = words[i]
            for a in word_start_map:
                if word.startswith(a):
                    b = word_start_map[a]
                    word = word.replace(a, b, 1)
                    words[i] = word
                    break
        s = ' '.join(words)

        trans = []
        for a in s:
            if a in map:
                b = map[a]
            elif not a in string.printable:
                b = '_'
            else:
                b = a
            trans.append(b)
        s = ''.join(trans)
    return s


examples_KMU = [
    ('Алушта      ', 'Alushta'),
    ('Борщагівка  ', 'Borshchahivka'),
    ('Вишгород    ', 'Vyshhorod'),
    ('Гадяч       ', 'Hadiach'),
    ('Згорани     ', 'Zghorany'),
    ('Ґалаґан     ', 'Galagan'),
    ('Дон         ', 'Don'),
    ('Рівне       ', 'Rivne'),
    ('Єнакієве    ', 'Yenakiieve'),
    ('Наєнко      ', 'Naienko'),
    ('Житомир     ', 'Zhytomyr'),
    ('Закарпаття  ', 'Zakarpattia'),
    ('Медвин      ', 'Medvyn'),
    ('Іршава      ', 'Irshava'),
    ('Їжакевич    ', 'Yizhakevych'),
    ('Кадіївка    ', 'Kadiivka'),
    ('Йосипівка   ', 'Yosypivka'),
    ('Стрий       ', 'Stryi'),
    ('Київ        ', 'Kyiv'),
    ('Лебедин     ', 'Lebedyn'),
    ('Миколаїв    ', 'Mykolaiv'),
    ('Ніжин       ', 'Nizhyn'),
    ('Одеса       ', 'Odesa'),
    ('Полтава     ', 'Poltava'),
    ('Ромни       ', 'Romny'),
    ('Суми        ', 'Sumy'),
    ('Тетерів     ', 'Teteriv'),
    ('Ужгород     ', 'Uzhhorod'),
    ('Фастів      ', 'Fastiv'),
    ('Харків      ', 'Kharkiv'),
    ('Біла Церква ', 'Bila Tserkva'),
    ('Чернівці    ', 'Chernivtsi'),
    ('Шостка      ', 'Shostka'),
    ('Гоща        ', 'Hoshcha'),
    ('Юрій        ', 'Yurii'),
    ('Крюківка    ', 'Kriukivka'),
    ('Яготин      ', 'Yahotyn'),
    ('Ічня        ', 'Ichnia'),
]
examples = [
    ('йцукенгшщзхї',    'ytsukenhshshchzkhi'),
    ('ЙЦУКЕНГШЩЗХЇ',    'YTsUKENHShShchZKhI'),
    ('фівапролджє',     'fivaproldzhie'),
    ('ФІВАПРОЛДЖЄ',     'FIVAPROLDZhIe'),
    ('ячсмитьбюґ',      'yachsmytbiug'),
    ('ЯЧСМИТЬБЮҐ',      'YaChSMYTBIuG'),
    ('"`1234567890-=',  '"`1234567890-='),
    ('~!@#$%^&*()_+',   '~!@#$%^&*()_+'),
    (";:',<.>/?|",       ";:',<.>/?|"),
    ('ЪъЫыЭэ',          '______'),
]



import unittest

class TestTransliterate(unittest.TestCase):

    def test_KMU_examples(self):
        for e in examples_KMU:
            ukr = e[0].strip()
            eng = e[1]
            trans = transliterate(ukr)
            self.assertEqual(trans, eng)

    def test_other_examples(self):
        for e in examples:
            ukr = e[0].strip()
            eng = e[1]
            trans = transliterate(ukr)
            self.assertEqual(trans, eng)

if __name__ == '__main__':
    unittest.main()

'''
Українська	Англійська	Коментарі	Приклад
А	А	-	Алушта - Alushta
Б	B	-	Борщагівка - Borshchahivka
В	V	-	Вишгород - Vyshhorod
Г	H	-	Гадяч - Hadiach;Згорани - Zghorany
Ґ	G	-	Ґалаґан - Galagan
Д	D	-	Дон - Don
Е	E	-	Рівне - Rivne
Є	Ye, ie	Ye - на початку слова, іе - в інших позиціях	Єнакієве - Yenakiieve;Наєнко - Naienko
Ж	Zh	-	Житомир - Zhytomyr
З	Z	-	Закарпаття - Zakarpattia
И	Y	-	Медвин - Medvyn
І	I	-	Іршава - Irshava
Ї	Yi, I	Yi - на початку слова, і - в інших позиціях	Їжакевич - Yizhakevych;Кадіївка - Kadiivka
Й	Y, i	Y - на початку слова, і - в інших позиціях	Йосипівка - Yosypivka;Стрий - Stryi
К	K	-	Київ - Kyiv
Л	L	-	Лебедин - Lebedyn
М	M	-	Миколаїв - Mykolaiv
Н	N	-	Ніжин - Nizhyn
О	O	-	Одеса - Odesa
П	P	-	Полтава - Poltava
Р	R	-	Ромни - Romny
С	S	-	Суми - Sumy
Т	T	-	Тетерів - Teteriv
У	U	-	Ужгород - Uzhhorod
Ф	F	-	Фастів - Fastiv
Х	Kh	-	Харків - Kharkiv
Ц	Ts	-	Біла Церква - Bila Tserkva
Ч	Ch	-	Чернівці - Chernivtsi
Ш	Sh	-	Шостка - Shostka
Щ	Shch	-	Гоща -Hoshcha
Ю	Yu, iu	Yu - на початку слова, iu - в інших позиціях	Юрій - Yurii;Крюківка - Kriukivka
Я	Ya, ia	Ya - на початку слова, іа - в інших позиціях	Яготин - Yahotyn;Ічня - Ichnia
'''
