# Lokalisierungsabgleich

0.9.0 enthält 320 Grundaufgaben und 640 freiwillige Bonusaufgaben in jeweils drei Sprachen. Die Strukturprüfung deckt Übersetzungsfelder, Antwortoptionen, native Lernwörter und kyrillische russische Inhalte ab. Sie ersetzt keine muttersprachliche oder fachliche Freigabe.

809 geänderte Grundaufgaben-Textfelder seit Ausgangscommit `cca9b049c11cc131ef331f064e4fe28af9ec9130` sind unten protokolliert. Bonusinhalte stehen vollständig in `tasks.json` und den versionierten Inhaltsquellen.

## Aktuelle Regeln

- Deutsch vermittelt deutsche, English englische und Русский russische Lernwörter, Anfangsbuchstaben und Silben. Keine automatische deutsche Folgeaufnahme in EN/RU.
- Russische sichtbare Texte, Namen, Musikbeschriftungen und alle 1947 gesprochenen Einträge sind ohne lateinische Buchstaben. Interne stabile IDs und Quellen-/Lizenzdateien sind keine Lerninhalte.
- Englische Silbenvarianten für flower und battery werden akzeptiert. Rechtschreibung und Anfangsbuchstaben sind von Lautschrift zu unterscheiden.
- 200 Sachfragen verwenden Kontextzeichnungen statt Kopien der richtigen Antwort. Kurze Hinweiswörter ergänzen die gesprochene Frage. Auswahlbilder und freigegebene Grundantworten bleiben erhalten.
- Pro Grundaufgabe zwei unabhängig wählbare, überspringbare Herausforderungen mit 50/100 Punkten. Die Sachbonusfragen verwenden wiederkehrende Konzepte; 640 Bonusplätze bedeuten nicht 640 einzigartige redaktionelle Fragestellungen.

## Offene Prüfung

- Muttersprachler: Aussprache, natürliche Formulierungen, Silbenzählung und vollständige russische UI am Android-Gerät.
- Fachpersonen: eindeutige Ablenker, Kontextbilder und höhere Schwierigkeit der Bonusaufgaben; Kinder mit unterschiedlichen Vorkenntnissen.
- Hörprobe ohne eingeblendeten Text, danach im Spiel mit Musik. Technische Dauermessung und ASR sind keine Hörfreigabe.
- Eine identische weibliche Stimme in allen Sprachen ist noch nicht erreicht. Die getestete Umwandlung verschlechterte deutsche Aussprache und wurde nicht ausgeliefert.

## Änderungsprotokoll der Grundaufgaben

| Aufgabe | Sprache | Feld | Vorher | Jetzt |
|---|---|---|---|---|
| math_count | en | prompt | How many can you see? | How many apples can you see? |
| math_count | en | tip | Tap each picture once and count. | Tap each apple once. Count as you go. |
| math_count | ru | prompt | Сколько ты видишь? | Сколько яблок ты видишь? |
| math_count | ru | tip | Коснись каждой картинки один раз и посчитай. | Коснись каждого яблока один раз. Считай при этом. |
| math_add | en | prompt | 3 and 2. How many altogether? | Three apples and two apples. How many altogether? |
| math_add | en | tip | Count the left group, then keep counting the right group. | Count the left group first. Then keep counting on the right. |
| math_add | ru | prompt | 3 и 2. Сколько всего? | Три яблока и два яблока. Сколько всего? |
| math_add | ru | tip | Сначала посчитай слева, затем продолжи считать справа. | Сначала посчитай слева. Затем продолжи считать справа. |
| math_take | en | prompt | There are 7. Take away 3. How many remain? | Seven leaves. Three fly away. How many remain? |
| math_take | en | tip | Count only the pictures without a cross. | Count only the leaves without a cross. |
| math_take | ru | prompt | Было 7. Убрали 3. Сколько осталось? | Семь листьев. Три улетают. Сколько осталось? |
| math_take | ru | tip | Считай только картинки без крестика. | Считай только листья без крестика. |
| math_ten | en | prompt | There are 4. How many more make 10? | Four stars are already there. How many more make ten? |
| math_ten | ru | prompt | Есть 4. Сколько не хватает до 10? | Уже есть четыре звезды. Сколько не хватает до десяти? |
| math_compare | en | prompt | Which group has more? | Where are there more apples? |
| math_compare | en | tip | Count both groups and tap the larger one. | Compare both groups. Tap the larger group. |
| math_compare | ru | prompt | Где больше? | Где больше яблок? |
| math_compare | ru | tip | Посчитай обе группы. Коснись той, где больше. | Сравни обе группы. Коснись той, где больше. |
| math_steps | en | prompt | Which number comes next? | Two, four, six. Which number comes next? |
| math_steps | en | tip | Add 2 each time. | Add two each time. |
| math_steps | ru | prompt | Какое число следующее? | Два, четыре, шесть. Какое число следующее? |
| math_steps | ru | tip | Каждый раз прибавляй 2. | Каждый раз прибавляй два. |
| math_twenty | en | prompt | 10 and 4. How many altogether? | Ten and four. How many altogether? |
| math_twenty | en | tip | Count the left group, then keep counting the right group. | The first group has ten. Count on four more. |
| math_twenty | ru | prompt | 10 и 4. Сколько всего? | Десять и четыре. Сколько всего? |
| math_twenty | ru | tip | Сначала посчитай слева, затем продолжи считать справа. | В первой группе десять. Отсчитай ещё четыре. |
| math_split | en | prompt | There are 5. How many more make 8? | Five stars are already there. How many more make eight? |
| math_split | ru | prompt | Есть 5. Сколько не хватает до 8? | Уже есть пять звёзд. Сколько не хватает до восьми? |
| german_sun | en | prompt | Listen to the German word. Which letter does it start with? | Sun. Which letter comes first? |
| german_sun | en | tip | The German word starts with the letter S. Choose that letter. | Sun starts with S. |
| german_sun | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Солнце. Какая первая буква? |
| german_sun | ru | tip | Немецкое слово начинается с буквы S. Выбери эту букву. | В слове Солнце первая буква С. |
| german_mouse | en | prompt | Listen to the German word. Which letter does it start with? | Mouse. Which letter comes first? |
| german_mouse | en | tip | The German word starts with the letter M. Choose that letter. | Mouse starts with M. |
| german_mouse | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Мышь. Какая первая буква? |
| german_mouse | ru | tip | Немецкое слово начинается с буквы M. Выбери эту букву. | В слове Мышь первая буква М. |
| german_apple | en | prompt | Listen to the German word. Which letter does it start with? | Apple. Which letter comes first? |
| german_apple | en | tip | The German word starts with the letter A. Choose that letter. | Apple starts with A. |
| german_apple | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Яблоко. Какая первая буква? |
| german_apple | ru | tip | Немецкое слово начинается с буквы A. Выбери эту букву. | В слове Яблоко первая буква Я. |
| german_rhyme | en | prompt | Listen to the German words. Which one rhymes with the word for house? | House. Which word rhymes? |
| german_rhyme | en | tip | The German words for house and mouse rhyme: listen to the German example. | House and mouse have the same ending sound. |
| german_rhyme | ru | prompt | Послушай немецкие слова. Какое рифмуется со словом «дом» по-немецки? | Дом. Какое слово рифмуется? |
| german_rhyme | ru | tip | Немецкие слова «дом» и «мышь» рифмуются. Послушай пример по-немецки. | Дом и сом звучат похоже в конце. |
| german_robot | en | prompt | Listen to the German word. How many syllables does it have? | Robot. How many syllables? |
| german_robot | en | tip | Clap along with the German word. It has 3 syllables. | Say and clap: Ro. Bot. |
| german_robot | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Робот. Сколько слогов? |
| german_robot | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 3 слога. | Произнеси и хлопай: Ро. Бот. |
| german_read | en | prompt | Which German word matches the picture? | Which word matches the picture? |
| german_read | en | tip | Match the written German word to the picture. Listen to its German reading next. | The word is Ball. |
| german_read | ru | prompt | Какое немецкое слово подходит к картинке? | Какое слово подходит к картинке? |
| german_read | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Это слово Мяч. |
| german_flower | en | prompt | Listen to the German word. How many syllables does it have? | Flower. How many syllables? |
| german_flower | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Flow. Er. |
| german_flower | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Цветок. Сколько слогов? |
| german_flower | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Цве. Ток. |
| german_fish | en | prompt | Listen to the German word. Which letter does it start with? | Fish. Which letter comes first? |
| german_fish | en | tip | The German word starts with the letter F. Choose that letter. | Fish starts with F. |
| german_fish | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Рыба. Какая первая буква? |
| german_fish | ru | tip | Немецкое слово начинается с буквы F. Выбери эту букву. | В слове Рыба первая буква Р. |
| math_09 | de | prompt | Wie viele siehst du? | Wie viele Bienen siehst du? |
| math_09 | en | prompt | How many can you see? | How many bees can you see? |
| math_09 | ru | prompt | Сколько ты видишь? | Сколько пчёл ты видишь? |
| math_10 | de | prompt | Wie viele siehst du? | Wie viele Fische siehst du? |
| math_10 | en | prompt | How many can you see? | How many fish can you see? |
| math_10 | ru | prompt | Сколько ты видишь? | Сколько рыб ты видишь? |
| math_11 | de | prompt | Wie viele siehst du? | Wie viele Blumen siehst du? |
| math_11 | en | prompt | How many can you see? | How many flowers can you see? |
| math_11 | ru | prompt | Сколько ты видишь? | Сколько цветов ты видишь? |
| math_12 | de | prompt | Wie viele siehst du? | Wie viele Blätter siehst du? |
| math_12 | en | prompt | How many can you see? | How many leaves can you see? |
| math_12 | ru | prompt | Сколько ты видишь? | Сколько листьев ты видишь? |
| math_13 | de | prompt | Wie viele siehst du? | Wie viele Sterne siehst du? |
| math_13 | en | prompt | How many can you see? | How many stars can you see? |
| math_13 | ru | prompt | Сколько ты видишь? | Сколько звёзд ты видишь? |
| math_14 | de | prompt | Wie viele siehst du? | Wie viele Äpfel siehst du? |
| math_14 | en | prompt | How many can you see? | How many apples can you see? |
| math_14 | ru | prompt | Сколько ты видишь? | Сколько яблок ты видишь? |
| german_09 | en | prompt | Listen to the German word. Which letter does it start with? | Bee. Which letter comes first? |
| german_09 | en | tip | The German word starts with the letter B. Choose that letter. | Bee starts with B. |
| german_09 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Пчела. Какая первая буква? |
| german_09 | ru | tip | Немецкое слово начинается с буквы B. Выбери эту букву. | В слове Пчела первая буква П. |
| german_10 | en | prompt | Listen to the German word. Which letter does it start with? | Frog. Which letter comes first? |
| german_10 | en | tip | The German word starts with the letter F. Choose that letter. | Frog starts with F. |
| german_10 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Лягушка. Какая первая буква? |
| german_10 | ru | tip | Немецкое слово начинается с буквы F. Выбери эту букву. | В слове Лягушка первая буква Л. |
| german_11 | en | prompt | Listen to the German word. Which letter does it start with? | Cat. Which letter comes first? |
| german_11 | en | tip | The German word starts with the letter K. Choose that letter. | Cat starts with C. |
| german_11 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Кошка. Какая первая буква? |
| german_11 | ru | tip | Немецкое слово начинается с буквы K. Выбери эту букву. | В слове Кошка первая буква К. |
| german_12 | en | prompt | Listen to the German word. Which letter does it start with? | Nest. Which letter comes first? |
| german_12 | en | tip | The German word starts with the letter N. Choose that letter. | Nest starts with N. |
| german_12 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Гнездо. Какая первая буква? |
| german_12 | ru | tip | Немецкое слово начинается с буквы N. Выбери эту букву. | В слове Гнездо первая буква Г. |
| german_13 | en | prompt | Listen to the German word. Which letter does it start with? | Worm. Which letter comes first? |
| german_13 | en | tip | The German word starts with the letter W. Choose that letter. | Worm starts with W. |
| german_13 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Червяк. Какая первая буква? |
| german_13 | ru | tip | Немецкое слово начинается с буквы W. Выбери эту букву. | В слове Червяк первая буква Ч. |
| german_14 | en | prompt | Listen to the German word. Which letter does it start with? | Water. Which letter comes first? |
| german_14 | en | tip | The German word starts with the letter W. Choose that letter. | Water starts with W. |
| german_14 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Вода. Какая первая буква? |
| german_14 | ru | tip | Немецкое слово начинается с буквы W. Выбери эту букву. | В слове Вода первая буква В. |
| german_15 | en | prompt | Listen to the German word. Which letter does it start with? | Salt. Which letter comes first? |
| german_15 | en | tip | The German word starts with the letter S. Choose that letter. | Salt starts with S. |
| german_15 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Соль. Какая первая буква? |
| german_15 | ru | tip | Немецкое слово начинается с буквы S. Выбери эту букву. | В слове Соль первая буква С. |
| german_16 | en | prompt | Listen to the German word. Which letter does it start with? | Sand. Which letter comes first? |
| german_16 | en | tip | The German word starts with the letter S. Choose that letter. | Sand starts with S. |
| german_16 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Песок. Какая первая буква? |
| german_16 | ru | tip | Немецкое слово начинается с буквы S. Выбери эту букву. | В слове Песок первая буква П. |
| german_17 | en | prompt | Listen to the German word. Which letter does it start with? | Wood. Which letter comes first? |
| german_17 | en | tip | The German word starts with the letter H. Choose that letter. | Wood starts with W. |
| german_17 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Дерево. Какая первая буква? |
| german_17 | ru | tip | Немецкое слово начинается с буквы H. Выбери эту букву. | В слове Дерево первая буква Д. |
| german_18 | en | prompt | Listen to the German word. Which letter does it start with? | Nose. Which letter comes first? |
| german_18 | en | tip | The German word starts with the letter N. Choose that letter. | Nose starts with N. |
| german_18 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Нос. Какая первая буква? |
| german_18 | ru | tip | Немецкое слово начинается с буквы N. Выбери эту букву. | В слове Нос первая буква Н. |
| german_19 | en | prompt | Listen to the German word. Which letter does it start with? | Hand. Which letter comes first? |
| german_19 | en | tip | The German word starts with the letter H. Choose that letter. | Hand starts with H. |
| german_19 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Рука. Какая первая буква? |
| german_19 | ru | tip | Немецкое слово начинается с буквы H. Выбери эту букву. | В слове Рука первая буква Р. |
| german_20 | en | prompt | Listen to the German word. Which letter does it start with? | Heart. Which letter comes first? |
| german_20 | en | tip | The German word starts with the letter H. Choose that letter. | Heart starts with H. |
| german_20 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Сердце. Какая первая буква? |
| german_20 | ru | tip | Немецкое слово начинается с буквы H. Выбери эту букву. | В слове Сердце первая буква С. |
| german_21 | en | prompt | Listen to the German word. How many syllables does it have? | Butterfly. How many syllables? |
| german_21 | en | tip | Clap along with the German word. It has 3 syllables. | Say and clap: But. Ter. Fly. |
| german_21 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Бабочка. Сколько слогов? |
| german_21 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 3 слога. | Произнеси и хлопай: Ба. Боч. Ка. |
| german_22 | en | prompt | Listen to the German word. How many syllables does it have? | Turtle. How many syllables? |
| german_22 | en | tip | Clap along with the German word. It has 3 syllables. | Say and clap: Tur. Tle. |
| german_22 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Черепаха. Сколько слогов? |
| german_22 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 3 слога. | Произнеси и хлопай: Че. Ре. Па. Ха. |
| german_23 | en | prompt | Listen to the German word. How many syllables does it have? | Battery. How many syllables? |
| german_23 | en | tip | Clap along with the German word. It has 3 syllables. | Say and clap: Bat. Ter. Y. |
| german_23 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Батарейка. Сколько слогов? |
| german_23 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 3 слога. | Произнеси и хлопай: Ба. Та. Рей. Ка. |
| german_24 | en | prompt | Listen to the German word. How many syllables does it have? | Paper. How many syllables? |
| german_24 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Pa. Per. |
| german_24 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Бумага. Сколько слогов? |
| german_24 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Бу. Ма. Га. |
| german_25 | en | prompt | Listen to the German word. How many syllables does it have? | Soap. How many syllables? |
| german_25 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Soap. |
| german_25 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Мыло. Сколько слогов? |
| german_25 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Мы. Ло. |
| german_26 | en | prompt | Listen to the German word. How many syllables does it have? | Eye. How many syllables? |
| german_26 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Eye. |
| german_26 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Глаз. Сколько слогов? |
| german_26 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Глаз. |
| german_27 | en | prompt | Listen to the German word. How many syllables does it have? | Brain. How many syllables? |
| german_27 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Brain. |
| german_27 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Мозг. Сколько слогов? |
| german_27 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Мозг. |
| german_28 | en | prompt | Listen to the German word. How many syllables does it have? | Stomach. How many syllables? |
| german_28 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Stom. Ach. |
| german_28 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Желудок. Сколько слогов? |
| german_28 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Же. Лу. Док. |
| german_29 | en | prompt | Listen to the German word. How many syllables does it have? | Cloud. How many syllables? |
| german_29 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Cloud. |
| german_29 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Облако. Сколько слогов? |
| german_29 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Об. Ла. Ко. |
| german_30 | en | prompt | Listen to the German word. How many syllables does it have? | Rain. How many syllables? |
| german_30 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Rain. |
| german_30 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Дождь. Сколько слогов? |
| german_30 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Дождь. |
| german_31 | en | prompt | Listen to the German word. How many syllables does it have? | Island. How many syllables? |
| german_31 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Is. Land. |
| german_31 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Остров. Сколько слогов? |
| german_31 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Ос. Тров. |
| german_32 | en | prompt | Listen to the German word. How many syllables does it have? | Hammer. How many syllables? |
| german_32 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Ham. Mer. |
| german_32 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Молоток. Сколько слогов? |
| german_32 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Мо. Ло. Ток. |
| german_33 | en | tip | Match the written German word to the picture. Listen to its German reading next. | The word is Fish. |
| german_33 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Это слово Рыба. |
| german_34 | en | tip | Match the written German word to the picture. Listen to its German reading next. | The word is Bird. |
| german_34 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Это слово Птица. |
| german_35 | en | tip | Match the written German word to the picture. Listen to its German reading next. | The word is Moon. |
| german_35 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Это слово Луна. |
| german_36 | en | tip | Match the written German word to the picture. Listen to its German reading next. | The word is Tree. |
| german_36 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Это слово Дерево. |
| german_37 | en | tip | Match the written German word to the picture. Listen to its German reading next. | The word is Tooth. |
| german_37 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Это слово Зуб. |
| german_38 | en | tip | Match the written German word to the picture. Listen to its German reading next. | The word is Foot. |
| german_38 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Это слово Стопа. |
| german_39 | en | tip | Match the written German word to the picture. Listen to its German reading next. | The word is Egg. |
| german_39 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Это слово Яйцо. |
| german_40 | en | tip | Match the written German word to the picture. Listen to its German reading next. | The word is Sea. |
| german_40 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Это слово Море. |
| physics_18 | en | tip | A hand can push the ball and make it move. | A hand can exert a force on the ball and make it move. |
| physics_18 | ru | tip | Рука может подействовать на мяч и привести его в движение. | Рука может подействовать на мяч с силой и привести его в движение. |
| biology_25 | en | prompt | Where do many trees grow together? | Life. Where do many trees grow close together? |
| biology_25 | ru | prompt | Где много деревьев растёт рядом? | Жизнь. Где много деревьев растёт близко друг к другу? |
| biology_37 | ru | tip | Дождевые черви затаскивают опавшие листья в свои ходы. | Дождевые черви затаскивают отмершие опавшие листья в свои ходы. |
| body_17 | en | prompt | Which body part needs protection from very loud sounds? | Hearing. Which body part needs protection from loud noise? |
| body_17 | ru | prompt | Что нужно защищать от очень громких звуков? | Слух. Какую часть тела нужно защищать от шума? |
| body_24 | ru | prompt | Где обрабатываются воспоминания? | Мысли. Какой орган обрабатывает воспоминания? |
| geography_33 | ru | prompt | Что течёт, имеет русло и два берега? | Открытие. Что длинное, течёт и имеет два берега? |
| german_33 | en | prompt | Which German word matches the picture? | Which word matches the picture? |
| german_33 | ru | prompt | Какое немецкое слово подходит к картинке? | Какое слово подходит к картинке? |
| german_34 | en | prompt | Which German word matches the picture? | Which word matches the picture? |
| german_34 | ru | prompt | Какое немецкое слово подходит к картинке? | Какое слово подходит к картинке? |
| german_35 | en | prompt | Which German word matches the picture? | Which word matches the picture? |
| german_35 | ru | prompt | Какое немецкое слово подходит к картинке? | Какое слово подходит к картинке? |
| german_36 | en | prompt | Which German word matches the picture? | Which word matches the picture? |
| german_36 | ru | prompt | Какое немецкое слово подходит к картинке? | Какое слово подходит к картинке? |
| german_37 | en | prompt | Which German word matches the picture? | Which word matches the picture? |
| german_37 | ru | prompt | Какое немецкое слово подходит к картинке? | Какое слово подходит к картинке? |
| german_38 | en | prompt | Which German word matches the picture? | Which word matches the picture? |
| german_38 | ru | prompt | Какое немецкое слово подходит к картинке? | Какое слово подходит к картинке? |
| german_39 | en | prompt | Which German word matches the picture? | Which word matches the picture? |
| german_39 | ru | prompt | Какое немецкое слово подходит к картинке? | Какое слово подходит к картинке? |
| german_40 | en | prompt | Which German word matches the picture? | Which word matches the picture? |
| german_40 | ru | prompt | Какое немецкое слово подходит к картинке? | Какое слово подходит к картинке? |
| physics_01 | de | prompt | Was lässt ein Fahrrad rollen? | Bewegen. Was lässt ein Fahrrad rollen? |
| physics_01 | en | prompt | What lets a bicycle roll? | Motion. What lets a bicycle roll? |
| physics_01 | ru | prompt | Что помогает велосипеду катиться? | Движение. Что помогает велосипеду катиться? |
| physics_02 | de | prompt | Womit schneidest du Papier? | Werkeln. Womit schneidest du Papier? |
| physics_02 | en | prompt | What cuts paper? | Making. What cuts paper? |
| physics_02 | ru | prompt | Чем режут бумагу? | Мастерская. Чем режут бумагу? |
| physics_03 | de | prompt | Womit schlägt man einen Nagel ein? | Werkeln. Womit schlägt man einen Nagel ein? |
| physics_03 | en | prompt | What drives a nail into wood? | Build. What drives a nail into wood? |
| physics_03 | ru | prompt | Чем забивают гвоздь в дерево? | Мастерить. Чем забивают гвоздь в дерево? |
| physics_04 | de | prompt | Was dreht eine Schraube? | Werkeln. Was dreht eine Schraube? |
| physics_04 | en | prompt | What turns a screw? | Making. What turns a screw? |
| physics_04 | ru | prompt | Чем поворачивают винт? | Мастерская. Чем поворачивают винт? |
| physics_05 | de | prompt | Was zieht ein Magnet an: Eisen, Holz oder Papier? | Verändern. Eisen, Holz, Papier. Was zieht ein Magnet an? |
| physics_05 | en | prompt | What does a magnet attract: iron, wood or paper? | Change. Iron, wood, paper. Which does a magnet attract? |
| physics_05 | ru | prompt | Что притягивает магнит: железо, дерево или бумагу? | Изменение. Железо, дерево, бумага. Что притянет магнит? |
| physics_06 | de | prompt | Was führt einen Weg über einen Fluss? | Entdecken. Was führt einen Weg über einen Fluss? |
| physics_06 | en | prompt | What carries a path across a river? | Explore. What carries a path across a river? |
| physics_06 | ru | prompt | Что проводит дорогу через реку? | Открытие. Что проводит дорогу через реку? |
| physics_07 | de | prompt | Was macht eine dunkle Ecke hell? | Leuchten. Was macht eine dunkle Ecke hell? |
| physics_07 | en | prompt | What lights up a dark corner? | Light. What lights up a dark corner? |
| physics_07 | ru | prompt | Что освещает тёмный угол? | Свет. Что освещает тёмный угол? |
| physics_08 | de | prompt | Was versorgt eine Taschenlampe mit Energie? | Versorgen. Was versorgt eine Taschenlampe mit Energie? |
| physics_08 | en | prompt | What supplies energy to a battery-powered torch? | Power. What supplies energy to a battery-powered torch? |
| physics_08 | ru | prompt | Что даёт энергию карманному фонарику? | Энергия. Что даёт энергию карманному фонарику? |
| physics_09 | de | prompt | Was schützt beim Radfahren den Kopf? | Schützen. Was schützt beim Radfahren den Kopf? |
| physics_09 | en | prompt | What protects your head when cycling? | Protection. What protects your head when cycling? |
| physics_09 | ru | prompt | Что защищает голову при езде на велосипеде? | Защита. Что защищает голову при езде на велосипеде? |
| physics_10 | de | prompt | Was hat Zähne und überträgt Drehbewegungen? | Übertragen. Was hat Zähne und überträgt Drehbewegungen? |
| physics_10 | en | prompt | What has teeth and passes on a turning movement? | Transfer. What has teeth and passes on a turning movement? |
| physics_10 | ru | prompt | Что имеет зубцы и передаёт вращение? | Передавать. Что имеет зубцы и передаёт вращение? |
| physics_11 | de | prompt | Welches Gerät kippt um einen Drehpunkt? | Werkeln. Welches Gerät kippt um einen Drehpunkt? |
| physics_11 | en | prompt | Which device tilts around a pivot? | Making. Which device tilts around a pivot? |
| physics_11 | ru | prompt | Какое устройство качается вокруг опоры? | Мастерская. Какое устройство качается вокруг опоры? |
| physics_12 | de | prompt | Was lenkt ein Seil beim Hochziehen um? | Umlenken. Was lenkt ein Seil beim Hochziehen um? |
| physics_12 | en | prompt | What changes a rope's direction when lifting? | Direction. What changes a rope's direction when lifting? |
| physics_12 | ru | prompt | Что меняет направление верёвки при подъёме? | Направление. Что меняет направление верёвки при подъёме? |
| physics_13 | de | prompt | Wodurch kannst du gut hindurchsehen? | Leuchten. Wodurch kannst du gut hindurchsehen? |
| physics_13 | en | prompt | Which material can you see through clearly? | Light. Which material can you see through clearly? |
| physics_13 | ru | prompt | Сквозь какой материал хорошо видно? | Свет. Сквозь какой материал хорошо видно? |
| physics_14 | de | prompt | Welcher Baustoff kommt von Bäumen? | Ausprobieren. Welcher Baustoff kommt von Bäumen? |
| physics_14 | en | prompt | Which building material comes from trees? | Experiment. Which building material comes from trees? |
| physics_14 | ru | prompt | Какой строительный материал получают из деревьев? | Опыт. Какой строительный материал получают из деревьев? |
| physics_15 | de | prompt | Welches Material eignet sich für ein weiches Tuch? | Fühlen. Welches Material eignet sich für ein weiches Tuch? |
| physics_15 | en | prompt | Which material makes a soft cloth? | Touch. Which material makes a soft cloth? |
| physics_15 | ru | prompt | Какой материал подходит для мягкой ткани? | Осязание. Какой материал подходит для мягкой ткани? |
| physics_16 | de | prompt | Worauf kannst du einen Bauplan zeichnen? | Ausprobieren. Worauf kannst du einen Bauplan zeichnen? |
| physics_16 | en | prompt | What can you draw a building plan on? | Experiment. What can you draw a building plan on? |
| physics_16 | ru | prompt | На чём можно нарисовать план постройки? | Опыт. На чём можно нарисовать план постройки? |
| physics_17 | de | prompt | Was hilft dir, Norden zu finden? | Orientieren. Was hilft dir, Norden zu finden? |
| physics_17 | en | prompt | What helps you find north? | Direction. What helps you find north? |
| physics_17 | ru | prompt | Что помогает найти север? | Ориентир. Что помогает найти север? |
| physics_18 | de | prompt | Was kann einen ruhenden Ball anschubsen? | Ausprobieren. Was kann einen ruhenden Ball anschubsen? |
| physics_18 | en | prompt | What can push a ball that is still? | Experiment. What can push a ball that is still? |
| physics_18 | ru | prompt | Что может толкнуть неподвижный мяч? | Опыт. Что может толкнуть неподвижный мяч? |
| physics_19 | de | prompt | Was entsteht, wenn Eis gerade schmilzt? | Verändern. Was entsteht, wenn Eis gerade schmilzt? |
| physics_19 | en | prompt | What forms when ice is melting? | Change. What forms when ice is melting? |
| physics_19 | ru | prompt | Что образуется, когда лёд тает? | Изменение. Что образуется, когда лёд тает? |
| physics_20 | de | prompt | Was wirft im Lampenlicht einen deutlichen Schatten: Holz, klares Glas oder klares Wasser? | Leuchten. Was wirft einen deutlichen Schatten: Holz, klares Glas oder klares Wasser? |
| physics_20 | en | prompt | What casts a clear shadow in lamp light: wood, clear glass or clear water? | Light. What casts a clear shadow: wood, clear glass or clear water? |
| physics_20 | ru | prompt | Что даёт отчётливую тень в свете лампы: дерево, прозрачное стекло или прозрачная вода? | Свет. Что даёт чёткую тень: дерево, прозрачное стекло или чистая вода? |
| physics_21 | de | prompt | Was schwimmt meist: ein leichtes trockenes Holzstück, ein Eisenklotz oder Sand? | Verändern. Was schwimmt meist: trockenes leichtes Holz, Eisen oder Sand? |
| physics_21 | en | prompt | What usually floats: a light dry piece of wood, an iron block or sand? | Change. Which usually floats: light dry wood, iron or sand? |
| physics_21 | ru | prompt | Что обычно плавает: лёгкая сухая деревяшка, железный брусок или песок? | Изменение. Что обычно плавает: лёгкое сухое дерево, железо или песок? |
| physics_22 | de | prompt | Wodurch kann Licht gut hindurchscheinen? | Leuchten. Wodurch kann Licht gut hindurchscheinen? |
| physics_22 | en | prompt | Which material lets light pass through clearly? | Light. Which material lets light pass through clearly? |
| physics_22 | ru | prompt | Какой материал хорошо пропускает свет? | Свет. Какой материал хорошо пропускает свет? |
| physics_23 | de | prompt | Welcher Körperteil nimmt Schallwellen wahr? | Hören. Welcher Körperteil nimmt Schallwellen wahr? |
| physics_23 | en | prompt | Which body part detects sound waves? | Hearing. Which body part detects sound waves? |
| physics_23 | ru | prompt | Какая часть тела воспринимает звуковые волны? | Слух. Какая часть тела воспринимает звуковые волны? |
| physics_24 | de | prompt | Was dämpft Klopfgeräusche auf einem Tisch am besten: ein weiches Tuch, Glas oder Eisen? | Fühlen. Was dämpft Klopfen besser: weiches Tuch, Glas oder Eisen? |
| physics_24 | en | prompt | What best softens tapping sounds on a table: a soft cloth, glass or iron? | Touch. What cushions tapping better: soft cloth, glass or iron? |
| physics_24 | ru | prompt | Что лучше приглушает стук по столу: мягкая ткань, стекло или железо? | Осязание. Что лучше приглушит стук: мягкая ткань, стекло или железо? |
| physics_25 | de | prompt | Was erzeugt selbst Licht: Sonne, Mond oder Wolke? | Leuchten. Was erzeugt selbst Licht: Sonne, Mond oder Wolke? |
| physics_25 | en | prompt | Which makes its own light: the sun, the moon or a cloud? | Light. Which makes its own light: the sun, the moon or a cloud? |
| physics_25 | ru | prompt | Что само создаёт свет: Солнце, Луна или облако? | Свет. Что само создаёт свет: Солнце, Луна или облако? |
| physics_26 | de | prompt | Welcher dieser Stoffe hat eine feste eigene Form? | Verändern. Welcher dieser Stoffe hat eine feste eigene Form? |
| physics_26 | en | prompt | Which of these has its own solid shape? | Change. Which of these has its own solid shape? |
| physics_26 | ru | prompt | Что из этого имеет собственную твёрдую форму? | Изменение. Что из этого имеет собственную твёрдую форму? |
| physics_27 | de | prompt | Was entsteht unsichtbar, wenn Wasser verdunstet? | Verwandeln. Was entsteht unsichtbar, wenn Wasser verdunstet? |
| physics_27 | en | prompt | What forms invisibly when water evaporates? | Changing. What forms invisibly when water evaporates? |
| physics_27 | ru | prompt | Что незаметно образуется, когда вода испаряется? | Превращение. Что незаметно образуется, когда вода испаряется? |
| physics_28 | de | prompt | Was gibt Licht und Wärme ab, durch die Eis draußen schmelzen kann? | Leuchten. Was gibt Licht und Wärme ab, durch die Eis draußen schmelzen kann? |
| physics_28 | en | prompt | What gives off light and warmth that can melt ice outdoors? | Light. What gives off light and warmth that can melt ice outdoors? |
| physics_28 | ru | prompt | Что излучает свет и тепло, от которых лёд на улице может растаять? | Свет. Что излучает свет и тепло, от которых лёд на улице может растаять? |
| physics_29 | de | prompt | Was zeigt Straßen und Wege als Zeichnung? | Orientieren. Was zeigt Straßen und Wege als Zeichnung? |
| physics_29 | en | prompt | What shows roads and paths in a drawing? | Direction. What shows roads and paths in a drawing? |
| physics_29 | ru | prompt | Что показывает дороги и тропинки на рисунке? | Ориентир. Что показывает дороги и тропинки на рисунке? |
| physics_30 | de | prompt | Womit hörst du, ob eine Fahrradklingel klingelt? | Hören. Womit hörst du, ob eine Fahrradklingel klingelt? |
| physics_30 | en | prompt | How do you hear a bicycle bell? | Hearing. How do you hear a bicycle bell? |
| physics_30 | ru | prompt | Чем ты слышишь велосипедный звонок? | Слух. Чем ты слышишь велосипедный звонок? |
| physics_31 | de | prompt | Welches Material ist für eine stabile Fahrrad-Radachse üblich? | Bewegen. Welches Material ist für eine stabile Fahrrad-Radachse üblich? |
| physics_31 | en | prompt | Which material is normally used for a strong bicycle wheel axle? | Motion. Which material is normally used for a strong bicycle wheel axle? |
| physics_31 | ru | prompt | Из какого материала обычно делают прочную ось велосипедного колеса? | Движение. Из какого материала обычно делают прочную ось велосипедного колеса? |
| physics_32 | de | prompt | Welches Bauwerk braucht tragfähige Stützen? | Ausprobieren. Welches Bauwerk braucht tragfähige Stützen? |
| physics_32 | en | prompt | Which structure needs strong supports? | Experiment. Which structure needs strong supports? |
| physics_32 | ru | prompt | Какому сооружению нужны прочные опоры? | Опыт. Какому сооружению нужны прочные опоры? |
| physics_33 | de | prompt | Was nimmt Wasser beim Abtrocknen gut auf: Stoff, Glas oder Eisen? | Verändern. Was nimmt Wasser beim Abtrocknen gut auf: Stoff, Glas oder Eisen? |
| physics_33 | en | prompt | What soaks up water well when drying: fabric, glass or iron? | Change. What soaks up water well when drying: fabric, glass or iron? |
| physics_33 | ru | prompt | Что хорошо впитывает воду при вытирании: ткань, стекло или железо? | Изменение. Что хорошо впитывает воду при вытирании: ткань, стекло или железо? |
| physics_34 | de | prompt | Was kann eine Solarzelle mit Energie versorgen? | Versorgen. Was kann eine Solarzelle mit Energie versorgen? |
| physics_34 | en | prompt | What supplies energy to a solar cell? | Power. What supplies energy to a solar cell? |
| physics_34 | ru | prompt | Что даёт энергию солнечной батарее? | Энергия. Что даёт энергию солнечной батарее? |
| physics_35 | de | prompt | Was dreht sich an einem fahrenden Fahrrad? | Bewegen. Was dreht sich an einem fahrenden Fahrrad? |
| physics_35 | en | prompt | What turns on a moving bicycle? | Motion. What turns on a moving bicycle? |
| physics_35 | ru | prompt | Что вращается у едущего велосипеда? | Движение. Что вращается у едущего велосипеда? |
| physics_36 | de | prompt | Woraus besteht eine durchsichtige Fensterscheibe? | Leuchten. Woraus besteht eine durchsichtige Fensterscheibe? |
| physics_36 | en | prompt | What is a transparent window pane made of? | Light. What is a transparent window pane made of? |
| physics_36 | ru | prompt | Из чего делают прозрачное оконное стекло? | Свет. Из чего делают прозрачное оконное стекло? |
| physics_37 | de | prompt | Welches Material kannst du mit einer Stoffschere schneiden? | Werkeln. Welches Material kannst du mit einer Stoffschere schneiden? |
| physics_37 | en | prompt | Which material can fabric scissors cut? | Making. Which material can fabric scissors cut? |
| physics_37 | ru | prompt | Какой материал можно разрезать ножницами для ткани? | Мастерская. Какой материал можно разрезать ножницами для ткани? |
| physics_38 | de | prompt | Welcher Teil einer Seilrolle dreht sich? | Bewegen. Welcher Teil einer Seilrolle dreht sich? |
| physics_38 | en | prompt | Which part of a pulley turns? | Motion. Which part of a pulley turns? |
| physics_38 | ru | prompt | Какая часть блока вращается? | Движение. Какая часть блока вращается? |
| physics_39 | de | prompt | Was gehört in das Batteriefach einer Spielzeuglampe? | Versorgen. Was gehört in das Batteriefach einer Spielzeuglampe? |
| physics_39 | en | prompt | What goes in a toy lamp's battery compartment? | Power. What goes in a toy lamp's battery compartment? |
| physics_39 | ru | prompt | Что кладут в отсек питания игрушечного фонарика? | Питать. Что кладут в отсек питания игрушечного фонарика? |
| physics_40 | de | prompt | Was hat einen Nordpol und einen Südpol? | Ausprobieren. Was hat einen Nordpol und einen Südpol? |
| physics_40 | en | prompt | What has a north pole and a south pole? | Experiment. What has a north pole and a south pole? |
| physics_40 | ru | prompt | У чего есть северный и южный полюс? | Опыт. У чего есть северный и южный полюс? |
| biology_01 | de | prompt | Wo kann ein Fisch mit Kiemen atmen? | Entwickeln. Wo kann ein Fisch mit Kiemen atmen? |
| biology_01 | en | prompt | Where can a fish breathe with gills? | Life. Where can a fish breathe with gills? |
| biology_01 | ru | prompt | Где рыба дышит жабрами? | Жизнь. Где рыба дышит жабрами? |
| biology_02 | de | prompt | Wo brütet ein Amselvogel seine Eier aus? | Entwickeln. Wo brütet ein Amselvogel seine Eier aus? |
| biology_02 | en | prompt | Where does a blackbird hatch its eggs? | Life. Where does a blackbird hatch its eggs? |
| biology_02 | ru | prompt | Где дрозд высиживает яйца? | Жизнь. Где дрозд высиживает яйца? |
| biology_03 | de | prompt | Wo findet eine Biene Nektar? | Wachsen. Wo findet eine Biene Nektar? |
| biology_03 | en | prompt | Where does a bee find nectar? | Growing. Where does a bee find nectar? |
| biology_03 | ru | prompt | Где пчела находит нектар? | Рост. Где пчела находит нектар? |
| biology_04 | de | prompt | Womit nimmt ein Baum Wasser aus dem Boden auf? | Verwandeln. Womit nimmt ein Baum Wasser aus dem Boden auf? |
| biology_04 | en | prompt | What takes water from the soil into a tree? | Changing. What takes water from the soil into a tree? |
| biology_04 | ru | prompt | Чем дерево впитывает воду из земли? | Превращение. Чем дерево впитывает воду из земли? |
| biology_05 | de | prompt | Was braucht ein Samen zum Keimen? | Wachsen. Was braucht ein Samen zum Keimen? |
| biology_05 | en | prompt | What does a seed need to start growing? | Growing. What does a seed need to start growing? |
| biology_05 | ru | prompt | Что нужно семени для прорастания? | Рост. Что нужно семени для прорастания? |
| biology_06 | de | prompt | Was liefert einer grünen Pflanze Licht zum Wachsen? | Leuchten. Was liefert einer grünen Pflanze Licht zum Wachsen? |
| biology_06 | en | prompt | What gives a green plant light to grow? | Light. What gives a green plant light to grow? |
| biology_06 | ru | prompt | Что даёт зелёному растению свет для роста? | Свет. Что даёт зелёному растению свет для роста? |
| biology_07 | de | prompt | Welches Tier entsteht aus einer Raupe? | Entwickeln. Welches Tier entsteht aus einer Raupe? |
| biology_07 | en | prompt | Which animal develops from a caterpillar? | Life. Which animal develops from a caterpillar? |
| biology_07 | ru | prompt | Какое животное вырастает из гусеницы? | Жизнь. Какое животное вырастает из гусеницы? |
| biology_08 | de | prompt | Welches Tier wächst aus einer Kaulquappe heran? | Entwickeln. Welches Tier wächst aus einer Kaulquappe heran? |
| biology_08 | en | prompt | Which animal grows from a tadpole? | Life. Which animal grows from a tadpole? |
| biology_08 | ru | prompt | Кто вырастает из головастика? | Жизнь. Кто вырастает из головастика? |
| biology_09 | de | prompt | Wer kann aus einem Hühnerei schlüpfen? | Entwickeln. Wer kann aus einem Hühnerei schlüpfen? |
| biology_09 | en | prompt | What can hatch from a hen's egg? | Life. What can hatch from a hen's egg? |
| biology_09 | ru | prompt | Кто может вылупиться из куриного яйца? | Жизнь. Кто может вылупиться из куриного яйца? |
| biology_10 | de | prompt | Welches Tier ist ein Säugetier? | Entwickeln. Welches Tier ist ein Säugetier? |
| biology_10 | en | prompt | Which animal is a mammal? | Life. Which animal is a mammal? |
| biology_10 | ru | prompt | Кто из них млекопитающее? | Жизнь. Кто из них млекопитающее? |
| biology_11 | de | prompt | Wer hat Federn? | Entwickeln. Wer hat Federn? |
| biology_11 | en | prompt | Which animal has feathers? | Life. Which animal has feathers? |
| biology_11 | ru | prompt | У кого есть перья? | Жизнь. У кого есть перья? |
| biology_12 | de | prompt | Wer trägt einen festen Panzer? | Entwickeln. Wer trägt einen festen Panzer? |
| biology_12 | en | prompt | Which animal has a hard shell? | Life. Which animal has a hard shell? |
| biology_12 | ru | prompt | У кого есть твёрдый панцирь? | Жизнь. У кого есть твёрдый панцирь? |
| biology_13 | de | prompt | Welches Tier lockert Erde beim Graben? | Entwickeln. Welches Tier lockert Erde beim Graben? |
| biology_13 | en | prompt | Which animal loosens soil as it burrows? | Life. Which animal loosens soil as it burrows? |
| biology_13 | ru | prompt | Кто рыхлит землю, прокладывая ходы? | Жизнь. Кто рыхлит землю, прокладывая ходы? |
| biology_14 | de | prompt | Woraus kann ein neuer Apfelbaum wachsen? | Entwickeln. Woraus kann ein neuer Apfelbaum wachsen? |
| biology_14 | en | prompt | What can grow into a new apple tree? | Life. What can grow into a new apple tree? |
| biology_14 | ru | prompt | Из чего может вырасти новая яблоня? | Жизнь. Из чего может вырасти новая яблоня? |
| biology_15 | de | prompt | Wer kann Blüten bestäuben? | Wachsen. Wer kann Blüten bestäuben? |
| biology_15 | en | prompt | Which animal can pollinate flowers? | Growing. Which animal can pollinate flowers? |
| biology_15 | ru | prompt | Кто может опылять цветки? | Рост. Кто может опылять цветки? |
| biology_16 | de | prompt | Welche grünen Pflanzenteile bilden hier die Baumkrone? | Wachsen. Welche grünen Pflanzenteile bilden hier die Baumkrone? |
| biology_16 | en | prompt | Which green plant parts form the tree crown here? | Growing. Which green plant parts form the tree crown here? |
| biology_16 | ru | prompt | Какие зелёные части растения образуют здесь крону дерева? | Рост. Какие зелёные части растения образуют здесь крону дерева? |
| biology_17 | de | prompt | Was ist ein Pilz und keine Pflanze? | Wachsen. Was ist ein Pilz und keine Pflanze? |
| biology_17 | en | prompt | Which is a fungus rather than a plant? | Growing. Which is a fungus rather than a plant? |
| biology_17 | ru | prompt | Что относится к грибам, а не к растениям? | Рост. Что относится к грибам, а не к растениям? |
| biology_18 | de | prompt | Was braucht eine Katze täglich zum Trinken? | Trinken. Was braucht eine Katze täglich zum Trinken? |
| biology_18 | en | prompt | What does a cat need to drink every day? | Drink. What does a cat need to drink every day? |
| biology_18 | ru | prompt | Что кошке нужно пить каждый день? | Пить. Что кошке нужно пить каждый день? |
| biology_19 | de | prompt | Was frisst eine Amsel zum Beispiel? | Entwickeln. Was frisst eine Amsel zum Beispiel? |
| biology_19 | en | prompt | What might a blackbird eat? | Life. What might a blackbird eat? |
| biology_19 | ru | prompt | Что, например, ест дрозд? | Жизнь. Что, например, ест дрозд? |
| biology_20 | de | prompt | Wo kann ein Schmetterling Nektar trinken? | Wachsen. Wo kann ein Schmetterling Nektar trinken? |
| biology_20 | en | prompt | Where can a butterfly drink nectar? | Growing. Where can a butterfly drink nectar? |
| biology_20 | ru | prompt | Где бабочка может пить нектар? | Рост. Где бабочка может пить нектар? |
| biology_21 | de | prompt | Welches dieser Tiere lebt im Wasser? | Entwickeln. Welches dieser Tiere lebt im Wasser? |
| biology_21 | en | prompt | Which of these animals lives in water? | Life. Which of these animals lives in water? |
| biology_21 | ru | prompt | Кто из этих животных живёт в воде? | Жизнь. Кто из этих животных живёт в воде? |
| biology_22 | de | prompt | Wo legt ein Grasfrosch seine Eier ab? | Entwickeln. Wo legt ein Grasfrosch seine Eier ab? |
| biology_22 | en | prompt | Where does a common frog lay its eggs? | Life. Where does a common frog lay its eggs? |
| biology_22 | ru | prompt | Где травяная лягушка откладывает икру? | Жизнь. Где травяная лягушка откладывает икру? |
| biology_23 | de | prompt | Was wächst bei einem keimenden Samen zuerst in den Boden? | Wachsen. Was wächst bei einem keimenden Samen zuerst in den Boden? |
| biology_23 | en | prompt | What grows into the soil first when a seed sprouts? | Growing. What grows into the soil first when a seed sprouts? |
| biology_23 | ru | prompt | Что первым растёт в землю при прорастании семени? | Рост. Что первым растёт в землю при прорастании семени? |
| biology_24 | de | prompt | Was nehmen Wurzeln auf? | Wachsen. Was nehmen Wurzeln auf? |
| biology_24 | en | prompt | What do roots absorb? | Growing. What do roots absorb? |
| biology_24 | ru | prompt | Что впитывают корни? | Рост. Что впитывают корни? |
| biology_25 | de | prompt | Wo stehen viele Bäume dicht beieinander? | Entwickeln. Wo stehen viele Bäume dicht beieinander? |
| biology_26 | de | prompt | Welche Teile der Baumkrone werden im Herbst oft gelb oder rot? | Wachsen. Welche Teile der Baumkrone werden im Herbst oft gelb oder rot? |
| biology_26 | en | prompt | Which parts of the tree crown often turn yellow or red in autumn? | Growing. Which parts of the tree crown often turn yellow or red in autumn? |
| biology_26 | ru | prompt | Какие части кроны дерева осенью часто становятся жёлтыми или красными? | Рост. Какие части кроны дерева осенью часто становятся жёлтыми или красными? |
| biology_27 | de | prompt | Wer hat einen Schnabel? | Entwickeln. Wer hat einen Schnabel? |
| biology_27 | en | prompt | Which animal has a beak? | Life. Which animal has a beak? |
| biology_27 | ru | prompt | У кого есть клюв? | Жизнь. У кого есть клюв? |
| biology_28 | de | prompt | Welches dieser Tiere ist ein Insekt? | Entwickeln. Welches dieser Tiere ist ein Insekt? |
| biology_28 | en | prompt | Which of these animals is an insect? | Life. Which of these animals is an insect? |
| biology_28 | ru | prompt | Кто из этих животных насекомое? | Жизнь. Кто из этих животных насекомое? |
| biology_29 | de | prompt | Woraus schlüpfen junge Schildkröten? | Entwickeln. Woraus schlüpfen junge Schildkröten? |
| biology_29 | en | prompt | What do young turtles hatch from? | Life. What do young turtles hatch from? |
| biology_29 | ru | prompt | Из чего вылупляются черепашки? | Жизнь. Из чего вылупляются черепашки? |
| biology_30 | de | prompt | Was kann nach der Blüte entstehen und neue Pflanzen hervorbringen? | Wachsen. Was kann nach der Blüte entstehen und neue Pflanzen hervorbringen? |
| biology_30 | en | prompt | What can form after flowering and grow into new plants? | Growing. What can form after flowering and grow into new plants? |
| biology_30 | ru | prompt | Что может появиться после цветения и дать новые растения? | Рост. Что может появиться после цветения и дать новые растения? |
| biology_31 | de | prompt | Womit hört eine Katze? | Hören. Womit hört eine Katze? |
| biology_31 | en | prompt | What does a cat use to hear? | Hearing. What does a cat use to hear? |
| biology_31 | ru | prompt | Чем кошка слышит? | Слух. Чем кошка слышит? |
| biology_32 | de | prompt | Wer ist ein Lebewesen: Maus, Papier oder Glas? | Entwickeln. Wer ist ein Lebewesen: Maus, Papier oder Glas? |
| biology_32 | en | prompt | Which is a living thing: a mouse, paper or glass? | Life. Which is a living thing: a mouse, paper or glass? |
| biology_32 | ru | prompt | Кто живой: мышь, бумага или стекло? | Жизнь. Кто живой: мышь, бумага или стекло? |
| biology_33 | de | prompt | Was lässt du beim Beobachten von Vogeleiern in Ruhe? | Entwickeln. Was lässt du beim Beobachten von Vogeleiern in Ruhe? |
| biology_33 | en | prompt | What should you leave undisturbed when watching bird eggs? | Life. What should you leave undisturbed when watching bird eggs? |
| biology_33 | ru | prompt | Что нельзя тревожить, наблюдая за птичьими яйцами? | Жизнь. Что нельзя тревожить, наблюдая за птичьими яйцами? |
| biology_34 | de | prompt | Welcher Pflanzenteil verankert eine Blume im Boden? | Wachsen. Welcher Pflanzenteil verankert eine Blume im Boden? |
| biology_34 | en | prompt | Which plant part holds a flower in the ground? | Growing. Which plant part holds a flower in the ground? |
| biology_34 | ru | prompt | Какая часть растения удерживает цветок в земле? | Рост. Какая часть растения удерживает цветок в земле? |
| biology_35 | de | prompt | Eine Topfpflanze hat trockene Erde. Was kann ihr fehlen? | Trinken. Eine Topfpflanze hat trockene Erde. Was kann ihr fehlen? |
| biology_35 | en | prompt | A plant's soil is dry. What might it need? | Drink. A plant's soil is dry. What might it need? |
| biology_35 | ru | prompt | Земля в горшке сухая. Чего может не хватать растению? | Пить. Земля в горшке сухая. Чего может не хватать растению? |
| biology_36 | de | prompt | Was hilft Bienen im Garten? | Wachsen. Was hilft Bienen im Garten? |
| biology_36 | en | prompt | What helps bees in a garden? | Growing. What helps bees in a garden? |
| biology_36 | ru | prompt | Что помогает пчёлам в саду? | Рост. Что помогает пчёлам в саду? |
| biology_37 | de | prompt | Was können Regenwürmer in die Erde ziehen? | Entwickeln. Was können Regenwürmer in die Erde ziehen? |
| biology_37 | en | prompt | What can earthworms pull into the soil? | Life. What can earthworms pull into the soil? |
| biology_37 | ru | prompt | Что дождевые черви могут затаскивать в землю? | Жизнь. Что дождевые черви могут затаскивать в землю? |
| biology_38 | de | prompt | Worin schwimmen Fische eines Teichs? | Entwickeln. Worin schwimmen Fische eines Teichs? |
| biology_38 | en | prompt | What do pond fish swim in? | Life. What do pond fish swim in? |
| biology_38 | ru | prompt | В чём плавают прудовые рыбы? | Жизнь. В чём плавают прудовые рыбы? |
| biology_39 | de | prompt | Was kann aus einer Eichel wachsen? | Wachsen. Was kann aus einer Eichel wachsen? |
| biology_39 | en | prompt | What can grow from an acorn? | Growing. What can grow from an acorn? |
| biology_39 | ru | prompt | Что может вырасти из жёлудя? | Рост. Что может вырасти из жёлудя? |
| biology_40 | de | prompt | Wer hat als erwachsenes Tier vier Flügel? | Entwickeln. Wer hat als erwachsenes Tier vier Flügel? |
| biology_40 | en | prompt | Which adult animal has four wings? | Life. Which adult animal has four wings? |
| biology_40 | ru | prompt | У кого во взрослом состоянии четыре крыла? | Жизнь. У кого во взрослом состоянии четыре крыла? |
| chemistry_01 | de | prompt | Was wird aus Eis, wenn es schmilzt? | Verändern. Was wird aus Eis, wenn es schmilzt? |
| chemistry_01 | en | prompt | What does ice become when it melts? | Change. What does ice become when it melts? |
| chemistry_01 | ru | prompt | Во что превращается лёд, когда тает? | Изменение. Во что превращается лёд, когда тает? |
| chemistry_02 | de | prompt | Was kann aus Wasser im Gefrierfach werden? | Verändern. Was kann aus Wasser im Gefrierfach werden? |
| chemistry_02 | en | prompt | What can water become in a freezer? | Change. What can water become in a freezer? |
| chemistry_02 | ru | prompt | Во что вода может превратиться в морозильнике? | Изменение. Во что вода может превратиться в морозильнике? |
| chemistry_03 | de | prompt | Was ist bei Zimmertemperatur flüssig? | Entdecken. Was ist bei Zimmertemperatur flüssig? |
| chemistry_03 | en | prompt | Which is liquid at room temperature? | Explore. Which is liquid at room temperature? |
| chemistry_03 | ru | prompt | Что жидкое при комнатной температуре? | Открытие. Что жидкое при комнатной температуре? |
| chemistry_04 | de | prompt | Was ist bei Zimmertemperatur fest? | Untersuchen. Was ist bei Zimmertemperatur fest? |
| chemistry_04 | en | prompt | Which is solid at room temperature? | Materials. Which is solid at room temperature? |
| chemistry_04 | ru | prompt | Что твёрдое при комнатной температуре? | Вещества. Что твёрдое при комнатной температуре? |
| chemistry_05 | de | prompt | Welches Gefäß hält Trinkwasser zuverlässig? | Verwandeln. Welches Gefäß hält Trinkwasser zuverlässig? |
| chemistry_05 | en | prompt | Which container reliably holds drinking water? | Changing. Which container reliably holds drinking water? |
| chemistry_05 | ru | prompt | Какая ёмкость надёжно удерживает питьевую воду? | Превращение. Какая ёмкость надёжно удерживает питьевую воду? |
| chemistry_06 | de | prompt | Was löst sich in Wasser: Salz, Sand oder Holz? | Verwandeln. Was löst sich in Wasser: Salz, Sand oder Holz? |
| chemistry_06 | en | prompt | What dissolves in water: salt, sand or wood? | Changing. What dissolves in water: salt, sand or wood? |
| chemistry_06 | ru | prompt | Что растворяется в воде: соль, песок или дерево? | Превращение. Что растворяется в воде: соль, песок или дерево? |
| chemistry_07 | de | prompt | Was bleibt als Körnchen sichtbar, wenn es in Wasser liegt? | Verwandeln. Was bleibt als Körnchen sichtbar, wenn es in Wasser liegt? |
| chemistry_07 | en | prompt | What stays visible as grains in water? | Changing. What stays visible as grains in water? |
| chemistry_07 | ru | prompt | Что остаётся видимыми крупинками в воде? | Превращение. Что остаётся видимыми крупинками в воде? |
| chemistry_08 | de | prompt | Was bildet mit Wasser oft zwei Schichten? | Verwandeln. Was bildet mit Wasser oft zwei Schichten? |
| chemistry_08 | en | prompt | What often forms two layers with water? | Changing. What often forms two layers with water? |
| chemistry_08 | ru | prompt | Что часто образует с водой два слоя? | Превращение. Что часто образует с водой два слоя? |
| chemistry_09 | de | prompt | Welcher Gegenstand zieht Eisen aus einer Mischung an? | Verändern. Welcher Gegenstand zieht Eisen aus einer Mischung an? |
| chemistry_09 | en | prompt | Which object attracts iron out of a mixture? | Change. Which object attracts iron out of a mixture? |
| chemistry_09 | ru | prompt | Какой предмет притягивает железо из смеси? | Изменение. Какой предмет притягивает железо из смеси? |
| chemistry_10 | de | prompt | Was entsteht unsichtbar, wenn Wasser verdunstet? | Verwandeln. Was entsteht unsichtbar, wenn Wasser verdunstet? |
| chemistry_10 | en | prompt | What forms invisibly when water evaporates? | Changing. What forms invisibly when water evaporates? |
| chemistry_10 | ru | prompt | Что образуется незаметно, когда вода испаряется? | Превращение. Что образуется незаметно, когда вода испаряется? |
| chemistry_11 | de | prompt | Was bilden kleine Tropfen an einem kalten Fenster? | Verändern. Was bilden kleine Tropfen an einem kalten Fenster? |
| chemistry_11 | en | prompt | What are the little drops on a cold window made of? | Change. What are the little drops on a cold window made of? |
| chemistry_11 | ru | prompt | Из чего состоят капельки на холодном окне? | Изменение. Из чего состоят капельки на холодном окне? |
| chemistry_12 | de | prompt | Welcher Zustand von Wasser ist fest? | Verwandeln. Welcher Zustand von Wasser ist fest? |
| chemistry_12 | en | prompt | Which form of water is solid? | Changing. Which form of water is solid? |
| chemistry_12 | ru | prompt | Какое состояние воды твёрдое? | Превращение. Какое состояние воды твёрдое? |
| chemistry_13 | de | prompt | Welches Zeichen steht für gasförmiges Wasser? | Verwandeln. Welches Zeichen steht für gasförmiges Wasser? |
| chemistry_13 | en | prompt | Which symbol stands for water as a gas? | Changing. Which symbol stands for water as a gas? |
| chemistry_13 | ru | prompt | Какой значок обозначает воду в газообразном состоянии? | Превращение. Какой значок обозначает воду в газообразном состоянии? |
| chemistry_14 | de | prompt | Worin löst sich etwas Kochsalz gut? | Untersuchen. Worin löst sich etwas Kochsalz gut? |
| chemistry_14 | en | prompt | What dissolves a little table salt well? | Materials. What dissolves a little table salt well? |
| chemistry_14 | ru | prompt | В чём хорошо растворяется немного поваренной соли? | Вещества. В чём хорошо растворяется немного поваренной соли? |
| chemistry_15 | de | prompt | Welches Material ist durchsichtig? | Leuchten. Welches Material ist durchsichtig? |
| chemistry_15 | en | prompt | Which material is transparent? | Light. Which material is transparent? |
| chemistry_15 | ru | prompt | Какой материал прозрачный? | Свет. Какой материал прозрачный? |
| chemistry_16 | de | prompt | Welches Material saugt Wasser leicht auf? | Verwandeln. Welches Material saugt Wasser leicht auf? |
| chemistry_16 | en | prompt | Which material easily soaks up water? | Changing. Which material easily soaks up water? |
| chemistry_16 | ru | prompt | Какой материал легко впитывает воду? | Превращение. Какой материал легко впитывает воду? |
| chemistry_17 | de | prompt | Was lässt sich weich zusammenfalten? | Fühlen. Was lässt sich weich zusammenfalten? |
| chemistry_17 | en | prompt | What can be softly folded up? | Touch. What can be softly folded up? |
| chemistry_17 | ru | prompt | Что можно мягко сложить? | Осязание. Что можно мягко сложить? |
| chemistry_18 | de | prompt | Was kann Wärme gut weiterleiten? | Erwärmen. Was kann Wärme gut weiterleiten? |
| chemistry_18 | en | prompt | Which material can conduct heat well? | Warming. Which material can conduct heat well? |
| chemistry_18 | ru | prompt | Какой материал хорошо проводит тепло? | Нагрев. Какой материал хорошо проводит тепло? |
| chemistry_19 | de | prompt | Welches Material zeigt oft Jahresringe? | Untersuchen. Welches Material zeigt oft Jahresringe? |
| chemistry_19 | en | prompt | Which material often shows growth rings? | Materials. Which material often shows growth rings? |
| chemistry_19 | ru | prompt | На каком материале часто видны годичные кольца? | Вещества. На каком материале часто видны годичные кольца? |
| chemistry_20 | de | prompt | Was hilft, Fett mit Wasser zu vermischen und abzuwaschen? | Reinigen. Was hilft, Fett mit Wasser zu vermischen und abzuwaschen? |
| chemistry_20 | en | prompt | What helps grease mix with water so it can be washed away? | Cleaning. What helps grease mix with water so it can be washed away? |
| chemistry_20 | ru | prompt | Что помогает смешать жир с водой и смыть его? | Чистота. Что помогает смешать жир с водой и смыть его? |
| chemistry_21 | de | prompt | Welcher Stoff wird oft zum Kochen verwendet und bleibt flüssig? | Entdecken. Welcher Stoff wird oft zum Kochen verwendet und bleibt flüssig? |
| chemistry_21 | en | prompt | Which substance is often used in cooking and stays liquid? | Explore. Which substance is often used in cooking and stays liquid? |
| chemistry_21 | ru | prompt | Какое вещество часто используют при готовке и оно остаётся жидким? | Открытие. Какое вещество часто используют при готовке и оно остаётся жидким? |
| chemistry_22 | de | prompt | Was besteht hier aus vielen kleinen Körnern? | Untersuchen. Was besteht hier aus vielen kleinen Körnern? |
| chemistry_22 | en | prompt | Which of these consists of many little grains? | Materials. Which of these consists of many little grains? |
| chemistry_22 | ru | prompt | Что здесь состоит из множества маленьких крупинок? | Вещества. Что здесь состоит из множества маленьких крупинок? |
| chemistry_23 | de | prompt | Was liefert Wärme, die draußen Eis schmelzen lässt? | Verändern. Was liefert Wärme, die draußen Eis schmelzen lässt? |
| chemistry_23 | en | prompt | What provides warmth that can melt ice outdoors? | Change. What provides warmth that can melt ice outdoors? |
| chemistry_23 | ru | prompt | Что даёт тепло и может растопить лёд на улице? | Изменение. Что даёт тепло и может растопить лёд на улице? |
| chemistry_24 | de | prompt | Wo sammeln sich viele winzige Wassertropfen am Himmel? | Beobachten. Wo sammeln sich viele winzige Wassertropfen am Himmel? |
| chemistry_24 | en | prompt | Where do many tiny water drops gather in the sky? | Observe. Where do many tiny water drops gather in the sky? |
| chemistry_24 | ru | prompt | Где в небе собирается много крошечных капель воды? | Наблюдение. Где в небе собирается много крошечных капель воды? |
| chemistry_25 | de | prompt | Woraus bestehen Regentropfen hauptsächlich? | Beobachten. Woraus bestehen Regentropfen hauptsächlich? |
| chemistry_25 | en | prompt | What are raindrops mainly made of? | Observe. What are raindrops mainly made of? |
| chemistry_25 | ru | prompt | Из чего в основном состоят капли дождя? | Наблюдение. Из чего в основном состоят капли дождя? |
| chemistry_26 | de | prompt | Woraus bestehen Schneeflocken? | Beobachten. Woraus bestehen Schneeflocken? |
| chemistry_26 | en | prompt | What are snowflakes made of? | Observe. What are snowflakes made of? |
| chemistry_26 | ru | prompt | Из чего состоят снежинки? | Наблюдение. Из чего состоят снежинки? |
| chemistry_27 | de | prompt | Was passt sich der Form eines Glases an? | Untersuchen. Was passt sich der Form eines Glases an? |
| chemistry_27 | en | prompt | What takes the shape of a glass? | Materials. What takes the shape of a glass? |
| chemistry_27 | ru | prompt | Что принимает форму стакана? | Вещества. Что принимает форму стакана? |
| chemistry_28 | de | prompt | Was behält auf dem Teller zunächst seine eigene Form? | Verändern. Was behält auf dem Teller zunächst seine eigene Form? |
| chemistry_28 | en | prompt | What keeps its own shape on a plate before warming up? | Change. What keeps its own shape on a plate before warming up? |
| chemistry_28 | ru | prompt | Что сначала сохраняет свою форму на тарелке, пока не нагрелось? | Изменение. Что сначала сохраняет свою форму на тарелке, пока не нагрелось? |
| chemistry_29 | de | prompt | Welches Material kann splittern, wenn es herunterfällt? | Untersuchen. Welches Material kann splittern, wenn es herunterfällt? |
| chemistry_29 | en | prompt | Which material can shatter if dropped? | Materials. Which material can shatter if dropped? |
| chemistry_29 | ru | prompt | Какой материал может разбиться на осколки при падении? | Вещества. Какой материал может разбиться на осколки при падении? |
| chemistry_30 | de | prompt | Welches Mittel ist zum Händewaschen mit Wasser gedacht? | Reinigen. Welches Mittel ist zum Händewaschen mit Wasser gedacht? |
| chemistry_30 | en | prompt | Which product is intended for washing hands with water? | Cleaning. Which product is intended for washing hands with water? |
| chemistry_30 | ru | prompt | Какое средство предназначено для мытья рук с водой? | Чистота. Какое средство предназначено для мытья рук с водой? |
| chemistry_31 | de | prompt | Was bleibt zurück, wenn Salzwasser ganz verdunstet? | Verwandeln. Was bleibt zurück, wenn Salzwasser ganz verdunstet? |
| chemistry_31 | en | prompt | What is left when salt water completely evaporates? | Changing. What is left when salt water completely evaporates? |
| chemistry_31 | ru | prompt | Что остаётся, когда солёная вода полностью испаряется? | Превращение. Что остаётся, когда солёная вода полностью испаряется? |
| chemistry_32 | de | prompt | Welcher Gegenstand zieht Eisenstücke aus Sand an? | Verändern. Welcher Gegenstand zieht Eisenstücke aus Sand an? |
| chemistry_32 | en | prompt | Which object attracts iron pieces out of sand? | Change. Which object attracts iron pieces out of sand? |
| chemistry_32 | ru | prompt | Какой предмет притягивает кусочки железа из песка? | Изменение. Какой предмет притягивает кусочки железа из песка? |
| chemistry_33 | de | prompt | Welcher Stoff fließt aus einer umgekippten offenen Flasche? | Untersuchen. Welcher Stoff fließt aus einer umgekippten offenen Flasche? |
| chemistry_33 | en | prompt | Which substance flows from a tipped open bottle? | Materials. Which substance flows from a tipped open bottle? |
| chemistry_33 | ru | prompt | Какое вещество вытекает из наклонённой открытой бутылки? | Вещества. Какое вещество вытекает из наклонённой открытой бутылки? |
| chemistry_34 | de | prompt | Was wird häufig aus Pflanzenfasern gemacht? | Wachsen. Was wird häufig aus Pflanzenfasern gemacht? |
| chemistry_34 | en | prompt | What is often made from plant fibres? | Growing. What is often made from plant fibres? |
| chemistry_34 | ru | prompt | Что часто делают из растительных волокон? | Рост. Что часто делают из растительных волокон? |
| chemistry_35 | de | prompt | Was ist dieselbe Substanz wie Wasser, nur fest? | Verwandeln. Was ist dieselbe Substanz wie Wasser, nur fest? |
| chemistry_35 | en | prompt | What is the same substance as water, but solid? | Changing. What is the same substance as water, but solid? |
| chemistry_35 | ru | prompt | Что является тем же веществом, что вода, только твёрдым? | Превращение. Что является тем же веществом, что вода, только твёрдым? |
| chemistry_36 | de | prompt | Woraus wird gewöhnliches Glas hauptsächlich hergestellt? | Untersuchen. Woraus wird gewöhnliches Glas hauptsächlich hergestellt? |
| chemistry_36 | en | prompt | What is ordinary glass mainly made from? | Materials. What is ordinary glass mainly made from? |
| chemistry_36 | ru | prompt | Из чего в основном делают обычное стекло? | Вещества. Из чего в основном делают обычное стекло? |
| chemistry_37 | de | prompt | Welches Material besteht aus gewebten Fäden? | Fühlen. Welches Material besteht aus gewebten Fäden? |
| chemistry_37 | en | prompt | Which material can be made from woven threads? | Touch. Which material can be made from woven threads? |
| chemistry_37 | ru | prompt | Какой материал можно сделать из переплетённых нитей? | Осязание. Какой материал можно сделать из переплетённых нитей? |
| chemistry_38 | de | prompt | Womit spülst du Seife von den Händen ab? | Reinigen. Womit spülst du Seife von den Händen ab? |
| chemistry_38 | en | prompt | What rinses soap off your hands? | Cleaning. What rinses soap off your hands? |
| chemistry_38 | ru | prompt | Чем смывают мыло с рук? | Чистота. Чем смывают мыло с рук? |
| chemistry_39 | de | prompt | Was bleibt in Wasser bei Zimmertemperatur fest: Glas, Eis oder Salz? | Verändern. Was bleibt in Wasser bei Zimmertemperatur fest: Glas, Eis oder Salz? |
| chemistry_39 | en | prompt | What stays solid in water at room temperature: glass, ice or salt? | Change. What stays solid in water at room temperature: glass, ice or salt? |
| chemistry_39 | ru | prompt | Что остаётся твёрдым в воде при комнатной температуре: стекло, лёд или соль? | Изменение. Что остаётся твёрдым в воде при комнатной температуре: стекло, лёд или соль? |
| chemistry_40 | de | prompt | Was entsteht aus dem Eiswürfel, wenn er im Glas schmilzt? | Verändern. Was entsteht aus dem Eiswürfel, wenn er im Glas schmilzt? |
| chemistry_40 | en | prompt | What does an ice cube become when it melts in a glass? | Change. What does an ice cube become when it melts in a glass? |
| chemistry_40 | ru | prompt | Во что превращается кубик льда, когда тает в стакане? | Изменение. Во что превращается кубик льда, когда тает в стакане? |
| body_01 | de | prompt | Womit nimmst du Licht und Farben wahr? | Sehen. Womit sehen Menschen? |
| body_01 | en | prompt | Which body part detects light and colours? | Seeing. What do people use to see? |
| body_01 | ru | prompt | Чем воспринимают свет и цвета? | Зрение. Чем видит человек? |
| body_02 | de | prompt | Welcher Körperteil nimmt Schall auf? | Hören. Womit hört der Mensch? |
| body_02 | en | prompt | Which body part detects sounds? | Hearing. What do people use to hear? |
| body_02 | ru | prompt | Какая часть тела воспринимает звуки? | Слух. Чем слышит человек? |
| body_03 | de | prompt | Womit riechen Menschen? | Riechen. Womit riechen Menschen? |
| body_03 | en | prompt | What do people use to smell? | Smell. What do people use to smell? |
| body_03 | ru | prompt | Чем люди ощущают запахи? | Запах. Чем человек чувствует запах? |
| body_04 | de | prompt | Womit kannst du süß und sauer schmecken? | Schmecken. Womit schmeckst du süß und sauer? |
| body_04 | en | prompt | What helps you taste sweet and sour? | Taste. What detects sweet and sour tastes? |
| body_04 | ru | prompt | Что помогает различать сладкий и кислый вкус? | Вкус. Чем чувствуешь сладкий и кислый вкус? |
| body_05 | de | prompt | Womit kannst du fühlen, ob ein Tuch weich ist? | Fühlen. Womit ertastest du ein weiches Tuch? |
| body_05 | en | prompt | What can feel whether a cloth is soft? | Touch. What do you use to feel a soft cloth? |
| body_05 | ru | prompt | Чем можно почувствовать, мягкая ли ткань? | Осязание. Чем ощупываешь мягкую ткань? |
| body_06 | de | prompt | Welches Organ pumpt Blut durch den Körper? | Antreiben. Welches Organ pumpt Blut? |
| body_06 | en | prompt | Which organ pumps blood around the body? | Pumping. Which organ pumps blood? |
| body_06 | ru | prompt | Какой орган перекачивает кровь по телу? | Движение. Какой орган качает кровь? |
| body_07 | de | prompt | Welche Organe nehmen beim Atmen Luft auf? | Atmen. Welche Organe nehmen Atemluft auf? |
| body_07 | en | prompt | Which organs take in air when you breathe? | Breathing. Which organs take in air? |
| body_07 | ru | prompt | Какие органы принимают воздух при дыхании? | Дыхание. Какие органы принимают воздух при вдохе? |
| body_08 | de | prompt | Welches Organ verarbeitet Sinneseindrücke? | Denken. Welches Organ verarbeitet Sinneseindrücke? |
| body_08 | en | prompt | Which organ processes information from your senses? | Thinking. Which organ processes what we sense? |
| body_08 | ru | prompt | Какой орган обрабатывает сигналы органов чувств? | Мысли. Какой орган обрабатывает ощущения? |
| body_09 | de | prompt | Was bildet das feste Gerüst im Körper? | Stützen. Was bildet das feste Körpergerüst? |
| body_09 | en | prompt | What forms the body's hard framework? | Support. What forms the body's hard frame? |
| body_09 | ru | prompt | Что образует твёрдую опору тела? | Опора. Что образует твёрдую опору тела? |
| body_10 | de | prompt | Womit zerkleinerst du Essen im Mund? | Zerkleinern. Womit zerkleinerst du Essen? |
| body_10 | en | prompt | What breaks food into smaller pieces in your mouth? | Biting. What breaks food into small pieces? |
| body_10 | ru | prompt | Чем измельчают пищу во рту? | Измельчение. Чем измельчаешь пищу? |
| body_11 | de | prompt | Wohin gelangt Essen nach der Speiseröhre? | Verdauen. Wohin kommt Essen nach der Speiseröhre? |
| body_11 | en | prompt | Where does food go after the food pipe? | Digestion. Where does food go after the food pipe? |
| body_11 | ru | prompt | Куда попадает пища после пищевода? | Пищеварение. Куда еда попадает после пищевода? |
| body_12 | de | prompt | Was hilft, die Hände sauber zu waschen? | Reinigen. Was hilft beim Händewaschen? |
| body_12 | en | prompt | What helps wash your hands clean? | Cleaning. What helps wash your hands? |
| body_12 | ru | prompt | Что помогает хорошо вымыть руки? | Чистота. Что помогает мыть руки? |
| body_13 | de | prompt | Was eignet sich als Durstlöscher? | Trinken. Was eignet sich als Durstlöscher? |
| body_13 | en | prompt | What is a good drink when you are thirsty? | Drink. What is a good drink when thirsty? |
| body_13 | ru | prompt | Что хорошо утоляет жажду? | Пить. Чем лучше утолить жажду? |
| body_14 | de | prompt | Welches Bild steht hier für die Nacht und die Schlafenszeit? | Ruhen. Welches Bild steht für die Nacht? |
| body_14 | en | prompt | Which picture here stands for nighttime and bedtime? | Rest. Which picture stands for night? |
| body_14 | ru | prompt | Какая картинка здесь обозначает ночь и время сна? | Отдых. Какая картинка означает ночь? |
| body_15 | de | prompt | Welcher Körperteil trägt oft einen Schuh? | Tragen. Welcher Körperteil steckt im Schuh? |
| body_15 | en | prompt | Which body part often wears a shoe? | Support. Which body part goes in a shoe? |
| body_15 | ru | prompt | На какую часть тела обычно надевают обувь? | Опора. Какую часть тела обувают? |
| body_16 | de | prompt | Was schützt den Kopf beim Fahrradfahren? | Schützen. Was schützt beim Radfahren den Kopf? |
| body_16 | en | prompt | What protects your head when cycling? | Protection. What protects your head when cycling? |
| body_16 | ru | prompt | Что защищает голову на велосипеде? | Защита. Что защищает голову на велосипеде? |
| body_17 | de | prompt | Welcher Sinn braucht Schutz vor sehr lauten Tönen? | Hören. Welcher Körperteil braucht Schutz vor Lärm? |
| body_18 | de | prompt | Welchen Körperteil schützen Augenlider? | Sehen. Was schützen die Augenlider? |
| body_18 | en | prompt | Which body part do eyelids protect? | Seeing. What do eyelids protect? |
| body_18 | ru | prompt | Что защищают веки? | Зрение. Что защищают веки? |
| body_19 | de | prompt | Welcher Körperteil hilft, eingeatmete Luft zu filtern? | Entdecken. Was hilft, Atemluft zu filtern? |
| body_19 | en | prompt | Which body part helps filter the air you breathe in? | Explore. What helps filter the air you breathe? |
| body_19 | ru | prompt | Что помогает очищать вдыхаемый воздух? | Открытие. Что помогает очищать вдыхаемый воздух? |
| body_20 | de | prompt | Was fällt bei vielen Kindern aus und wächst neu nach? | Zerkleinern. Was fällt aus und wächst bei Kindern neu? |
| body_20 | en | prompt | What do many children lose and replace as they grow? | Biting. What falls out and regrows in children? |
| body_20 | ru | prompt | Что у многих детей выпадает и заменяется новым? | Измельчение. Что выпадает и вырастает заново у детей? |
| body_21 | de | prompt | Welcher Körperteil hat normalerweise fünf Finger? | Greifen. Welcher Körperteil hat normalerweise fünf Finger? |
| body_21 | en | prompt | Which body part usually has five fingers? | Grasp. Which body part usually has five fingers? |
| body_21 | ru | prompt | У какой части тела обычно пять пальцев? | Брать. У какой части тела обычно пять пальцев? |
| body_22 | de | prompt | Was schlägt meist schneller, wenn du dich anstrengst? | Antreiben. Was schlägt beim Rennen meist schneller? |
| body_22 | en | prompt | What usually beats faster when you exercise? | Pumping. What usually beats faster when running? |
| body_22 | ru | prompt | Что обычно бьётся быстрее при физической нагрузке? | Движение. Что при беге обычно бьётся быстрее? |
| body_23 | de | prompt | Wohin strömt Luft beim Einatmen? | Atmen. Wohin strömt Luft beim Einatmen? |
| body_23 | en | prompt | Where does air go when you breathe in? | Breathing. Where does air go when breathing in? |
| body_23 | ru | prompt | Куда поступает воздух при вдохе? | Дыхание. Куда поступает воздух при вдохе? |
| body_24 | de | prompt | Wo werden viele Erinnerungen verarbeitet? | Denken. Welches Organ verarbeitet Erinnerungen? |
| body_24 | en | prompt | Where are many memories processed? | Thinking. Which organ processes memories? |
| body_25 | de | prompt | Was schützt das Gehirn als Schädel? | Stützen. Was bildet den schützenden Schädel? |
| body_25 | en | prompt | What protects the brain as the skull? | Support. What makes the protective skull? |
| body_25 | ru | prompt | Что образует череп и защищает мозг? | Опора. Из чего состоит защитный череп? |
| body_26 | de | prompt | Welches Organ mischt und verdaut Nahrung weiter? | Verdauen. Welches Organ mischt Nahrung weiter? |
| body_26 | en | prompt | Which organ mixes food and continues digestion? | Digestion. Which organ keeps mixing food? |
| body_26 | ru | prompt | Какой орган перемешивает пищу и продолжает пищеварение? | Пищеварение. Какой орган продолжает перемешивать пищу? |
| body_27 | de | prompt | Welcher Körperteil nimmt beim Essen Duftstoffe wahr? | Riechen. Womit riechst du das Essen? |
| body_27 | en | prompt | Which part of the body senses smells while you eat? | Smell. What do you use to smell food? |
| body_27 | ru | prompt | Какая часть тела чувствует запахи во время еды? | Запах. Чем чувствуешь запах еды? |
| body_28 | de | prompt | Was nimmst du zum Händewaschen vor dem Essen? | Reinigen. Was brauchst du beim Händewaschen? |
| body_28 | en | prompt | What do you use to wash your hands before eating? | Cleaning. What do you need when washing hands? |
| body_28 | ru | prompt | Чем моют руки перед едой? | Чистота. Что нужно для мытья рук? |
| body_29 | de | prompt | Was davon ist ein Lebensmittel? | Entdecken. Was davon ist ein Lebensmittel? |
| body_29 | en | prompt | Which of these is food? | Explore. Which of these is food? |
| body_29 | ru | prompt | Что из этого является едой? | Открытие. Что из этого еда? |
| body_30 | de | prompt | Was befindet sich im Fuß und gibt Halt? | Stützen. Was gibt dem Fuß innen Halt? |
| body_30 | en | prompt | What is inside a foot and gives it support? | Support. What supports the foot from inside? |
| body_30 | ru | prompt | Что находится внутри стопы и даёт ей опору? | Опора. Что поддерживает стопу изнутри? |
| body_31 | de | prompt | Welches Organ verarbeitet die Signale der Ohren, damit du Geräusche erkennst? | Denken. Welches Organ erkennt gehörte Geräusche? |
| body_31 | en | prompt | Which organ processes signals from your ears so you recognize sounds? | Thinking. Which organ recognises sounds you hear? |
| body_31 | ru | prompt | Какой орган обрабатывает сигналы от ушей, чтобы ты узнавал звуки? | Мысли. Какой орган узнаёт услышанные звуки? |
| body_32 | de | prompt | Wohin senden die Augen ihre Signale? | Denken. Welches Organ verarbeitet Signale der Augen? |
| body_32 | en | prompt | Where do eyes send their signals? | Think. Which organ processes signals from the eyes? |
| body_32 | ru | prompt | Куда глаза посылают сигналы? | Думать. Какой орган обрабатывает сигналы глаз? |
| body_33 | de | prompt | Welches Organ bringt Sauerstoff aus der Luft ins Blut? | Atmen. Welches Organ bringt Sauerstoff ins Blut? |
| body_33 | en | prompt | Which organ brings oxygen from air into the blood? | Breathe. Which organ transfers oxygen into blood? |
| body_33 | ru | prompt | Какой орган передаёт кислород из воздуха в кровь? | Дышать. Какой орган передаёт кислород в кровь? |
| body_34 | de | prompt | Welches Organ ist ein kräftiger Muskel in der Brust? | Antreiben. Welches Organ pumpt als Muskel in der Brust? |
| body_34 | en | prompt | Which organ is a strong muscle in the chest? | Pumping. Which muscular organ pumps inside your chest? |
| body_34 | ru | prompt | Какой орган — сильная мышца в груди? | Движение. Какой мышечный орган качает кровь в груди? |
| body_35 | de | prompt | Was fühlt sich meist weich und biegsam an? | Fühlen. Was ist meist weich und biegsam? |
| body_35 | en | prompt | What usually feels soft and bendy? | Touch. Which is usually soft and flexible? |
| body_35 | ru | prompt | Что обычно мягкое на ощупь и легко сгибается? | Осязание. Что обычно мягкое и гибкое? |
| body_36 | de | prompt | Welchen Körperteil reinigst du mit einer Zahnbürste? | Pflegen. Was reinigst du mit einer Zahnbürste? |
| body_36 | en | prompt | Which body part do you clean with a toothbrush? | Care. What do you clean with a toothbrush? |
| body_36 | ru | prompt | Что чистят зубной щёткой? | Уход. Что чистишь зубной щёткой? |
| body_37 | de | prompt | Wodurch kannst du beim ruhigen Atmen Luft einziehen? | Entdecken. Wodurch ziehst du ruhig Atemluft ein? |
| body_37 | en | prompt | What can you breathe through when resting? | Explore. Through what can you breathe in quietly? |
| body_37 | ru | prompt | Через что можно вдыхать воздух в покое? | Открытие. Через что спокойно вдыхаешь воздух? |
| body_38 | de | prompt | Womit hörst du die Musik in diesem Spiel? | Hören. Womit hörst du Musik? |
| body_38 | en | prompt | What helps you hear this game's music? | Hearing. What do you use to hear music? |
| body_38 | ru | prompt | Что помогает слышать музыку в этой игре? | Слух. Чем слышишь музыку? |
| body_39 | de | prompt | Was braucht der Körper zum Trinken? | Trinken. Was braucht der Körper zum Trinken? |
| body_39 | en | prompt | What does the body need to drink? | Drink. What does the body need to drink? |
| body_39 | ru | prompt | Что нужно организму для питья? | Пить. Что нужно организму для питья? |
| body_40 | de | prompt | Womit kannst du einen weichen Ball vorsichtig greifen? | Fühlen. Womit greifst du vorsichtig einen Ball? |
| body_40 | en | prompt | What can gently hold a soft ball? | Touch. What gently grasps a ball? |
| body_40 | ru | prompt | Чем можно осторожно взять мягкий мяч? | Осязание. Чем осторожно берёшь мяч? |
| geography_01 | de | prompt | Was zeigt die Erde als kleine Kugel? | Orientieren. Was zeigt die Erde als kleine Kugel? |
| geography_01 | en | prompt | What shows Earth as a small sphere? | Direction. What shows Earth as a small sphere? |
| geography_01 | ru | prompt | Что показывает Землю в виде маленького шара? | Ориентир. Что показывает Землю в виде маленького шара? |
| geography_02 | de | prompt | Welche Zeichnung auf einem flachen Blatt zeigt Orte und Wege von oben? | Orientieren. Welche Zeichnung auf einem flachen Blatt zeigt Orte und Wege von oben? |
| geography_02 | en | prompt | Which drawing on a flat sheet shows places and paths from above? | Direction. Which drawing on a flat sheet shows places and paths from above? |
| geography_02 | ru | prompt | Какой рисунок на плоском листе показывает места и дороги сверху? | Ориентир. Какой рисунок на плоском листе показывает места и дороги сверху? |
| geography_03 | de | prompt | Welches Gerät hat eine Nadel, die nach Norden zeigt? | Orientieren. Welches Gerät hat eine Nadel, die nach Norden zeigt? |
| geography_03 | en | prompt | Which instrument has a needle that points north? | Direction. Which instrument has a needle that points north? |
| geography_03 | ru | prompt | У какого прибора есть стрелка, показывающая на север? | Ориентир. У какого прибора есть стрелка, показывающая на север? |
| geography_04 | de | prompt | Was ragt hoch über seine Umgebung hinaus? | Entdecken. Was ragt hoch über seine Umgebung hinaus? |
| geography_04 | en | prompt | What rises high above the land around it? | Explore. What rises high above the land around it? |
| geography_04 | ru | prompt | Что высоко поднимается над окружающей местностью? | Открытие. Что высоко поднимается над окружающей местностью? |
| geography_05 | de | prompt | Was fließt in einem Bett durch die Landschaft? | Entdecken. Was fließt in einem Bett durch die Landschaft? |
| geography_05 | en | prompt | What flows in a channel through the landscape? | Explore. What flows in a channel through the landscape? |
| geography_05 | ru | prompt | Что течёт по руслу через местность? | Открытие. Что течёт по руслу через местность? |
| geography_06 | de | prompt | Was ist ganz von Wasser umgebenes Land? | Entdecken. Was ist ganz von Wasser umgebenes Land? |
| geography_06 | en | prompt | What is land surrounded by water on all sides? | Explore. What is land surrounded by water on all sides? |
| geography_06 | ru | prompt | Как называется суша, со всех сторон окружённая водой? | Исследовать. Как называется суша, со всех сторон окружённая водой? |
| geography_07 | de | prompt | Wo findest du sehr viel Salzwasser? | Entdecken. Wo findest du sehr viel Salzwasser? |
| geography_07 | en | prompt | Where can you find a very large amount of salt water? | Explore. Where can you find a very large amount of salt water? |
| geography_07 | ru | prompt | Где находится очень много солёной воды? | Исследовать. Где находится очень много солёной воды? |
| geography_08 | de | prompt | Wo fällt über lange Zeit sehr wenig Niederschlag? | Beobachten. Wo fällt über lange Zeit sehr wenig Niederschlag? |
| geography_08 | en | prompt | Where is there very little precipitation over a long time? | Observe. Where is there very little precipitation over a long time? |
| geography_08 | ru | prompt | Где долгое время выпадает очень мало осадков? | Наблюдение. Где долгое время выпадает очень мало осадков? |
| geography_09 | de | prompt | Wo wachsen viele Bäume zusammen? | Entdecken. Wo wachsen viele Bäume zusammen? |
| geography_09 | en | prompt | Where do many trees grow together? | Explore. Where do many trees grow together? |
| geography_09 | ru | prompt | Где много деревьев растёт вместе? | Открытие. Где много деревьев растёт вместе? |
| geography_10 | de | prompt | Was kann aus Wolken zum Boden fallen? | Beobachten. Was kann aus Wolken zum Boden fallen? |
| geography_10 | en | prompt | What can fall from clouds to the ground? | Observe. What can fall from clouds to the ground? |
| geography_10 | ru | prompt | Что может падать из облаков на землю? | Наблюдение. Что может падать из облаков на землю? |
| geography_11 | de | prompt | Was fällt als Eiskristalle vom Himmel? | Entdecken. Was fällt als Eiskristalle vom Himmel? |
| geography_11 | en | prompt | What falls from the sky as ice crystals? | Explore. What falls from the sky as ice crystals? |
| geography_11 | ru | prompt | Что падает с неба в виде кристалликов льда? | Открытие. Что падает с неба в виде кристалликов льда? |
| geography_12 | de | prompt | Was versorgt die Erde mit Licht und Wärme? | Leuchten. Was versorgt die Erde mit Licht und Wärme? |
| geography_12 | en | prompt | What gives Earth light and warmth? | Light. What gives Earth light and warmth? |
| geography_12 | ru | prompt | Что даёт Земле свет и тепло? | Свет. Что даёт Земле свет и тепло? |
| geography_13 | de | prompt | Was umkreist die Erde? | Verändern. Was umkreist die Erde? |
| geography_13 | en | prompt | What orbits Earth? | Change. What orbits Earth? |
| geography_13 | ru | prompt | Что обращается вокруг Земли? | Изменение. Что обращается вокруг Земли? |
| geography_14 | de | prompt | Was verbindet zwei Ufer für einen Weg? | Entdecken. Was verbindet zwei Ufer für einen Weg? |
| geography_14 | en | prompt | What connects two banks so a path can cross? | Explore. What connects two banks so a path can cross? |
| geography_14 | ru | prompt | Что соединяет берега и позволяет перейти реку? | Открытие. Что соединяет берега и позволяет перейти реку? |
| geography_15 | de | prompt | Wohin fließen viele große Flüsse schließlich? | Entdecken. Wohin fließen viele große Flüsse schließlich? |
| geography_15 | en | prompt | Where do many large rivers eventually flow? | Explore. Where do many large rivers eventually flow? |
| geography_15 | ru | prompt | Куда в конце концов впадают многие большие реки? | Открытие. Куда в конце концов впадают многие большие реки? |
| geography_16 | de | prompt | Was kann als gefrorene weiße Schicht auch im Sommer auf hohen Bergen liegen? | Entdecken. Was kann als gefrorene weiße Schicht auch im Sommer auf hohen Bergen liegen? |
| geography_16 | en | prompt | What can remain as a frozen white layer on high mountains even in summer? | Explore. What can remain as a frozen white layer on high mountains even in summer? |
| geography_16 | ru | prompt | Что может лежать замёрзшим белым слоем на высоких горах даже летом? | Открытие. Что может лежать замёрзшим белым слоем на высоких горах даже летом? |
| geography_17 | de | prompt | Was ist auf Karten oft blau eingezeichnet? | Orientieren. Was ist auf Karten oft blau eingezeichnet? |
| geography_17 | en | prompt | What is often coloured blue on maps? | Direction. What is often coloured blue on maps? |
| geography_17 | ru | prompt | Что на картах часто обозначают синим цветом? | Ориентир. Что на картах часто обозначают синим цветом? |
| geography_18 | de | prompt | Was bedeutet ein Waldzeichen auf einer Karte? | Orientieren. Was bedeutet ein Waldzeichen auf einer Karte? |
| geography_18 | en | prompt | What does a forest symbol on a map show? | Direction. What does a forest symbol on a map show? |
| geography_18 | ru | prompt | Что показывает знак леса на карте? | Ориентир. Что показывает знак леса на карте? |
| geography_19 | de | prompt | Was zeigt ein Brückenzeichen auf einer Karte? | Orientieren. Was zeigt ein Brückenzeichen auf einer Karte? |
| geography_19 | en | prompt | What does a bridge symbol on a map show? | Direction. What does a bridge symbol on a map show? |
| geography_19 | ru | prompt | Что показывает знак моста на карте? | Ориентир. Что показывает знак моста на карте? |
| geography_20 | de | prompt | Was bedeckt den größten Teil der Erdoberfläche? | Entdecken. Was bedeckt den größten Teil der Erdoberfläche? |
| geography_20 | en | prompt | What covers most of Earth’s surface? | Explore. What covers most of Earth’s surface? |
| geography_20 | ru | prompt | Что покрывает большую часть поверхности Земли? | Открытие. Что покрывает большую часть поверхности Земли? |
| geography_21 | de | prompt | Wo entstehen Regentropfen am Himmel? | Beobachten. Wo entstehen Regentropfen am Himmel? |
| geography_21 | en | prompt | Where do raindrops form in the sky? | Observe. Where do raindrops form in the sky? |
| geography_21 | ru | prompt | Где в небе образуются дождевые капли? | Наблюдение. Где в небе образуются дождевые капли? |
| geography_22 | de | prompt | Was erwärmt das Wasser im Wasserkreislauf vor allem? | Verändern. Was erwärmt das Wasser im Wasserkreislauf vor allem? |
| geography_22 | en | prompt | What mainly warms water in Earth’s water cycle? | Change. What mainly warms water in Earth’s water cycle? |
| geography_22 | ru | prompt | Что в основном нагревает воду в круговороте воды на Земле? | Изменение. Что в основном нагревает воду в круговороте воды на Земле? |
| geography_23 | de | prompt | Wie gelangt Wasser aus Wolken zurück zum Boden? | Beobachten. Wie gelangt Wasser aus Wolken zurück zum Boden? |
| geography_23 | en | prompt | How can water return from clouds to the ground? | Observe. How can water return from clouds to the ground? |
| geography_23 | ru | prompt | Как вода из облаков возвращается на землю? | Наблюдение. Как вода из облаков возвращается на землю? |
| geography_24 | de | prompt | Wo kann ein Fluss hoch oben entspringen? | Entdecken. Wo kann ein Fluss hoch oben entspringen? |
| geography_24 | en | prompt | Where can a river begin high above the plains? | Explore. Where can a river begin high above the plains? |
| geography_24 | ru | prompt | Где высоко над равниной может начинаться река? | Открытие. Где высоко над равниной может начинаться река? |
| geography_25 | de | prompt | Was liegt an vielen Stränden als kleine Körner? | Entdecken. Was liegt an vielen Stränden als kleine Körner? |
| geography_25 | en | prompt | What lies in little grains on many beaches? | Explore. What lies in little grains on many beaches? |
| geography_25 | ru | prompt | Что лежит мелкими крупинками на многих пляжах? | Открытие. Что лежит мелкими крупинками на многих пляжах? |
| geography_26 | de | prompt | Was ist in trockenen Wüsten besonders knapp? | Entdecken. Was ist in trockenen Wüsten besonders knapp? |
| geography_26 | en | prompt | What is especially scarce in dry deserts? | Explore. What is especially scarce in dry deserts? |
| geography_26 | ru | prompt | Чего особенно мало в сухих пустынях? | Открытие. Чего особенно мало в сухих пустынях? |
| geography_27 | de | prompt | Was siehst du rings um eine Meeresinsel? | Entdecken. Was siehst du rings um eine Meeresinsel? |
| geography_27 | en | prompt | What surrounds an island in the sea? | Explore. What surrounds an island in the sea? |
| geography_27 | ru | prompt | Что окружает морской остров? | Открытие. Что окружает морской остров? |
| geography_28 | de | prompt | Was gehört zu einem Wald? | Wachsen. Was gehört zu einem Wald? |
| geography_28 | en | prompt | What belongs in a forest? | Grow. What belongs in a forest? |
| geography_28 | ru | prompt | Что относится к лесу? | Расти. Что относится к лесу? |
| geography_29 | de | prompt | Was lässt sich zusammenfalten und zeigt deinen Spazierweg? | Entdecken. Was lässt sich zusammenfalten und zeigt deinen Spazierweg? |
| geography_29 | en | prompt | What can be folded up and show your walking route? | Explore. What can be folded up and show your walking route? |
| geography_29 | ru | prompt | Что можно сложить и использовать для выбора маршрута прогулки? | Открытие. Что можно сложить и использовать для выбора маршрута прогулки? |
| geography_30 | de | prompt | Welches Modell zeigt auch die Rückseite der Erde beim Drehen? | Orientieren. Welches Modell zeigt auch die Rückseite der Erde beim Drehen? |
| geography_30 | en | prompt | Which model shows Earth's other side when you turn it? | Direction. Which model shows Earth's other side when you turn it? |
| geography_30 | ru | prompt | Какая модель показывает другую сторону Земли при повороте? | Ориентир. Какая модель показывает другую сторону Земли при повороте? |
| geography_31 | de | prompt | Was kann die Sonne am Himmel verdecken? | Beobachten. Was kann die Sonne am Himmel verdecken? |
| geography_31 | en | prompt | What can hide the sun in the sky? | Observe. What can hide the sun in the sky? |
| geography_31 | ru | prompt | Что может закрыть Солнце в небе? | Наблюдение. Что может закрыть Солнце в небе? |
| geography_32 | de | prompt | Was kann im Frühling Schnee schmelzen lassen? | Beobachten. Was kann im Frühling Schnee schmelzen lassen? |
| geography_32 | en | prompt | What can help melt snow in spring? | Observe. What can help melt snow in spring? |
| geography_32 | ru | prompt | Что помогает снегу таять весной? | Наблюдение. Что помогает снегу таять весной? |
| geography_33 | de | prompt | Was ist lang, fließt und hat zwei Ufer? | Entdecken. Was ist lang, fließt und hat zwei Ufer? |
| geography_33 | en | prompt | What is long, flows and has two banks? | Explore. What is long, flows and has two banks? |
| geography_34 | de | prompt | Welche Landschaft erkennst du an einem hohen Gipfel? | Entdecken. Welche Landschaft erkennst du an einem hohen Gipfel? |
| geography_34 | en | prompt | Which landscape has a high peak? | Explore. Which landscape has a high peak? |
| geography_34 | ru | prompt | У какого элемента рельефа высокая вершина? | Открытие. У какого элемента рельефа высокая вершина? |
| geography_35 | de | prompt | Welches große Gewässer ist normalerweise salzig? | Entdecken. Welches große Gewässer ist normalerweise salzig? |
| geography_35 | en | prompt | Which large body of water is normally salty? | Explore. Which large body of water is normally salty? |
| geography_35 | ru | prompt | Какой большой водоём обычно солёный? | Открытие. Какой большой водоём обычно солёный? |
| geography_36 | de | prompt | Welches Gerät zeigt mit einer Magnetnadel die Nordrichtung für deine Karte? | Orientieren. Welches Gerät zeigt mit einer Magnetnadel die Nordrichtung für deine Karte? |
| geography_36 | en | prompt | Which instrument uses a magnetic needle to show north for your map? | Direction. Which instrument uses a magnetic needle to show north for your map? |
| geography_36 | ru | prompt | Какой прибор магнитной стрелкой показывает север для твоей карты? | Ориентир. Какой прибор магнитной стрелкой показывает север для твоей карты? |
| geography_37 | de | prompt | Welcher Niederschlag ist flüssig? | Entdecken. Welcher Niederschlag ist flüssig? |
| geography_37 | en | prompt | Which kind of precipitation is liquid? | Explore. Which kind of precipitation is liquid? |
| geography_37 | ru | prompt | Какие осадки жидкие? | Открытие. Какие осадки жидкие? |
| geography_38 | de | prompt | Was ist ein Stern: Sonne, Wolke oder Mond? | Beobachten. Was ist ein Stern: Sonne, Wolke oder Mond? |
| geography_38 | en | prompt | Which is a star: the sun, a cloud or the moon? | Observe. Which is a star: the sun, a cloud or the moon? |
| geography_38 | ru | prompt | Что является звездой: Солнце, облако или Луна? | Наблюдение. Что является звездой: Солнце, облако или Луна? |
| geography_39 | de | prompt | Welcher Himmelskörper liefert das meiste Licht, das der Mond zurückwirft? | Leuchten. Wessen Licht wirft der Mond hauptsächlich zurück? |
| geography_39 | en | prompt | Which celestial body supplies most of the light reflected by the Moon? | Light. Whose light does the Moon mainly reflect? |
| geography_39 | ru | prompt | Какое небесное тело даёт большую часть света, отражаемого Луной? | Свет. Чей свет в основном отражает Луна? |
| geography_40 | de | prompt | Was bringen Regen und Flüsse vielen Pflanzen? | Wachsen. Was bringen Regen und Flüsse vielen Pflanzen? |
| geography_40 | en | prompt | What do rain and rivers bring to many plants? | Growing. What do rain and rivers bring to many plants? |
| geography_40 | ru | prompt | Что дождь и реки приносят многим растениям? | Рост. Что дождь и реки приносят многим растениям? |
