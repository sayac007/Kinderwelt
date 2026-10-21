# Lokalisierungsabgleich

Verglichen: alle 320 Fragen und Hinweise in Deutsch, Englisch und Russisch (960 Sprachfassungen). Die 200 Sachfragen wurden inhaltlich auf Objekte, Bedingungen, Mengen, Verneinungen und Sicherheitshinweise abgeglichen; außerdem alle 120 Mathe-, Deutsch- und Logikaufgaben. Dies ist eine redaktionelle Prüfung, keine unabhängige muttersprachliche Freigabe.

199 Textfelder in 60 Aufgaben geändert; Ausgangscommit `cca9b049c11cc131ef331f064e4fe28af9ec9130`. Richtige Antworten, Zuordnung, Bilder und Mechanik bleiben erhalten. Die ursprünglichen 24 deutschen Aufgabentexte bleiben wortgleich.

## Abgleich und Grenzen

- Mengenaufgaben nennen die Gegenstände, wenn die deutsche Fassung sie nennt. Ursprüngliche Zahlenfolgen und konkrete Hinweise sind in EN/RU vollständig.
- Deutsche Lernwörter, einzelne Buchstaben und Klatsch-Silben stehen auch in EN/RU auf dem Bildschirm. Die Erklärung wird lokal gesprochen, anschließend folgen Wort und Hinweis aus der deutschen Aufnahme. Fremdsprachige Modelle sprechen keine deutschen Lernwörter vor.
- Sachfragen behalten Einschränkungen wie „meist“, „nicht alle“, „bei Raumtemperatur“, „unsichtbar“, konkrete Materialien und Hilfe durch Erwachsene. Ergänzt wurden unter anderem Kraftwirkung, dicht beieinander stehende Bäume, abgestorbene Blätter, langer Fluss und die Unterscheidung Sinn/Körperteil.
- Keine automatische Behauptung vollständiger Bedeutungsäquivalenz. Tests schützen ausgewählte konkrete Informationsverluste und die Reproduzierbarkeit.

## Noch durch Muttersprachler / Fachpersonen prüfen

- EN/RU: natürliches Sprechtempo und Verständnis bei Kindern der ersten und zweiten Klasse; alle 320 Aufgaben im Kontext der Bilder.
- RU: technische Begriffe „блок“ (Seilrolle), „качели-доска“, „ось“, „вкусовые почки“ und Schulkontext der Fremdsprachensilben. Verständlichkeit gezielt beobachten; keine ungeprüften Fachbegriffe ersetzen.
- EN: „food pipe“, „forewings/hindwings“, „precipitation“ und „physiology“ auf altersgerechtes Verständnis prüfen.
- Deutsche Rechtschreibung versus gehörte Anlaute (z. B. Sonne): die Fragen prüfen den Anfangsbuchstaben; keine Lautschrift oder Übersetzung des Lernworts lehren.
- Mehrsprachige Bildschirmtexte und deutsche Folgeaufnahme gemeinsam hören; ASR allein kann diese Lernsequenzen nicht freigeben.

## Vollständiges Änderungsprotokoll

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
| german_sun | en | prompt | Listen to the German word. Which letter does it start with? | German word: Sonne. Which letter does it start with? |
| german_sun | en | tip | The German word starts with the letter S. Choose that letter. | Sonne starts with the letter S. Choose that letter. |
| german_sun | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Sonne. С какой буквы его пишут? |
| german_sun | ru | tip | Немецкое слово начинается с буквы S. Выбери эту букву. | Sonne начинается с буквы S. Выбери эту букву. |
| german_mouse | en | prompt | Listen to the German word. Which letter does it start with? | German word: Maus. Which letter does it start with? |
| german_mouse | en | tip | The German word starts with the letter M. Choose that letter. | Maus starts with the letter M. Choose that letter. |
| german_mouse | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Maus. С какой буквы его пишут? |
| german_mouse | ru | tip | Немецкое слово начинается с буквы M. Выбери эту букву. | Maus начинается с буквы M. Выбери эту букву. |
| german_apple | en | prompt | Listen to the German word. Which letter does it start with? | German word: Apfel. Which letter does it start with? |
| german_apple | en | tip | The German word starts with the letter A. Choose that letter. | Apfel starts with the letter A. Choose that letter. |
| german_apple | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Apfel. С какой буквы его пишут? |
| german_apple | ru | tip | Немецкое слово начинается с буквы A. Выбери эту букву. | Apfel начинается с буквы A. Выбери эту букву. |
| german_rhyme | en | prompt | Listen to the German words. Which one rhymes with the word for house? | Which German word rhymes with Haus? |
| german_rhyme | en | tip | The German words for house and mouse rhyme: listen to the German example. | Haus and Maus sound the same at the end. |
| german_rhyme | ru | prompt | Послушай немецкие слова. Какое рифмуется со словом «дом» по-немецки? | Какое немецкое слово рифмуется со словом Haus? |
| german_rhyme | ru | tip | Немецкие слова «дом» и «мышь» рифмуются. Послушай пример по-немецки. | Haus и Maus звучат одинаково в конце. |
| german_robot | en | prompt | Listen to the German word. How many syllables does it have? | German word: Roboter. How many syllables can you hear? |
| german_robot | en | tip | Clap along with the German word. It has 3 syllables. | Say and clap: Ro. Bo. Ter. That is 3 syllables. |
| german_robot | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Roboter. Сколько слогов ты слышишь? |
| german_robot | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 3 слога. | Произнеси и хлопай: Ro. Bo. Ter. Это 3 слога. |
| german_read | en | prompt | Which German word matches the picture? | Which German word belongs to the ball? |
| german_read | en | tip | Match the written German word to the picture. Listen to its German reading next. | B. A. L. L. Find the word Ball. |
| german_read | ru | prompt | Какое немецкое слово подходит к картинке? | Какое немецкое слово подходит к мячу? |
| german_read | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | B. A. L. L. Найди слово Ball. |
| german_flower | en | prompt | Listen to the German word. How many syllables does it have? | German word: Blume. How many syllables can you hear? |
| german_flower | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Blu. Me. That is 2 syllables. |
| german_flower | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Blume. Сколько слогов ты слышишь? |
| german_flower | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Blu. Me. Это 2 слога. |
| german_fish | en | prompt | Listen to the German word. Which letter does it start with? | German word: Fisch. Which letter does it start with? |
| german_fish | en | tip | The German word starts with the letter F. Choose that letter. | Fisch starts with the letter F. Choose that letter. |
| german_fish | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Fisch. С какой буквы его пишут? |
| german_fish | ru | tip | Немецкое слово начинается с буквы F. Выбери эту букву. | Fisch начинается с буквы F. Выбери эту букву. |
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
| german_09 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Biene. Which letter does it start with? |
| german_09 | en | tip | The German word starts with the letter B. Choose that letter. | Biene starts with the letter B. Choose that letter. |
| german_09 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Biene. С какой буквы его пишут? |
| german_09 | ru | tip | Немецкое слово начинается с буквы B. Выбери эту букву. | Biene начинается с буквы B. Выбери эту букву. |
| german_10 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Frosch. Which letter does it start with? |
| german_10 | en | tip | The German word starts with the letter F. Choose that letter. | Frosch starts with the letter F. Choose that letter. |
| german_10 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Frosch. С какой буквы его пишут? |
| german_10 | ru | tip | Немецкое слово начинается с буквы F. Выбери эту букву. | Frosch начинается с буквы F. Выбери эту букву. |
| german_11 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Katze. Which letter does it start with? |
| german_11 | en | tip | The German word starts with the letter K. Choose that letter. | Katze starts with the letter K. Choose that letter. |
| german_11 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Katze. С какой буквы его пишут? |
| german_11 | ru | tip | Немецкое слово начинается с буквы K. Выбери эту букву. | Katze начинается с буквы K. Выбери эту букву. |
| german_12 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Nest. Which letter does it start with? |
| german_12 | en | tip | The German word starts with the letter N. Choose that letter. | Nest starts with the letter N. Choose that letter. |
| german_12 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Nest. С какой буквы его пишут? |
| german_12 | ru | tip | Немецкое слово начинается с буквы N. Выбери эту букву. | Nest начинается с буквы N. Выбери эту букву. |
| german_13 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Wurm. Which letter does it start with? |
| german_13 | en | tip | The German word starts with the letter W. Choose that letter. | Wurm starts with the letter W. Choose that letter. |
| german_13 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Wurm. С какой буквы его пишут? |
| german_13 | ru | tip | Немецкое слово начинается с буквы W. Выбери эту букву. | Wurm начинается с буквы W. Выбери эту букву. |
| german_14 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Wasser. Which letter does it start with? |
| german_14 | en | tip | The German word starts with the letter W. Choose that letter. | Wasser starts with the letter W. Choose that letter. |
| german_14 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Wasser. С какой буквы его пишут? |
| german_14 | ru | tip | Немецкое слово начинается с буквы W. Выбери эту букву. | Wasser начинается с буквы W. Выбери эту букву. |
| german_15 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Salz. Which letter does it start with? |
| german_15 | en | tip | The German word starts with the letter S. Choose that letter. | Salz starts with the letter S. Choose that letter. |
| german_15 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Salz. С какой буквы его пишут? |
| german_15 | ru | tip | Немецкое слово начинается с буквы S. Выбери эту букву. | Salz начинается с буквы S. Выбери эту букву. |
| german_16 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Sand. Which letter does it start with? |
| german_16 | en | tip | The German word starts with the letter S. Choose that letter. | Sand starts with the letter S. Choose that letter. |
| german_16 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Sand. С какой буквы его пишут? |
| german_16 | ru | tip | Немецкое слово начинается с буквы S. Выбери эту букву. | Sand начинается с буквы S. Выбери эту букву. |
| german_17 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Holz. Which letter does it start with? |
| german_17 | en | tip | The German word starts with the letter H. Choose that letter. | Holz starts with the letter H. Choose that letter. |
| german_17 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Holz. С какой буквы его пишут? |
| german_17 | ru | tip | Немецкое слово начинается с буквы H. Выбери эту букву. | Holz начинается с буквы H. Выбери эту букву. |
| german_18 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Nase. Which letter does it start with? |
| german_18 | en | tip | The German word starts with the letter N. Choose that letter. | Nase starts with the letter N. Choose that letter. |
| german_18 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Nase. С какой буквы его пишут? |
| german_18 | ru | tip | Немецкое слово начинается с буквы N. Выбери эту букву. | Nase начинается с буквы N. Выбери эту букву. |
| german_19 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Hand. Which letter does it start with? |
| german_19 | en | tip | The German word starts with the letter H. Choose that letter. | Hand starts with the letter H. Choose that letter. |
| german_19 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Hand. С какой буквы его пишут? |
| german_19 | ru | tip | Немецкое слово начинается с буквы H. Выбери эту букву. | Hand начинается с буквы H. Выбери эту букву. |
| german_20 | en | prompt | Listen to the German word. Which letter does it start with? | German word: Herz. Which letter does it start with? |
| german_20 | en | tip | The German word starts with the letter H. Choose that letter. | Herz starts with the letter H. Choose that letter. |
| german_20 | ru | prompt | Послушай немецкое слово. С какой буквы его пишут? | Немецкое слово: Herz. С какой буквы его пишут? |
| german_20 | ru | tip | Немецкое слово начинается с буквы H. Выбери эту букву. | Herz начинается с буквы H. Выбери эту букву. |
| german_21 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Schmetterling. How many syllables can you hear? |
| german_21 | en | tip | Clap along with the German word. It has 3 syllables. | Say and clap: Schmet. Ter. Ling. That is 3 syllables. |
| german_21 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Schmetterling. Сколько слогов ты слышишь? |
| german_21 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 3 слога. | Произнеси и хлопай: Schmet. Ter. Ling. Это 3 слога. |
| german_22 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Schildkröte. How many syllables can you hear? |
| german_22 | en | tip | Clap along with the German word. It has 3 syllables. | Say and clap: Schild. Krö. Te. That is 3 syllables. |
| german_22 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Schildkröte. Сколько слогов ты слышишь? |
| german_22 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 3 слога. | Произнеси и хлопай: Schild. Krö. Te. Это 3 слога. |
| german_23 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Batterie. How many syllables can you hear? |
| german_23 | en | tip | Clap along with the German word. It has 3 syllables. | Say and clap: Bat. Te. Rie. That is 3 syllables. |
| german_23 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Batterie. Сколько слогов ты слышишь? |
| german_23 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 3 слога. | Произнеси и хлопай: Bat. Te. Rie. Это 3 слога. |
| german_24 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Papier. How many syllables can you hear? |
| german_24 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Pa. Pier. That is 2 syllables. |
| german_24 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Papier. Сколько слогов ты слышишь? |
| german_24 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Pa. Pier. Это 2 слога. |
| german_25 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Seife. How many syllables can you hear? |
| german_25 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Sei. Fe. That is 2 syllables. |
| german_25 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Seife. Сколько слогов ты слышишь? |
| german_25 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Sei. Fe. Это 2 слога. |
| german_26 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Auge. How many syllables can you hear? |
| german_26 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Au. Ge. That is 2 syllables. |
| german_26 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Auge. Сколько слогов ты слышишь? |
| german_26 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Au. Ge. Это 2 слога. |
| german_27 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Gehirn. How many syllables can you hear? |
| german_27 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Ge. Hirn. That is 2 syllables. |
| german_27 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Gehirn. Сколько слогов ты слышишь? |
| german_27 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Ge. Hirn. Это 2 слога. |
| german_28 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Magen. How many syllables can you hear? |
| german_28 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Ma. Gen. That is 2 syllables. |
| german_28 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Magen. Сколько слогов ты слышишь? |
| german_28 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Ma. Gen. Это 2 слога. |
| german_29 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Wolke. How many syllables can you hear? |
| german_29 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Wol. Ke. That is 2 syllables. |
| german_29 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Wolke. Сколько слогов ты слышишь? |
| german_29 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Wol. Ke. Это 2 слога. |
| german_30 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Regen. How many syllables can you hear? |
| german_30 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Re. Gen. That is 2 syllables. |
| german_30 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Regen. Сколько слогов ты слышишь? |
| german_30 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Re. Gen. Это 2 слога. |
| german_31 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Insel. How many syllables can you hear? |
| german_31 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: In. Sel. That is 2 syllables. |
| german_31 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Insel. Сколько слогов ты слышишь? |
| german_31 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: In. Sel. Это 2 слога. |
| german_32 | en | prompt | Listen to the German word. How many syllables does it have? | German word: Hammer. How many syllables can you hear? |
| german_32 | en | tip | Clap along with the German word. It has 2 syllables. | Say and clap: Ham. Mer. That is 2 syllables. |
| german_32 | ru | prompt | Послушай немецкое слово. Сколько в нём слогов? | Немецкое слово: Hammer. Сколько слогов ты слышишь? |
| german_32 | ru | tip | Произнеси немецкое слово, хлопая по слогам. В нём 2 слога. | Произнеси и хлопай: Ham. Mer. Это 2 слога. |
| german_33 | en | tip | Match the written German word to the picture. Listen to its German reading next. | Find the letters of Fisch: F. I. S. C. H. |
| german_33 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Найди буквы слова Fisch: F. I. S. C. H. |
| german_34 | en | tip | Match the written German word to the picture. Listen to its German reading next. | Find the letters of Vogel: V. O. G. E. L. |
| german_34 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Найди буквы слова Vogel: V. O. G. E. L. |
| german_35 | en | tip | Match the written German word to the picture. Listen to its German reading next. | Find the letters of Mond: M. O. N. D. |
| german_35 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Найди буквы слова Mond: M. O. N. D. |
| german_36 | en | tip | Match the written German word to the picture. Listen to its German reading next. | Find the letters of Baum: B. A. U. M. |
| german_36 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Найди буквы слова Baum: B. A. U. M. |
| german_37 | en | tip | Match the written German word to the picture. Listen to its German reading next. | Find the letters of Zahn: Z. A. H. N. |
| german_37 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Найди буквы слова Zahn: Z. A. H. N. |
| german_38 | en | tip | Match the written German word to the picture. Listen to its German reading next. | Find the letters of Fuss: F. U. S. S. |
| german_38 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Найди буквы слова Fuss: F. U. S. S. |
| german_39 | en | tip | Match the written German word to the picture. Listen to its German reading next. | Find the letters of Ei: E. I. |
| german_39 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Найди буквы слова Ei: E. I. |
| german_40 | en | tip | Match the written German word to the picture. Listen to its German reading next. | Find the letters of Meer: M. E. E. R. |
| german_40 | ru | tip | Найди немецкое слово к картинке. Сейчас послушай, как оно читается по-немецки. | Найди буквы слова Meer: M. E. E. R. |
| physics_18 | en | tip | A hand can push the ball and make it move. | A hand can exert a force on the ball and make it move. |
| physics_18 | ru | tip | Рука может подействовать на мяч и привести его в движение. | Рука может подействовать на мяч с силой и привести его в движение. |
| biology_25 | en | prompt | Where do many trees grow together? | Where do many trees grow close together? |
| biology_25 | ru | prompt | Где много деревьев растёт рядом? | Где много деревьев растёт близко друг к другу? |
| biology_37 | ru | tip | Дождевые черви затаскивают опавшие листья в свои ходы. | Дождевые черви затаскивают отмершие опавшие листья в свои ходы. |
| body_17 | en | prompt | Which body part needs protection from very loud sounds? | Which sense needs protection from very loud sounds? |
| body_17 | ru | prompt | Что нужно защищать от очень громких звуков? | Какое чувство нужно защищать от очень громких звуков? |
| body_24 | ru | prompt | Где обрабатываются воспоминания? | Где обрабатывается много воспоминаний? |
| geography_33 | ru | prompt | Что течёт, имеет русло и два берега? | Что длинное, течёт и имеет два берега? |
