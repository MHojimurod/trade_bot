from django.test import TestCase

# Create your tests here.
a = '<option value="Toshkent">Toshkent</option>'
b = [
{"id":"1","name_uz":"Qoraqalpog‘iston Respublikasi","name_oz":"?îđŕ?ŕëďî?čńňîí Đĺńďóáëčęŕńč","name_ru":"Đĺńďóáëčęŕ Ęŕđŕęŕëďŕęńňŕí"},
{"id":"2","name_uz":"Andijon viloyati","name_oz":"Ŕíäčćîí âčëî˙ňč","name_ru":"Ŕíäčćŕíńęŕ˙ îáëŕńňü"},
{"id":"3","name_uz":"Buxoro viloyati","name_oz":"Áóőîđî âčëî˙ňč","name_ru":"Áóőŕđńęŕ˙ îáëŕńňü"},
{"id":"4","name_uz":"Jizzax viloyati","name_oz":"Ćčççŕő âčëî˙ňč","name_ru":"Äćčçŕęńęŕ˙ îáëŕńňü"},
{"id":"5","name_uz":"Qashqadaryo viloyati","name_oz":"?ŕř?ŕäŕđ¸ âčëî˙ňč","name_ru":"Ęŕřęŕäŕđüčíńęŕ˙ îáëŕńňü"},
{"id":"6","name_uz":"Navoiy viloyati","name_oz":"Íŕâîčé âčëî˙ňč","name_ru":"Íŕâîčéńęŕ˙ îáëŕńňü"},
{"id":"7","name_uz":"Namangan viloyati","name_oz":"Íŕěŕíăŕí âčëî˙ňč","name_ru":"Íŕěŕíăŕíńęŕ˙ îáëŕńňü"},
{"id":"8","name_uz":"Samarqand viloyati","name_oz":"Ńŕěŕđ?ŕíä âčëî˙ňč","name_ru":"Ńŕěŕđęŕíäńęŕ˙ îáëŕńňü"},
{"id":"9","name_uz":"Surxandaryo viloyati","name_oz":"Ńóđőŕíäŕđ¸ âčëî˙ňč","name_ru":"Ńóđőŕíäŕđüčíńęŕ˙ îáëŕńňü"},
{"id":"10","name_uz":"Sirdaryo viloyati","name_oz":"Ńčđäŕđ¸ âčëî˙ňč","name_ru":"Ńűđäŕđüčíńęŕ˙ îáëŕńňü"},
{"id":"11","name_uz":"Toshkent viloyati","name_oz":"Ňîřęĺíň âčëî˙ňč","name_ru":"Ňŕřęĺíňńęŕ˙ îáëŕńňü"},
{"id":"12","name_uz":"Farg‘ona viloyati","name_oz":"Ôŕđ?îíŕ âčëî˙ňč","name_ru":"Ôĺđăŕíńęŕ˙ îáëŕńňü"},
{"id":"13","name_uz":"Xorazm viloyati","name_oz":"Őîđŕçě âčëî˙ňč","name_ru":"Őîđĺçěńęŕ˙ îáëŕńňü"},
{"id":"14","name_uz":"Toshkent shahri","name_oz":"Ňîřęĺíň řŕ?đč","name_ru":"Ăîđîä Ňŕřęĺíň"}]
d = ""
for i in b:
    d+= f'<option value="{i["name_uz"]}">{i["name_uz"]}</option>\n'

print(d)