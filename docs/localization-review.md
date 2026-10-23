# Lokalisierungsabgleich

0.9.0 enthält 320 Grundaufgaben und 640 freiwillige Bonusaufgaben in jeweils drei Sprachen. Die Strukturprüfung deckt Übersetzungsfelder, Antwortoptionen, native Lernwörter und kyrillische russische Inhalte ab. Sie ersetzt keine muttersprachliche oder fachliche Freigabe.

1920 geänderte Grundaufgaben-Textfelder seit Ausgangscommit `f513bf43d1270d7caa8750fd13b39052a9dee3a3` sind unten protokolliert. Bonusinhalte stehen vollständig in `tasks.json` und den versionierten Inhaltsquellen.

## Aktuelle Regeln

- Deutsch vermittelt deutsche, English englische und Русский russische Lernwörter, Anfangsbuchstaben und Silben. Keine automatische deutsche Folgeaufnahme in EN/RU.
- Russische sichtbare Texte, Namen, Musikbeschriftungen und alle 1947 gesprochenen Einträge sind ohne lateinische Buchstaben. Interne stabile IDs und Quellen-/Lizenzdateien sind keine Lerninhalte.
- Die zweite Runde ersetzt alle 320 Fragen. Neue native Wörter haben zwei Buchstabenlücken, freiwillige Boni drei oder vier. Rechtschreibung ist von Lautschrift zu unterscheiden.
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
| math_count | de | prompt | Wie viele Äpfel siehst du? | Zu 9 kommen 4, dann gehen 2. Wie viele bleiben? |
| math_count | de | tip | Tippe jeden Apfel einmal an. Zähle dabei mit. | 9 plus 4 sind 13. Dann 2 weg. |
| math_count | en | prompt | How many apples can you see? | 4 join 9, then 2 leave. How many remain? |
| math_count | en | tip | Tap each apple once. Count as you go. | 9 plus 4 is 13. Then take away 2. |
| math_count | ru | prompt | Сколько яблок ты видишь? | Было 9. Добавили 4, убрали 2. Сколько осталось? |
| math_count | ru | tip | Коснись каждого яблока один раз. Считай при этом. | 9 плюс 4 — это 13. Потом убери 2. |
| math_add | de | prompt | Drei Äpfel und zwei Äpfel. Wie viele sind es zusammen? | Ergänze 10 bis 14. Welche Zahl fehlt? |
| math_add | de | tip | Zähle erst links. Zähle dann rechts weiter. | Gehe zuerst zum nächsten Zehner, dann bis 14. |
| math_add | en | prompt | Three apples and two apples. How many altogether? | Complete 10 up to 14. Which number is missing? |
| math_add | en | tip | Count the left group first. Then keep counting on the right. | Go to the next ten first, then up to 14. |
| math_add | ru | prompt | Три яблока и два яблока. Сколько всего? | Было 10, стало 14. Сколько добавили? |
| math_add | ru | tip | Сначала посчитай слева. Затем продолжи считать справа. | Сначала дойди до следующего десятка, потом до 14. |
| math_take | de | prompt | Sieben Blätter. Drei fliegen weg. Wie viele bleiben? | 2 Körbe mit je 3 Äpfeln. Du verschenkst 1. Wie viele bleiben? |
| math_take | de | tip | Zähle nur die Blätter ohne Kreuz. | Alle Körbe zusammen: 6. Nun 1 abziehen. |
| math_take | en | prompt | Seven leaves. Three fly away. How many remain? | 2 baskets have 3 apples each. You give away 1. How many remain? |
| math_take | en | tip | Count only the leaves without a cross. | All baskets together: 6. Now subtract 1. |
| math_take | ru | prompt | Семь листьев. Три улетают. Сколько осталось? | Корзин: 2. В каждой яблок: 3. Отдали 1. Сколько осталось? |
| math_take | ru | tip | Считай только листья без крестика. | Во всех корзинах вместе 6. Теперь вычти 1. |
| math_ten | de | prompt | Vier Sterne sind schon da. Wie viele fehlen bis zehn? | Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg? |
| math_ten | de | tip | Zähle die leeren Sternplätze. | Nimm die 3 zuerst wieder weg. Vergleiche 15 mit 20. |
| math_ten | en | prompt | Four stars are already there. How many more make ten? | A number is taken away, then some is added. How much was taken away? |
| math_ten | en | tip | Count the empty star spaces. | Undo the added 3 first. Compare 15 with 20. |
| math_ten | ru | prompt | Уже есть четыре звезды. Сколько не хватает до десяти? | Сначала число убрали, потом немного добавили. Сколько убрали? |
| math_ten | ru | tip | Посчитай пустые места для звёзд. | Сначала отмени прибавление 3. Сравни 15 и 20. |
| math_compare | de | prompt | Wo sind mehr Äpfel? | Zu 13 kommen 5, dann gehen 2. Wie viele bleiben? |
| math_compare | de | tip | Vergleiche die beiden Mengen. Tippe die größere an. | 13 plus 5 sind 18. Dann 2 weg. |
| math_compare | en | prompt | Where are there more apples? | 5 join 13, then 2 leave. How many remain? |
| math_compare | en | tip | Compare both groups. Tap the larger group. | 13 plus 5 is 18. Then take away 2. |
| math_compare | ru | prompt | Где больше яблок? | Было 13. Добавили 5, убрали 2. Сколько осталось? |
| math_compare | ru | tip | Сравни обе группы. Коснись той, где больше. | 13 плюс 5 — это 18. Потом убери 2. |
| math_steps | de | prompt | Zwei, vier, sechs. Welche Zahl kommt als Nächstes? | Ergänze 14 bis 19. Welche Zahl fehlt? |
| math_steps | de | tip | Es kommen jedes Mal zwei dazu. | Gehe zuerst zum nächsten Zehner, dann bis 19. |
| math_steps | en | prompt | Two, four, six. Which number comes next? | Complete 14 up to 19. Which number is missing? |
| math_steps | en | tip | Add two each time. | Go to the next ten first, then up to 19. |
| math_steps | ru | prompt | Два, четыре, шесть. Какое число следующее? | Было 14, стало 19. Сколько добавили? |
| math_steps | ru | tip | Каждый раз прибавляй два. | Сначала дойди до следующего десятка, потом до 19. |
| math_twenty | de | prompt | Zehn und vier. Wie viel ist das zusammen? | 2 Körbe mit je 4 Äpfeln. Du verschenkst 2. Wie viele bleiben? |
| math_twenty | de | tip | Die erste Menge ist zehn. Zähle vier weiter. | Alle Körbe zusammen: 8. Nun 2 abziehen. |
| math_twenty | en | prompt | Ten and four. How many altogether? | 2 baskets have 4 apples each. You give away 2. How many remain? |
| math_twenty | en | tip | The first group has ten. Count on four more. | All baskets together: 8. Now subtract 2. |
| math_twenty | ru | prompt | Десять и четыре. Сколько всего? | Корзин: 2. В каждой яблок: 4. Отдали 2. Сколько осталось? |
| math_twenty | ru | tip | В первой группе десять. Отсчитай ещё четыре. | Во всех корзинах вместе 8. Теперь вычти 2. |
| math_split | de | prompt | Fünf Sterne sind schon da. Wie viele fehlen bis acht? | Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg? |
| math_split | de | tip | Zähle die leeren Sternplätze. | Nimm die 3 zuerst wieder weg. Vergleiche 22 mit 24. |
| math_split | en | prompt | Five stars are already there. How many more make eight? | A number is taken away, then some is added. How much was taken away? |
| math_split | en | tip | Count the empty star spaces. | Undo the added 3 first. Compare 22 with 24. |
| math_split | ru | prompt | Уже есть пять звёзд. Сколько не хватает до восьми? | Сначала число убрали, потом немного добавили. Сколько убрали? |
| math_split | ru | tip | Посчитай пустые места для звёзд. | Сначала отмени прибавление 3. Сравни 22 и 24. |
| german_sun | de | prompt | Sonne. Welcher Buchstabe passt am Anfang? | Sonnenstrahl. Welche beiden Buchstaben fehlen? |
| german_sun | de | tip | Das Wort Sonne beginnt mit S. Suche das S. | Lies von links nach rechts. Die Lücken brauchen S. S. |
| german_sun | en | prompt | German word: Sonne. Which letter does it start with? | Sunshine. Which two letters are missing? |
| german_sun | en | tip | Sonne starts with the letter S. Choose that letter. | Read from left to right. The gaps need S. H. |
| german_sun | ru | prompt | Немецкое слово: Sonne. С какой буквы его пишут? | Солнышко. Какие две буквы пропущены? |
| german_sun | ru | tip | Sonne начинается с буквы S. Выбери эту букву. | Читай слева направо. В пропусках: С. Ы. |
| german_mouse | de | prompt | Maus. Welcher Buchstabe passt am Anfang? | Mauseloch. Welche beiden Buchstaben fehlen? |
| german_mouse | de | tip | Maus beginnt mit M. Suche das M. | Lies von links nach rechts. Die Lücken brauchen A. L. |
| german_mouse | en | prompt | German word: Maus. Which letter does it start with? | Mousehole. Which two letters are missing? |
| german_mouse | en | tip | Maus starts with the letter M. Choose that letter. | Read from left to right. The gaps need O. H. |
| german_mouse | ru | prompt | Немецкое слово: Maus. С какой буквы его пишут? | Мышонок. Какие две буквы пропущены? |
| german_mouse | ru | tip | Maus начинается с буквы M. Выбери эту букву. | Читай слева направо. В пропусках: Ы. Н. |
| german_apple | de | prompt | Apfel. Welcher Buchstabe passt am Anfang? | Apfelsaft. Welche beiden Buchstaben fehlen? |
| german_apple | de | tip | Apfel beginnt mit A. Suche das A. | Lies von links nach rechts. Die Lücken brauchen F. A. |
| german_apple | en | prompt | German word: Apfel. Which letter does it start with? | Applesauce. Which two letters are missing? |
| german_apple | en | tip | Apfel starts with the letter A. Choose that letter. | Read from left to right. The gaps need P. U. |
| german_apple | ru | prompt | Немецкое слово: Apfel. С какой буквы его пишут? | Яблочко. Какие две буквы пропущены? |
| german_apple | ru | tip | Apfel начинается с буквы A. Выбери эту букву. | Читай слева направо. В пропусках: Л. К. |
| german_rhyme | de | prompt | Was reimt sich auf Haus? | Baumhaus. Welche beiden Buchstaben fehlen? |
| german_rhyme | de | tip | Haus und Maus klingen hinten gleich. | Lies von links nach rechts. Die Lücken brauchen M. S. |
| german_rhyme | en | prompt | Which German word rhymes with Haus? | Treehouse. Which two letters are missing? |
| german_rhyme | en | tip | Haus and Maus sound the same at the end. | Read from left to right. The gaps need E. S. |
| german_rhyme | ru | prompt | Какое немецкое слово рифмуется со словом Haus? | Домик. Какие две буквы пропущены? |
| german_rhyme | ru | tip | Haus и Maus звучат одинаково в конце. | Читай слева направо. В пропусках: Д. И. |
| german_robot | de | prompt | Roboter. Wie viele Silben hörst du? | Raumfahrt. Welche beiden Buchstaben fehlen? |
| german_robot | de | tip | Sprich und klatsche: Ro. Bo. Ter. Das sind drei Silben. | Lies von links nach rechts. Die Lücken brauchen F. T. |
| german_robot | en | prompt | German word: Roboter. How many syllables can you hear? | Spaceship. Which two letters are missing? |
| german_robot | en | tip | Say and clap: Ro. Bo. Ter. That is 3 syllables. | Read from left to right. The gaps need E. P. |
| german_robot | ru | prompt | Немецкое слово: Roboter. Сколько слогов ты слышишь? | Ракета. Какие две буквы пропущены? |
| german_robot | ru | tip | Произнеси и хлопай: Ro. Bo. Ter. Это 3 слога. | Читай слева направо. В пропусках: А. Т. |
| german_read | de | prompt | Welches Wort gehört zum Ball? | Ballspiel. Welche beiden Buchstaben fehlen? |
| german_read | de | tip | B. A. L. L. Suche das Wort Ball. | Lies von links nach rechts. Die Lücken brauchen B. P. |
| german_read | en | prompt | Which German word belongs to the ball? | Football. Which two letters are missing? |
| german_read | en | tip | B. A. L. L. Find the word Ball. | Read from left to right. The gaps need O. A. |
| german_read | ru | prompt | Какое немецкое слово подходит к мячу? | Футбол. Какие две буквы пропущены? |
| german_read | ru | tip | B. A. L. L. Найди слово Ball. | Читай слева направо. В пропусках: Т. Л. |
| german_flower | de | prompt | Blume. Wie viele Silben hörst du? | Blumenvase. Welche beiden Buchstaben fehlen? |
| german_flower | de | tip | Sprich und klatsche: Blu. Me. Das sind zwei Silben. | Lies von links nach rechts. Die Lücken brauchen L. V. |
| german_flower | en | prompt | German word: Blume. How many syllables can you hear? | Flowerpot. Which two letters are missing? |
| german_flower | en | tip | Say and clap: Blu. Me. That is 2 syllables. | Read from left to right. The gaps need L. P. |
| german_flower | ru | prompt | Немецкое слово: Blume. Сколько слогов ты слышишь? | Цветочек. Какие две буквы пропущены? |
| german_flower | ru | tip | Произнеси и хлопай: Blu. Me. Это 2 слога. | Читай слева направо. В пропусках: Е. Е. |
| german_fish | de | prompt | Fisch. Welcher Buchstabe passt am Anfang? | Goldfisch. Welche beiden Buchstaben fehlen? |
| german_fish | de | tip | Fisch beginnt mit F. Suche das F. | Lies von links nach rechts. Die Lücken brauchen L. C. |
| german_fish | en | prompt | German word: Fisch. Which letter does it start with? | Goldfish. Which two letters are missing? |
| german_fish | en | tip | Fisch starts with the letter F. Choose that letter. | Read from left to right. The gaps need D. H. |
| german_fish | ru | prompt | Немецкое слово: Fisch. С какой буквы его пишут? | Аквариум. Какие две буквы пропущены? |
| german_fish | ru | tip | Fisch начинается с буквы F. Выбери эту букву. | Читай слева направо. В пропусках: А. М. |
| logic_repeat | de | prompt | Was kommt als Nächstes? | Zwei Schritte wechseln sich ab. Welche Zahl folgt? |
| logic_repeat | de | tip | Apfel, Blatt. Apfel, Blatt. Nach dem Apfel kommt ein Blatt. | Abwechselnd 2 dazu, dann eins dazu. |
| logic_repeat | en | prompt | Apple, leaf. What comes next? | Two steps alternate. Which number follows? |
| logic_repeat | en | tip | Apple and leaf alternate. The next picture is a leaf. | Alternate adding 2, then adding one. |
| logic_repeat | ru | prompt | Яблоко, лист. Что дальше? | Два шага чередуются. Какое число дальше? |
| logic_repeat | ru | tip | Яблоко и лист чередуются. Дальше будет лист. | Чередуй: прибавь 2, потом один. |
| logic_triple | de | prompt | Wie geht das Muster weiter? | Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts? |
| logic_triple | de | tip | Zwei Sterne, dann ein Mond. Jetzt kommt wieder ein Mond. | Nach rechts 2 dazu, nach unten 4 dazu. |
| logic_triple | en | prompt | How does this pattern continue? | A fixed step goes right and another goes down. What is missing at bottom right? |
| logic_triple | en | tip | Two stars, then a moon. The next picture is a moon. | Add 2 going right, add 4 going down. |
| logic_triple | ru | prompt | Как продолжается узор? | Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа? |
| logic_triple | ru | tip | Две звезды, затем Луна. Дальше будет Луна. | Вправо прибавь 2, вниз прибавь 4. |
| logic_odd | de | prompt | Was passt hier nicht dazu? | Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort? |
| logic_odd | de | tip | Apfel, Blatt und Blume wachsen. Ein Ball wächst nicht. | Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins. |
| logic_odd | en | prompt | Which does not grow like these plants? | Picture and number have separate rules. Which pair continues both? |
| logic_odd | en | tip | Apples, leaves and flowers grow. A ball does not grow. | The three pictures repeat. The numbers alternate adding two and adding one. |
| logic_odd | ru | prompt | Что не растёт, как эти растения? | У картинок и чисел свои правила. Какая пара продолжает оба ряда? |
| logic_odd | ru | tip | Яблоки, листья и цветы растут. Мяч не растёт. | Три картинки повторяются. У чисел чередуются прибавления двух и одного. |
| logic_shadow | de | prompt | Welcher Gegenstand passt zum Schatten? | Katze steht vor Frosch. Vogel steht vor Katze. Wer steht ganz vorn? |
| logic_shadow | de | tip | Vergleiche die Umrisse. Der Schatten zeigt einen Baum. | Von vorn nach hinten: Vogel, Katze, Frosch. |
| logic_shadow | en | prompt | What matches the shadow? | The cat is before the frog. The bird is before the cat. Who is first? |
| logic_shadow | en | tip | Compare the outlines. The shadow shows a tree. | From first to last: bird, cat, frog. |
| logic_shadow | ru | prompt | Что подходит к тени? | кошка раньше, чем лягушка. птица раньше, чем кошка. Кто самый первый? |
| logic_shadow | ru | tip | Сравни контуры. Это тень дерева. | От первого к последнему: птица, кошка, лягушка. |
| logic_size | de | prompt | Welcher Baum ist am größten? | Zwei Schritte wechseln sich ab. Welche Zahl folgt? |
| logic_size | de | tip | Der höchste Baum ist gesucht. Tippe ihn an. | Abwechselnd 2 dazu, dann eins dazu. |
| logic_size | en | prompt | Which tree is the tallest? | Two steps alternate. Which number follows? |
| logic_size | en | tip | Choose the tallest tree. | Alternate adding 2, then adding one. |
| logic_size | ru | prompt | Какое дерево самое высокое? | Два шага чередуются. Какое число дальше? |
| logic_size | ru | tip | Выбери самое высокое дерево. | Чередуй: прибавь 2, потом один. |
| logic_double | de | prompt | Was kommt in die Lücke? | Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts? |
| logic_double | de | tip | Eine Sonne und zwei Monde. Dann beginnt das Muster von vorn. | Nach rechts 2 dazu, nach unten 4 dazu. |
| logic_double | en | prompt | What comes in the gap? | A fixed step goes right and another goes down. What is missing at bottom right? |
| logic_double | en | tip | One sun, then two moons. The pattern repeats. | Add 2 going right, add 4 going down. |
| logic_double | ru | prompt | Что поставить в пропуск? | Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа? |
| logic_double | ru | tip | Одно Солнце, затем две Луны. Узор повторяется. | Вправо прибавь 2, вниз прибавь 4. |
| logic_shape | de | prompt | Welcher Gegenstand passt zum Schatten? | Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort? |
| logic_shape | de | tip | Achte auf den eckigen Kopf und die beiden Arme. | Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins. |
| logic_shape | en | prompt | What matches the shadow? | Picture and number have separate rules. Which pair continues both? |
| logic_shape | en | tip | Look for the square head and two arms of the robot. | The three pictures repeat. The numbers alternate adding two and adding one. |
| logic_shape | ru | prompt | Что подходит к тени? | У картинок и чисел свои правила. Какая пара продолжает оба ряда? |
| logic_shape | ru | tip | Найди квадратную голову и две руки робота. | Три картинки повторяются. У чисел чередуются прибавления двух и одного. |
| logic_rule | de | prompt | Was gehört nicht zu den Himmelskörpern? | Frosch steht vor Vogel. Maus steht vor Frosch. Wer steht ganz hinten? |
| logic_rule | de | tip | Sonne, Mond und Sterne stehen am Himmel. Eine Blume wächst am Boden. | Von vorn nach hinten: Maus, Frosch, Vogel. |
| logic_rule | en | prompt | Which does not belong with the objects in the sky? | The frog is before the bird. The mouse is before the frog. Who is last? |
| logic_rule | en | tip | The sun, moon and stars are in the sky. A flower grows on the ground. | From first to last: mouse, frog, bird. |
| logic_rule | ru | prompt | Что лишнее среди небесных тел? | лягушка раньше, чем птица. мышь раньше, чем лягушка. Кто самый последний? |
| logic_rule | ru | tip | Солнце, Луна и звёзды находятся в небе. Цветок растёт на земле. | От первого к последнему: мышь, лягушка, птица. |
| math_09 | de | prompt | Wie viele Bienen siehst du? | Zu 17 kommen 6, dann gehen 2. Wie viele bleiben? |
| math_09 | de | tip | Tippe jedes Bild einmal an und zähle mit. | 17 plus 6 sind 23. Dann 2 weg. |
| math_09 | en | prompt | How many bees can you see? | 6 join 17, then 2 leave. How many remain? |
| math_09 | en | tip | Tap each picture once and count. | 17 plus 6 is 23. Then take away 2. |
| math_09 | ru | prompt | Сколько пчёл ты видишь? | Было 17. Добавили 6, убрали 2. Сколько осталось? |
| math_09 | ru | tip | Коснись каждой картинки один раз и посчитай. | 17 плюс 6 — это 23. Потом убери 2. |
| math_10 | de | prompt | Wie viele Fische siehst du? | Ergänze 18 bis 24. Welche Zahl fehlt? |
| math_10 | de | tip | Tippe jedes Bild einmal an und zähle mit. | Gehe zuerst zum nächsten Zehner, dann bis 24. |
| math_10 | en | prompt | How many fish can you see? | Complete 18 up to 24. Which number is missing? |
| math_10 | en | tip | Tap each picture once and count. | Go to the next ten first, then up to 24. |
| math_10 | ru | prompt | Сколько рыб ты видишь? | Было 18, стало 24. Сколько добавили? |
| math_10 | ru | tip | Коснись каждой картинки один раз и посчитай. | Сначала дойди до следующего десятка, потом до 24. |
| math_11 | de | prompt | Wie viele Blumen siehst du? | 2 Körbe mit je 5 Äpfeln. Du verschenkst 3. Wie viele bleiben? |
| math_11 | de | tip | Tippe jedes Bild einmal an und zähle mit. | Alle Körbe zusammen: 10. Nun 3 abziehen. |
| math_11 | en | prompt | How many flowers can you see? | 2 baskets have 5 apples each. You give away 3. How many remain? |
| math_11 | en | tip | Tap each picture once and count. | All baskets together: 10. Now subtract 3. |
| math_11 | ru | prompt | Сколько цветов ты видишь? | Корзин: 2. В каждой яблок: 5. Отдали 3. Сколько осталось? |
| math_11 | ru | tip | Коснись каждой картинки один раз и посчитай. | Во всех корзинах вместе 10. Теперь вычти 3. |
| math_12 | de | prompt | Wie viele Blätter siehst du? | Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg? |
| math_12 | de | tip | Tippe jedes Bild einmal an und zähle mit. | Nimm die 4 zuerst wieder weg. Vergleiche 13 mit 19. |
| math_12 | en | prompt | How many leaves can you see? | A number is taken away, then some is added. How much was taken away? |
| math_12 | en | tip | Tap each picture once and count. | Undo the added 4 first. Compare 13 with 19. |
| math_12 | ru | prompt | Сколько листьев ты видишь? | Сначала число убрали, потом немного добавили. Сколько убрали? |
| math_12 | ru | tip | Коснись каждой картинки один раз и посчитай. | Сначала отмени прибавление 4. Сравни 13 и 19. |
| math_13 | de | prompt | Wie viele Sterne siehst du? | Zu 11 kommen 7, dann gehen 2. Wie viele bleiben? |
| math_13 | de | tip | Tippe jedes Bild einmal an und zähle mit. | 11 plus 7 sind 18. Dann 2 weg. |
| math_13 | en | prompt | How many stars can you see? | 7 join 11, then 2 leave. How many remain? |
| math_13 | en | tip | Tap each picture once and count. | 11 plus 7 is 18. Then take away 2. |
| math_13 | ru | prompt | Сколько звёзд ты видишь? | Было 11. Добавили 7, убрали 2. Сколько осталось? |
| math_13 | ru | tip | Коснись каждой картинки один раз и посчитай. | 11 плюс 7 — это 18. Потом убери 2. |
| math_14 | de | prompt | Wie viele Äpfel siehst du? | Ergänze 12 bis 19. Welche Zahl fehlt? |
| math_14 | de | tip | Tippe jedes Bild einmal an und zähle mit. | Gehe zuerst zum nächsten Zehner, dann bis 19. |
| math_14 | en | prompt | How many apples can you see? | Complete 12 up to 19. Which number is missing? |
| math_14 | en | tip | Tap each picture once and count. | Go to the next ten first, then up to 19. |
| math_14 | ru | prompt | Сколько яблок ты видишь? | Было 12, стало 19. Сколько добавили? |
| math_14 | ru | tip | Коснись каждой картинки один раз и посчитай. | Сначала дойди до следующего десятка, потом до 19. |
| math_15 | de | prompt | 2 und 2. Wie viele zusammen? | 2 Körbe mit je 6 Äpfeln. Du verschenkst 1. Wie viele bleiben? |
| math_15 | de | tip | Zähle zuerst links und dann rechts weiter. | Alle Körbe zusammen: 12. Nun 1 abziehen. |
| math_15 | en | prompt | 2 and 2. How many altogether? | 2 baskets have 6 apples each. You give away 1. How many remain? |
| math_15 | en | tip | Count the left group, then keep counting the right group. | All baskets together: 12. Now subtract 1. |
| math_15 | ru | prompt | 2 и 2. Сколько всего? | Корзин: 2. В каждой яблок: 6. Отдали 1. Сколько осталось? |
| math_15 | ru | tip | Сначала посчитай слева, затем продолжи считать справа. | Во всех корзинах вместе 12. Теперь вычти 1. |
| math_16 | de | prompt | 4 und 3. Wie viele zusammen? | Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg? |
| math_16 | de | tip | Zähle zuerst links und dann rechts weiter. | Nimm die 4 zuerst wieder weg. Vergleiche 20 mit 23. |
| math_16 | en | prompt | 4 and 3. How many altogether? | A number is taken away, then some is added. How much was taken away? |
| math_16 | en | tip | Count the left group, then keep counting the right group. | Undo the added 4 first. Compare 20 with 23. |
| math_16 | ru | prompt | 4 и 3. Сколько всего? | Сначала число убрали, потом немного добавили. Сколько убрали? |
| math_16 | ru | tip | Сначала посчитай слева, затем продолжи считать справа. | Сначала отмени прибавление 4. Сравни 20 и 23. |
| math_17 | de | prompt | 5 und 4. Wie viele zusammen? | Zu 15 kommen 8, dann gehen 2. Wie viele bleiben? |
| math_17 | de | tip | Zähle zuerst links und dann rechts weiter. | 15 plus 8 sind 23. Dann 2 weg. |
| math_17 | en | prompt | 5 and 4. How many altogether? | 8 join 15, then 2 leave. How many remain? |
| math_17 | en | tip | Count the left group, then keep counting the right group. | 15 plus 8 is 23. Then take away 2. |
| math_17 | ru | prompt | 5 и 4. Сколько всего? | Было 15. Добавили 8, убрали 2. Сколько осталось? |
| math_17 | ru | tip | Сначала посчитай слева, затем продолжи считать справа. | 15 плюс 8 — это 23. Потом убери 2. |
| math_18 | de | prompt | 6 und 2. Wie viele zusammen? | Ergänze 16 bis 24. Welche Zahl fehlt? |
| math_18 | de | tip | Zähle zuerst links und dann rechts weiter. | Gehe zuerst zum nächsten Zehner, dann bis 24. |
| math_18 | en | prompt | 6 and 2. How many altogether? | Complete 16 up to 24. Which number is missing? |
| math_18 | en | tip | Count the left group, then keep counting the right group. | Go to the next ten first, then up to 24. |
| math_18 | ru | prompt | 6 и 2. Сколько всего? | Было 16, стало 24. Сколько добавили? |
| math_18 | ru | tip | Сначала посчитай слева, затем продолжи считать справа. | Сначала дойди до следующего десятка, потом до 24. |
| math_19 | de | prompt | 8 und 3. Wie viele zusammen? | 2 Körbe mit je 7 Äpfeln. Du verschenkst 2. Wie viele bleiben? |
| math_19 | de | tip | Zähle zuerst links und dann rechts weiter. | Alle Körbe zusammen: 14. Nun 2 abziehen. |
| math_19 | en | prompt | 8 and 3. How many altogether? | 2 baskets have 7 apples each. You give away 2. How many remain? |
| math_19 | en | tip | Count the left group, then keep counting the right group. | All baskets together: 14. Now subtract 2. |
| math_19 | ru | prompt | 8 и 3. Сколько всего? | Корзин: 2. В каждой яблок: 7. Отдали 2. Сколько осталось? |
| math_19 | ru | tip | Сначала посчитай слева, затем продолжи считать справа. | Во всех корзинах вместе 14. Теперь вычти 2. |
| math_20 | de | prompt | 10 und 5. Wie viele zusammen? | Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg? |
| math_20 | de | tip | Zähle zuerst links und dann rechts weiter. | Nimm die 4 zuerst wieder weg. Vergleiche 11 mit 18. |
| math_20 | en | prompt | 10 and 5. How many altogether? | A number is taken away, then some is added. How much was taken away? |
| math_20 | en | tip | Count the left group, then keep counting the right group. | Undo the added 4 first. Compare 11 with 18. |
| math_20 | ru | prompt | 10 и 5. Сколько всего? | Сначала число убрали, потом немного добавили. Сколько убрали? |
| math_20 | ru | tip | Сначала посчитай слева, затем продолжи считать справа. | Сначала отмени прибавление 4. Сравни 11 и 18. |
| math_21 | de | prompt | 9 und 6. Wie viele zusammen? | Zu 9 kommen 9, dann gehen 2. Wie viele bleiben? |
| math_21 | de | tip | Zähle zuerst links und dann rechts weiter. | 9 plus 9 sind 18. Dann 2 weg. |
| math_21 | en | prompt | 9 and 6. How many altogether? | 9 join 9, then 2 leave. How many remain? |
| math_21 | en | tip | Count the left group, then keep counting the right group. | 9 plus 9 is 18. Then take away 2. |
| math_21 | ru | prompt | 9 и 6. Сколько всего? | Было 9. Добавили 9, убрали 2. Сколько осталось? |
| math_21 | ru | tip | Сначала посчитай слева, затем продолжи считать справа. | 9 плюс 9 — это 18. Потом убери 2. |
| math_22 | de | prompt | 12 und 7. Wie viele zusammen? | Ergänze 10 bis 19. Welche Zahl fehlt? |
| math_22 | de | tip | Zähle zuerst links und dann rechts weiter. | Gehe zuerst zum nächsten Zehner, dann bis 19. |
| math_22 | en | prompt | 12 and 7. How many altogether? | Complete 10 up to 19. Which number is missing? |
| math_22 | en | tip | Count the left group, then keep counting the right group. | Go to the next ten first, then up to 19. |
| math_22 | ru | prompt | 12 и 7. Сколько всего? | Было 10, стало 19. Сколько добавили? |
| math_22 | ru | tip | Сначала посчитай слева, затем продолжи считать справа. | Сначала дойди до следующего десятка, потом до 19. |
| math_23 | de | prompt | 5 sind da. 2 gehen weg. Wie viele bleiben? | 3 Körbe mit je 3 Äpfeln. Du verschenkst 3. Wie viele bleiben? |
| math_23 | de | tip | Zähle die Bilder ohne Kreuz. | Alle Körbe zusammen: 9. Nun 3 abziehen. |
| math_23 | en | prompt | There are 5. Take away 2. How many remain? | 3 baskets have 3 apples each. You give away 3. How many remain? |
| math_23 | en | tip | Count only the pictures without a cross. | All baskets together: 9. Now subtract 3. |
| math_23 | ru | prompt | Было 5. Убрали 2. Сколько осталось? | Корзин: 3. В каждой яблок: 3. Отдали 3. Сколько осталось? |
| math_23 | ru | tip | Считай только картинки без крестика. | Во всех корзинах вместе 9. Теперь вычти 3. |
| math_24 | de | prompt | 8 sind da. 4 gehen weg. Wie viele bleiben? | Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg? |
| math_24 | de | tip | Zähle die Bilder ohne Kreuz. | Nimm die 5 zuerst wieder weg. Vergleiche 18 mit 22. |
| math_24 | en | prompt | There are 8. Take away 4. How many remain? | A number is taken away, then some is added. How much was taken away? |
| math_24 | en | tip | Count only the pictures without a cross. | Undo the added 5 first. Compare 18 with 22. |
| math_24 | ru | prompt | Было 8. Убрали 4. Сколько осталось? | Сначала число убрали, потом немного добавили. Сколько убрали? |
| math_24 | ru | tip | Считай только картинки без крестика. | Сначала отмени прибавление 5. Сравни 18 и 22. |
| math_25 | de | prompt | 9 sind da. 2 gehen weg. Wie viele bleiben? | Zu 13 kommen 10, dann gehen 2. Wie viele bleiben? |
| math_25 | de | tip | Zähle die Bilder ohne Kreuz. | 13 plus 10 sind 23. Dann 2 weg. |
| math_25 | en | prompt | There are 9. Take away 2. How many remain? | 10 join 13, then 2 leave. How many remain? |
| math_25 | en | tip | Count only the pictures without a cross. | 13 plus 10 is 23. Then take away 2. |
| math_25 | ru | prompt | Было 9. Убрали 2. Сколько осталось? | Было 13. Добавили 10, убрали 2. Сколько осталось? |
| math_25 | ru | tip | Считай только картинки без крестика. | 13 плюс 10 — это 23. Потом убери 2. |
| math_26 | de | prompt | 10 sind da. 1 gehen weg. Wie viele bleiben? | Ergänze 14 bis 24. Welche Zahl fehlt? |
| math_26 | de | tip | Zähle die Bilder ohne Kreuz. | Gehe zuerst zum nächsten Zehner, dann bis 24. |
| math_26 | en | prompt | There are 10. Take away 1. How many remain? | Complete 14 up to 24. Which number is missing? |
| math_26 | en | tip | Count only the pictures without a cross. | Go to the next ten first, then up to 24. |
| math_26 | ru | prompt | Было 10. Убрали 1. Сколько осталось? | Было 14, стало 24. Сколько добавили? |
| math_26 | ru | tip | Считай только картинки без крестика. | Сначала дойди до следующего десятка, потом до 24. |
| math_27 | de | prompt | 12 sind da. 3 gehen weg. Wie viele bleiben? | 3 Körbe mit je 4 Äpfeln. Du verschenkst 1. Wie viele bleiben? |
| math_27 | de | tip | Zähle die Bilder ohne Kreuz. | Alle Körbe zusammen: 12. Nun 1 abziehen. |
| math_27 | en | prompt | There are 12. Take away 3. How many remain? | 3 baskets have 4 apples each. You give away 1. How many remain? |
| math_27 | en | tip | Count only the pictures without a cross. | All baskets together: 12. Now subtract 1. |
| math_27 | ru | prompt | Было 12. Убрали 3. Сколько осталось? | Корзин: 3. В каждой яблок: 4. Отдали 1. Сколько осталось? |
| math_27 | ru | tip | Считай только картинки без крестика. | Во всех корзинах вместе 12. Теперь вычти 1. |
| math_28 | de | prompt | 14 sind da. 4 gehen weg. Wie viele bleiben? | Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg? |
| math_28 | de | tip | Zähle die Bilder ohne Kreuz. | Nimm die 5 zuerst wieder weg. Vergleiche 9 mit 17. |
| math_28 | en | prompt | There are 14. Take away 4. How many remain? | A number is taken away, then some is added. How much was taken away? |
| math_28 | en | tip | Count only the pictures without a cross. | Undo the added 5 first. Compare 9 with 17. |
| math_28 | ru | prompt | Было 14. Убрали 4. Сколько осталось? | Сначала число убрали, потом немного добавили. Сколько убрали? |
| math_28 | ru | tip | Считай только картинки без крестика. | Сначала отмени прибавление 5. Сравни 9 и 17. |
| math_29 | de | prompt | 16 sind da. 6 gehen weg. Wie viele bleiben? | Zu 17 kommen 11, dann gehen 2. Wie viele bleiben? |
| math_29 | de | tip | Zähle die Bilder ohne Kreuz. | 17 plus 11 sind 28. Dann 2 weg. |
| math_29 | en | prompt | There are 16. Take away 6. How many remain? | 11 join 17, then 2 leave. How many remain? |
| math_29 | en | tip | Count only the pictures without a cross. | 17 plus 11 is 28. Then take away 2. |
| math_29 | ru | prompt | Было 16. Убрали 6. Сколько осталось? | Было 17. Добавили 11, убрали 2. Сколько осталось? |
| math_29 | ru | tip | Считай только картинки без крестика. | 17 плюс 11 — это 28. Потом убери 2. |
| math_30 | de | prompt | 20 sind da. 5 gehen weg. Wie viele bleiben? | Ergänze 18 bis 29. Welche Zahl fehlt? |
| math_30 | de | tip | Zähle die Bilder ohne Kreuz. | Gehe zuerst zum nächsten Zehner, dann bis 29. |
| math_30 | en | prompt | There are 20. Take away 5. How many remain? | Complete 18 up to 29. Which number is missing? |
| math_30 | en | tip | Count only the pictures without a cross. | Go to the next ten first, then up to 29. |
| math_30 | ru | prompt | Было 20. Убрали 5. Сколько осталось? | Было 18, стало 29. Сколько добавили? |
| math_30 | ru | tip | Считай только картинки без крестика. | Сначала дойди до следующего десятка, потом до 29. |
| math_31 | de | prompt | 2 sind da. Wie viele fehlen bis 5? | 3 Körbe mit je 5 Äpfeln. Du verschenkst 2. Wie viele bleiben? |
| math_31 | de | tip | Zähle die leeren Sternplätze. | Alle Körbe zusammen: 15. Nun 2 abziehen. |
| math_31 | en | prompt | There are 2. How many more make 5? | 3 baskets have 5 apples each. You give away 2. How many remain? |
| math_31 | en | tip | Count the empty star spaces. | All baskets together: 15. Now subtract 2. |
| math_31 | ru | prompt | Есть 2. Сколько не хватает до 5? | Корзин: 3. В каждой яблок: 5. Отдали 2. Сколько осталось? |
| math_31 | ru | tip | Посчитай пустые места для звёзд. | Во всех корзинах вместе 15. Теперь вычти 2. |
| math_32 | de | prompt | 6 sind da. Wie viele fehlen bis 10? | Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg? |
| math_32 | de | tip | Zähle die leeren Sternplätze. | Nimm die 6 zuerst wieder weg. Vergleiche 16 mit 21. |
| math_32 | en | prompt | There are 6. How many more make 10? | A number is taken away, then some is added. How much was taken away? |
| math_32 | en | tip | Count the empty star spaces. | Undo the added 6 first. Compare 16 with 21. |
| math_32 | ru | prompt | Есть 6. Сколько не хватает до 10? | Сначала число убрали, потом немного добавили. Сколько убрали? |
| math_32 | ru | tip | Посчитай пустые места для звёзд. | Сначала отмени прибавление 6. Сравни 16 и 21. |
| math_33 | de | prompt | 7 sind da. Wie viele fehlen bis 10? | Zu 11 kommen 12, dann gehen 2. Wie viele bleiben? |
| math_33 | de | tip | Zähle die leeren Sternplätze. | 11 plus 12 sind 23. Dann 2 weg. |
| math_33 | en | prompt | There are 7. How many more make 10? | 12 join 11, then 2 leave. How many remain? |
| math_33 | en | tip | Count the empty star spaces. | 11 plus 12 is 23. Then take away 2. |
| math_33 | ru | prompt | Есть 7. Сколько не хватает до 10? | Было 11. Добавили 12, убрали 2. Сколько осталось? |
| math_33 | ru | tip | Посчитай пустые места для звёзд. | 11 плюс 12 — это 23. Потом убери 2. |
| math_34 | de | prompt | 8 sind da. Wie viele fehlen bis 12? | Ergänze 12 bis 24. Welche Zahl fehlt? |
| math_34 | de | tip | Zähle die leeren Sternplätze. | Gehe zuerst zum nächsten Zehner, dann bis 24. |
| math_34 | en | prompt | There are 8. How many more make 12? | Complete 12 up to 24. Which number is missing? |
| math_34 | en | tip | Count the empty star spaces. | Go to the next ten first, then up to 24. |
| math_34 | ru | prompt | Есть 8. Сколько не хватает до 12? | Было 12, стало 24. Сколько добавили? |
| math_34 | ru | tip | Посчитай пустые места для звёзд. | Сначала дойди до следующего десятка, потом до 24. |
| math_35 | de | prompt | 10 sind da. Wie viele fehlen bis 15? | 3 Körbe mit je 6 Äpfeln. Du verschenkst 3. Wie viele bleiben? |
| math_35 | de | tip | Zähle die leeren Sternplätze. | Alle Körbe zusammen: 18. Nun 3 abziehen. |
| math_35 | en | prompt | There are 10. How many more make 15? | 3 baskets have 6 apples each. You give away 3. How many remain? |
| math_35 | en | tip | Count the empty star spaces. | All baskets together: 18. Now subtract 3. |
| math_35 | ru | prompt | Есть 10. Сколько не хватает до 15? | Корзин: 3. В каждой яблок: 6. Отдали 3. Сколько осталось? |
| math_35 | ru | tip | Посчитай пустые места для звёзд. | Во всех корзинах вместе 18. Теперь вычти 3. |
| math_36 | de | prompt | 14 sind da. Wie viele fehlen bis 20? | Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg? |
| math_36 | de | tip | Zähle die leeren Sternplätze. | Nimm die 6 zuerst wieder weg. Vergleiche 23 mit 25. |
| math_36 | en | prompt | There are 14. How many more make 20? | A number is taken away, then some is added. How much was taken away? |
| math_36 | en | tip | Count the empty star spaces. | Undo the added 6 first. Compare 23 with 25. |
| math_36 | ru | prompt | Есть 14. Сколько не хватает до 20? | Сначала число убрали, потом немного добавили. Сколько убрали? |
| math_36 | ru | tip | Посчитай пустые места для звёзд. | Сначала отмени прибавление 6. Сравни 23 и 25. |
| math_37 | de | prompt | Wo sind mehr? | Zu 15 kommen 13, dann gehen 2. Wie viele bleiben? |
| math_37 | de | tip | Zähle beide Mengen. Tippe die größere an. | 15 plus 13 sind 28. Dann 2 weg. |
| math_37 | en | prompt | Which group has more? | 13 join 15, then 2 leave. How many remain? |
| math_37 | en | tip | Count both groups and tap the larger one. | 15 plus 13 is 28. Then take away 2. |
| math_37 | ru | prompt | Где больше? | Было 15. Добавили 13, убрали 2. Сколько осталось? |
| math_37 | ru | tip | Посчитай обе группы. Коснись той, где больше. | 15 плюс 13 — это 28. Потом убери 2. |
| math_38 | de | prompt | Wo sind mehr? | Ergänze 16 bis 29. Welche Zahl fehlt? |
| math_38 | de | tip | Zähle beide Mengen. Tippe die größere an. | Gehe zuerst zum nächsten Zehner, dann bis 29. |
| math_38 | en | prompt | Which group has more? | Complete 16 up to 29. Which number is missing? |
| math_38 | en | tip | Count both groups and tap the larger one. | Go to the next ten first, then up to 29. |
| math_38 | ru | prompt | Где больше? | Было 16, стало 29. Сколько добавили? |
| math_38 | ru | tip | Посчитай обе группы. Коснись той, где больше. | Сначала дойди до следующего десятка, потом до 29. |
| math_39 | de | prompt | Wo sind mehr? | 3 Körbe mit je 7 Äpfeln. Du verschenkst 1. Wie viele bleiben? |
| math_39 | de | tip | Zähle beide Mengen. Tippe die größere an. | Alle Körbe zusammen: 21. Nun 1 abziehen. |
| math_39 | en | prompt | Which group has more? | 3 baskets have 7 apples each. You give away 1. How many remain? |
| math_39 | en | tip | Count both groups and tap the larger one. | All baskets together: 21. Now subtract 1. |
| math_39 | ru | prompt | Где больше? | Корзин: 3. В каждой яблок: 7. Отдали 1. Сколько осталось? |
| math_39 | ru | tip | Посчитай обе группы. Коснись той, где больше. | Во всех корзинах вместе 21. Теперь вычти 1. |
| math_40 | de | prompt | Wo sind mehr? | Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg? |
| math_40 | de | tip | Zähle beide Mengen. Tippe die größere an. | Nimm die 6 zuerst wieder weg. Vergleiche 14 mit 20. |
| math_40 | en | prompt | Which group has more? | A number is taken away, then some is added. How much was taken away? |
| math_40 | en | tip | Count both groups and tap the larger one. | Undo the added 6 first. Compare 14 with 20. |
| math_40 | ru | prompt | Где больше? | Сначала число убрали, потом немного добавили. Сколько убрали? |
| math_40 | ru | tip | Посчитай обе группы. Коснись той, где больше. | Сначала отмени прибавление 6. Сравни 14 и 20. |
| german_09 | de | prompt | Biene. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Bienenkorb. Welche beiden Buchstaben fehlen? |
| german_09 | de | tip | Biene beginnt mit B. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen N. R. |
| german_09 | en | prompt | German word: Biene. Which letter does it start with? | Beehive. Which two letters are missing? |
| german_09 | en | tip | Biene starts with the letter B. Choose that letter. | Read from left to right. The gaps need E. I. |
| german_09 | ru | prompt | Немецкое слово: Biene. С какой буквы его пишут? | Улей. Какие две буквы пропущены? |
| german_09 | ru | tip | Biene начинается с буквы B. Выбери эту букву. | Читай слева направо. В пропусках: У. Е. |
| german_10 | de | prompt | Frosch. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Froschteich. Welche beiden Buchstaben fehlen? |
| german_10 | de | tip | Frosch beginnt mit F. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen S. C. |
| german_10 | en | prompt | German word: Frosch. Which letter does it start with? | Tadpole. Which two letters are missing? |
| german_10 | en | tip | Frosch starts with the letter F. Choose that letter. | Read from left to right. The gaps need D. L. |
| german_10 | ru | prompt | Немецкое слово: Frosch. С какой буквы его пишут? | Головастик. Какие две буквы пропущены? |
| german_10 | ru | tip | Frosch начинается с буквы F. Выбери эту букву. | Читай слева направо. В пропусках: В. К. |
| german_11 | de | prompt | Katze. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Katzenpfote. Welche beiden Buchstaben fehlen? |
| german_11 | de | tip | Katze beginnt mit K. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen E. E. |
| german_11 | en | prompt | German word: Katze. Which letter does it start with? | Kitten. Which two letters are missing? |
| german_11 | en | tip | Katze starts with the letter K. Choose that letter. | Read from left to right. The gaps need I. E. |
| german_11 | ru | prompt | Немецкое слово: Katze. С какой буквы его пишут? | Котёнок. Какие две буквы пропущены? |
| german_11 | ru | tip | Katze начинается с буквы K. Выбери эту букву. | Читай слева направо. В пропусках: Ё. К. |
| german_12 | de | prompt | Nest. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Vogelnest. Welche beiden Buchstaben fehlen? |
| german_12 | de | tip | Nest beginnt mit N. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen G. E. |
| german_12 | en | prompt | German word: Nest. Which letter does it start with? | Nestling. Which two letters are missing? |
| german_12 | en | tip | Nest starts with the letter N. Choose that letter. | Read from left to right. The gaps need T. G. |
| german_12 | ru | prompt | Немецкое слово: Nest. С какой буквы его пишут? | Птенец. Какие две буквы пропущены? |
| german_12 | ru | tip | Nest начинается с буквы N. Выбери эту букву. | Читай слева направо. В пропусках: Е. Ц. |
| german_13 | de | prompt | Wurm. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Regenwurm. Welche beiden Buchstaben fehlen? |
| german_13 | de | tip | Wurm beginnt mit W. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen E. R. |
| german_13 | en | prompt | German word: Wurm. Which letter does it start with? | Earthworm. Which two letters are missing? |
| german_13 | en | tip | Wurm starts with the letter W. Choose that letter. | Read from left to right. The gaps need T. R. |
| german_13 | ru | prompt | Немецкое слово: Wurm. С какой буквы его пишут? | Червячок. Какие две буквы пропущены? |
| german_13 | ru | tip | Wurm начинается с буквы W. Выбери эту букву. | Читай слева направо. В пропусках: Ч. Я. |
| german_14 | de | prompt | Wasser. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Wassertropfen. Welche beiden Buchstaben fehlen? |
| german_14 | de | tip | Wasser beginnt mit W. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen W. T. |
| german_14 | en | prompt | German word: Wasser. Which letter does it start with? | Raindrop. Which two letters are missing? |
| german_14 | en | tip | Wasser starts with the letter W. Choose that letter. | Read from left to right. The gaps need A. R. |
| german_14 | ru | prompt | Немецкое слово: Wasser. С какой буквы его пишут? | Капелька. Какие две буквы пропущены? |
| german_14 | ru | tip | Wasser начинается с буквы W. Выбери эту букву. | Читай слева направо. В пропусках: А. Ь. |
| german_15 | de | prompt | Salz. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Salzkristall. Welche beiden Buchstaben fehlen? |
| german_15 | de | tip | Salz beginnt mit S. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen L. T. |
| german_15 | en | prompt | German word: Salz. Which letter does it start with? | Crystal. Which two letters are missing? |
| german_15 | en | tip | Salz starts with the letter S. Choose that letter. | Read from left to right. The gaps need C. S. |
| german_15 | ru | prompt | Немецкое слово: Salz. С какой буквы его пишут? | Кристалл. Какие две буквы пропущены? |
| german_15 | ru | tip | Salz начинается с буквы S. Выбери эту букву. | Читай слева направо. В пропусках: И. Л. |
| german_16 | de | prompt | Sand. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Sandkasten. Welche beiden Buchstaben fehlen? |
| german_16 | de | tip | Sand beginnt mit S. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen S. A. |
| german_16 | en | prompt | German word: Sand. Which letter does it start with? | Sandcastle. Which two letters are missing? |
| german_16 | en | tip | Sand starts with the letter S. Choose that letter. | Read from left to right. The gaps need S. A. |
| german_16 | ru | prompt | Немецкое слово: Sand. С какой буквы его пишут? | Песочница. Какие две буквы пропущены? |
| german_16 | ru | tip | Sand начинается с буквы S. Выбери эту букву. | Читай слева направо. В пропусках: Е. И. |
| german_17 | de | prompt | Holz. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Holzlöffel. Welche beiden Buchstaben fehlen? |
| german_17 | de | tip | Holz beginnt mit H. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen O. F. |
| german_17 | en | prompt | German word: Holz. Which letter does it start with? | Woodland. Which two letters are missing? |
| german_17 | en | tip | Holz starts with the letter H. Choose that letter. | Read from left to right. The gaps need W. L. |
| german_17 | ru | prompt | Немецкое слово: Holz. С какой буквы его пишут? | Древесина. Какие две буквы пропущены? |
| german_17 | ru | tip | Holz начинается с буквы H. Выбери эту букву. | Читай слева направо. В пропусках: Е. Н. |
| german_18 | de | prompt | Nase. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Nasenspitze. Welche beiden Buchstaben fehlen? |
| german_18 | de | tip | Nase beginnt mit N. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen N. P. |
| german_18 | en | prompt | German word: Nase. Which letter does it start with? | Nostril. Which two letters are missing? |
| german_18 | en | tip | Nase starts with the letter N. Choose that letter. | Read from left to right. The gaps need T. L. |
| german_18 | ru | prompt | Немецкое слово: Nase. С какой буквы его пишут? | Носик. Какие две буквы пропущены? |
| german_18 | ru | tip | Nase начинается с буквы N. Выбери эту букву. | Читай слева направо. В пропусках: С. К. |
| german_19 | de | prompt | Hand. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Handschuh. Welche beiden Buchstaben fehlen? |
| german_19 | de | tip | Hand beginnt mit H. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen H. S. |
| german_19 | en | prompt | German word: Hand. Which letter does it start with? | Mitten. Which two letters are missing? |
| german_19 | en | tip | Hand starts with the letter H. Choose that letter. | Read from left to right. The gaps need M. T. |
| german_19 | ru | prompt | Немецкое слово: Hand. С какой буквы его пишут? | Варежка. Какие две буквы пропущены? |
| german_19 | ru | tip | Hand начинается с буквы H. Выбери эту букву. | Читай слева направо. В пропусках: В. Ж. |
| german_20 | de | prompt | Herz. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang? | Herzschlag. Welche beiden Buchstaben fehlen? |
| german_20 | de | tip | Herz beginnt mit H. Suche diesen Buchstaben. | Lies von links nach rechts. Die Lücken brauchen S. G. |
| german_20 | en | prompt | German word: Herz. Which letter does it start with? | Heartbeat. Which two letters are missing? |
| german_20 | en | tip | Herz starts with the letter H. Choose that letter. | Read from left to right. The gaps need E. B. |
| german_20 | ru | prompt | Немецкое слово: Herz. С какой буквы его пишут? | Сердечко. Какие две буквы пропущены? |
| german_20 | ru | tip | Herz начинается с буквы H. Выбери эту букву. | Читай слева направо. В пропусках: Д. О. |
| german_21 | de | prompt | Schmetterling. Wie viele Silben hörst du? | Schmetterling. Welche beiden Buchstaben fehlen? |
| german_21 | de | tip | Sprich und klatsche: Schmet. Ter. Ling. Das sind 3 Silben. | Lies von links nach rechts. Die Lücken brauchen S. E. |
| german_21 | en | prompt | German word: Schmetterling. How many syllables can you hear? | Butterfly. Which two letters are missing? |
| german_21 | en | tip | Say and clap: Schmet. Ter. Ling. That is 3 syllables. | Read from left to right. The gaps need T. F. |
| german_21 | ru | prompt | Немецкое слово: Schmetterling. Сколько слогов ты слышишь? | Бабочка. Какие две буквы пропущены? |
| german_21 | ru | tip | Произнеси и хлопай: Schmet. Ter. Ling. Это 3 слога. | Читай слева направо. В пропусках: Б. А. |
| german_22 | de | prompt | Schildkröte. Wie viele Silben hörst du? | Schildkröte. Welche beiden Buchstaben fehlen? |
| german_22 | de | tip | Sprich und klatsche: Schild. Krö. Te. Das sind 3 Silben. | Lies von links nach rechts. Die Lücken brauchen L. E. |
| german_22 | en | prompt | German word: Schildkröte. How many syllables can you hear? | Tortoise. Which two letters are missing? |
| german_22 | en | tip | Say and clap: Schild. Krö. Te. That is 3 syllables. | Read from left to right. The gaps need O. I. |
| german_22 | ru | prompt | Немецкое слово: Schildkröte. Сколько слогов ты слышишь? | Черепашка. Какие две буквы пропущены? |
| german_22 | ru | tip | Произнеси и хлопай: Schild. Krö. Te. Это 3 слога. | Читай слева направо. В пропусках: Е. К. |
| german_23 | de | prompt | Batterie. Wie viele Silben hörst du? | Taschenlampe. Welche beiden Buchstaben fehlen? |
| german_23 | de | tip | Sprich und klatsche: Bat. Te. Rie. Das sind 3 Silben. | Lies von links nach rechts. Die Lücken brauchen H. P. |
| german_23 | en | prompt | German word: Batterie. How many syllables can you hear? | Flashlight. Which two letters are missing? |
| german_23 | en | tip | Say and clap: Bat. Te. Rie. That is 3 syllables. | Read from left to right. The gaps need A. G. |
| german_23 | ru | prompt | Немецкое слово: Batterie. Сколько слогов ты слышишь? | Фонарик. Какие две буквы пропущены? |
| german_23 | ru | tip | Произнеси и хлопай: Bat. Te. Rie. Это 3 слога. | Читай слева направо. В пропусках: О. Р. |
| german_24 | de | prompt | Papier. Wie viele Silben hörst du? | Papierflieger. Welche beiden Buchstaben fehlen? |
| german_24 | de | tip | Sprich und klatsche: Pa. Pier. Das sind 2 Silben. | Lies von links nach rechts. Die Lücken brauchen I. G. |
| german_24 | en | prompt | German word: Papier. How many syllables can you hear? | Airplane. Which two letters are missing? |
| german_24 | en | tip | Say and clap: Pa. Pier. That is 2 syllables. | Read from left to right. The gaps need P. E. |
| german_24 | ru | prompt | Немецкое слово: Papier. Сколько слогов ты слышишь? | Самолёт. Какие две буквы пропущены? |
| german_24 | ru | tip | Произнеси и хлопай: Pa. Pier. Это 2 слога. | Читай слева направо. В пропусках: М. Ё. |
| german_25 | de | prompt | Seife. Wie viele Silben hörst du? | Seifenblase. Welche beiden Buchstaben fehlen? |
| german_25 | de | tip | Sprich und klatsche: Sei. Fe. Das sind 2 Silben. | Lies von links nach rechts. Die Lücken brauchen I. L. |
| german_25 | en | prompt | German word: Seife. How many syllables can you hear? | Bubble. Which two letters are missing? |
| german_25 | en | tip | Say and clap: Sei. Fe. That is 2 syllables. | Read from left to right. The gaps need B. B. |
| german_25 | ru | prompt | Немецкое слово: Seife. Сколько слогов ты слышишь? | Пузырёк. Какие две буквы пропущены? |
| german_25 | ru | tip | Произнеси и хлопай: Sei. Fe. Это 2 слога. | Читай слева направо. В пропусках: Ы. К. |
| german_26 | de | prompt | Auge. Wie viele Silben hörst du? | Augenbraue. Welche beiden Buchstaben fehlen? |
| german_26 | de | tip | Sprich und klatsche: Au. Ge. Das sind 2 Silben. | Lies von links nach rechts. Die Lücken brauchen A. B. |
| german_26 | en | prompt | German word: Auge. How many syllables can you hear? | Eyebrow. Which two letters are missing? |
| german_26 | en | tip | Say and clap: Au. Ge. That is 2 syllables. | Read from left to right. The gaps need E. R. |
| german_26 | ru | prompt | Немецкое слово: Auge. Сколько слогов ты слышишь? | Брови. Какие две буквы пропущены? |
| german_26 | ru | tip | Произнеси и хлопай: Au. Ge. Это 2 слога. | Читай слева направо. В пропусках: Б. О. |
| german_27 | de | prompt | Gehirn. Wie viele Silben hörst du? | Gedanken. Welche beiden Buchstaben fehlen? |
| german_27 | de | tip | Sprich und klatsche: Ge. Hirn. Das sind 2 Silben. | Lies von links nach rechts. Die Lücken brauchen D. E. |
| german_27 | en | prompt | German word: Gehirn. How many syllables can you hear? | Thought. Which two letters are missing? |
| german_27 | en | tip | Say and clap: Ge. Hirn. That is 2 syllables. | Read from left to right. The gaps need H. H. |
| german_27 | ru | prompt | Немецкое слово: Gehirn. Сколько слогов ты слышишь? | Мысли. Какие две буквы пропущены? |
| german_27 | ru | tip | Произнеси и хлопай: Ge. Hirn. Это 2 слога. | Читай слева направо. В пропусках: Ы. Л. |
| german_28 | de | prompt | Magen. Wie viele Silben hörst du? | Bauchnabel. Welche beiden Buchstaben fehlen? |
| german_28 | de | tip | Sprich und klatsche: Ma. Gen. Das sind 2 Silben. | Lies von links nach rechts. Die Lücken brauchen U. B. |
| german_28 | en | prompt | German word: Magen. How many syllables can you hear? | Bellybutton. Which two letters are missing? |
| german_28 | en | tip | Say and clap: Ma. Gen. That is 2 syllables. | Read from left to right. The gaps need B. N. |
| german_28 | ru | prompt | Немецкое слово: Magen. Сколько слогов ты слышишь? | Пупок. Какие две буквы пропущены? |
| german_28 | ru | tip | Произнеси и хлопай: Ma. Gen. Это 2 слога. | Читай слева направо. В пропусках: П. К. |
| german_29 | de | prompt | Wolke. Wie viele Silben hörst du? | Gewitter. Welche beiden Buchstaben fehlen? |
| german_29 | de | tip | Sprich und klatsche: Wol. Ke. Das sind 2 Silben. | Lies von links nach rechts. Die Lücken brauchen G. T. |
| german_29 | en | prompt | German word: Wolke. How many syllables can you hear? | Thunder. Which two letters are missing? |
| german_29 | en | tip | Say and clap: Wol. Ke. That is 2 syllables. | Read from left to right. The gaps need T. N. |
| german_29 | ru | prompt | Немецкое слово: Wolke. Сколько слогов ты слышишь? | Гроза. Какие две буквы пропущены? |
| german_29 | ru | tip | Произнеси и хлопай: Wol. Ke. Это 2 слога. | Читай слева направо. В пропусках: Г. З. |
| german_30 | de | prompt | Regen. Wie viele Silben hörst du? | Regenbogen. Welche beiden Buchstaben fehlen? |
| german_30 | de | tip | Sprich und klatsche: Re. Gen. Das sind 2 Silben. | Lies von links nach rechts. Die Lücken brauchen N. N. |
| german_30 | en | prompt | German word: Regen. How many syllables can you hear? | Rainbow. Which two letters are missing? |
| german_30 | en | tip | Say and clap: Re. Gen. That is 2 syllables. | Read from left to right. The gaps need A. B. |
| german_30 | ru | prompt | Немецкое слово: Regen. Сколько слогов ты слышишь? | Радуга. Какие две буквы пропущены? |
| german_30 | ru | tip | Произнеси и хлопай: Re. Gen. Это 2 слога. | Читай слева направо. В пропусках: Д. А. |
| german_31 | de | prompt | Insel. Wie viele Silben hörst du? | Schatzinsel. Welche beiden Buchstaben fehlen? |
| german_31 | de | tip | Sprich und klatsche: In. Sel. Das sind 2 Silben. | Lies von links nach rechts. Die Lücken brauchen H. S. |
| german_31 | en | prompt | German word: Insel. How many syllables can you hear? | Treasure. Which two letters are missing? |
| german_31 | en | tip | Say and clap: In. Sel. That is 2 syllables. | Read from left to right. The gaps need E. R. |
| german_31 | ru | prompt | Немецкое слово: Insel. Сколько слогов ты слышишь? | Сокровище. Какие две буквы пропущены? |
| german_31 | ru | tip | Произнеси и хлопай: In. Sel. Это 2 слога. | Читай слева направо. В пропусках: Р. Щ. |
| german_32 | de | prompt | Hammer. Wie viele Silben hörst du? | Werkzeug. Welche beiden Buchstaben fehlen? |
| german_32 | de | tip | Sprich und klatsche: Ham. Mer. Das sind 2 Silben. | Lies von links nach rechts. Die Lücken brauchen K. G. |
| german_32 | en | prompt | German word: Hammer. How many syllables can you hear? | Toolbox. Which two letters are missing? |
| german_32 | en | tip | Say and clap: Ham. Mer. That is 2 syllables. | Read from left to right. The gaps need L. X. |
| german_32 | ru | prompt | Немецкое слово: Hammer. Сколько слогов ты слышишь? | Инструмент. Какие две буквы пропущены? |
| german_32 | ru | tip | Произнеси и хлопай: Ham. Mer. Это 2 слога. | Читай слева направо. В пропусках: Н. М. |
| german_33 | de | prompt | Welches deutsche Wort passt zum Bild? | Vogelhaus. Welche beiden Buchstaben fehlen? |
| german_33 | de | tip | Suche die Buchstaben von Fisch: F. I. S. C. H. | Lies von links nach rechts. Die Lücken brauchen V. H. |
| german_33 | en | prompt | Which German word matches the picture? | Birdhouse. Which two letters are missing? |
| german_33 | en | tip | Find the letters of Fisch: F. I. S. C. H. | Read from left to right. The gaps need B. O. |
| german_33 | ru | prompt | Какое немецкое слово подходит к картинке? | Скворечник. Какие две буквы пропущены? |
| german_33 | ru | tip | Найди буквы слова Fisch: F. I. S. C. H. | Читай слева направо. В пропусках: В. Н. |
| german_34 | de | prompt | Welches deutsche Wort passt zum Bild? | Mondlicht. Welche beiden Buchstaben fehlen? |
| german_34 | de | tip | Suche die Buchstaben von Vogel: V. O. G. E. L. | Lies von links nach rechts. Die Lücken brauchen O. C. |
| german_34 | en | prompt | Which German word matches the picture? | Moonlight. Which two letters are missing? |
| german_34 | en | tip | Find the letters of Vogel: V. O. G. E. L. | Read from left to right. The gaps need O. G. |
| german_34 | ru | prompt | Какое немецкое слово подходит к картинке? | Спутник. Какие две буквы пропущены? |
| german_34 | ru | tip | Найди буквы слова Vogel: V. O. G. E. L. | Читай слева направо. В пропусках: П. И. |
| german_35 | de | prompt | Welches deutsche Wort passt zum Bild? | Baumkrone. Welche beiden Buchstaben fehlen? |
| german_35 | de | tip | Suche die Buchstaben von Mond: M. O. N. D. | Lies von links nach rechts. Die Lücken brauchen U. N. |
| german_35 | en | prompt | Which German word matches the picture? | Treetop. Which two letters are missing? |
| german_35 | en | tip | Find the letters of Mond: M. O. N. D. | Read from left to right. The gaps need E. P. |
| german_35 | ru | prompt | Какое немецкое слово подходит к картинке? | Макушка. Какие две буквы пропущены? |
| german_35 | ru | tip | Найди буквы слова Mond: M. O. N. D. | Читай слева направо. В пропусках: К. А. |
| german_36 | de | prompt | Welches deutsche Wort passt zum Bild? | Milchzahn. Welche beiden Buchstaben fehlen? |
| german_36 | de | tip | Suche die Buchstaben von Baum: B. A. U. M. | Lies von links nach rechts. Die Lücken brauchen C. N. |
| german_36 | en | prompt | Which German word matches the picture? | Toothbrush. Which two letters are missing? |
| german_36 | en | tip | Find the letters of Baum: B. A. U. M. | Read from left to right. The gaps need T. B. |
| german_36 | ru | prompt | Какое немецкое слово подходит к картинке? | Зубик. Какие две буквы пропущены? |
| german_36 | ru | tip | Найди буквы слова Baum: B. A. U. M. | Читай слева направо. В пропусках: З. Б. |
| german_37 | de | prompt | Welches deutsche Wort passt zum Bild? | Fußabdruck. Welche beiden Buchstaben fehlen? |
| german_37 | de | tip | Suche die Buchstaben von Zahn: Z. A. H. N. | Lies von links nach rechts. Die Lücken brauchen S. U. |
| german_37 | en | prompt | Which German word matches the picture? | Footprint. Which two letters are missing? |
| german_37 | en | tip | Find the letters of Zahn: Z. A. H. N. | Read from left to right. The gaps need F. P. |
| german_37 | ru | prompt | Какое немецкое слово подходит к картинке? | Следопыт. Какие две буквы пропущены? |
| german_37 | ru | tip | Найди буквы слова Zahn: Z. A. H. N. | Читай слева направо. В пропусках: С. О. |
| german_38 | de | prompt | Welches deutsche Wort passt zum Bild? | Schildkrötenei. Welche beiden Buchstaben fehlen? |
| german_38 | de | tip | Suche die Buchstaben von Fuss: F. U. S. S. | Lies von links nach rechts. Die Lücken brauchen H. T. |
| german_38 | en | prompt | Which German word matches the picture? | Eggshell. Which two letters are missing? |
| german_38 | en | tip | Find the letters of Fuss: F. U. S. S. | Read from left to right. The gaps need G. E. |
| german_38 | ru | prompt | Какое немецкое слово подходит к картинке? | Скорлупа. Какие две буквы пропущены? |
| german_38 | ru | tip | Найди буквы слова Fuss: F. U. S. S. | Читай слева направо. В пропусках: К. У. |
| german_39 | de | prompt | Welches deutsche Wort passt zum Bild? | Meereswelle. Welche beiden Buchstaben fehlen? |
| german_39 | de | tip | Suche die Buchstaben von Ei: E. I. | Lies von links nach rechts. Die Lücken brauchen S. E. |
| german_39 | en | prompt | Which German word matches the picture? | Seashell. Which two letters are missing? |
| german_39 | en | tip | Find the letters of Ei: E. I. | Read from left to right. The gaps need A. L. |
| german_39 | ru | prompt | Какое немецкое слово подходит к картинке? | Ракушка. Какие две буквы пропущены? |
| german_39 | ru | tip | Найди буквы слова Ei: E. I. | Читай слева направо. В пропусках: У. А. |
| german_40 | de | prompt | Welches deutsche Wort passt zum Bild? | Abenteuer. Welche beiden Buchstaben fehlen? |
| german_40 | de | tip | Suche die Buchstaben von Meer: M. E. E. R. | Lies von links nach rechts. Die Lücken brauchen N. E. |
| german_40 | en | prompt | Which German word matches the picture? | Adventure. Which two letters are missing? |
| german_40 | en | tip | Find the letters of Meer: M. E. E. R. | Read from left to right. The gaps need E. R. |
| german_40 | ru | prompt | Какое немецкое слово подходит к картинке? | Приключение. Какие две буквы пропущены? |
| german_40 | ru | tip | Найди буквы слова Meer: M. E. E. R. | Читай слева направо. В пропусках: П. Ч. |
| logic_09 | de | prompt | Was kommt als Nächstes? | Zwei Schritte wechseln sich ab. Welche Zahl folgt? |
| logic_09 | de | tip | Das Muster wiederholt sich: Apfel, Stern. Danach kommt Apfel. | Abwechselnd 3 dazu, dann eins dazu. |
| logic_09 | en | prompt | What comes next? | Two steps alternate. Which number follows? |
| logic_09 | en | tip | The pattern repeats: apple, star. Next comes apple. | Alternate adding 3, then adding one. |
| logic_09 | ru | prompt | Что дальше? | Два шага чередуются. Какое число дальше? |
| logic_09 | ru | tip | Узор повторяется: яблоко, звезда. Дальше: яблоко. | Чередуй: прибавь 3, потом один. |
| logic_10 | de | prompt | Was kommt als Nächstes? | Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts? |
| logic_10 | de | tip | Das Muster wiederholt sich: Sonne, Blatt, Blatt. Danach kommt Blatt. | Nach rechts 3 dazu, nach unten 6 dazu. |
| logic_10 | en | prompt | What comes next? | A fixed step goes right and another goes down. What is missing at bottom right? |
| logic_10 | en | tip | The pattern repeats: sun, leaf, leaf. Next comes leaf. | Add 3 going right, add 6 going down. |
| logic_10 | ru | prompt | Что дальше? | Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа? |
| logic_10 | ru | tip | Узор повторяется: Солнце, лист, лист. Дальше: лист. | Вправо прибавь 3, вниз прибавь 6. |
| logic_11 | de | prompt | Was kommt als Nächstes? | Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort? |
| logic_11 | de | tip | Das Muster wiederholt sich: Fisch, Blume. Danach kommt Fisch. | Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins. |
| logic_11 | en | prompt | What comes next? | Picture and number have separate rules. Which pair continues both? |
| logic_11 | en | tip | The pattern repeats: fish, flower. Next comes fish. | The three pictures repeat. The numbers alternate adding two and adding one. |
| logic_11 | ru | prompt | Что дальше? | У картинок и чисел свои правила. Какая пара продолжает оба ряда? |
| logic_11 | ru | tip | Узор повторяется: рыба, цветок. Дальше: рыба. | Три картинки повторяются. У чисел чередуются прибавления двух и одного. |
| logic_12 | de | prompt | Was kommt als Nächstes? | Vogel steht vor Maus. Schildkröte steht vor Vogel. Wer steht ganz vorn? |
| logic_12 | de | tip | Das Muster wiederholt sich: Mond, Stern, Stern. Danach kommt Stern. | Von vorn nach hinten: Schildkröte, Vogel, Maus. |
| logic_12 | en | prompt | What comes next? | The bird is before the mouse. The turtle is before the bird. Who is first? |
| logic_12 | en | tip | The pattern repeats: moon, star, star. Next comes star. | From first to last: turtle, bird, mouse. |
| logic_12 | ru | prompt | Что дальше? | птица раньше, чем мышь. черепаха раньше, чем птица. Кто самый первый? |
| logic_12 | ru | tip | Узор повторяется: Луна, звезда, звезда. Дальше: звезда. | От первого к последнему: черепаха, птица, мышь. |
| logic_13 | de | prompt | Was kommt als Nächstes? | Zwei Schritte wechseln sich ab. Welche Zahl folgt? |
| logic_13 | de | tip | Das Muster wiederholt sich: Biene, Blatt, Blume. Danach kommt Blume. | Abwechselnd 3 dazu, dann eins dazu. |
| logic_13 | en | prompt | What comes next? | Two steps alternate. Which number follows? |
| logic_13 | en | tip | The pattern repeats: bee, leaf, flower. Next comes flower. | Alternate adding 3, then adding one. |
| logic_13 | ru | prompt | Что дальше? | Два шага чередуются. Какое число дальше? |
| logic_13 | ru | tip | Узор повторяется: пчела, лист, цветок. Дальше: цветок. | Чередуй: прибавь 3, потом один. |
| logic_14 | de | prompt | Was kommt als Nächstes? | Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts? |
| logic_14 | de | tip | Das Muster wiederholt sich: Ball, Ball, Roboter. Danach kommt Ball. | Nach rechts 3 dazu, nach unten 6 dazu. |
| logic_14 | en | prompt | What comes next? | A fixed step goes right and another goes down. What is missing at bottom right? |
| logic_14 | en | tip | The pattern repeats: ball, ball, robot. Next comes ball. | Add 3 going right, add 6 going down. |
| logic_14 | ru | prompt | Что дальше? | Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа? |
| logic_14 | ru | tip | Узор повторяется: мяч, мяч, робот. Дальше: мяч. | Вправо прибавь 3, вниз прибавь 6. |
| logic_15 | de | prompt | Was kommt als Nächstes? | Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort? |
| logic_15 | de | tip | Das Muster wiederholt sich: Baum, Sonne. Danach kommt Baum. | Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins. |
| logic_15 | en | prompt | What comes next? | Picture and number have separate rules. Which pair continues both? |
| logic_15 | en | tip | The pattern repeats: tree, sun. Next comes tree. | The three pictures repeat. The numbers alternate adding two and adding one. |
| logic_15 | ru | prompt | Что дальше? | У картинок и чисел свои правила. Какая пара продолжает оба ряда? |
| logic_15 | ru | tip | Узор повторяется: дерево, Солнце. Дальше: дерево. | Три картинки повторяются. У чисел чередуются прибавления двух и одного. |
| logic_16 | de | prompt | Was kommt als Nächstes? | Maus steht vor Schildkröte. Biene steht vor Maus. Wer steht ganz hinten? |
| logic_16 | de | tip | Das Muster wiederholt sich: Ei, Vogel, Vogel. Danach kommt Vogel. | Von vorn nach hinten: Biene, Maus, Schildkröte. |
| logic_16 | en | prompt | What comes next? | The mouse is before the turtle. The bee is before the mouse. Who is last? |
| logic_16 | en | tip | The pattern repeats: egg, bird, bird. Next comes bird. | From first to last: bee, mouse, turtle. |
| logic_16 | ru | prompt | Что дальше? | мышь раньше, чем черепаха. пчела раньше, чем мышь. Кто самый последний? |
| logic_16 | ru | tip | Узор повторяется: яйцо, птица, птица. Дальше: птица. | От первого к последнему: пчела, мышь, черепаха. |
| logic_17 | de | prompt | Was passt zum Schatten? | Zwei Schritte wechseln sich ab. Welche Zahl folgt? |
| logic_17 | de | tip | Vergleiche die Umrisse. Gesucht ist: Vogel. | Abwechselnd 4 dazu, dann eins dazu. |
| logic_17 | en | prompt | What matches the shadow? | Two steps alternate. Which number follows? |
| logic_17 | en | tip | Compare the outlines. Find the bird. | Alternate adding 4, then adding one. |
| logic_17 | ru | prompt | Что подходит к тени? | Два шага чередуются. Какое число дальше? |
| logic_17 | ru | tip | Сравни контуры. Найди: птица. | Чередуй: прибавь 4, потом один. |
| logic_18 | de | prompt | Was passt zum Schatten? | Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts? |
| logic_18 | de | tip | Vergleiche die Umrisse. Gesucht ist: Katze. | Nach rechts 4 dazu, nach unten 8 dazu. |
| logic_18 | en | prompt | What matches the shadow? | A fixed step goes right and another goes down. What is missing at bottom right? |
| logic_18 | en | tip | Compare the outlines. Find the cat. | Add 4 going right, add 8 going down. |
| logic_18 | ru | prompt | Что подходит к тени? | Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа? |
| logic_18 | ru | tip | Сравни контуры. Найди: кошка. | Вправо прибавь 4, вниз прибавь 8. |
| logic_19 | de | prompt | Was passt zum Schatten? | Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort? |
| logic_19 | de | tip | Vergleiche die Umrisse. Gesucht ist: Schmetterling. | Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins. |
| logic_19 | en | prompt | What matches the shadow? | Picture and number have separate rules. Which pair continues both? |
| logic_19 | en | tip | Compare the outlines. Find the butterfly. | The three pictures repeat. The numbers alternate adding two and adding one. |
| logic_19 | ru | prompt | Что подходит к тени? | У картинок и чисел свои правила. Какая пара продолжает оба ряда? |
| logic_19 | ru | tip | Сравни контуры. Найди: бабочка. | Три картинки повторяются. У чисел чередуются прибавления двух и одного. |
| logic_20 | de | prompt | Was passt zum Schatten? | Schildkröte steht vor Biene. Fisch steht vor Schildkröte. Wer steht ganz vorn? |
| logic_20 | de | tip | Vergleiche die Umrisse. Gesucht ist: Hammer. | Von vorn nach hinten: Fisch, Schildkröte, Biene. |
| logic_20 | en | prompt | What matches the shadow? | The turtle is before the bee. The fish is before the turtle. Who is first? |
| logic_20 | en | tip | Compare the outlines. Find the hammer. | From first to last: fish, turtle, bee. |
| logic_20 | ru | prompt | Что подходит к тени? | черепаха раньше, чем пчела. рыба раньше, чем черепаха. Кто самый первый? |
| logic_20 | ru | tip | Сравни контуры. Найди: молоток. | От первого к последнему: рыба, черепаха, пчела. |
| logic_21 | de | prompt | Was passt zum Schatten? | Zwei Schritte wechseln sich ab. Welche Zahl folgt? |
| logic_21 | de | tip | Vergleiche die Umrisse. Gesucht ist: Helm. | Abwechselnd 4 dazu, dann eins dazu. |
| logic_21 | en | prompt | What matches the shadow? | Two steps alternate. Which number follows? |
| logic_21 | en | tip | Compare the outlines. Find the helmet. | Alternate adding 4, then adding one. |
| logic_21 | ru | prompt | Что подходит к тени? | Два шага чередуются. Какое число дальше? |
| logic_21 | ru | tip | Сравни контуры. Найди: шлем. | Чередуй: прибавь 4, потом один. |
| logic_22 | de | prompt | Was passt zum Schatten? | Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts? |
| logic_22 | de | tip | Vergleiche die Umrisse. Gesucht ist: Frosch. | Nach rechts 4 dazu, nach unten 8 dazu. |
| logic_22 | en | prompt | What matches the shadow? | A fixed step goes right and another goes down. What is missing at bottom right? |
| logic_22 | en | tip | Compare the outlines. Find the frog. | Add 4 going right, add 8 going down. |
| logic_22 | ru | prompt | Что подходит к тени? | Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа? |
| logic_22 | ru | tip | Сравни контуры. Найди: лягушка. | Вправо прибавь 4, вниз прибавь 8. |
| logic_23 | de | prompt | Was passt zum Schatten? | Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort? |
| logic_23 | de | tip | Vergleiche die Umrisse. Gesucht ist: Hand. | Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins. |
| logic_23 | en | prompt | What matches the shadow? | Picture and number have separate rules. Which pair continues both? |
| logic_23 | en | tip | Compare the outlines. Find the hand. | The three pictures repeat. The numbers alternate adding two and adding one. |
| logic_23 | ru | prompt | Что подходит к тени? | У картинок и чисел свои правила. Какая пара продолжает оба ряда? |
| logic_23 | ru | tip | Сравни контуры. Найди: кисть. | Три картинки повторяются. У чисел чередуются прибавления двух и одного. |
| logic_24 | de | prompt | Was passt zum Schatten? | Biene steht vor Fisch. Katze steht vor Biene. Wer steht ganz hinten? |
| logic_24 | de | tip | Vergleiche die Umrisse. Gesucht ist: Rad. | Von vorn nach hinten: Katze, Biene, Fisch. |
| logic_24 | en | prompt | What matches the shadow? | The bee is before the fish. The cat is before the bee. Who is last? |
| logic_24 | en | tip | Compare the outlines. Find the wheel. | From first to last: cat, bee, fish. |
| logic_24 | ru | prompt | Что подходит к тени? | пчела раньше, чем рыба. кошка раньше, чем пчела. Кто самый последний? |
| logic_24 | ru | tip | Сравни контуры. Найди: колесо. | От первого к последнему: кошка, пчела, рыба. |
| logic_25 | de | prompt | Welches Bild passt nicht zur gezeigten Gruppe? | Zwei Schritte wechseln sich ab. Welche Zahl folgt? |
| logic_25 | de | tip | Die Gruppe zeigt Pflanzen und Pflanzenteile. Ball passt nicht dazu. | Abwechselnd 5 dazu, dann eins dazu. |
| logic_25 | en | prompt | Which picture does not belong with this group? | Two steps alternate. Which number follows? |
| logic_25 | en | tip | The group shows plants and plant parts. ball does not belong. | Alternate adding 5, then adding one. |
| logic_25 | ru | prompt | Какая картинка не подходит к этой группе? | Два шага чередуются. Какое число дальше? |
| logic_25 | ru | tip | В группе: растения и части растений. мяч сюда не относится. | Чередуй: прибавь 5, потом один. |
| logic_26 | de | prompt | Welches Bild passt nicht zur gezeigten Gruppe? | Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts? |
| logic_26 | de | tip | Die Gruppe zeigt Tiere. Glas passt nicht dazu. | Nach rechts 5 dazu, nach unten 10 dazu. |
| logic_26 | en | prompt | Which picture does not belong with this group? | A fixed step goes right and another goes down. What is missing at bottom right? |
| logic_26 | en | tip | The group shows animals. glass does not belong. | Add 5 going right, add 10 going down. |
| logic_26 | ru | prompt | Какая картинка не подходит к этой группе? | Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа? |
| logic_26 | ru | tip | В группе: животные. стекло сюда не относится. | Вправо прибавь 5, вниз прибавь 10. |
| logic_27 | de | prompt | Welches Bild passt nicht zur gezeigten Gruppe? | Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort? |
| logic_27 | de | tip | Die Gruppe zeigt Sinnesorgane. Hammer passt nicht dazu. | Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins. |
| logic_27 | en | prompt | Which picture does not belong with this group? | Picture and number have separate rules. Which pair continues both? |
| logic_27 | en | tip | The group shows sense organs. hammer does not belong. | The three pictures repeat. The numbers alternate adding two and adding one. |
| logic_27 | ru | prompt | Какая картинка не подходит к этой группе? | У картинок и чисел свои правила. Какая пара продолжает оба ряда? |
| logic_27 | ru | tip | В группе: органы чувств. молоток сюда не относится. | Три картинки повторяются. У чисел чередуются прибавления двух и одного. |
| logic_28 | de | prompt | Welches Bild passt nicht zur gezeigten Gruppe? | Fisch steht vor Katze. Frosch steht vor Fisch. Wer steht ganz vorn? |
| logic_28 | de | tip | Die Gruppe zeigt Werkzeuge. Fisch passt nicht dazu. | Von vorn nach hinten: Frosch, Fisch, Katze. |
| logic_28 | en | prompt | Which picture does not belong with this group? | The fish is before the cat. The frog is before the fish. Who is first? |
| logic_28 | en | tip | The group shows tools. fish does not belong. | From first to last: frog, fish, cat. |
| logic_28 | ru | prompt | Какая картинка не подходит к этой группе? | рыба раньше, чем кошка. лягушка раньше, чем рыба. Кто самый первый? |
| logic_28 | ru | tip | В группе: инструменты. рыба сюда не относится. | От первого к последнему: лягушка, рыба, кошка. |
| logic_29 | de | prompt | Welches Bild passt nicht zur gezeigten Gruppe? | Zwei Schritte wechseln sich ab. Welche Zahl folgt? |
| logic_29 | de | tip | Die Gruppe zeigt Dinge am Himmel. Zahn passt nicht dazu. | Abwechselnd 5 dazu, dann eins dazu. |
| logic_29 | en | prompt | Which picture does not belong with this group? | Two steps alternate. Which number follows? |
| logic_29 | en | tip | The group shows things in the sky. tooth does not belong. | Alternate adding 5, then adding one. |
| logic_29 | ru | prompt | Какая картинка не подходит к этой группе? | Два шага чередуются. Какое число дальше? |
| logic_29 | ru | tip | В группе: явления в небе. зуб сюда не относится. | Чередуй: прибавь 5, потом один. |
| logic_30 | de | prompt | Welches Bild passt nicht zur gezeigten Gruppe? | Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts? |
| logic_30 | de | tip | Die Gruppe zeigt Zustände von Wasser. Holz passt nicht dazu. | Nach rechts 5 dazu, nach unten 10 dazu. |
| logic_30 | en | prompt | Which picture does not belong with this group? | A fixed step goes right and another goes down. What is missing at bottom right? |
| logic_30 | en | tip | The group shows forms of water. wood does not belong. | Add 5 going right, add 10 going down. |
| logic_30 | ru | prompt | Какая картинка не подходит к этой группе? | Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа? |
| logic_30 | ru | tip | В группе: состояния воды. древесина сюда не относится. | Вправо прибавь 5, вниз прибавь 10. |
| logic_31 | de | prompt | Welches Bild passt nicht zur gezeigten Gruppe? | Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort? |
| logic_31 | de | tip | Die Gruppe zeigt Tiere mit Flügeln. Knochen passt nicht dazu. | Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins. |
| logic_31 | en | prompt | Which picture does not belong with this group? | Picture and number have separate rules. Which pair continues both? |
| logic_31 | en | tip | The group shows animals with wings. bone does not belong. | The three pictures repeat. The numbers alternate adding two and adding one. |
| logic_31 | ru | prompt | Какая картинка не подходит к этой группе? | У картинок и чисел свои правила. Какая пара продолжает оба ряда? |
| logic_31 | ru | tip | В группе: животные с крыльями. кость сюда не относится. | Три картинки повторяются. У чисел чередуются прибавления двух и одного. |
| logic_32 | de | prompt | Welches Bild passt nicht zur gezeigten Gruppe? | Katze steht vor Frosch. Vogel steht vor Katze. Wer steht ganz hinten? |
| logic_32 | de | tip | Die Gruppe zeigt Werkstoffe. Katze passt nicht dazu. | Von vorn nach hinten: Vogel, Katze, Frosch. |
| logic_32 | en | prompt | Which picture does not belong with this group? | The cat is before the frog. The bird is before the cat. Who is last? |
| logic_32 | en | tip | The group shows materials. cat does not belong. | From first to last: bird, cat, frog. |
| logic_32 | ru | prompt | Какая картинка не подходит к этой группе? | кошка раньше, чем лягушка. птица раньше, чем кошка. Кто самый последний? |
| logic_32 | ru | tip | В группе: материалы. кошка сюда не относится. | От первого к последнему: птица, кошка, лягушка. |
| logic_33 | de | prompt | Welche Zahl kommt als Nächstes? | Zwei Schritte wechseln sich ab. Welche Zahl folgt? |
| logic_33 | de | tip | Es kommen jedes Mal 1 dazu. | Abwechselnd 6 dazu, dann eins dazu. |
| logic_33 | en | prompt | Which number comes next? | Two steps alternate. Which number follows? |
| logic_33 | en | tip | Add 1 each time. | Alternate adding 6, then adding one. |
| logic_33 | ru | prompt | Какое число следующее? | Два шага чередуются. Какое число дальше? |
| logic_33 | ru | tip | Каждый раз прибавляй 1. | Чередуй: прибавь 6, потом один. |
| logic_34 | de | prompt | Welche Zahl kommt als Nächstes? | Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts? |
| logic_34 | de | tip | Es kommen jedes Mal 1 dazu. | Nach rechts 6 dazu, nach unten 12 dazu. |
| logic_34 | en | prompt | Which number comes next? | A fixed step goes right and another goes down. What is missing at bottom right? |
| logic_34 | en | tip | Add 1 each time. | Add 6 going right, add 12 going down. |
| logic_34 | ru | prompt | Какое число следующее? | Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа? |
| logic_34 | ru | tip | Каждый раз прибавляй 1. | Вправо прибавь 6, вниз прибавь 12. |
| logic_35 | de | prompt | Welche Zahl kommt als Nächstes? | Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort? |
| logic_35 | de | tip | Es kommen jedes Mal 1 dazu. | Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins. |
| logic_35 | en | prompt | Which number comes next? | Picture and number have separate rules. Which pair continues both? |
| logic_35 | en | tip | Add 1 each time. | The three pictures repeat. The numbers alternate adding two and adding one. |
| logic_35 | ru | prompt | Какое число следующее? | У картинок и чисел свои правила. Какая пара продолжает оба ряда? |
| logic_35 | ru | tip | Каждый раз прибавляй 1. | Три картинки повторяются. У чисел чередуются прибавления двух и одного. |
| logic_36 | de | prompt | Welche Zahl kommt als Nächstes? | Frosch steht vor Vogel. Maus steht vor Frosch. Wer steht ganz vorn? |
| logic_36 | de | tip | Es kommen jedes Mal 1 dazu. | Von vorn nach hinten: Maus, Frosch, Vogel. |
| logic_36 | en | prompt | Which number comes next? | The frog is before the bird. The mouse is before the frog. Who is first? |
| logic_36 | en | tip | Add 1 each time. | From first to last: mouse, frog, bird. |
| logic_36 | ru | prompt | Какое число следующее? | лягушка раньше, чем птица. мышь раньше, чем лягушка. Кто самый первый? |
| logic_36 | ru | tip | Каждый раз прибавляй 1. | От первого к последнему: мышь, лягушка, птица. |
| logic_37 | de | prompt | Welche Zahl kommt als Nächstes? | Zwei Schritte wechseln sich ab. Welche Zahl folgt? |
| logic_37 | de | tip | Es kommen jedes Mal 2 dazu. | Abwechselnd 6 dazu, dann eins dazu. |
| logic_37 | en | prompt | Which number comes next? | Two steps alternate. Which number follows? |
| logic_37 | en | tip | Add 2 each time. | Alternate adding 6, then adding one. |
| logic_37 | ru | prompt | Какое число следующее? | Два шага чередуются. Какое число дальше? |
| logic_37 | ru | tip | Каждый раз прибавляй 2. | Чередуй: прибавь 6, потом один. |
| logic_38 | de | prompt | Welche Zahl kommt als Nächstes? | Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts? |
| logic_38 | de | tip | Es kommen jedes Mal 2 dazu. | Nach rechts 6 dazu, nach unten 12 dazu. |
| logic_38 | en | prompt | Which number comes next? | A fixed step goes right and another goes down. What is missing at bottom right? |
| logic_38 | en | tip | Add 2 each time. | Add 6 going right, add 12 going down. |
| logic_38 | ru | prompt | Какое число следующее? | Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа? |
| logic_38 | ru | tip | Каждый раз прибавляй 2. | Вправо прибавь 6, вниз прибавь 12. |
| logic_39 | de | prompt | Welche Zahl kommt als Nächstes? | Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort? |
| logic_39 | de | tip | Es kommen jedes Mal 5 dazu. | Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins. |
| logic_39 | en | prompt | Which number comes next? | Picture and number have separate rules. Which pair continues both? |
| logic_39 | en | tip | Add 5 each time. | The three pictures repeat. The numbers alternate adding two and adding one. |
| logic_39 | ru | prompt | Какое число следующее? | У картинок и чисел свои правила. Какая пара продолжает оба ряда? |
| logic_39 | ru | tip | Каждый раз прибавляй 5. | Три картинки повторяются. У чисел чередуются прибавления двух и одного. |
| logic_40 | de | prompt | Welche Zahl kommt als Nächstes? | Vogel steht vor Maus. Schildkröte steht vor Vogel. Wer steht ganz hinten? |
| logic_40 | de | tip | Es kommen jedes Mal 5 dazu. | Von vorn nach hinten: Schildkröte, Vogel, Maus. |
| logic_40 | en | prompt | Which number comes next? | The bird is before the mouse. The turtle is before the bird. Who is last? |
| logic_40 | en | tip | Add 5 each time. | From first to last: turtle, bird, mouse. |
| logic_40 | ru | prompt | Какое число следующее? | птица раньше, чем мышь. черепаха раньше, чем птица. Кто самый последний? |
| logic_40 | ru | tip | Каждый раз прибавляй 5. | От первого к последнему: черепаха, птица, мышь. |
| physics_01 | de | prompt | Was lässt ein Fahrrad rollen? | Bewegen. Eine Achse bleibt an ihrem Platz, doch außen dreht sich etwas. Was trägt ein rollendes Fahrrad? |
| physics_01 | de | tip | Räder drehen sich und rollen über den Boden. | Überlege beide Hinweise. Gesucht ist: Rad. |
| physics_01 | en | prompt | What lets a bicycle roll? | Motion. An axle stays in place while something turns around it. What carries a rolling bicycle? |
| physics_01 | en | tip | Wheels turn and roll along the ground. | Use both clues. The answer is wheel. |
| physics_01 | ru | prompt | Что помогает велосипеду катиться? | Движение. Ось остаётся на месте, а снаружи что-то вращается. Что несёт катящийся велосипед? |
| physics_01 | ru | tip | Колёса вращаются и катятся по земле. | Учти обе подсказки. Ответ: колесо. |
| physics_02 | de | prompt | Womit schneidest du Papier? | Werkeln. Zwei Schneiden bewegen sich aneinander vorbei. Womit trennst du damit Papier? |
| physics_02 | de | tip | Eine Kinderschere schneidet Papier. Schneide von dir weg. | Überlege beide Hinweise. Gesucht ist: Schere. |
| physics_02 | en | prompt | What cuts paper? | Making. Two blades move past each other. What uses this to cut paper? |
| physics_02 | en | tip | Safety scissors cut paper. Cut away from your body. | Use both clues. The answer is scissors. |
| physics_02 | ru | prompt | Чем режут бумагу? | Мастерская. Два лезвия проходят друг мимо друга. Чем так разрезают бумагу? |
| physics_02 | ru | tip | Детскими ножницами режут бумагу. Режь в сторону от себя. | Учти обе подсказки. Ответ: ножницы. |
| physics_03 | de | prompt | Womit schlägt man einen Nagel ein? | Werkeln. Eine Schraube wird gedreht, ein Nagel eingeschlagen. Welches Werkzeug braucht der Nagel? |
| physics_03 | de | tip | Ein Hammer schlägt Nägel ein. Ein Erwachsener hilft dabei. | Überlege beide Hinweise. Gesucht ist: Hammer. |
| physics_03 | en | prompt | What drives a nail into wood? | Build. A screw is turned but a nail is driven in. Which tool does the nail need? |
| physics_03 | en | tip | A hammer drives in nails. An adult helps with this. | Use both clues. The answer is hammer. |
| physics_03 | ru | prompt | Чем забивают гвоздь в дерево? | Мастерить. Винт вращают, а гвоздь забивают. Какой инструмент нужен гвоздю? |
| physics_03 | ru | tip | Молотком забивают гвозди. Взрослый помогает с такой работой. | Учти обе подсказки. Ответ: молоток. |
| physics_04 | de | prompt | Was dreht eine Schraube? | Werkeln. Eine Befestigung hat ein Gewinde. Womit lässt sie sich lösen, ohne darauf zu schlagen? |
| physics_04 | de | tip | Ein Schraubendreher dreht Schrauben hinein oder heraus. | Überlege beide Hinweise. Gesucht ist: Schraubendreher. |
| physics_04 | en | prompt | What turns a screw? | Making. A fastener has a thread. What loosens it without hitting it? |
| physics_04 | en | tip | A screwdriver turns screws in or out. | Use both clues. The answer is screwdriver. |
| physics_04 | ru | prompt | Чем поворачивают винт? | Мастерская. У крепежа есть резьба. Чем его можно ослабить без ударов? |
| physics_04 | ru | tip | Отвёрткой закручивают и выкручивают винты. | Учти обе подсказки. Ответ: отвёртка. |
| physics_05 | de | prompt | Was zieht ein Magnet an: Eisen, Holz oder Papier? | Verändern. Ein Magnet wirkt durch dünnes Papier hindurch. Welcher Stoff darunter wird angezogen: Eisen, Holz oder Papier? |
| physics_05 | de | tip | Eisen wird von Magneten angezogen. Nicht jedes Metall ist magnetisch. | Überlege beide Hinweise. Gesucht ist: Eisen. |
| physics_05 | en | prompt | What does a magnet attract: iron, wood or paper? | Change. A magnet acts through thin paper. Which material below is attracted: iron, wood or paper? |
| physics_05 | en | tip | Magnets attract iron. Not every metal is magnetic. | Use both clues. The answer is iron. |
| physics_05 | ru | prompt | Что притягивает магнит: железо, дерево или бумагу? | Изменение. Магнит действует через тонкую бумагу. Что под ней притянется: железо, дерево или бумага? |
| physics_05 | ru | tip | Магнит притягивает железо. Не каждый металл притягивается магнитом. | Учти обе подсказки. Ответ: железо. |
| physics_06 | de | prompt | Was führt einen Weg über einen Fluss? | Entdecken. Die Straße endet am Fluss, das andere Ufer soll erreichbar bleiben. Welches Bauwerk hilft? |
| physics_06 | de | tip | Eine Brücke verbindet die beiden Ufer. | Überlege beide Hinweise. Gesucht ist: Brücke. |
| physics_06 | en | prompt | What carries a path across a river? | Explore. A road ends at a river but the other bank must stay reachable. Which structure helps? |
| physics_06 | en | tip | A bridge connects the two banks. | Use both clues. The answer is bridge. |
| physics_06 | ru | prompt | Что проводит дорогу через реку? | Открытие. Дорога заканчивается у реки, но на другой берег нужно попасть. Какое сооружение поможет? |
| physics_06 | ru | tip | Мост соединяет два берега. | Учти обе подсказки. Ответ: мост. |
| physics_07 | de | prompt | Was macht eine dunkle Ecke hell? | Leuchten. Eine Batterie liefert Energie, macht aber die Ecke nicht hell. Welcher Teil wandelt Energie in Licht um? |
| physics_07 | de | tip | Eine eingeschaltete Lampe gibt Licht ab. | Überlege beide Hinweise. Gesucht ist: Lampe. |
| physics_07 | en | prompt | What lights up a dark corner? | Light. A battery provides energy but does not light the corner. Which part turns energy into light? |
| physics_07 | en | tip | A lamp gives off light when switched on. | Use both clues. The answer is lamp. |
| physics_07 | ru | prompt | Что освещает тёмный угол? | Свет. Батарейка даёт энергию, но угол не освещает. Какая деталь превращает энергию в свет? |
| physics_07 | ru | tip | Включённая лампа даёт свет. | Учти обе подсказки. Ответ: лампа. |
| physics_08 | de | prompt | Was versorgt eine Taschenlampe mit Energie? | Versorgen. Der Stromkreis ist geschlossen, doch die Energiequelle leer. Was muss ersetzt werden? |
| physics_08 | de | tip | Eine Batterie speichert Energie für die Taschenlampe. Nicht öffnen! | Überlege beide Hinweise. Gesucht ist: Batterie. |
| physics_08 | en | prompt | What supplies energy to a battery-powered torch? | Power. The circuit is closed but the energy source is flat. What needs replacing? |
| physics_08 | en | tip | A battery stores energy for the torch. Never open it. | Use both clues. The answer is battery. |
| physics_08 | ru | prompt | Что даёт энергию карманному фонарику? | Энергия. Цепь замкнута, но источник энергии разрядился. Что нужно заменить? |
| physics_08 | ru | tip | Батарейка хранит энергию для фонарика. Не открывай её. | Учти обе подсказки. Ответ: батарейка. |
| physics_09 | de | prompt | Was schützt beim Radfahren den Kopf? | Schützen. Beim Sturz trifft ein Schlag den Kopf. Was soll den Schlag abfedern? |
| physics_09 | de | tip | Ein passender, geschlossener Fahrradhelm schützt den Kopf. | Überlege beide Hinweise. Gesucht ist: Helm. |
| physics_09 | en | prompt | What protects your head when cycling? | Protection. In a fall, an impact hits the head. What should cushion it? |
| physics_09 | en | tip | A correctly fitted and fastened helmet protects your head. | Use both clues. The answer is helmet. |
| physics_09 | ru | prompt | Что защищает голову при езде на велосипеде? | Защита. При падении возможен удар по голове. Что должно его смягчить? |
| physics_09 | ru | tip | Подходящий застёгнутый шлем защищает голову. | Учти обе подсказки. Ответ: шлем. |
| physics_10 | de | prompt | Was hat Zähne und überträgt Drehbewegungen? | Übertragen. Ein Rad soll ein zweites ohne Durchrutschen drehen. Welcher Teil greift mit Zähnen ein? |
| physics_10 | de | tip | Die Zähne von Zahnrädern greifen ineinander. | Überlege beide Hinweise. Gesucht ist: Zahnrad. |
| physics_10 | en | prompt | What has teeth and passes on a turning movement? | Transfer. One wheel must turn another without slipping. Which part meshes using teeth? |
| physics_10 | en | tip | Gear teeth fit together to pass on turning movements. | Use both clues. The answer is gear. |
| physics_10 | ru | prompt | Что имеет зубцы и передаёт вращение? | Передавать. Одно колесо должно вращать другое без проскальзывания. Что сцепляется зубцами? |
| physics_10 | ru | tip | Зубцы шестерёнок входят друг в друга и передают вращение. | Учти обе подсказки. Ответ: шестерёнка. |
| physics_11 | de | prompt | Welches Gerät kippt um einen Drehpunkt? | Werkeln. Eine Seite der Wippe geht hinunter, die andere hoch. Welches einfache Gerät nutzt den Drehpunkt? |
| physics_11 | de | tip | Eine Wippe ist ein Hebel mit einem Drehpunkt. | Überlege beide Hinweise. Gesucht ist: Hebel. |
| physics_11 | en | prompt | Which device tilts around a pivot? | Making. One end of a seesaw goes down and the other up. Which simple machine uses the pivot? |
| physics_11 | en | tip | A seesaw is a lever with a pivot. | Use both clues. The answer is lever. |
| physics_11 | ru | prompt | Какое устройство качается вокруг опоры? | Мастерская. Один конец качелей-доски идёт вниз, другой вверх. Какой простой механизм использует опору? |
| physics_11 | ru | tip | Качели-доска — это рычаг с точкой опоры. | Учти обе подсказки. Ответ: рычаг. |
| physics_12 | de | prompt | Was lenkt ein Seil beim Hochziehen um? | Umlenken. Du ziehst ein Seil nach unten, die Last steigt hoch. Was kann die Zugrichtung ändern? |
| physics_12 | de | tip | Ein Seil läuft über eine Rolle. So kannst du nach unten ziehen. | Überlege beide Hinweise. Gesucht ist: Seilrolle. |
| physics_12 | en | prompt | What changes a rope's direction when lifting? | Direction. You pull a rope down and a load rises. What can change the pull direction? |
| physics_12 | en | tip | A rope runs over a pulley, so you can pull down to lift something. | Use both clues. The answer is pulley. |
| physics_12 | ru | prompt | Что меняет направление верёвки при подъёме? | Направление. Ты тянешь верёвку вниз, груз поднимается. Что меняет направление тяги? |
| physics_12 | ru | tip | Верёвка идёт через блок. Можно тянуть вниз, поднимая груз. | Учти обе подсказки. Ответ: блок. |
| physics_13 | de | prompt | Wodurch kannst du gut hindurchsehen? | Leuchten. Ein Fenster hält Wind ab, aber Licht soll hindurch. Welches Material erfüllt beides? |
| physics_13 | de | tip | Klares Glas lässt viel Licht hindurch. | Überlege beide Hinweise. Gesucht ist: Glas. |
| physics_13 | en | prompt | Which material can you see through clearly? | Light. A window blocks wind but must let light through. Which material does both? |
| physics_13 | en | tip | Clear glass lets lots of light through. | Use both clues. The answer is glass. |
| physics_13 | ru | prompt | Сквозь какой материал хорошо видно? | Свет. Окно задерживает ветер, но должно пропускать свет. Какой материал подходит для обоих условий? |
| physics_13 | ru | tip | Прозрачное стекло пропускает много света. | Учти обе подсказки. Ответ: стекло. |
| physics_14 | de | prompt | Welcher Baustoff kommt von Bäumen? | Ausprobieren. Ein Brett zeigt Jahresringe. Aus welchem Baustoff wurde es gesägt? |
| physics_14 | de | tip | Holz stammt aus den Stämmen und Ästen von Bäumen. | Überlege beide Hinweise. Gesucht ist: Holz. |
| physics_14 | en | prompt | Which building material comes from trees? | Experiment. A board shows growth rings. Which building material was sawn to make it? |
| physics_14 | en | tip | Wood comes from tree trunks and branches. | Use both clues. The answer is wood. |
| physics_14 | ru | prompt | Какой строительный материал получают из деревьев? | Опыт. На доске видны годичные кольца. Из какого материала её выпилили? |
| physics_14 | ru | tip | Древесину получают из стволов и веток деревьев. | Учти обе подсказки. Ответ: древесина. |
| physics_15 | de | prompt | Welches Material eignet sich für ein weiches Tuch? | Fühlen. Eine Hülle soll sich falten und an den Körper anschmiegen. Welches Material passt? |
| physics_15 | de | tip | Stoff ist biegsam und kann zu einem Tuch verarbeitet werden. | Überlege beide Hinweise. Gesucht ist: Stoff. |
| physics_15 | en | prompt | Which material makes a soft cloth? | Touch. A cover must fold and fit around the body. Which material fits? |
| physics_15 | en | tip | Fabric bends easily and can be made into a cloth. | Use both clues. The answer is fabric. |
| physics_15 | ru | prompt | Какой материал подходит для мягкой ткани? | Осязание. Покрытие должно складываться и облегать тело. Какой материал подходит? |
| physics_15 | ru | tip | Ткань легко сгибается. Из неё делают платки и полотенца. | Учти обе подсказки. Ответ: ткань. |
| physics_16 | de | prompt | Worauf kannst du einen Bauplan zeichnen? | Ausprobieren. Ein Plan muss beschreibbar und leicht zusammenfaltbar sein. Welches Material wählst du? |
| physics_16 | de | tip | Auf Papier kannst du deinen Plan zeichnen, bevor du baust. | Überlege beide Hinweise. Gesucht ist: Papier. |
| physics_16 | en | prompt | What can you draw a building plan on? | Experiment. A plan must be easy to draw on and fold. Which material do you choose? |
| physics_16 | en | tip | You can draw a plan on paper before you build. | Use both clues. The answer is paper. |
| physics_16 | ru | prompt | На чём можно нарисовать план постройки? | Опыт. На плане нужно рисовать, а потом легко его сложить. Какой материал выбрать? |
| physics_16 | ru | tip | На бумаге можно нарисовать план перед постройкой. | Учти обе подсказки. Ответ: бумага. |
| physics_17 | de | prompt | Was hilft dir, Norden zu finden? | Orientieren. Die Karte ist verdreht, Straßennamen fehlen. Welches Gerät hilft beim Ausrichten nach Norden? |
| physics_17 | de | tip | Die Magnetnadel im Kompass richtet sich ungefähr nach Norden aus. | Überlege beide Hinweise. Gesucht ist: Kompass. |
| physics_17 | en | prompt | What helps you find north? | Direction. The map is turned and street names are missing. Which instrument helps align it to north? |
| physics_17 | en | tip | A compass needle lines up roughly towards north. | Use both clues. The answer is compass. |
| physics_17 | ru | prompt | Что помогает найти север? | Ориентир. Карта повёрнута, названий улиц нет. Какой прибор поможет направить её на север? |
| physics_17 | ru | tip | Магнитная стрелка компаса указывает примерно на север. | Учти обе подсказки. Ответ: компас. |
| physics_18 | de | prompt | Was kann einen ruhenden Ball anschubsen? | Ausprobieren. Ein Ball ruht. Was kann ihn durch Berühren anschieben, statt nur am Himmel zu stehen? |
| physics_18 | de | tip | Eine Hand kann eine Kraft auf den Ball ausüben und ihn in Bewegung bringen. | Überlege beide Hinweise. Gesucht ist: Hand. |
| physics_18 | en | prompt | What can push a ball that is still? | Experiment. A ball is still. What can push it by contact rather than stay in the sky? |
| physics_18 | en | tip | A hand can exert a force on the ball and make it move. | Use both clues. The answer is hand. |
| physics_18 | ru | prompt | Что может толкнуть неподвижный мяч? | Опыт. Мяч неподвижен. Что может толкнуть его прикосновением, а не находится в небе? |
| physics_18 | ru | tip | Рука может подействовать на мяч с силой и привести его в движение. | Учти обе подсказки. Ответ: кисть. |
| physics_19 | de | prompt | Was entsteht, wenn Eis gerade schmilzt? | Verändern. Die Form eines Eiswürfels verschwindet beim Erwärmen. Welcher flüssige Stoff bleibt? |
| physics_19 | de | tip | Beim Schmelzen wird festes Eis zu flüssigem Wasser. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| physics_19 | en | prompt | What forms when ice is melting? | Change. An ice cube loses its shape when warmed. Which liquid remains? |
| physics_19 | en | tip | Melting changes solid ice into liquid water. | Use both clues. The answer is water. |
| physics_19 | ru | prompt | Что образуется, когда лёд тает? | Изменение. При нагревании кубик льда теряет форму. Какая жидкость остаётся? |
| physics_19 | ru | tip | При таянии твёрдый лёд становится жидкой водой. | Учти обе подсказки. Ответ: вода. |
| physics_20 | de | prompt | Was wirft im Lampenlicht einen deutlichen Schatten: Holz, klares Glas oder klares Wasser? | Leuchten. Licht trifft auf klares Glas, klares Wasser und Holz. Welches blockiert es am stärksten? |
| physics_20 | de | tip | Ein Holzklotz lässt Licht nicht hindurch. Dahinter entsteht ein deutlicher Schatten. | Überlege beide Hinweise. Gesucht ist: Holz. |
| physics_20 | en | prompt | What casts a clear shadow in lamp light: wood, clear glass or clear water? | Light. Light meets clear glass, clear water and wood. Which blocks it most? |
| physics_20 | en | tip | A wooden block blocks the light and casts a clear shadow. | Use both clues. The answer is wood. |
| physics_20 | ru | prompt | Что даёт отчётливую тень в свете лампы: дерево, прозрачное стекло или прозрачная вода? | Свет. Свет падает на прозрачное стекло, чистую воду и дерево. Что сильнее всего его задержит? |
| physics_20 | ru | tip | Деревянный брусок не пропускает свет. За ним появляется отчётливая тень. | Учти обе подсказки. Ответ: древесина. |
| physics_21 | de | prompt | Was schwimmt meist: ein leichtes trockenes Holzstück, ein Eisenklotz oder Sand? | Verändern. Eisen sinkt, Sandkörner sinken. Was schwimmt häufig, wenn es trocken und leicht ist? |
| physics_21 | de | tip | Viele leichte Holzarten schwimmen auf Wasser. Ein massiver Eisenklotz sinkt. | Überlege beide Hinweise. Gesucht ist: Holz. |
| physics_21 | en | prompt | What usually floats: a light dry piece of wood, an iron block or sand? | Change. Iron sinks and sand grains sink. What often floats when dry and light? |
| physics_21 | en | tip | Many light woods float in water. A solid iron block sinks. | Use both clues. The answer is wood. |
| physics_21 | ru | prompt | Что обычно плавает: лёгкая сухая деревяшка, железный брусок или песок? | Изменение. Железо тонет, песчинки тонут. Что часто плавает, если сухое и лёгкое? |
| physics_21 | ru | tip | Многие лёгкие породы дерева плавают в воде. Сплошной железный брусок тонет. | Учти обе подсказки. Ответ: древесина. |
| physics_22 | de | prompt | Wodurch kann Licht gut hindurchscheinen? | Leuchten. Du willst eine Lampe durch eine feste Scheibe sehen. Welches Material lässt das Licht gut durch? |
| physics_22 | de | tip | Klares Glas ist durchsichtig. Ein Eisenklotz und ein Holzklotz sind es nicht. | Überlege beide Hinweise. Gesucht ist: Glas. |
| physics_22 | en | prompt | Which material lets light pass through clearly? | Light. You want to see a lamp through a solid pane. Which material lets light pass well? |
| physics_22 | en | tip | Clear glass is transparent. Iron blocks and wood blocks are not. | Use both clues. The answer is glass. |
| physics_22 | ru | prompt | Какой материал хорошо пропускает свет? | Свет. Нужно увидеть лампу через твёрдую пластину. Какой материал хорошо пропускает свет? |
| physics_22 | ru | tip | Прозрачное стекло пропускает свет. Железный и деревянный бруски непрозрачны. | Учти обе подсказки. Ответ: стекло. |
| physics_23 | de | prompt | Welcher Körperteil nimmt Schallwellen wahr? | Hören. Eine Klingel bewegt Luft in Schwingungen. Welcher Körperteil empfängt diese Schwingungen? |
| physics_23 | de | tip | Deine Ohren nehmen Schwingungen der Luft als Schall wahr. | Überlege beide Hinweise. Gesucht ist: Ohr. |
| physics_23 | en | prompt | Which body part detects sound waves? | Hearing. A bell makes air vibrate. Which body part receives these vibrations? |
| physics_23 | en | tip | Your ears detect vibrations travelling through the air as sound. | Use both clues. The answer is ear. |
| physics_23 | ru | prompt | Какая часть тела воспринимает звуковые волны? | Слух. Звонок заставляет воздух колебаться. Какая часть тела воспринимает эти колебания? |
| physics_23 | ru | tip | Уши воспринимают распространяющиеся в воздухе колебания как звук. | Учти обе подсказки. Ответ: ухо. |
| physics_24 | de | prompt | Was dämpft Klopfgeräusche auf einem Tisch am besten: ein weiches Tuch, Glas oder Eisen? | Fühlen. Ein Spielzeug klopft auf den Tisch. Welche weiche Unterlage dämpft eher als Glas oder Eisen? |
| physics_24 | de | tip | Ein weiches Tuch kann Schwingungen und Klopfgeräusche dämpfen. | Überlege beide Hinweise. Gesucht ist: Stoff. |
| physics_24 | en | prompt | What best softens tapping sounds on a table: a soft cloth, glass or iron? | Touch. A toy taps on a table. Which soft layer cushions it better than glass or iron? |
| physics_24 | en | tip | A soft cloth can damp vibrations and tapping sounds. | Use both clues. The answer is fabric. |
| physics_24 | ru | prompt | Что лучше приглушает стук по столу: мягкая ткань, стекло или железо? | Осязание. Игрушка стучит по столу. Какая мягкая подкладка приглушит звук лучше стекла или железа? |
| physics_24 | ru | tip | Мягкая ткань может ослаблять колебания и приглушать стук. | Учти обе подсказки. Ответ: ткань. |
| physics_25 | de | prompt | Was erzeugt selbst Licht: Sonne, Mond oder Wolke? | Leuchten. Der Mond reflektiert nur Licht. Welcher Himmelskörper erzeugt das Licht selbst? |
| physics_25 | de | tip | Die Sonne leuchtet selbst. Der Mond und Wolken reflektieren Licht. | Überlege beide Hinweise. Gesucht ist: Sonne. |
| physics_25 | en | prompt | Which makes its own light: the sun, the moon or a cloud? | Light. The Moon only reflects light. Which celestial body makes the light itself? |
| physics_25 | en | tip | The sun gives off its own light. The moon and clouds reflect light. | Use both clues. The answer is sun. |
| physics_25 | ru | prompt | Что само создаёт свет: Солнце, Луна или облако? | Свет. Луна только отражает свет. Какое небесное тело само его излучает? |
| physics_25 | ru | tip | Солнце излучает собственный свет. Луна и облака отражают свет. | Учти обе подсказки. Ответ: Солнце. |
| physics_26 | de | prompt | Welcher dieser Stoffe hat eine feste eigene Form? | Verändern. Drei Stoffe liegen auf einem Teller. Welcher behält zunächst eine feste Form: Öl, Wasser oder Eis? |
| physics_26 | de | tip | Ein Eiswürfel ist fest. Flüssigkeiten wie Wasser und Öl passen sich dem Gefäß an. | Überlege beide Hinweise. Gesucht ist: Eis. |
| physics_26 | en | prompt | Which of these has its own solid shape? | Change. Three substances are on a plate. Which keeps a solid shape at first: oil, water or ice? |
| physics_26 | en | tip | An ice cube is solid. Liquids such as water and oil take the shape of their container. | Use both clues. The answer is ice. |
| physics_26 | ru | prompt | Что из этого имеет собственную твёрдую форму? | Изменение. Три вещества на тарелке. Что сначала сохраняет твёрдую форму: масло, вода или лёд? |
| physics_26 | ru | tip | Кубик льда твёрдый. Вода и масло принимают форму ёмкости. | Учти обе подсказки. Ответ: лёд. |
| physics_27 | de | prompt | Was entsteht unsichtbar, wenn Wasser verdunstet? | Verwandeln. Eine Pfütze wird kleiner, obwohl kein Wasser abfließt. In welchen unsichtbaren Zustand geht Wasser über? |
| physics_27 | de | tip | Es entsteht unsichtbarer Wasserdampf. Die weiße Wolke im Spiel ist nur ein Zeichen dafür. | Überlege beide Hinweise. Gesucht ist: Wasserdampf. |
| physics_27 | en | prompt | What forms invisibly when water evaporates? | Changing. A puddle shrinks without draining. Which invisible state does its water become? |
| physics_27 | en | tip | Invisible water vapour forms. The white cloud in the game is only a symbol. | Use both clues. The answer is water vapour. |
| physics_27 | ru | prompt | Что незаметно образуется, когда вода испаряется? | Превращение. Лужа уменьшается, хотя вода не стекает. В какое невидимое состояние переходит вода? |
| physics_27 | ru | tip | Образуется невидимый водяной пар. Белое облачко в игре — только условный значок. | Учти обе подсказки. Ответ: водяной пар. |
| physics_28 | de | prompt | Was gibt Licht und Wärme ab, durch die Eis draußen schmelzen kann? | Leuchten. Zwei Eisstücke liegen draußen. Eines bekommt mehr Sonnenlicht. Welcher Himmelskörper liefert die Wärme? |
| physics_28 | de | tip | Die Sonne liefert Energie. Wenn Eis warm genug wird, schmilzt es. | Überlege beide Hinweise. Gesucht ist: Sonne. |
| physics_28 | en | prompt | What gives off light and warmth that can melt ice outdoors? | Light. Two ice pieces are outside. One gets more sunlight. Which celestial body provides the warmth? |
| physics_28 | en | tip | The sun supplies energy. Ice melts when it warms enough. | Use both clues. The answer is sun. |
| physics_28 | ru | prompt | Что излучает свет и тепло, от которых лёд на улице может растаять? | Свет. Два кусочка льда снаружи. На один падает больше солнечного света. Какое небесное тело даёт тепло? |
| physics_28 | ru | tip | Солнце даёт энергию. При достаточном нагревании лёд тает. | Учти обе подсказки. Ответ: Солнце. |
| physics_29 | de | prompt | Was zeigt Straßen und Wege als Zeichnung? | Orientieren. Du brauchst die gezeichnete Form der Straßen, nicht bloß Norden. Was hilft beim Planen des Weges? |
| physics_29 | de | tip | Eine Karte zeigt Wege von oben in verkleinerter Form. | Überlege beide Hinweise. Gesucht ist: Karte. |
| physics_29 | en | prompt | What shows roads and paths in a drawing? | Direction. You need the drawn shape of streets, not just north. What helps plan the route? |
| physics_29 | en | tip | A map shows paths from above on a smaller scale. | Use both clues. The answer is map. |
| physics_29 | ru | prompt | Что показывает дороги и тропинки на рисунке? | Ориентир. Нужна нарисованная сеть улиц, а не только север. Что поможет спланировать путь? |
| physics_29 | ru | tip | Карта показывает пути сверху в уменьшенном виде. | Учти обе подсказки. Ответ: карта. |
| physics_30 | de | prompt | Womit hörst du, ob eine Fahrradklingel klingelt? | Hören. Du hörst eine Klingel, obwohl eine Wand sie verdeckt. Was empfängt den Schall? |
| physics_30 | de | tip | Deine Ohren nehmen den Klang der Klingel wahr. | Überlege beide Hinweise. Gesucht ist: Ohr. |
| physics_30 | en | prompt | How do you hear a bicycle bell? | Hearing. You hear a bell although a wall hides it. What receives the sound? |
| physics_30 | en | tip | Your ears detect the sound of the bell. | Use both clues. The answer is ear. |
| physics_30 | ru | prompt | Чем ты слышишь велосипедный звонок? | Слух. Ты слышишь звонок, хотя его закрывает стена. Что воспринимает звук? |
| physics_30 | ru | tip | Уши воспринимают звук звонка. | Учти обе подсказки. Ответ: ухо. |
| physics_31 | de | prompt | Welches Material ist für eine stabile Fahrrad-Radachse üblich? | Bewegen. Eine Radachse trägt viel Last und darf nicht weich nachgeben. Welcher Werkstoff ist üblich? |
| physics_31 | de | tip | Eine Achse aus Metall kann ein Rad tragen und führen. | Überlege beide Hinweise. Gesucht ist: Eisen. |
| physics_31 | en | prompt | Which material is normally used for a strong bicycle wheel axle? | Motion. A wheel axle carries heavy loads and must not bend softly. Which material is usual? |
| physics_31 | en | tip | A metal axle can support and guide a wheel. | Use both clues. The answer is iron. |
| physics_31 | ru | prompt | Из какого материала обычно делают прочную ось велосипедного колеса? | Движение. Ось колеса несёт большую нагрузку и не должна быть мягкой. Какой материал обычно используют? |
| physics_31 | ru | tip | Металлическая ось удерживает колесо и направляет его вращение. | Учти обе подсказки. Ответ: железо. |
| physics_32 | de | prompt | Welches Bauwerk braucht tragfähige Stützen? | Ausprobieren. Ein Weg führt über eine Lücke. Welches Bauwerk muss dort Lasten an Stützen weitergeben? |
| physics_32 | de | tip | Eine Brücke braucht ein tragfähiges Gerüst und passende Stützen. | Überlege beide Hinweise. Gesucht ist: Brücke. |
| physics_32 | en | prompt | Which structure needs strong supports? | Experiment. A road crosses a gap. Which structure must pass its loads to supports? |
| physics_32 | en | tip | A bridge needs a strong structure and suitable supports. | Use both clues. The answer is bridge. |
| physics_32 | ru | prompt | Какому сооружению нужны прочные опоры? | Опыт. Дорога проходит над разрывом. Какое сооружение должно передавать нагрузку опорам? |
| physics_32 | ru | tip | Мосту нужны прочная конструкция и подходящие опоры. | Учти обе подсказки. Ответ: мост. |
| physics_33 | de | prompt | Was nimmt Wasser beim Abtrocknen gut auf: Stoff, Glas oder Eisen? | Verändern. Wassertropfen sollen in viele kleine Zwischenräume ziehen. Was eignet sich zum Abtrocknen? |
| physics_33 | de | tip | Zwischen den Fasern eines saugfähigen Tuchs kann Wasser aufgenommen werden. | Überlege beide Hinweise. Gesucht ist: Stoff. |
| physics_33 | en | prompt | What soaks up water well when drying: fabric, glass or iron? | Change. Water drops should enter many tiny gaps. What is suitable for drying? |
| physics_33 | en | tip | An absorbent cloth holds water between its fibres. | Use both clues. The answer is fabric. |
| physics_33 | ru | prompt | Что хорошо впитывает воду при вытирании: ткань, стекло или железо? | Изменение. Капли воды должны попасть во множество маленьких промежутков. Что подходит для вытирания? |
| physics_33 | ru | tip | Впитывающая ткань удерживает воду между волокнами. | Учти обе подсказки. Ответ: ткань. |
| physics_34 | de | prompt | Was kann eine Solarzelle mit Energie versorgen? | Versorgen. Eine Solarzelle braucht Licht, keine Batterie im Fach. Welcher Himmelskörper kann sie versorgen? |
| physics_34 | de | tip | Eine Solarzelle wandelt Licht von der Sonne in elektrische Energie um. | Überlege beide Hinweise. Gesucht ist: Sonne. |
| physics_34 | en | prompt | What supplies energy to a solar cell? | Power. A solar cell needs light, not a battery inside. Which celestial body can power it? |
| physics_34 | en | tip | A solar cell turns sunlight into electrical energy. | Use both clues. The answer is sun. |
| physics_34 | ru | prompt | Что даёт энергию солнечной батарее? | Энергия. Солнечному элементу нужен свет, а не батарейка. Какое небесное тело может дать ему энергию? |
| physics_34 | ru | tip | Солнечная батарея превращает солнечный свет в электрическую энергию. | Учти обе подсказки. Ответ: Солнце. |
| physics_35 | de | prompt | Was dreht sich an einem fahrenden Fahrrad? | Bewegen. Das Fahrrad bewegt sich vorwärts. Welcher Teil dreht sich dabei um seine Achse? |
| physics_35 | de | tip | Die Räder drehen sich, während sich das Fahrrad vorwärts bewegt. | Überlege beide Hinweise. Gesucht ist: Rad. |
| physics_35 | en | prompt | What turns on a moving bicycle? | Motion. A bicycle moves forward. Which part turns about its axle? |
| physics_35 | en | tip | The wheels turn as the bicycle moves forward. | Use both clues. The answer is wheel. |
| physics_35 | ru | prompt | Что вращается у едущего велосипеда? | Движение. Велосипед едет вперёд. Какая часть при этом вращается вокруг оси? |
| physics_35 | ru | tip | Когда велосипед движется вперёд, его колёса вращаются. | Учти обе подсказки. Ответ: колесо. |
| physics_36 | de | prompt | Woraus besteht eine durchsichtige Fensterscheibe? | Leuchten. Eine Scheibe muss fest sein und trotzdem den Blick nach draußen erlauben. Welcher Werkstoff passt? |
| physics_36 | de | tip | Klares Glas lässt viel Licht in einen Raum hinein. | Überlege beide Hinweise. Gesucht ist: Glas. |
| physics_36 | en | prompt | What is a transparent window pane made of? | Light. A pane must be solid yet allow a view outside. Which material fits? |
| physics_36 | en | tip | Clear glass lets plenty of light into a room. | Use both clues. The answer is glass. |
| physics_36 | ru | prompt | Из чего делают прозрачное оконное стекло? | Свет. Пластина должна быть твёрдой, но через неё нужно видеть улицу. Какой материал подходит? |
| physics_36 | ru | tip | Прозрачное стекло пропускает в комнату много света. | Учти обе подсказки. Ответ: стекло. |
| physics_37 | de | prompt | Welches Material kannst du mit einer Stoffschere schneiden? | Werkeln. Du willst einen weichen gewebten Stoff kürzen. Welchen Werkstoff schneidet eine Stoffschere? |
| physics_37 | de | tip | Eine Stoffschere schneidet Stoff. Glas und einen Eisenblock schneidet sie nicht. | Überlege beide Hinweise. Gesucht ist: Stoff. |
| physics_37 | en | prompt | Which material can fabric scissors cut? | Making. You want to shorten a soft woven sheet. Which material does a fabric scissors cut? |
| physics_37 | en | tip | Fabric scissors cut fabric. They do not cut glass or an iron block. | Use both clues. The answer is fabric. |
| physics_37 | ru | prompt | Какой материал можно разрезать ножницами для ткани? | Мастерская. Нужно укоротить мягкое тканое полотно. Какой материал режут портновскими ножницами? |
| physics_37 | ru | tip | Ножницы для ткани режут ткань. Они не режут стекло или железный брусок. | Учти обе подсказки. Ответ: ткань. |
| physics_38 | de | prompt | Welcher Teil einer Seilrolle dreht sich? | Bewegen. Das Seil einer Seilrolle bewegt sich weiter. Welcher runde Teil dreht sich darunter mit? |
| physics_38 | de | tip | Das runde Rad der Rolle dreht sich mit dem Seil. | Überlege beide Hinweise. Gesucht ist: Rad. |
| physics_38 | en | prompt | Which part of a pulley turns? | Motion. The rope of a pulley moves along. Which round part turns beneath it? |
| physics_38 | en | tip | The pulley's round wheel turns as the rope moves. | Use both clues. The answer is wheel. |
| physics_38 | ru | prompt | Какая часть блока вращается? | Движение. Верёвка блока движется дальше. Какая круглая деталь вращается под ней? |
| physics_38 | ru | tip | Круглое колесо блока вращается вместе с движением верёвки. | Учти обе подсказки. Ответ: колесо. |
| physics_39 | de | prompt | Was gehört in das Batteriefach einer Spielzeuglampe? | Versorgen. Eine Lampe soll ohne Steckdose funktionieren. Was gehört als Energiequelle ins Fach? |
| physics_39 | de | tip | Nur passende Batterien gehören hinein. Ein Erwachsener hilft beim Wechseln. | Überlege beide Hinweise. Gesucht ist: Batterie. |
| physics_39 | en | prompt | What goes in a toy lamp's battery compartment? | Power. A lamp must work without a wall socket. What goes into its compartment as a power source? |
| physics_39 | en | tip | Only the correct batteries go there. An adult helps replace them. | Use both clues. The answer is battery. |
| physics_39 | ru | prompt | Что кладут в отсек питания игрушечного фонарика? | Питать. Лампа должна работать без розетки. Что кладут в отсек как источник энергии? |
| physics_39 | ru | tip | Туда кладут только подходящие батарейки. Взрослый помогает их менять. | Учти обе подсказки. Ответ: батарейка. |
| physics_40 | de | prompt | Was hat einen Nordpol und einen Südpol? | Ausprobieren. Ein Gegenstand zieht Eisen ohne Berührung an. Was besitzt dafür einen Nordpol und Südpol? |
| physics_40 | de | tip | Ein Magnet hat zwei Pole. Gleiche Pole stoßen sich ab. | Überlege beide Hinweise. Gesucht ist: Magnet. |
| physics_40 | en | prompt | What has a north pole and a south pole? | Experiment. An object attracts iron without touching it. What has a north and south pole for this? |
| physics_40 | en | tip | A magnet has two poles. Matching poles repel each other. | Use both clues. The answer is magnet. |
| physics_40 | ru | prompt | У чего есть северный и южный полюс? | Опыт. Предмет притягивает железо без прикосновения. Что имеет для этого северный и южный полюс? |
| physics_40 | ru | tip | У магнита два полюса. Одинаковые полюса отталкиваются. | Учти обе подсказки. Ответ: магнит. |
| biology_01 | de | prompt | Wo kann ein Fisch mit Kiemen atmen? | Entwickeln. Ein Fisch braucht Sauerstoff, atmet aber mit Kiemen. Worin muss er dafür bleiben? |
| biology_01 | de | tip | Fische nehmen mit ihren Kiemen Sauerstoff aus dem Wasser auf. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| biology_01 | en | prompt | Where can a fish breathe with gills? | Life. A fish needs oxygen but breathes using gills. What must it stay in? |
| biology_01 | en | tip | Fish use gills to take oxygen from water. | Use both clues. The answer is water. |
| biology_01 | ru | prompt | Где рыба дышит жабрами? | Жизнь. Рыбе нужен кислород, но она дышит жабрами. В чём ей нужно оставаться? |
| biology_01 | ru | tip | Рыбы получают кислород из воды с помощью жабр. | Учти обе подсказки. Ответ: вода. |
| biology_02 | de | prompt | Wo brütet ein Amselvogel seine Eier aus? | Entwickeln. Eine Amsel sammelt Halme, bevor sie Eier legt. Welcher geschützte Ort entsteht? |
| biology_02 | de | tip | Amseln bauen Nester für ihre Eier und Jungvögel. | Überlege beide Hinweise. Gesucht ist: Nest. |
| biology_02 | en | prompt | Where does a blackbird hatch its eggs? | Life. A blackbird gathers grass before laying eggs. Which sheltered place is made? |
| biology_02 | en | tip | Blackbirds build nests for their eggs and chicks. | Use both clues. The answer is nest. |
| biology_02 | ru | prompt | Где дрозд высиживает яйца? | Жизнь. Дрозд собирает травинки до откладки яиц. Какое защищённое место получается? |
| biology_02 | ru | tip | Дрозды строят гнёзда для яиц и птенцов. | Учти обе подсказки. Ответ: гнездо. |
| biology_03 | de | prompt | Wo findet eine Biene Nektar? | Wachsen. Eine Biene sucht süßen Nektar. Welcher Pflanzenteil lockt sie dafür an? |
| biology_03 | de | tip | Viele Blüten enthalten Nektar, den Bienen sammeln. | Überlege beide Hinweise. Gesucht ist: Blume. |
| biology_03 | en | prompt | Where does a bee find nectar? | Growing. A bee seeks sweet nectar. Which plant part attracts it for this? |
| biology_03 | en | tip | Many flowers contain nectar that bees collect. | Use both clues. The answer is flower. |
| biology_03 | ru | prompt | Где пчела находит нектар? | Рост. Пчела ищет сладкий нектар. Какая часть растения её привлекает? |
| biology_03 | ru | tip | Во многих цветках есть нектар, который собирают пчёлы. | Учти обе подсказки. Ответ: цветок. |
| biology_04 | de | prompt | Womit nimmt ein Baum Wasser aus dem Boden auf? | Verwandeln. Wasser ist im Boden, Blätter sind oben. Welcher Teil nimmt das Wasser zuerst auf? |
| biology_04 | de | tip | Die Wurzeln nehmen Wasser aus dem Boden auf. | Überlege beide Hinweise. Gesucht ist: Wurzeln. |
| biology_04 | en | prompt | What takes water from the soil into a tree? | Changing. Water is in soil and leaves are above. Which part takes the water in first? |
| biology_04 | en | tip | Roots take water from the soil. | Use both clues. The answer is roots. |
| biology_04 | ru | prompt | Чем дерево впитывает воду из земли? | Превращение. Вода в почве, листья наверху. Какая часть первой получает воду? |
| biology_04 | ru | tip | Корни впитывают воду из почвы. | Учти обе подсказки. Ответ: корни. |
| biology_05 | de | prompt | Was braucht ein Samen zum Keimen? | Wachsen. Ein Samen liegt warm, aber ganz trocken. Was fehlt ihm zum Keimen? |
| biology_05 | de | tip | Viele Samen brauchen Wasser, Luft und passende Wärme zum Keimen. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| biology_05 | en | prompt | What does a seed need to start growing? | Growing. A seed is warm but completely dry. What is missing for germination? |
| biology_05 | en | tip | Many seeds need water, air and suitable warmth to germinate. | Use both clues. The answer is water. |
| biology_05 | ru | prompt | Что нужно семени для прорастания? | Рост. Семя в тепле, но совершенно сухое. Чего не хватает для прорастания? |
| biology_05 | ru | tip | Многим семенам для прорастания нужны вода, воздух и подходящее тепло. | Учти обе подсказки. Ответ: вода. |
| biology_06 | de | prompt | Was liefert einer grünen Pflanze Licht zum Wachsen? | Leuchten. Eine grüne Pflanze hat Wasser, steht aber im Dunkeln. Welche natürliche Lichtquelle fehlt? |
| biology_06 | de | tip | Grüne Pflanzen nutzen Sonnenlicht, um Nahrung herzustellen. | Überlege beide Hinweise. Gesucht ist: Sonne. |
| biology_06 | en | prompt | What gives a green plant light to grow? | Light. A green plant has water but stands in darkness. Which natural light source is missing? |
| biology_06 | en | tip | Green plants use sunlight to make food. | Use both clues. The answer is sun. |
| biology_06 | ru | prompt | Что даёт зелёному растению свет для роста? | Свет. У зелёного растения есть вода, но оно в темноте. Какого естественного источника света не хватает? |
| biology_06 | ru | tip | Зелёные растения используют солнечный свет, чтобы создавать питание. | Учти обе подсказки. Ответ: Солнце. |
| biology_07 | de | prompt | Welches Tier entsteht aus einer Raupe? | Entwickeln. Erst frisst die Raupe, dann bildet sie eine Puppe. Welches erwachsene Tier folgt? |
| biology_07 | de | tip | Eine Raupe wird zur Puppe. Daraus schlüpft ein Schmetterling. | Überlege beide Hinweise. Gesucht ist: Schmetterling. |
| biology_07 | en | prompt | Which animal develops from a caterpillar? | Life. First a caterpillar feeds, then forms a chrysalis. Which adult animal follows? |
| biology_07 | en | tip | A caterpillar becomes a pupa. A butterfly emerges from it. | Use both clues. The answer is butterfly. |
| biology_07 | ru | prompt | Какое животное вырастает из гусеницы? | Жизнь. Сначала гусеница ест, потом становится куколкой. Какое взрослое животное появляется дальше? |
| biology_07 | ru | tip | Гусеница становится куколкой. Из куколки выходит бабочка. | Учти обе подсказки. Ответ: бабочка. |
| biology_08 | de | prompt | Welches Tier wächst aus einer Kaulquappe heran? | Entwickeln. Ein Jungtier verliert seinen Schwanz und bekommt Beine. Wer entwickelt sich aus der Kaulquappe? |
| biology_08 | de | tip | Aus einer Froschkaulquappe wächst ein Frosch mit Beinen. | Überlege beide Hinweise. Gesucht ist: Frosch. |
| biology_08 | en | prompt | Which animal grows from a tadpole? | Life. A young animal loses its tail and grows legs. What develops from the tadpole? |
| biology_08 | en | tip | A frog tadpole develops into a frog with legs. | Use both clues. The answer is frog. |
| biology_08 | ru | prompt | Кто вырастает из головастика? | Жизнь. У детёныша исчезает хвост и вырастают ноги. Кто развивается из головастика? |
| biology_08 | ru | tip | Из головастика лягушки вырастает лягушка с лапами. | Учти обе подсказки. Ответ: лягушка. |
| biology_09 | de | prompt | Wer kann aus einem Hühnerei schlüpfen? | Entwickeln. Im Hühnerei wächst ein Küken. Zu welcher gezeigten Tiergruppe gehört es? |
| biology_09 | de | tip | Aus einem befruchteten und bebrüteten Hühnerei kann ein Küken schlüpfen. | Überlege beide Hinweise. Gesucht ist: Vogel. |
| biology_09 | en | prompt | What can hatch from a hen's egg? | Life. A chick grows inside a chicken egg. Which pictured animal group does it belong to? |
| biology_09 | en | tip | A chick can hatch from a fertilised hen's egg that is kept warm. | Use both clues. The answer is bird. |
| biology_09 | ru | prompt | Кто может вылупиться из куриного яйца? | Жизнь. В курином яйце растёт цыплёнок. К какой показанной группе животных он относится? |
| biology_09 | ru | tip | Из оплодотворённого куриного яйца при высиживании может появиться цыплёнок. | Учти обе подсказки. Ответ: птица. |
| biology_10 | de | prompt | Welches Tier ist ein Säugetier? | Entwickeln. Ein Jungtier bekommt Milch von seiner Mutter statt Nektar. Welches Tier passt? |
| biology_10 | de | tip | Katzenmütter säugen ihre Jungen mit Milch. | Überlege beide Hinweise. Gesucht ist: Katze. |
| biology_10 | en | prompt | Which animal is a mammal? | Life. A young animal receives its mother's milk instead of nectar. Which animal fits? |
| biology_10 | en | tip | Mother cats feed their kittens with milk. | Use both clues. The answer is cat. |
| biology_10 | ru | prompt | Кто из них млекопитающее? | Жизнь. Детёныш получает материнское молоко, а не нектар. Какое животное подходит? |
| biology_10 | ru | tip | Кошки кормят котят молоком. | Учти обе подсказки. Ответ: кошка. |
| biology_11 | de | prompt | Wer hat Federn? | Entwickeln. Nicht jedes Tier mit Flügeln hat Federn. Welches dieser Tiere besitzt Federn? |
| biology_11 | de | tip | Vögel haben Federn. Sie helfen zum Beispiel beim Warmhalten. | Überlege beide Hinweise. Gesucht ist: Vogel. |
| biology_11 | en | prompt | Which animal has feathers? | Life. Not every winged animal has feathers. Which of these animals has feathers? |
| biology_11 | en | tip | Birds have feathers, which help keep them warm. | Use both clues. The answer is bird. |
| biology_11 | ru | prompt | У кого есть перья? | Жизнь. Не у каждого крылатого животного есть перья. У кого из этих животных они есть? |
| biology_11 | ru | tip | У птиц есть перья. Они помогают сохранять тепло. | Учти обе подсказки. Ответ: птица. |
| biology_12 | de | prompt | Wer trägt einen festen Panzer? | Entwickeln. Ein Tier schlüpft bereits mit einem Rückenpanzer. Welches Tier passt? |
| biology_12 | de | tip | Eine Schildkröte trägt einen Panzer, der zum Körper gehört. | Überlege beide Hinweise. Gesucht ist: Schildkröte. |
| biology_12 | en | prompt | Which animal has a hard shell? | Life. An animal hatches already wearing a shell on its back. Which fits? |
| biology_12 | en | tip | A turtle has a shell that is part of its body. | Use both clues. The answer is turtle. |
| biology_12 | ru | prompt | У кого есть твёрдый панцирь? | Жизнь. Животное вылупляется уже с панцирем на спине. Кто подходит? |
| biology_12 | ru | tip | Панцирь черепахи — часть её тела. | Учти обе подсказки. Ответ: черепаха. |
| biology_13 | de | prompt | Welches Tier lockert Erde beim Graben? | Entwickeln. Gänge entstehen ohne Schaufel und Beine. Welches Tier lockert so die Erde? |
| biology_13 | de | tip | Regenwürmer graben Gänge in der Erde. | Überlege beide Hinweise. Gesucht ist: Regenwurm. |
| biology_13 | en | prompt | Which animal loosens soil as it burrows? | Life. Tunnels form without a spade or legs. Which animal loosens soil this way? |
| biology_13 | en | tip | Earthworms make tunnels in the soil. | Use both clues. The answer is earthworm. |
| biology_13 | ru | prompt | Кто рыхлит землю, прокладывая ходы? | Жизнь. Ходы появляются без лопаты и ног. Кто так рыхлит почву? |
| biology_13 | ru | tip | Дождевые черви прокладывают ходы в почве. | Учти обе подсказки. Ответ: дождевой червь. |
| biology_14 | de | prompt | Woraus kann ein neuer Apfelbaum wachsen? | Entwickeln. Im Apfel steckt der Anfang einer neuen Pflanze. Was kann keimen? |
| biology_14 | de | tip | In einem Apfel stecken Kerne. Daraus können neue Bäume wachsen. | Überlege beide Hinweise. Gesucht ist: Samen. |
| biology_14 | en | prompt | What can grow into a new apple tree? | Life. An apple contains the start of a new plant. What can germinate? |
| biology_14 | en | tip | An apple contains seeds that can grow into new trees. | Use both clues. The answer is seed. |
| biology_14 | ru | prompt | Из чего может вырасти новая яблоня? | Жизнь. В яблоке есть начало нового растения. Что может прорасти? |
| biology_14 | ru | tip | В яблоке есть семена. Из них могут вырасти новые деревья. | Учти обе подсказки. Ответ: семя. |
| biology_15 | de | prompt | Wer kann Blüten bestäuben? | Wachsen. Blütenstaub bleibt an einem Tier hängen und reist zur nächsten Blüte. Wer hilft so bei der Bestäubung? |
| biology_15 | de | tip | Bienen tragen Blütenstaub von einer Blüte zur nächsten. | Überlege beide Hinweise. Gesucht ist: Biene. |
| biology_15 | en | prompt | Which animal can pollinate flowers? | Growing. Pollen sticks to an animal and travels to another flower. Who helps pollinate this way? |
| biology_15 | en | tip | Bees carry pollen from one flower to another. | Use both clues. The answer is bee. |
| biology_15 | ru | prompt | Кто может опылять цветки? | Рост. Пыльца прилипает к животному и попадает на другой цветок. Кто так помогает опылению? |
| biology_15 | ru | tip | Пчёлы переносят пыльцу с цветка на цветок. | Учти обе подсказки. Ответ: пчела. |
| biology_16 | de | prompt | Welche grünen Pflanzenteile bilden hier die Baumkrone? | Wachsen. Wurzeln sind im Dunkeln. Welche grünen Teile oben fangen viel Licht auf? |
| biology_16 | de | tip | Viele Bäume tragen Blätter, die Licht aufnehmen. | Überlege beide Hinweise. Gesucht ist: Blatt. |
| biology_16 | en | prompt | Which green plant parts form the tree crown here? | Growing. Roots are in darkness. Which green parts above collect lots of light? |
| biology_16 | en | tip | Many trees have leaves that absorb light. | Use both clues. The answer is leaf. |
| biology_16 | ru | prompt | Какие зелёные части растения образуют здесь крону дерева? | Рост. Корни в темноте. Какие зелёные части наверху улавливают много света? |
| biology_16 | ru | tip | У многих деревьев листья поглощают свет. | Учти обе подсказки. Ответ: лист. |
| biology_17 | de | prompt | Was ist ein Pilz und keine Pflanze? | Wachsen. Es wächst ohne grüne Blätter und ist weder Tier noch Pflanze. Was gehört zu einem eigenen Reich? |
| biology_17 | de | tip | Pilze bilden eine eigene Gruppe. Unbekannte Pilze nie essen. | Überlege beide Hinweise. Gesucht ist: Pilz. |
| biology_17 | en | prompt | Which is a fungus rather than a plant? | Growing. It grows without green leaves and is neither animal nor plant. What belongs to its own kingdom? |
| biology_17 | en | tip | Fungi form their own group. Never eat an unknown mushroom. | Use both clues. The answer is mushroom. |
| biology_17 | ru | prompt | Что относится к грибам, а не к растениям? | Рост. Растёт без зелёных листьев, не является ни животным, ни растением. Что относится к отдельному царству? |
| biology_17 | ru | tip | Грибы — отдельная группа живых существ. Незнакомые грибы нельзя есть. | Учти обе подсказки. Ответ: гриб. |
| biology_18 | de | prompt | Was braucht eine Katze täglich zum Trinken? | Trinken. Eine Katze verliert Flüssigkeit beim Atmen. Was braucht sie deshalb täglich im Napf? |
| biology_18 | de | tip | Katzen brauchen frisches Wasser zum Trinken. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| biology_18 | en | prompt | What does a cat need to drink every day? | Drink. A cat loses fluid through breathing. What does it therefore need in its bowl daily? |
| biology_18 | en | tip | Cats need fresh drinking water. | Use both clues. The answer is water. |
| biology_18 | ru | prompt | Что кошке нужно пить каждый день? | Пить. Кошка теряет жидкость при дыхании. Что поэтому нужно ежедневно в миске? |
| biology_18 | ru | tip | Кошкам нужна свежая питьевая вода. | Учти обе подсказки. Ответ: вода. |
| biology_19 | de | prompt | Was frisst eine Amsel zum Beispiel? | Entwickeln. Nach Regen sucht eine Amsel im Boden nach weichen Tieren ohne Beine. Welche Beute passt? |
| biology_19 | de | tip | Amseln fressen unter anderem Regenwürmer und Beeren. | Überlege beide Hinweise. Gesucht ist: Regenwurm. |
| biology_19 | en | prompt | What might a blackbird eat? | Life. After rain a blackbird searches soil for soft legless animals. Which prey fits? |
| biology_19 | en | tip | Blackbirds eat earthworms and berries, among other foods. | Use both clues. The answer is earthworm. |
| biology_19 | ru | prompt | Что, например, ест дрозд? | Жизнь. После дождя дрозд ищет в земле мягких животных без ног. Какая добыча подходит? |
| biology_19 | ru | tip | Дрозды едят дождевых червей и ягоды, а также другую пищу. | Учти обе подсказки. Ответ: дождевой червь. |
| biology_20 | de | prompt | Wo kann ein Schmetterling Nektar trinken? | Wachsen. Ein Schmetterling braucht flüssigen Nektar statt Wurzeln. Welcher Pflanzenteil bietet ihn an? |
| biology_20 | de | tip | Viele Schmetterlinge saugen mit ihrem Rüssel Nektar aus Blüten. | Überlege beide Hinweise. Gesucht ist: Blume. |
| biology_20 | en | prompt | Where can a butterfly drink nectar? | Growing. A butterfly needs liquid nectar, not roots. Which plant part offers it? |
| biology_20 | en | tip | Many butterflies use a long mouthpart to drink nectar from flowers. | Use both clues. The answer is flower. |
| biology_20 | ru | prompt | Где бабочка может пить нектар? | Рост. Бабочке нужен жидкий нектар, а не корни. Какая часть растения его предлагает? |
| biology_20 | ru | tip | Многие бабочки пьют нектар из цветков с помощью хоботка. | Учти обе подсказки. Ответ: цветок. |
| biology_21 | de | prompt | Welches dieser Tiere lebt im Wasser? | Entwickeln. Flossen statt Beine, Kiemen statt Lungen. Welches Tier kann damit dauerhaft unter Wasser leben? |
| biology_21 | de | tip | Der abgebildete Fisch lebt im Wasser. | Überlege beide Hinweise. Gesucht ist: Fisch. |
| biology_21 | en | prompt | Which of these animals lives in water? | Life. Fins instead of legs, gills instead of lungs. Which animal can live underwater with these? |
| biology_21 | en | tip | The fish in the picture lives in water. | Use both clues. The answer is fish. |
| biology_21 | ru | prompt | Кто из этих животных живёт в воде? | Жизнь. Вместо ног плавники, вместо лёгких жабры. Кто так может постоянно жить под водой? |
| biology_21 | ru | tip | Изображённая рыба живёт в воде. | Учти обе подсказки. Ответ: рыба. |
| biology_22 | de | prompt | Wo legt ein Grasfrosch seine Eier ab? | Entwickeln. Aus Froscheiern werden schwimmende Kaulquappen. Wo brauchen die Eier deshalb ihren Platz? |
| biology_22 | de | tip | Grasfrösche legen ihren Laich in Gewässern ab. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| biology_22 | en | prompt | Where does a common frog lay its eggs? | Life. Frog eggs become swimming tadpoles. Where must the eggs therefore be? |
| biology_22 | en | tip | Common frogs lay their eggs in water. | Use both clues. The answer is water. |
| biology_22 | ru | prompt | Где травяная лягушка откладывает икру? | Жизнь. Из икры появляются плавающие головастики. Где поэтому должна находиться икра? |
| biology_22 | ru | tip | Травяные лягушки откладывают икру в водоёмах. | Учти обе подсказки. Ответ: вода. |
| biology_23 | de | prompt | Was wächst bei einem keimenden Samen zuerst in den Boden? | Wachsen. Ein Samen keimt. Was wächst nach unten, bevor der Spross nach oben wächst? |
| biology_23 | de | tip | Zuerst wächst eine kleine Wurzel in den Boden. | Überlege beide Hinweise. Gesucht ist: Wurzeln. |
| biology_23 | en | prompt | What grows into the soil first when a seed sprouts? | Growing. A seed germinates. What grows down before the shoot grows up? |
| biology_23 | en | tip | A small root grows into the soil first. | Use both clues. The answer is roots. |
| biology_23 | ru | prompt | Что первым растёт в землю при прорастании семени? | Рост. Семя прорастает. Что растёт вниз до того, как побег растёт вверх? |
| biology_23 | ru | tip | Сначала в почву растёт маленький корень. | Учти обе подсказки. Ответ: корни. |
| biology_24 | de | prompt | Was nehmen Wurzeln auf? | Wachsen. Zwei Pflanzen stehen gleich hell. Nur eine wird gegossen. Was fehlt der welkenden Pflanze? |
| biology_24 | de | tip | Wurzeln nehmen Wasser und darin gelöste Mineralstoffe auf. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| biology_24 | en | prompt | What do roots absorb? | Growing. Two plants have equal light. Only one is watered. What is the wilting plant missing? |
| biology_24 | en | tip | Roots absorb water and dissolved minerals. | Use both clues. The answer is water. |
| biology_24 | ru | prompt | Что впитывают корни? | Рост. Два растения одинаково освещены. Поливают одно. Чего не хватает увядающему растению? |
| biology_24 | ru | tip | Корни впитывают воду и растворённые в ней минеральные вещества. | Учти обе подсказки. Ответ: вода. |
| biology_25 | de | prompt | Wo stehen viele Bäume dicht beieinander? | Entwickeln. Oben schließen sich viele Baumkronen, unten liegt Laub. Welcher Lebensraum hat solche Schichten? |
| biology_25 | de | tip | In einem Wald wachsen viele Bäume zusammen. | Überlege beide Hinweise. Gesucht ist: Wald. |
| biology_25 | en | prompt | Where do many trees grow close together? | Life. Many treetops meet above and leaves cover the ground. Which habitat has these layers? |
| biology_25 | en | tip | Many trees grow together in a forest. | Use both clues. The answer is forest. |
| biology_25 | ru | prompt | Где много деревьев растёт близко друг к другу? | Жизнь. Наверху смыкаются кроны, внизу лежат листья. У какой среды обитания есть такие ярусы? |
| biology_25 | ru | tip | В лесу рядом растёт много деревьев. | Учти обе подсказки. Ответ: лес. |
| biology_26 | de | prompt | Welche Teile der Baumkrone werden im Herbst oft gelb oder rot? | Wachsen. Im Herbst wird die Krone bunt, der Stamm bleibt braun. Welche Teile ändern ihre Farbe? |
| biology_26 | de | tip | Die Blätter vieler Laubbäume werden im Herbst gelb, rot oder braun. | Überlege beide Hinweise. Gesucht ist: Blatt. |
| biology_26 | en | prompt | Which parts of the tree crown often turn yellow or red in autumn? | Growing. In autumn the crown becomes colourful but the trunk stays brown. Which parts change colour? |
| biology_26 | en | tip | Many broadleaf trees have leaves that turn yellow, red or brown in autumn. | Use both clues. The answer is leaf. |
| biology_26 | ru | prompt | Какие части кроны дерева осенью часто становятся жёлтыми или красными? | Рост. Осенью крона становится разноцветной, ствол остаётся коричневым. Какие части меняют цвет? |
| biology_26 | ru | tip | Осенью листья многих лиственных деревьев желтеют, краснеют или буреют. | Учти обе подсказки. Ответ: лист. |
| biology_27 | de | prompt | Wer hat einen Schnabel? | Entwickeln. Ein Tier sammelt Nahrung mit einem Schnabel statt mit Zähnen. Wer passt? |
| biology_27 | de | tip | Vögel haben Schnäbel. Die Form passt oft zu ihrer Nahrung. | Überlege beide Hinweise. Gesucht ist: Vogel. |
| biology_27 | en | prompt | Which animal has a beak? | Life. An animal gathers food with a beak instead of teeth. Which fits? |
| biology_27 | en | tip | Birds have beaks, often shaped to suit their food. | Use both clues. The answer is bird. |
| biology_27 | ru | prompt | У кого есть клюв? | Жизнь. Животное собирает пищу клювом, а не зубами. Кто подходит? |
| biology_27 | ru | tip | У птиц есть клювы. Их форма часто связана с пищей. | Учти обе подсказки. Ответ: птица. |
| biology_28 | de | prompt | Welches dieser Tiere ist ein Insekt? | Entwickeln. Sechs Beine und ein Körper mit drei Abschnitten. Welches Tier ist ein Insekt? |
| biology_28 | de | tip | Eine Biene ist ein Insekt. Insekten haben sechs Beine. | Überlege beide Hinweise. Gesucht ist: Biene. |
| biology_28 | en | prompt | Which of these animals is an insect? | Life. Six legs and a body with three sections. Which animal is an insect? |
| biology_28 | en | tip | A bee is an insect. Insects have six legs. | Use both clues. The answer is bee. |
| biology_28 | ru | prompt | Кто из этих животных насекомое? | Жизнь. Шесть ног и тело из трёх отделов. Кто относится к насекомым? |
| biology_28 | ru | tip | Пчела — насекомое. У насекомых шесть ног. | Учти обе подсказки. Ответ: пчела. |
| biology_29 | de | prompt | Woraus schlüpfen junge Schildkröten? | Entwickeln. Eine Schildkröte bringt keine lebenden Jungen zur Welt. Woraus schlüpft ihr Nachwuchs? |
| biology_29 | de | tip | Schildkröten legen Eier. Daraus schlüpfen ihre Jungen. | Überlege beide Hinweise. Gesucht ist: Ei. |
| biology_29 | en | prompt | What do young turtles hatch from? | Life. A turtle does not give birth to live young. What do its young hatch from? |
| biology_29 | en | tip | Turtles lay eggs, and their young hatch from them. | Use both clues. The answer is egg. |
| biology_29 | ru | prompt | Из чего вылупляются черепашки? | Жизнь. Черепаха не рождает живых детёнышей. Из чего вылупляется её потомство? |
| biology_29 | ru | tip | Черепахи откладывают яйца. Из них вылупляются детёныши. | Учти обе подсказки. Ответ: яйцо. |
| biology_30 | de | prompt | Was kann nach der Blüte entstehen und neue Pflanzen hervorbringen? | Wachsen. Die Blüte ist verblüht. Was kann sich bilden und später eine neue Pflanze hervorbringen? |
| biology_30 | de | tip | Nach der Bestäubung können Samen entstehen. | Überlege beide Hinweise. Gesucht ist: Samen. |
| biology_30 | en | prompt | What can form after flowering and grow into new plants? | Growing. The flower has faded. What can form and later produce a new plant? |
| biology_30 | en | tip | Seeds can form after pollination. | Use both clues. The answer is seed. |
| biology_30 | ru | prompt | Что может появиться после цветения и дать новые растения? | Рост. Цветок отцвёл. Что может образоваться и позже дать новое растение? |
| biology_30 | ru | tip | После опыления могут образоваться семена. | Учти обе подсказки. Ответ: семя. |
| biology_31 | de | prompt | Womit hört eine Katze? | Hören. Eine Katze erkennt ein Rascheln, auch ohne die Maus zu sehen. Was nimmt den Schall auf? |
| biology_31 | de | tip | Katzen hören mit ihren Ohren. | Überlege beide Hinweise. Gesucht ist: Ohr. |
| biology_31 | en | prompt | What does a cat use to hear? | Hearing. A cat detects rustling without seeing the mouse. What receives the sound? |
| biology_31 | en | tip | Cats hear with their ears. | Use both clues. The answer is ear. |
| biology_31 | ru | prompt | Чем кошка слышит? | Слух. Кошка замечает шорох, даже не видя мышь. Что воспринимает звук? |
| biology_31 | ru | tip | Кошки слышат ушами. | Учти обе подсказки. Ответ: ухо. |
| biology_32 | de | prompt | Wer ist ein Lebewesen: Maus, Papier oder Glas? | Entwickeln. Wachsen, Nahrung aufnehmen, Junge bekommen. Welches davon ist ein Lebewesen? |
| biology_32 | de | tip | Eine Maus lebt: Sie wächst, atmet und braucht Nahrung. | Überlege beide Hinweise. Gesucht ist: Maus. |
| biology_32 | en | prompt | Which is a living thing: a mouse, paper or glass? | Life. Growing, taking in food and having young. Which of these is alive? |
| biology_32 | en | tip | A mouse is alive: it grows, breathes and needs food. | Use both clues. The answer is mouse. |
| biology_32 | ru | prompt | Кто живой: мышь, бумага или стекло? | Жизнь. Растёт, питается, даёт потомство. Кто из показанных является живым существом? |
| biology_32 | ru | tip | Мышь живая: она растёт, дышит и нуждается в пище. | Учти обе подсказки. Ответ: мышь. |
| biology_33 | de | prompt | Was lässt du beim Beobachten von Vogeleiern in Ruhe? | Entwickeln. Ein Vogel wärmt Eier. Was darfst du beim Beobachten nicht anfassen oder verschieben? |
| biology_33 | de | tip | Beobachte ein Nest nur aus Abstand, damit die Eltern sich sicher fühlen. | Überlege beide Hinweise. Gesucht ist: Nest. |
| biology_33 | en | prompt | What should you leave undisturbed when watching bird eggs? | Life. A bird warms eggs. What must you not touch or move while observing? |
| biology_33 | en | tip | Watch a nest from a distance so the parents feel safe. | Use both clues. The answer is nest. |
| biology_33 | ru | prompt | Что нельзя тревожить, наблюдая за птичьими яйцами? | Жизнь. Птица согревает яйца. Что при наблюдении нельзя трогать или передвигать? |
| biology_33 | ru | tip | Наблюдай за гнездом издалека, чтобы не пугать родителей птенцов. | Учти обе подсказки. Ответ: гнездо. |
| biology_34 | de | prompt | Welcher Pflanzenteil verankert eine Blume im Boden? | Wachsen. Eine Blume soll fest im Boden bleiben und Wasser aufnehmen. Welcher Teil hilft bei beidem? |
| biology_34 | de | tip | Die Wurzeln halten die Pflanze im Boden fest. | Überlege beide Hinweise. Gesucht ist: Wurzeln. |
| biology_34 | en | prompt | Which plant part holds a flower in the ground? | Growing. A flower needs anchoring and water uptake. Which part helps with both? |
| biology_34 | en | tip | Roots anchor the plant in the soil. | Use both clues. The answer is roots. |
| biology_34 | ru | prompt | Какая часть растения удерживает цветок в земле? | Рост. Цветку нужно держаться в земле и получать воду. Какая часть помогает в обоих случаях? |
| biology_34 | ru | tip | Корни удерживают растение в почве. | Учти обе подсказки. Ответ: корни. |
| biology_35 | de | prompt | Eine Topfpflanze hat trockene Erde. Was kann ihr fehlen? | Trinken. Die Blätter hängen, die Erde ist trocken, Licht ist vorhanden. Was kann fehlen? |
| biology_35 | de | tip | Der Pflanze kann Wasser fehlen. Gieße passend zur Pflanzenart. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| biology_35 | en | prompt | A plant's soil is dry. What might it need? | Drink. Leaves droop, soil is dry and light is available. What may be missing? |
| biology_35 | en | tip | The plant may need water. Give the amount that suits that plant. | Use both clues. The answer is water. |
| biology_35 | ru | prompt | Земля в горшке сухая. Чего может не хватать растению? | Пить. Листья поникли, почва сухая, свет есть. Чего может не хватать? |
| biology_35 | ru | tip | Растению может не хватать воды. Поливай с учётом вида растения. | Учти обе подсказки. Ответ: вода. |
| biology_36 | de | prompt | Was hilft Bienen im Garten? | Wachsen. Ein Garten hat viel Rasen, aber kaum Nektar. Was hilft den Bienen zusätzlich? |
| biology_36 | de | tip | Verschiedene Blüten bieten Bienen Nahrung. | Überlege beide Hinweise. Gesucht ist: Blume. |
| biology_36 | en | prompt | What helps bees in a garden? | Growing. A garden has plenty of grass but little nectar. What else helps bees? |
| biology_36 | en | tip | A variety of flowers provides food for bees. | Use both clues. The answer is flower. |
| biology_36 | ru | prompt | Что помогает пчёлам в саду? | Рост. В саду много травы, но мало нектара. Что ещё поможет пчёлам? |
| biology_36 | ru | tip | Разные цветы дают пчёлам пищу. | Учти обе подсказки. Ответ: цветок. |
| biology_37 | de | prompt | Was können Regenwürmer in die Erde ziehen? | Entwickeln. Abgestorbene Pflanzenteile werden von Würmern in die Erde gezogen. Was davon passt? |
| biology_37 | de | tip | Regenwürmer ziehen abgestorbene Blätter in ihre Gänge. | Überlege beide Hinweise. Gesucht ist: Blatt. |
| biology_37 | en | prompt | What can earthworms pull into the soil? | Life. Worms pull dead plant parts into soil. Which pictured thing fits? |
| biology_37 | en | tip | Earthworms pull fallen, dead leaves into their burrows. | Use both clues. The answer is leaf. |
| biology_37 | ru | prompt | Что дождевые черви могут затаскивать в землю? | Жизнь. Черви втягивают отмершие части растений в почву. Что из показанного подходит? |
| biology_37 | ru | tip | Дождевые черви затаскивают отмершие опавшие листья в свои ходы. | Учти обе подсказки. Ответ: лист. |
| biology_38 | de | prompt | Worin schwimmen Fische eines Teichs? | Entwickeln. Kiemen dürfen nicht austrocknen. Worin bewegt sich deshalb ein Teichfisch? |
| biology_38 | de | tip | Ein Teich enthält Wasser. Er ist Lebensraum für verschiedene Tiere. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| biology_38 | en | prompt | What do pond fish swim in? | Life. Gills must not dry out. What does a pond fish therefore move in? |
| biology_38 | en | tip | A pond contains water and is home to different animals. | Use both clues. The answer is water. |
| biology_38 | ru | prompt | В чём плавают прудовые рыбы? | Жизнь. Жабры не должны высыхать. В чём поэтому двигается прудовая рыба? |
| biology_38 | ru | tip | В пруду есть вода. В нём обитают разные животные. | Учти обе подсказки. Ответ: вода. |
| biology_39 | de | prompt | Was kann aus einer Eichel wachsen? | Wachsen. Ein Eichhörnchen vergisst eine Eichel im Boden. Welche große Pflanze kann daraus wachsen? |
| biology_39 | de | tip | Eine Eichel ist ein Samen einer Eiche. Daraus kann ein Baum wachsen. | Überlege beide Hinweise. Gesucht ist: Baum. |
| biology_39 | en | prompt | What can grow from an acorn? | Growing. A squirrel forgets an acorn in soil. Which large plant can grow from it? |
| biology_39 | en | tip | An acorn is an oak seed. It can grow into a tree. | Use both clues. The answer is tree. |
| biology_39 | ru | prompt | Что может вырасти из жёлудя? | Рост. Белка забыла жёлудь в земле. Какое большое растение может из него вырасти? |
| biology_39 | ru | tip | Жёлудь — семя дуба. Из него может вырасти дерево. | Учти обе подсказки. Ответ: дерево. |
| biology_40 | de | prompt | Wer hat als erwachsenes Tier vier Flügel? | Entwickeln. Sechs Beine, vier große Flügel, vorher eine Raupe. Welches Tier passt? |
| biology_40 | de | tip | Ein Schmetterling hat zwei Vorderflügel und zwei Hinterflügel. | Überlege beide Hinweise. Gesucht ist: Schmetterling. |
| biology_40 | en | prompt | Which adult animal has four wings? | Life. Six legs, four large wings, previously a caterpillar. Which animal fits? |
| biology_40 | en | tip | A butterfly has two forewings and two hindwings. | Use both clues. The answer is butterfly. |
| biology_40 | ru | prompt | У кого во взрослом состоянии четыре крыла? | Жизнь. Шесть ног, четыре больших крыла, раньше была гусеницей. Кто подходит? |
| biology_40 | ru | tip | У бабочки два передних и два задних крыла. | Учти обе подсказки. Ответ: бабочка. |
| chemistry_01 | de | prompt | Was wird aus Eis, wenn es schmilzt? | Verändern. Ein Eiswürfel verliert seine feste Form. Welcher Stoff bleibt nach dem Schmelzen flüssig? |
| chemistry_01 | de | tip | Eis ist gefrorenes Wasser. Beim Schmelzen wird es flüssig. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| chemistry_01 | en | prompt | What does ice become when it melts? | Change. An ice cube loses its solid shape. Which substance remains liquid after melting? |
| chemistry_01 | en | tip | Ice is frozen water. Melting turns it into liquid water. | Use both clues. The answer is water. |
| chemistry_01 | ru | prompt | Во что превращается лёд, когда тает? | Изменение. Кубик льда теряет твёрдую форму. Какое вещество остаётся жидким после таяния? |
| chemistry_01 | ru | tip | Лёд — замёрзшая вода. При таянии он становится жидкой водой. | Учти обе подсказки. Ответ: вода. |
| chemistry_02 | de | prompt | Was kann aus Wasser im Gefrierfach werden? | Verändern. Eine Flüssigkeit kommt ins Gefrierfach und wird fest. Was wird aus Wasser? |
| chemistry_02 | de | tip | Wenn Wasser kalt genug wird, kann es zu Eis gefrieren. | Überlege beide Hinweise. Gesucht ist: Eis. |
| chemistry_02 | en | prompt | What can water become in a freezer? | Change. A liquid goes into a freezer and becomes solid. What does water become? |
| chemistry_02 | en | tip | When water gets cold enough, it can freeze into ice. | Use both clues. The answer is ice. |
| chemistry_02 | ru | prompt | Во что вода может превратиться в морозильнике? | Изменение. Жидкость попала в морозильник и затвердела. Во что превратилась вода? |
| chemistry_02 | ru | tip | При достаточно низкой температуре вода может замёрзнуть и стать льдом. | Учти обе подсказки. Ответ: лёд. |
| chemistry_03 | de | prompt | Was ist bei Zimmertemperatur flüssig? | Entdecken. Ein Stoff fließt und nimmt bei Zimmertemperatur die Form seines Gefäßes an. Welcher passt? |
| chemistry_03 | de | tip | Wasser ist bei normaler Zimmertemperatur flüssig. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| chemistry_03 | en | prompt | Which is liquid at room temperature? | Explore. A substance flows and takes its container's shape at room temperature. Which fits? |
| chemistry_03 | en | tip | Water is liquid at normal room temperature. | Use both clues. The answer is water. |
| chemistry_03 | ru | prompt | Что жидкое при комнатной температуре? | Открытие. Вещество течёт и при комнатной температуре принимает форму сосуда. Что подходит? |
| chemistry_03 | ru | tip | При обычной комнатной температуре вода жидкая. | Учти обе подсказки. Ответ: вода. |
| chemistry_04 | de | prompt | Was ist bei Zimmertemperatur fest? | Untersuchen. Zwei Stoffe fließen, einer bleibt ein festes Stück. Welcher ist bei Zimmertemperatur fest? |
| chemistry_04 | de | tip | Ein Holzklotz hat eine feste Form. | Überlege beide Hinweise. Gesucht ist: Holz. |
| chemistry_04 | en | prompt | Which is solid at room temperature? | Materials. Two substances flow while one stays a solid piece. Which is solid at room temperature? |
| chemistry_04 | en | tip | A block of wood has a fixed shape. | Use both clues. The answer is wood. |
| chemistry_04 | ru | prompt | Что твёрдое при комнатной температуре? | Вещества. Два вещества текут, одно остаётся твёрдым куском. Что твёрдое при комнатной температуре? |
| chemistry_04 | ru | tip | Деревянный брусок сохраняет свою форму. | Учти обе подсказки. Ответ: древесина. |
| chemistry_05 | de | prompt | Welches Gefäß hält Trinkwasser zuverlässig? | Verwandeln. Ein Gefäß soll Wasser halten, ohne aufzuweichen oder auszulaufen. Welches Material eignet sich? |
| chemistry_05 | de | tip | Ein unbeschädigtes Trinkglas lässt Wasser nicht hindurch. | Überlege beide Hinweise. Gesucht ist: Glas. |
| chemistry_05 | en | prompt | Which container reliably holds drinking water? | Changing. A container must hold water without softening or leaking. Which material is suitable? |
| chemistry_05 | en | tip | An undamaged drinking glass does not let water pass through. | Use both clues. The answer is glass. |
| chemistry_05 | ru | prompt | Какая ёмкость надёжно удерживает питьевую воду? | Превращение. Сосуд должен держать воду, не размокая и не протекая. Какой материал подходит? |
| chemistry_05 | ru | tip | Целый питьевой стакан не пропускает воду. | Учти обе подсказки. Ответ: стекло. |
| chemistry_06 | de | prompt | Was löst sich in Wasser: Salz, Sand oder Holz? | Verwandeln. Nach dem Rühren sind keine Körnchen mehr sichtbar. Welcher Stoff kann sich in Wasser lösen? |
| chemistry_06 | de | tip | Kleine Mengen Salz lösen sich in Wasser. Das Salz bleibt dabei vorhanden. | Überlege beide Hinweise. Gesucht ist: Salz. |
| chemistry_06 | en | prompt | What dissolves in water: salt, sand or wood? | Changing. After stirring, no grains remain visible. Which substance can dissolve in water? |
| chemistry_06 | en | tip | Small amounts of salt dissolve in water. The salt is still there. | Use both clues. The answer is salt. |
| chemistry_06 | ru | prompt | Что растворяется в воде: соль, песок или дерево? | Превращение. После размешивания крупинок не видно. Какое вещество может раствориться в воде? |
| chemistry_06 | ru | tip | Небольшое количество соли растворяется в воде. Соль при этом не исчезает. | Учти обе подсказки. Ответ: соль. |
| chemistry_07 | de | prompt | Was bleibt als Körnchen sichtbar, wenn es in Wasser liegt? | Verwandeln. Nach Rühren und Warten liegen Körnchen am Boden. Welcher Stoff hat sich nicht gelöst? |
| chemistry_07 | de | tip | Sand löst sich normalerweise nicht in Wasser auf. | Überlege beide Hinweise. Gesucht ist: Sand. |
| chemistry_07 | en | prompt | What stays visible as grains in water? | Changing. After stirring and waiting, grains lie at the bottom. Which substance did not dissolve? |
| chemistry_07 | en | tip | Sand does not normally dissolve in water. | Use both clues. The answer is sand. |
| chemistry_07 | ru | prompt | Что остаётся видимыми крупинками в воде? | Превращение. После размешивания и ожидания крупинки лежат на дне. Какое вещество не растворилось? |
| chemistry_07 | ru | tip | Песок обычно не растворяется в воде. | Учти обе подсказки. Ответ: песок. |
| chemistry_08 | de | prompt | Was bildet mit Wasser oft zwei Schichten? | Verwandeln. Wir schütteln zwei Flüssigkeiten. Bald liegen wieder zwei Schichten vor. Was trennt sich vom Wasser? |
| chemistry_08 | de | tip | Speiseöl und Wasser mischen sich nicht dauerhaft. | Überlege beide Hinweise. Gesucht ist: Öl. |
| chemistry_08 | en | prompt | What often forms two layers with water? | Changing. We shake two liquids. Soon two layers return. What separates from the water? |
| chemistry_08 | en | tip | Cooking oil and water do not stay mixed. | Use both clues. The answer is oil. |
| chemistry_08 | ru | prompt | Что часто образует с водой два слоя? | Превращение. Две жидкости встряхнули. Вскоре снова два слоя. Что отделяется от воды? |
| chemistry_08 | ru | tip | Растительное масло и вода не образуют устойчивую смесь. | Учти обе подсказки. Ответ: масло. |
| chemistry_09 | de | prompt | Welcher Gegenstand zieht Eisen aus einer Mischung an? | Verändern. Eisenstücke liegen im Sand. Welcher Gegenstand trennt sie ohne Aussieben ab? |
| chemistry_09 | de | tip | Ein Magnet zieht Eisen an. Hier zeigt das Metallbild das Eisen. | Überlege beide Hinweise. Gesucht ist: Magnet. |
| chemistry_09 | en | prompt | Which object attracts iron out of a mixture? | Change. Iron pieces are mixed with sand. Which object separates them without sieving? |
| chemistry_09 | en | tip | A magnet attracts iron. The metal picture here stands for iron. | Use both clues. The answer is magnet. |
| chemistry_09 | ru | prompt | Какой предмет притягивает железо из смеси? | Изменение. Кусочки железа смешаны с песком. Чем отделить их без просеивания? |
| chemistry_09 | ru | tip | Магнит притягивает железо. На картинке с металлом здесь изображено железо. | Учти обе подсказки. Ответ: магнит. |
| chemistry_10 | de | prompt | Was entsteht unsichtbar, wenn Wasser verdunstet? | Verwandeln. Eine Pfütze trocknet, obwohl kein Abfluss da ist. Welcher unsichtbare Zustand entsteht? |
| chemistry_10 | de | tip | Wasser wird zu unsichtbarem Wasserdampf. Die weiße Wolke steht hier als Zeichen dafür. | Überlege beide Hinweise. Gesucht ist: Wasserdampf. |
| chemistry_10 | en | prompt | What forms invisibly when water evaporates? | Changing. A puddle dries without a drain. Which invisible state forms? |
| chemistry_10 | en | tip | Water becomes invisible water vapour. The white cloud is only a symbol for it. | Use both clues. The answer is water vapour. |
| chemistry_10 | ru | prompt | Что образуется незаметно, когда вода испаряется? | Превращение. Лужа высыхает, хотя стока нет. Какое невидимое состояние возникает? |
| chemistry_10 | ru | tip | Вода превращается в невидимый водяной пар. Белое облачко — только его условный значок. | Учти обе подсказки. Ответ: водяной пар. |
| chemistry_11 | de | prompt | Was bilden kleine Tropfen an einem kalten Fenster? | Verändern. Unsichtbares Wasser in der Luft kühlt am Fenster ab. Welcher flüssige Stoff bildet Tropfen? |
| chemistry_11 | de | tip | Wasserdampf aus der Luft kann an der kalten Scheibe zu Wasser werden. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| chemistry_11 | en | prompt | What are the little drops on a cold window made of? | Change. Invisible water in air cools at a window. Which liquid forms drops? |
| chemistry_11 | en | tip | Water vapour in the air can turn into liquid water on cold glass. | Use both clues. The answer is water. |
| chemistry_11 | ru | prompt | Из чего состоят капельки на холодном окне? | Изменение. Невидимая вода в воздухе охлаждается у окна. Какая жидкость образует капли? |
| chemistry_11 | ru | tip | Водяной пар из воздуха может превратиться в воду на холодном стекле. | Учти обе подсказки. Ответ: вода. |
| chemistry_12 | de | prompt | Welcher Zustand von Wasser ist fest? | Verwandeln. Du vergleichst drei Formen desselben Stoffes. Welche behält eine feste eigene Form? |
| chemistry_12 | de | tip | Gefrorenes Wasser nennen wir Eis. | Überlege beide Hinweise. Gesucht ist: Eis. |
| chemistry_12 | en | prompt | Which form of water is solid? | Changing. You compare three forms of the same substance. Which keeps its own solid shape? |
| chemistry_12 | en | tip | Frozen water is called ice. | Use both clues. The answer is ice. |
| chemistry_12 | ru | prompt | Какое состояние воды твёрдое? | Превращение. Ты сравниваешь три формы одного вещества. Какая сохраняет твёрдую форму? |
| chemistry_12 | ru | tip | Замёрзшую воду называют льдом. | Учти обе подсказки. Ответ: лёд. |
| chemistry_13 | de | prompt | Welches Zeichen steht für gasförmiges Wasser? | Verwandeln. Wasser kann unsichtbar in der Luft sein. Welches Zeichen steht für diesen gasförmigen Zustand? |
| chemistry_13 | de | tip | Gasförmiges Wasser ist unsichtbar. Die Dampf-Wolke ist ein vereinfachtes Zeichen. | Überlege beide Hinweise. Gesucht ist: Wasserdampf. |
| chemistry_13 | en | prompt | Which symbol stands for water as a gas? | Changing. Water can be invisible in air. Which symbol represents this gaseous state? |
| chemistry_13 | en | tip | Water as a gas is invisible. The vapour cloud is a simplified symbol. | Use both clues. The answer is water vapour. |
| chemistry_13 | ru | prompt | Какой значок обозначает воду в газообразном состоянии? | Превращение. Вода может быть невидимой в воздухе. Какой знак обозначает это газообразное состояние? |
| chemistry_13 | ru | tip | Газообразная вода невидима. Облачко пара — упрощённый условный значок. | Учти обе подсказки. Ответ: водяной пар. |
| chemistry_14 | de | prompt | Worin löst sich etwas Kochsalz gut? | Untersuchen. Etwas Salz soll sich beim Rühren lösen. Welche Flüssigkeit eignet sich dafür? |
| chemistry_14 | de | tip | Etwas Salz löst sich in Wasser. Unbekannte Stoffe darfst du nicht probieren. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| chemistry_14 | en | prompt | What dissolves a little table salt well? | Materials. Some salt must dissolve when stirred. Which liquid is suitable? |
| chemistry_14 | en | tip | A little salt dissolves in water. Never taste an unknown substance. | Use both clues. The answer is water. |
| chemistry_14 | ru | prompt | В чём хорошо растворяется немного поваренной соли? | Вещества. Немного соли должно раствориться при размешивании. Какая жидкость подходит? |
| chemistry_14 | ru | tip | Немного соли растворяется в воде. Незнакомые вещества нельзя пробовать на вкус. | Учти обе подсказки. Ответ: вода. |
| chemistry_15 | de | prompt | Welches Material ist durchsichtig? | Leuchten. Ein Material bleibt fest, lässt aber Licht hindurch. Welcher Werkstoff passt zu beiden Eigenschaften? |
| chemistry_15 | de | tip | Klares Glas lässt Licht hindurch, sodass du hindurchsehen kannst. | Überlege beide Hinweise. Gesucht ist: Glas. |
| chemistry_15 | en | prompt | Which material is transparent? | Light. A material stays solid but lets light through. Which fits both properties? |
| chemistry_15 | en | tip | Clear glass lets light through so you can see through it. | Use both clues. The answer is glass. |
| chemistry_15 | ru | prompt | Какой материал прозрачный? | Свет. Материал остаётся твёрдым, но пропускает свет. Что обладает обоими свойствами? |
| chemistry_15 | ru | tip | Прозрачное стекло пропускает свет, поэтому сквозь него видно. | Учти обе подсказки. Ответ: стекло. |
| chemistry_16 | de | prompt | Welches Material saugt Wasser leicht auf? | Verwandeln. Ein Tropfen zieht in viele Pflanzenfasern hinein. Welches Material wird dabei leicht nass und weich? |
| chemistry_16 | de | tip | Unbeschichtetes Papier nimmt Wasser zwischen seinen Fasern auf. | Überlege beide Hinweise. Gesucht ist: Papier. |
| chemistry_16 | en | prompt | Which material easily soaks up water? | Changing. A drop enters many plant fibres. Which material becomes wet and soft easily? |
| chemistry_16 | en | tip | Uncoated paper absorbs water between its fibres. | Use both clues. The answer is paper. |
| chemistry_16 | ru | prompt | Какой материал легко впитывает воду? | Превращение. Капля проникает во множество растительных волокон. Какой материал легко намокает и размягчается? |
| chemistry_16 | ru | tip | Бумага без покрытия впитывает воду между волокнами. | Учти обе подсказки. Ответ: бумага. |
| chemistry_17 | de | prompt | Was lässt sich weich zusammenfalten? | Fühlen. Ein Material besteht aus Fäden und lässt sich weich falten. Welches passt? |
| chemistry_17 | de | tip | Ein Tuch aus Stoff ist biegsam. Ein Metallbarren ist viel starrer. | Überlege beide Hinweise. Gesucht ist: Stoff. |
| chemistry_17 | en | prompt | What can be softly folded up? | Touch. A material consists of threads and folds softly. Which fits? |
| chemistry_17 | en | tip | A fabric cloth bends easily. A metal bar is much stiffer. | Use both clues. The answer is fabric. |
| chemistry_17 | ru | prompt | Что можно мягко сложить? | Осязание. Материал состоит из нитей и мягко складывается. Что подходит? |
| chemistry_17 | ru | tip | Ткань легко сгибается. Металлический слиток гораздо жёстче. | Учти обе подсказки. Ответ: ткань. |
| chemistry_18 | de | prompt | Was kann Wärme gut weiterleiten? | Erwärmen. Ein Erwachsener vergleicht Wärmeleitung. Welcher Werkstoff leitet Wärme meist besser als Papier oder Stoff? |
| chemistry_18 | de | tip | Viele Metalle leiten Wärme gut. Heiße Dinge fasst du nicht an. | Überlege beide Hinweise. Gesucht ist: Eisen. |
| chemistry_18 | en | prompt | Which material can conduct heat well? | Warming. An adult compares heat conduction. Which material usually conducts better than paper or fabric? |
| chemistry_18 | en | tip | Many metals conduct heat well. Never touch hot objects. | Use both clues. The answer is iron. |
| chemistry_18 | ru | prompt | Какой материал хорошо проводит тепло? | Нагрев. Взрослый сравнивает теплопроводность. Какой материал обычно проводит тепло лучше бумаги или ткани? |
| chemistry_18 | ru | tip | Многие металлы хорошо проводят тепло. Горячие предметы трогать нельзя. | Учти обе подсказки. Ответ: железо. |
| chemistry_19 | de | prompt | Welches Material zeigt oft Jahresringe? | Untersuchen. Ein Material wurde gesägt und zeigt Ringe statt Fäden. Welcher Werkstoff passt? |
| chemistry_19 | de | tip | Holz stammt von Bäumen. Im Querschnitt sind oft Jahresringe sichtbar. | Überlege beide Hinweise. Gesucht ist: Holz. |
| chemistry_19 | en | prompt | Which material often shows growth rings? | Materials. A material was sawn and shows rings rather than threads. Which fits? |
| chemistry_19 | en | tip | Wood comes from trees. Growth rings are often visible in a cut section. | Use both clues. The answer is wood. |
| chemistry_19 | ru | prompt | На каком материале часто видны годичные кольца? | Вещества. Материал распилили, видны кольца, а не нити. Что подходит? |
| chemistry_19 | ru | tip | Древесину получают из деревьев. На срезе часто видны годичные кольца. | Учти обе подсказки. Ответ: древесина. |
| chemistry_20 | de | prompt | Was hilft, Fett mit Wasser zu vermischen und abzuwaschen? | Reinigen. Fett lässt sich mit Wasser allein schlecht entfernen. Welcher Zusatz hilft beim Händewaschen? |
| chemistry_20 | de | tip | Seife hilft, Fett und Schmutz mit Wasser zu entfernen. | Überlege beide Hinweise. Gesucht ist: Seife. |
| chemistry_20 | en | prompt | What helps grease mix with water so it can be washed away? | Cleaning. Water alone removes grease poorly. Which addition helps when washing hands? |
| chemistry_20 | en | tip | Soap helps water remove grease and dirt. | Use both clues. The answer is soap. |
| chemistry_20 | ru | prompt | Что помогает смешать жир с водой и смыть его? | Чистота. Одной водой жир смывается плохо. Что помогает при мытье рук? |
| chemistry_20 | ru | tip | Мыло помогает воде смывать жир и грязь. | Учти обе подсказки. Ответ: мыло. |
| chemistry_21 | de | prompt | Welcher Stoff wird oft zum Kochen verwendet und bleibt flüssig? | Entdecken. Eis schmilzt erst, Salz besteht aus Körnchen. Welcher Kochstoff ist schon flüssig? |
| chemistry_21 | de | tip | Viele Speiseöle sind bei Zimmertemperatur flüssig. | Überlege beide Hinweise. Gesucht ist: Öl. |
| chemistry_21 | en | prompt | Which substance is often used in cooking and stays liquid? | Explore. Ice must melt and salt has grains. Which cooking substance is already liquid? |
| chemistry_21 | en | tip | Many cooking oils are liquid at room temperature. | Use both clues. The answer is oil. |
| chemistry_21 | ru | prompt | Какое вещество часто используют при готовке и оно остаётся жидким? | Открытие. Лёд сначала нужно растопить, соль состоит из крупинок. Что для готовки уже жидкое? |
| chemistry_21 | ru | tip | Многие растительные масла жидкие при комнатной температуре. | Учти обе подсказки. Ответ: масло. |
| chemistry_22 | de | prompt | Was besteht hier aus vielen kleinen Körnern? | Untersuchen. Ein Stoff rieselt als feste Körnchen und löst sich nicht einfach in Wasser. Welcher passt? |
| chemistry_22 | de | tip | Sand besteht aus vielen kleinen festen Körnern. | Überlege beide Hinweise. Gesucht ist: Sand. |
| chemistry_22 | en | prompt | Which of these consists of many little grains? | Materials. A substance pours as solid grains and does not readily dissolve in water. Which fits? |
| chemistry_22 | en | tip | Sand consists of many small solid grains. | Use both clues. The answer is sand. |
| chemistry_22 | ru | prompt | Что здесь состоит из множества маленьких крупинок? | Вещества. Вещество сыплется твёрдыми крупинками и не растворяется просто в воде. Что подходит? |
| chemistry_22 | ru | tip | Песок состоит из множества мелких твёрдых зёрен. | Учти обе подсказки. Ответ: песок. |
| chemistry_23 | de | prompt | Was liefert Wärme, die draußen Eis schmelzen lässt? | Verändern. Ein Eisstück im Schatten schmilzt langsamer. Welcher Himmelskörper liefert dem anderen zusätzliche Wärme? |
| chemistry_23 | de | tip | Die Sonne liefert Energie. Wärme kann Eis schmelzen lassen. | Überlege beide Hinweise. Gesucht ist: Sonne. |
| chemistry_23 | en | prompt | What provides warmth that can melt ice outdoors? | Change. An ice piece melts slower in shade. Which celestial body gives another piece extra warmth? |
| chemistry_23 | en | tip | The sun supplies energy. Heat can make ice melt. | Use both clues. The answer is sun. |
| chemistry_23 | ru | prompt | Что даёт тепло и может растопить лёд на улице? | Изменение. Кусочек льда в тени тает медленнее. Какое небесное тело даёт другому дополнительное тепло? |
| chemistry_23 | ru | tip | Солнце даёт энергию. Тепло может растопить лёд. | Учти обе подсказки. Ответ: Солнце. |
| chemistry_24 | de | prompt | Wo sammeln sich viele winzige Wassertropfen am Himmel? | Beobachten. Wasserdampf kühlt hoch oben ab. Wo sammeln sich viele entstandene winzige Tropfen? |
| chemistry_24 | de | tip | Wolken bestehen aus winzigen Wassertröpfchen oder Eiskristallen. | Überlege beide Hinweise. Gesucht ist: Wolke. |
| chemistry_24 | en | prompt | Where do many tiny water drops gather in the sky? | Observe. Water vapour cools high above. Where do many resulting tiny drops collect? |
| chemistry_24 | en | tip | Clouds contain tiny water droplets or ice crystals. | Use both clues. The answer is cloud. |
| chemistry_24 | ru | prompt | Где в небе собирается много крошечных капель воды? | Наблюдение. Водяной пар охлаждается высоко наверху. Где собираются образовавшиеся мелкие капли? |
| chemistry_24 | ru | tip | Облака состоят из крошечных капель воды или кристалликов льда. | Учти обе подсказки. Ответ: облако. |
| chemistry_25 | de | prompt | Woraus bestehen Regentropfen hauptsächlich? | Beobachten. Regen füllt einen Eimer ohne Salz hinzuzugeben. Welcher Stoff bildet die Tropfen hauptsächlich? |
| chemistry_25 | de | tip | Regentropfen bestehen hauptsächlich aus flüssigem Wasser. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| chemistry_25 | en | prompt | What are raindrops mainly made of? | Observe. Rain fills a bucket without adding salt. Which substance mainly forms its drops? |
| chemistry_25 | en | tip | Raindrops are mainly liquid water. | Use both clues. The answer is water. |
| chemistry_25 | ru | prompt | Из чего в основном состоят капли дождя? | Наблюдение. Дождь наполняет ведро без добавления соли. Из какого вещества в основном капли? |
| chemistry_25 | ru | tip | Капли дождя состоят главным образом из жидкой воды. | Учти обе подсказки. Ответ: вода. |
| chemistry_26 | de | prompt | Woraus bestehen Schneeflocken? | Beobachten. Eine Schneeflocke wird in der Wärme zu Wasser. Aus welchem festen Stoff bestand sie? |
| chemistry_26 | de | tip | Schneeflocken bestehen aus Eiskristallen. | Überlege beide Hinweise. Gesucht ist: Eis. |
| chemistry_26 | en | prompt | What are snowflakes made of? | Observe. A snowflake becomes water when warmed. Which solid substance was it made of? |
| chemistry_26 | en | tip | Snowflakes are made of ice crystals. | Use both clues. The answer is ice. |
| chemistry_26 | ru | prompt | Из чего состоят снежинки? | Наблюдение. Снежинка в тепле превращается в воду. Из какого твёрдого вещества она состояла? |
| chemistry_26 | ru | tip | Снежинки состоят из кристалликов льда. | Учти обе подсказки. Ответ: лёд. |
| chemistry_27 | de | prompt | Was passt sich der Form eines Glases an? | Untersuchen. Ein Stoff wechselt seine Form beim Umgießen, nicht aber seine Menge. Welcher passt? |
| chemistry_27 | de | tip | Flüssiges Wasser hat keine feste eigene Form. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| chemistry_27 | en | prompt | What takes the shape of a glass? | Materials. A substance changes shape when poured but keeps its amount. Which fits? |
| chemistry_27 | en | tip | Liquid water does not have its own fixed shape. | Use both clues. The answer is water. |
| chemistry_27 | ru | prompt | Что принимает форму стакана? | Вещества. При переливании вещество меняет форму, но не количество. Что подходит? |
| chemistry_27 | ru | tip | У жидкой воды нет собственной постоянной формы. | Учти обе подсказки. Ответ: вода. |
| chemistry_28 | de | prompt | Was behält auf dem Teller zunächst seine eigene Form? | Verändern. Ein Stoff bleibt zunächst ein Stück statt als Pfütze zu verlaufen. Welcher passt? |
| chemistry_28 | de | tip | Ein Eiswürfel ist fest und behält seine Form, bis er schmilzt. | Überlege beide Hinweise. Gesucht ist: Eis. |
| chemistry_28 | en | prompt | What keeps its own shape on a plate before warming up? | Change. A substance initially stays a piece instead of spreading into a puddle. Which fits? |
| chemistry_28 | en | tip | An ice cube is solid and keeps its shape until it melts. | Use both clues. The answer is ice. |
| chemistry_28 | ru | prompt | Что сначала сохраняет свою форму на тарелке, пока не нагрелось? | Изменение. Вещество сначала остаётся куском, а не растекается лужицей. Что подходит? |
| chemistry_28 | ru | tip | Кубик льда твёрдый и сохраняет форму, пока не растает. | Учти обе подсказки. Ответ: лёд. |
| chemistry_29 | de | prompt | Welches Material kann splittern, wenn es herunterfällt? | Untersuchen. Das Material ist hart und durchsichtig, kann aber beim Fallen splittern. Welches ist es? |
| chemistry_29 | de | tip | Glas kann zerbrechen. Scherben lässt du von Erwachsenen entfernen. | Überlege beide Hinweise. Gesucht ist: Glas. |
| chemistry_29 | en | prompt | Which material can shatter if dropped? | Materials. The material is hard and transparent but may shatter when dropped. Which is it? |
| chemistry_29 | en | tip | Glass can break. Let an adult clear away the pieces. | Use both clues. The answer is glass. |
| chemistry_29 | ru | prompt | Какой материал может разбиться на осколки при падении? | Вещества. Материал твёрдый и прозрачный, но при падении может расколоться. Что это? |
| chemistry_29 | ru | tip | Стекло может разбиться. Осколки должен убрать взрослый. | Учти обе подсказки. Ответ: стекло. |
| chemistry_30 | de | prompt | Welches Mittel ist zum Händewaschen mit Wasser gedacht? | Reinigen. Eine Flüssigkeit allein entfernt Fett schlecht. Welches Waschmittel soll zusammen mit Wasser helfen? |
| chemistry_30 | de | tip | Seife ist für die Haut gedacht. Unbekannte Reinigungsmittel sind kein Spielzeug. | Überlege beide Hinweise. Gesucht ist: Seife. |
| chemistry_30 | en | prompt | Which product is intended for washing hands with water? | Cleaning. A liquid alone removes grease poorly. Which washing substance helps together with water? |
| chemistry_30 | en | tip | Soap is made for skin. Unknown cleaning products are not toys. | Use both clues. The answer is soap. |
| chemistry_30 | ru | prompt | Какое средство предназначено для мытья рук с водой? | Чистота. Одна жидкость плохо удаляет жир. Какое средство помогает вместе с водой? |
| chemistry_30 | ru | tip | Мыло предназначено для кожи. Незнакомые чистящие средства — не игрушки. | Учти обе подсказки. Ответ: мыло. |
| chemistry_31 | de | prompt | Was bleibt zurück, wenn Salzwasser ganz verdunstet? | Verwandeln. Das Wasser einer Salzlösung verdunstet vollständig. Welcher feste Stoff bleibt zurück? |
| chemistry_31 | de | tip | Das Wasser verdunstet. Das gelöste Salz kann als Kristalle zurückbleiben. | Überlege beide Hinweise. Gesucht ist: Salz. |
| chemistry_31 | en | prompt | What is left when salt water completely evaporates? | Changing. All water in a salt solution evaporates. Which solid substance remains? |
| chemistry_31 | en | tip | The water evaporates. Dissolved salt can remain as crystals. | Use both clues. The answer is salt. |
| chemistry_31 | ru | prompt | Что остаётся, когда солёная вода полностью испаряется? | Превращение. Вся вода из соляного раствора испарилась. Какое твёрдое вещество осталось? |
| chemistry_31 | ru | tip | Вода испаряется. Растворённая соль может остаться в виде кристалликов. | Учти обе подсказки. Ответ: соль. |
| chemistry_32 | de | prompt | Welcher Gegenstand zieht Eisenstücke aus Sand an? | Verändern. Sand bleibt liegen, Eisen bewegt sich ohne Berührung. Welcher Gegenstand kann das bewirken? |
| chemistry_32 | de | tip | Ein Magnet zieht die Eisenstücke an, den Sand normalerweise nicht. | Überlege beide Hinweise. Gesucht ist: Magnet. |
| chemistry_32 | en | prompt | Which object attracts iron pieces out of sand? | Change. Sand stays still while iron moves without contact. Which object can cause this? |
| chemistry_32 | en | tip | A magnet attracts the iron pieces, but normally not the sand. | Use both clues. The answer is magnet. |
| chemistry_32 | ru | prompt | Какой предмет притягивает кусочки железа из песка? | Изменение. Песок остаётся на месте, железо движется без прикосновения. Какой предмет это вызывает? |
| chemistry_32 | ru | tip | Магнит притягивает железные частички, но обычно не песок. | Учти обе подсказки. Ответ: магнит. |
| chemistry_33 | de | prompt | Welcher Stoff fließt aus einer umgekippten offenen Flasche? | Untersuchen. Ein Gefäß kippt. Welcher Stoff kann herausfließen statt als festes Stück herauszufallen? |
| chemistry_33 | de | tip | Flüssiges Wasser fließt und braucht ein dichtes Gefäß. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| chemistry_33 | en | prompt | Which substance flows from a tipped open bottle? | Materials. A container tips. Which substance can flow out rather than fall as a solid piece? |
| chemistry_33 | en | tip | Liquid water flows and needs a watertight container. | Use both clues. The answer is water. |
| chemistry_33 | ru | prompt | Какое вещество вытекает из наклонённой открытой бутылки? | Вещества. Сосуд опрокинулся. Какое вещество может вытечь, а не выпасть твёрдым куском? |
| chemistry_33 | ru | tip | Жидкая вода течёт. Для неё нужна непротекающая ёмкость. | Учти обе подсказки. Ответ: вода. |
| chemistry_34 | de | prompt | Was wird häufig aus Pflanzenfasern gemacht? | Wachsen. Holz wird in Fasern zerlegt und zu dünnen Blättern verarbeitet. Welches Material kann entstehen? |
| chemistry_34 | de | tip | Papier besteht aus miteinander verbundenen Fasern, oft aus Holz. | Überlege beide Hinweise. Gesucht ist: Papier. |
| chemistry_34 | en | prompt | What is often made from plant fibres? | Growing. Wood is broken into fibres and made into thin sheets. Which material can result? |
| chemistry_34 | en | tip | Paper contains connected fibres, often from wood. | Use both clues. The answer is paper. |
| chemistry_34 | ru | prompt | Что часто делают из растительных волокон? | Рост. Древесину разделили на волокна и сделали тонкие листы. Какой материал может получиться? |
| chemistry_34 | ru | tip | Бумага состоит из соединённых волокон, часто древесных. | Учти обе подсказки. Ответ: бумага. |
| chemistry_35 | de | prompt | Was ist dieselbe Substanz wie Wasser, nur fest? | Verwandeln. Schmelzen verändert die Form, nicht die Stoffart. Was ist festes Wasser? |
| chemistry_35 | de | tip | Eis und flüssiges Wasser sind dieselbe Substanz in verschiedenen Zuständen. | Überlege beide Hinweise. Gesucht ist: Eis. |
| chemistry_35 | en | prompt | What is the same substance as water, but solid? | Changing. Melting changes form, not the kind of substance. What is solid water? |
| chemistry_35 | en | tip | Ice and liquid water are the same substance in different states. | Use both clues. The answer is ice. |
| chemistry_35 | ru | prompt | Что является тем же веществом, что вода, только твёрдым? | Превращение. Таяние меняет форму, а не само вещество. Что является твёрдой водой? |
| chemistry_35 | ru | tip | Лёд и жидкая вода — одно вещество в разных состояниях. | Учти обе подсказки. Ответ: лёд. |
| chemistry_36 | de | prompt | Woraus wird gewöhnliches Glas hauptsächlich hergestellt? | Untersuchen. Ein Erwachsener erhitzt Rohstoffe für gewöhnliches Glas. Welcher körnige Stoff gehört vor allem dazu? |
| chemistry_36 | de | tip | Quarzsand ist ein wichtiger Rohstoff für Glas. Das geschieht in sehr heißen Öfen. | Überlege beide Hinweise. Gesucht ist: Sand. |
| chemistry_36 | en | prompt | What is ordinary glass mainly made from? | Materials. An adult heats raw materials for ordinary glass. Which granular substance is a main ingredient? |
| chemistry_36 | en | tip | Silica sand is an important ingredient in glass, made in very hot furnaces. | Use both clues. The answer is sand. |
| chemistry_36 | ru | prompt | Из чего в основном делают обычное стекло? | Вещества. Взрослый нагревает сырьё для обычного стекла. Какое сыпучее вещество входит в основу? |
| chemistry_36 | ru | tip | Кварцевый песок — важное сырьё для стекла. Его делают в очень горячих печах. | Учти обе подсказки. Ответ: песок. |
| chemistry_37 | de | prompt | Welches Material besteht aus gewebten Fäden? | Fühlen. Ein Material ist gewebt. Unter der Lupe erkennt man gekreuzte Fäden. Welches passt? |
| chemistry_37 | de | tip | Viele Stoffe werden aus Fäden gewebt. | Überlege beide Hinweise. Gesucht ist: Stoff. |
| chemistry_37 | en | prompt | Which material can be made from woven threads? | Touch. A material is woven. A magnifier reveals crossed threads. Which fits? |
| chemistry_37 | en | tip | Many fabrics are woven from threads. | Use both clues. The answer is fabric. |
| chemistry_37 | ru | prompt | Какой материал можно сделать из переплетённых нитей? | Осязание. Материал соткан. Под лупой видны перекрещённые нити. Что подходит? |
| chemistry_37 | ru | tip | Многие ткани делают переплетением нитей. | Учти обе подсказки. Ответ: ткань. |
| chemistry_38 | de | prompt | Womit spülst du Seife von den Händen ab? | Reinigen. Nach dem Einseifen sollen Schaum und Schmutz wegfließen. Womit spülst du nach? |
| chemistry_38 | de | tip | Sauberes Wasser spült die Seife und gelösten Schmutz ab. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| chemistry_38 | en | prompt | What rinses soap off your hands? | Cleaning. After soaping, foam and dirt should flow away. What do you rinse with? |
| chemistry_38 | en | tip | Clean water rinses away soap and loosened dirt. | Use both clues. The answer is water. |
| chemistry_38 | ru | prompt | Чем смывают мыло с рук? | Чистота. После намыливания пену и грязь нужно смыть. Чем ополоснуть руки? |
| chemistry_38 | ru | tip | Чистая вода смывает мыло и отделившуюся грязь. | Учти обе подсказки. Ответ: вода. |
| chemistry_39 | de | prompt | Was bleibt in Wasser bei Zimmertemperatur fest: Glas, Eis oder Salz? | Verändern. Salz löst sich, Eis schmilzt. Welches Material bleibt in Wasser bei Zimmertemperatur fest? |
| chemistry_39 | de | tip | Ein Trinkglas löst sich beim normalen Gebrauch nicht in Wasser auf. | Überlege beide Hinweise. Gesucht ist: Glas. |
| chemistry_39 | en | prompt | What stays solid in water at room temperature: glass, ice or salt? | Change. Salt dissolves and ice melts. Which material stays solid in water at room temperature? |
| chemistry_39 | en | tip | A drinking glass does not dissolve in water during normal use. | Use both clues. The answer is glass. |
| chemistry_39 | ru | prompt | Что остаётся твёрдым в воде при комнатной температуре: стекло, лёд или соль? | Изменение. Соль растворяется, лёд тает. Какой материал в воде комнатной температуры остаётся твёрдым? |
| chemistry_39 | ru | tip | Питьевой стакан при обычном использовании не растворяется в воде. | Учти обе подсказки. Ответ: стекло. |
| chemistry_40 | de | prompt | Was entsteht aus dem Eiswürfel, wenn er im Glas schmilzt? | Verändern. Ein Eiswürfel wird kleiner, die Flüssigkeitsmenge im Glas wächst. Welcher Stoff entsteht beim Schmelzen? |
| chemistry_40 | de | tip | Beim Schmelzen wird festes Eis zu flüssigem Wasser. Es ist kein neuer Stoff. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| chemistry_40 | en | prompt | What does an ice cube become when it melts in a glass? | Change. An ice cube shrinks while liquid in the glass increases. Which substance forms as it melts? |
| chemistry_40 | en | tip | Melting changes solid ice to liquid water. It does not make a new substance. | Use both clues. The answer is water. |
| chemistry_40 | ru | prompt | Во что превращается кубик льда, когда тает в стакане? | Изменение. Льдинка уменьшается, жидкости в стакане становится больше. Какое вещество образуется при таянии? |
| chemistry_40 | ru | tip | При таянии твёрдый лёд становится жидкой водой. Новое вещество не образуется. | Учти обе подсказки. Ответ: вода. |
| body_01 | de | prompt | Womit nimmst du Licht und Farben wahr? | Sehen. Licht kommt vom Bild. Welcher Körperteil meldet seine Farben ans Gehirn? |
| body_01 | de | tip | Die Augen nehmen Licht auf und senden Signale an das Gehirn. | Überlege beide Hinweise. Gesucht ist: Auge. |
| body_01 | en | prompt | Which body part detects light and colours? | Seeing. Light comes from a picture. Which body part sends its colours to the brain? |
| body_01 | en | tip | Eyes detect light and send signals to the brain. | Use both clues. The answer is eye. |
| body_01 | ru | prompt | Чем воспринимают свет и цвета? | Зрение. От картинки идёт свет. Какая часть тела сообщает мозгу её цвета? |
| body_01 | ru | tip | Глаза воспринимают свет и посылают сигналы в мозг. | Учти обе подсказки. Ответ: глаз. |
| body_02 | de | prompt | Welcher Körperteil nimmt Schall auf? | Hören. Die Augen sind zu, trotzdem erkennst du ein Lied. Was empfängt seinen Schall? |
| body_02 | de | tip | Die Ohren nehmen Schall auf. Das Gehirn verarbeitet die Signale. | Überlege beide Hinweise. Gesucht ist: Ohr. |
| body_02 | en | prompt | Which body part detects sounds? | Hearing. Your eyes are closed, yet you recognise a song. What receives its sound? |
| body_02 | en | tip | Ears detect sounds. The brain processes the signals. | Use both clues. The answer is ear. |
| body_02 | ru | prompt | Какая часть тела воспринимает звуки? | Слух. Глаза закрыты, но ты узнаёшь песню. Что воспринимает её звук? |
| body_02 | ru | tip | Уши воспринимают звуки. Мозг обрабатывает сигналы. | Учти обе подсказки. Ответ: ухо. |
| body_03 | de | prompt | Womit riechen Menschen? | Riechen. Ein Apfel liegt versteckt. Welcher Körperteil kann seinen Duft bemerken? |
| body_03 | de | tip | In der Nase sitzen Sinneszellen für Gerüche. | Überlege beide Hinweise. Gesucht ist: Nase. |
| body_03 | en | prompt | What do people use to smell? | Smell. An apple is hidden. Which body part can detect its scent? |
| body_03 | en | tip | The nose contains cells that detect smells. | Use both clues. The answer is nose. |
| body_03 | ru | prompt | Чем люди ощущают запахи? | Запах. Яблоко спрятано. Какая часть тела может почувствовать его запах? |
| body_03 | ru | tip | В носу есть клетки, которые воспринимают запахи. | Учти обе подсказки. Ответ: нос. |
| body_04 | de | prompt | Womit kannst du süß und sauer schmecken? | Schmecken. Zucker und Salz sehen ähnlich aus. Was unterscheidet ihren Geschmack? |
| body_04 | de | tip | Auf der Zunge sitzen viele Geschmacksknospen. | Überlege beide Hinweise. Gesucht ist: Zunge. |
| body_04 | en | prompt | What helps you taste sweet and sour? | Taste. Sugar and salt look similar. What distinguishes their taste? |
| body_04 | en | tip | The tongue has many taste buds. | Use both clues. The answer is tongue. |
| body_04 | ru | prompt | Что помогает различать сладкий и кислый вкус? | Вкус. Сахар и соль похожи на вид. Что различает их вкус? |
| body_04 | ru | tip | На языке много вкусовых почек. | Учти обе подсказки. Ответ: язык. |
| body_05 | de | prompt | Womit kannst du fühlen, ob ein Tuch weich ist? | Fühlen. Du suchst blind einen weichen Ball. Womit kannst du seine Oberfläche ertasten? |
| body_05 | de | tip | In der Haut deiner Hand sitzen Sinneszellen für Berührung. | Überlege beide Hinweise. Gesucht ist: Hand. |
| body_05 | en | prompt | What can feel whether a cloth is soft? | Touch. You search for a soft ball without looking. What can feel its surface? |
| body_05 | en | tip | The skin on your hand contains touch receptors. | Use both clues. The answer is hand. |
| body_05 | ru | prompt | Чем можно почувствовать, мягкая ли ткань? | Осязание. Не глядя ищешь мягкий мяч. Чем можно ощупать его поверхность? |
| body_05 | ru | tip | В коже руки есть чувствительные клетки, воспринимающие прикосновения. | Учти обе подсказки. Ответ: кисть. |
| body_06 | de | prompt | Welches Organ pumpt Blut durch den Körper? | Antreiben. Die Muskeln brauchen Blut. Welches Organ treibt es auch gegen die Schwerkraft an? |
| body_06 | de | tip | Das Herz ist ein Muskel, der Blut durch die Blutgefäße pumpt. | Überlege beide Hinweise. Gesucht ist: Herz. |
| body_06 | en | prompt | Which organ pumps blood around the body? | Pumping. Muscles need blood. Which organ drives it even against gravity? |
| body_06 | en | tip | The heart is a muscle that pumps blood through blood vessels. | Use both clues. The answer is heart. |
| body_06 | ru | prompt | Какой орган перекачивает кровь по телу? | Движение. Мышцам нужна кровь. Какой орган двигает её даже против силы тяжести? |
| body_06 | ru | tip | Сердце — мышца, которая перекачивает кровь по сосудам. | Учти обе подсказки. Ответ: сердце. |
| body_07 | de | prompt | Welche Organe nehmen beim Atmen Luft auf? | Atmen. Sauerstoff ist in der Luft. Welche Organe geben ihn beim Atmen ans Blut weiter? |
| body_07 | de | tip | In der Lunge gelangt Sauerstoff aus der Luft ins Blut. | Überlege beide Hinweise. Gesucht ist: Lunge. |
| body_07 | en | prompt | Which organs take in air when you breathe? | Breathing. Oxygen is in the air. Which organs pass it into the blood when you breathe? |
| body_07 | en | tip | In the lungs, oxygen moves from the air into the blood. | Use both clues. The answer is lungs. |
| body_07 | ru | prompt | Какие органы принимают воздух при дыхании? | Дыхание. Кислород находится в воздухе. Какие органы при дыхании передают его крови? |
| body_07 | ru | tip | В лёгких кислород из воздуха поступает в кровь. | Учти обе подсказки. Ответ: лёгкие. |
| body_08 | de | prompt | Welches Organ verarbeitet Sinneseindrücke? | Denken. Ein Geräusch kommt dir bekannt vor. Welches Organ vergleicht es mit Erinnerungen? |
| body_08 | de | tip | Das Gehirn verarbeitet Signale und steuert viele Vorgänge. | Überlege beide Hinweise. Gesucht ist: Gehirn. |
| body_08 | en | prompt | Which organ processes information from your senses? | Thinking. A sound seems familiar. Which organ compares it with memories? |
| body_08 | en | tip | The brain processes signals and controls many activities. | Use both clues. The answer is brain. |
| body_08 | ru | prompt | Какой орган обрабатывает сигналы органов чувств? | Мысли. Звук кажется знакомым. Какой орган сравнивает его с воспоминаниями? |
| body_08 | ru | tip | Мозг обрабатывает сигналы и управляет многими процессами. | Учти обе подсказки. Ответ: мозг. |
| body_09 | de | prompt | Was bildet das feste Gerüst im Körper? | Stützen. Die Haut ist weich. Was stützt den Körper von innen und schützt wichtige Organe? |
| body_09 | de | tip | Die Knochen bilden zusammen das Skelett. | Überlege beide Hinweise. Gesucht ist: Knochen. |
| body_09 | en | prompt | What forms the body's hard framework? | Support. Skin is soft. What supports the body inside and protects important organs? |
| body_09 | en | tip | The bones together form the skeleton. | Use both clues. The answer is bone. |
| body_09 | ru | prompt | Что образует твёрдую опору тела? | Опора. Кожа мягкая. Что поддерживает тело изнутри и защищает важные органы? |
| body_09 | ru | tip | Кости вместе образуют скелет. | Учти обе подсказки. Ответ: кость. |
| body_10 | de | prompt | Womit zerkleinerst du Essen im Mund? | Zerkleinern. Große Essensstücke passen schlecht zum Schlucken. Was macht sie beim Kauen kleiner? |
| body_10 | de | tip | Zähne zerkleinern Nahrung beim Kauen. | Überlege beide Hinweise. Gesucht ist: Zahn. |
| body_10 | en | prompt | What breaks food into smaller pieces in your mouth? | Biting. Large pieces of food are hard to swallow. What makes them smaller when chewing? |
| body_10 | en | tip | Teeth break up food when you chew. | Use both clues. The answer is tooth. |
| body_10 | ru | prompt | Чем измельчают пищу во рту? | Измельчение. Большие куски пищи трудно глотать. Что измельчает их при жевании? |
| body_10 | ru | tip | Зубы измельчают пищу при жевании. | Учти обе подсказки. Ответ: зуб. |
| body_11 | de | prompt | Wohin gelangt Essen nach der Speiseröhre? | Verdauen. Nach dem Kauen rutscht Essen durch die Speiseröhre. Wo wird es weiter durchmischt? |
| body_11 | de | tip | Nach der Speiseröhre gelangt Nahrung in den Magen. | Überlege beide Hinweise. Gesucht ist: Magen. |
| body_11 | en | prompt | Where does food go after the food pipe? | Digestion. After chewing, food travels down the food pipe. Where is it mixed next? |
| body_11 | en | tip | Food moves through the food pipe into the stomach. | Use both clues. The answer is stomach. |
| body_11 | ru | prompt | Куда попадает пища после пищевода? | Пищеварение. После жевания еда проходит по пищеводу. Где её дальше перемешивают? |
| body_11 | ru | tip | По пищеводу пища поступает в желудок. | Учти обе подсказки. Ответ: желудок. |
| body_12 | de | prompt | Was hilft, die Hände sauber zu waschen? | Reinigen. Fettiger Schmutz bleibt an den Fingern. Was hilft Wasser, ihn abzulösen? |
| body_12 | de | tip | Wasche die Hände mit Wasser und Seife, auch zwischen den Fingern. | Überlege beide Hinweise. Gesucht ist: Seife. |
| body_12 | en | prompt | What helps wash your hands clean? | Cleaning. Greasy dirt stays on your fingers. What helps water wash it away? |
| body_12 | en | tip | Wash with water and soap, including between your fingers. | Use both clues. The answer is soap. |
| body_12 | ru | prompt | Что помогает хорошо вымыть руки? | Чистота. Жирная грязь остаётся на пальцах. Что помогает воде её смыть? |
| body_12 | ru | tip | Мой руки водой с мылом, в том числе между пальцами. | Учти обе подсказки. Ответ: мыло. |
| body_13 | de | prompt | Was eignet sich als Durstlöscher? | Trinken. Beim Spielen verlierst du Flüssigkeit. Was ersetzt sie, ohne Zucker hinzuzufügen? |
| body_13 | de | tip | Sauberes Trinkwasser löscht Durst ohne zugesetzten Zucker. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| body_13 | en | prompt | What is a good drink when you are thirsty? | Drink. You lose fluid while playing. What replaces it without adding sugar? |
| body_13 | en | tip | Clean drinking water quenches thirst without added sugar. | Use both clues. The answer is water. |
| body_13 | ru | prompt | Что хорошо утоляет жажду? | Пить. Во время игры теряется жидкость. Что восполнит её без добавления сахара? |
| body_13 | ru | tip | Чистая питьевая вода утоляет жажду без добавленного сахара. | Учти обе подсказки. Ответ: вода. |
| body_14 | de | prompt | Welches Bild steht hier für die Nacht und die Schlafenszeit? | Ruhen. Tagsüber übst du, nachts erholt sich dein Körper. Welches Bild erinnert an diese Ruhezeit? |
| body_14 | de | tip | Nachts ist es dunkel. Schlaf gibt dem Körper Zeit zur Erholung. | Überlege beide Hinweise. Gesucht ist: Mond. |
| body_14 | en | prompt | Which picture here stands for nighttime and bedtime? | Rest. You practise by day and recover at night. Which picture suggests this rest time? |
| body_14 | en | tip | Night is dark. Sleep gives the body time to rest. | Use both clues. The answer is moon. |
| body_14 | ru | prompt | Какая картинка здесь обозначает ночь и время сна? | Отдых. Днём ты занимаешься, ночью тело отдыхает. Какая картинка напоминает об этом времени отдыха? |
| body_14 | ru | tip | Ночью темно. Сон даёт организму время на восстановление. | Учти обе подсказки. Ответ: Луна. |
| body_15 | de | prompt | Welcher Körperteil trägt oft einen Schuh? | Tragen. Beim Gehen rollt ein Körperteil von der Ferse zu den Zehen ab. Welcher? |
| body_15 | de | tip | Schuhe schützen die Füße. Nicht jeder Mensch bewegt sich auf dieselbe Weise. | Überlege beide Hinweise. Gesucht ist: Fuß. |
| body_15 | en | prompt | Which body part often wears a shoe? | Support. When walking, a body part rolls from heel to toes. Which one? |
| body_15 | en | tip | Shoes protect feet. People move in different ways. | Use both clues. The answer is foot. |
| body_15 | ru | prompt | На какую часть тела обычно надевают обувь? | Опора. При ходьбе часть тела перекатывается с пятки на пальцы. Какая? |
| body_15 | ru | tip | Обувь защищает стопы. Люди могут передвигаться по-разному. | Учти обе подсказки. Ответ: стопа. |
| body_16 | de | prompt | Was schützt den Kopf beim Fahrradfahren? | Schützen. Ein Sturz lässt sich nicht immer verhindern. Was kann dabei den Kopf schützen? |
| body_16 | de | tip | Ein gut sitzender Helm kann den Kopf bei einem Sturz schützen. | Überlege beide Hinweise. Gesucht ist: Helm. |
| body_16 | en | prompt | What protects your head when cycling? | Protection. A fall cannot always be prevented. What can protect your head during one? |
| body_16 | en | tip | A well-fitted helmet can protect your head if you fall. | Use both clues. The answer is helmet. |
| body_16 | ru | prompt | Что защищает голову на велосипеде? | Защита. Падение не всегда можно предотвратить. Что может защитить при нём голову? |
| body_16 | ru | tip | Правильно подобранный шлем может защитить голову при падении. | Учти обе подсказки. Ответ: шлем. |
| body_17 | de | prompt | Welcher Sinn braucht Schutz vor sehr lauten Tönen? | Hören. Laute Musik kann schaden, auch wenn nichts wehtut. Welcher Körperteil braucht Schutz? |
| body_17 | de | tip | Zu laute Töne können dem Gehör schaden. Drehe die Lautstärke herunter. | Überlege beide Hinweise. Gesucht ist: Ohr. |
| body_17 | en | prompt | Which sense needs protection from very loud sounds? | Hearing. Loud music can cause harm even without pain. Which body part needs protection? |
| body_17 | en | tip | Very loud sounds can harm hearing. Turn the volume down. | Use both clues. The answer is ear. |
| body_17 | ru | prompt | Какое чувство нужно защищать от очень громких звуков? | Слух. Громкая музыка может вредить даже без боли. Какая часть тела нуждается в защите? |
| body_17 | ru | tip | Слишком громкие звуки могут повредить слух. Уменьшай громкость. | Учти обе подсказки. Ответ: ухо. |
| body_18 | de | prompt | Welchen Körperteil schützen Augenlider? | Sehen. Du blinzelst, damit die Oberfläche feucht und sauber bleibt. Welchen Körperteil schützt das? |
| body_18 | de | tip | Augenlider schützen die Augen. Blinzeln verteilt Tränenflüssigkeit. | Überlege beide Hinweise. Gesucht ist: Auge. |
| body_18 | en | prompt | Which body part do eyelids protect? | Seeing. You blink to keep a surface moist and clean. Which body part does this protect? |
| body_18 | en | tip | Eyelids protect the eyes. Blinking spreads tear fluid. | Use both clues. The answer is eye. |
| body_18 | ru | prompt | Что защищают веки? | Зрение. Ты моргаешь, чтобы поверхность оставалась влажной и чистой. Какую часть тела это защищает? |
| body_18 | ru | tip | Веки защищают глаза. Моргание распределяет слёзную жидкость. | Учти обе подсказки. Ответ: глаз. |
| body_19 | de | prompt | Welcher Körperteil hilft, eingeatmete Luft zu filtern? | Entdecken. Atemluft kommt herein. Welcher Körperteil hält mit Härchen einen Teil des Staubs zurück? |
| body_19 | de | tip | Die Nase filtert, erwärmt und befeuchtet eingeatmete Luft. | Überlege beide Hinweise. Gesucht ist: Nase. |
| body_19 | en | prompt | Which body part helps filter the air you breathe in? | Explore. Air enters as you breathe. Which body part traps some dust with tiny hairs? |
| body_19 | en | tip | The nose filters, warms and moistens incoming air. | Use both clues. The answer is nose. |
| body_19 | ru | prompt | Что помогает очищать вдыхаемый воздух? | Открытие. При вдохе поступает воздух. Какая часть тела задерживает часть пыли волосками? |
| body_19 | ru | tip | Нос очищает, согревает и увлажняет вдыхаемый воздух. | Учти обе подсказки. Ответ: нос. |
| body_20 | de | prompt | Was fällt bei vielen Kindern aus und wächst neu nach? | Zerkleinern. Ein Milchzahn wird locker, darunter wächst etwas nach. Welcher Körperteil ersetzt ihn? |
| body_20 | de | tip | Milchzähne machen nach und nach Platz für bleibende Zähne. | Überlege beide Hinweise. Gesucht ist: Zahn. |
| body_20 | en | prompt | What do many children lose and replace as they grow? | Biting. A baby tooth loosens and something grows below. Which body part replaces it? |
| body_20 | en | tip | Baby teeth gradually make way for adult teeth. | Use both clues. The answer is tooth. |
| body_20 | ru | prompt | Что у многих детей выпадает и заменяется новым? | Измельчение. Молочный зуб шатается, снизу растёт новый. Какая часть тела его заменит? |
| body_20 | ru | tip | Молочные зубы постепенно сменяются постоянными. | Учти обе подсказки. Ответ: зуб. |
| body_21 | de | prompt | Welcher Körperteil hat normalerweise fünf Finger? | Greifen. Zum Greifen arbeiten Daumen und andere Finger zusammen. Welcher Körperteil ist gemeint? |
| body_21 | de | tip | Eine Hand hat normalerweise fünf Finger. Körper können verschieden aussehen. | Überlege beide Hinweise. Gesucht ist: Hand. |
| body_21 | en | prompt | Which body part usually has five fingers? | Grasp. The thumb works with the other fingers to grasp. Which body part is meant? |
| body_21 | en | tip | A hand usually has five fingers. Bodies can look different. | Use both clues. The answer is hand. |
| body_21 | ru | prompt | У какой части тела обычно пять пальцев? | Брать. Чтобы взять предмет, большой палец работает вместе с остальными. Какая часть тела имеется в виду? |
| body_21 | ru | tip | У кисти обычно пять пальцев. Тела людей могут выглядеть по-разному. | Учти обе подсказки. Ответ: кисть. |
| body_22 | de | prompt | Was schlägt meist schneller, wenn du dich anstrengst? | Antreiben. Beim Rennen brauchen Muskeln mehr Sauerstoff. Was pumpt dafür meist schneller? |
| body_22 | de | tip | Das Herz schlägt oft schneller, damit die Muskeln mehr Sauerstoff bekommen. | Überlege beide Hinweise. Gesucht ist: Herz. |
| body_22 | en | prompt | What usually beats faster when you exercise? | Pumping. Running muscles need more oxygen. What usually pumps faster to deliver it? |
| body_22 | en | tip | The heart often beats faster to bring muscles more oxygen. | Use both clues. The answer is heart. |
| body_22 | ru | prompt | Что обычно бьётся быстрее при физической нагрузке? | Движение. При беге мышцам нужно больше кислорода. Что обычно качает кровь быстрее? |
| body_22 | ru | tip | Сердце часто бьётся быстрее, чтобы мышцы получали больше кислорода. | Учти обе подсказки. Ответ: сердце. |
| body_23 | de | prompt | Wohin strömt Luft beim Einatmen? | Atmen. Brust und Bauch bewegen sich beim Atmen. Welche Organe füllen sich dabei mit Luft? |
| body_23 | de | tip | Die Luft strömt durch die Atemwege in die Lunge. | Überlege beide Hinweise. Gesucht ist: Lunge. |
| body_23 | en | prompt | Where does air go when you breathe in? | Breathing. Your chest and belly move while breathing. Which organs fill with air? |
| body_23 | en | tip | Air travels through the airways into the lungs. | Use both clues. The answer is lungs. |
| body_23 | ru | prompt | Куда поступает воздух при вдохе? | Дыхание. При дыхании двигаются грудь и живот. Какие органы наполняются воздухом? |
| body_23 | ru | tip | Воздух проходит по дыхательным путям в лёгкие. | Учти обе подсказки. Ответ: лёгкие. |
| body_24 | de | prompt | Wo werden viele Erinnerungen verarbeitet? | Denken. Du weißt noch, wo ein Spielzeug liegt. Welches Organ hilft mit dieser Erinnerung? |
| body_24 | de | tip | Das Gehirn hilft dir beim Lernen und Erinnern. | Überlege beide Hinweise. Gesucht ist: Gehirn. |
| body_24 | en | prompt | Where are many memories processed? | Thinking. You remember where a toy is. Which organ helps with this memory? |
| body_24 | en | tip | The brain helps you learn and remember. | Use both clues. The answer is brain. |
| body_24 | ru | prompt | Где обрабатывается много воспоминаний? | Мысли. Ты помнишь, где лежит игрушка. Какой орган помогает этим воспоминанием? |
| body_24 | ru | tip | Мозг помогает учиться и запоминать. | Учти обе подсказки. Ответ: мозг. |
| body_25 | de | prompt | Was schützt das Gehirn als Schädel? | Stützen. Ein Helm schützt außen. Was bildet im Kopf darunter eine feste Schutzkapsel? |
| body_25 | de | tip | Die Knochen des Schädels umgeben und schützen das Gehirn. | Überlege beide Hinweise. Gesucht ist: Knochen. |
| body_25 | en | prompt | What protects the brain as the skull? | Support. A helmet protects outside. What forms a hard protective case beneath it in your head? |
| body_25 | en | tip | The skull bones surround and protect the brain. | Use both clues. The answer is bone. |
| body_25 | ru | prompt | Что образует череп и защищает мозг? | Опора. Шлем защищает снаружи. Что образует под ним твёрдую защитную оболочку головы? |
| body_25 | ru | tip | Кости черепа окружают и защищают мозг. | Учти обе подсказки. Ответ: кость. |
| body_26 | de | prompt | Welches Organ mischt und verdaut Nahrung weiter? | Verdauen. Geschluckte Nahrung wird geknetet und mit Verdauungssaft vermischt. Welches Organ macht das? |
| body_26 | de | tip | Der Magen knetet Nahrung und mischt sie mit Magensaft. | Überlege beide Hinweise. Gesucht ist: Magen. |
| body_26 | en | prompt | Which organ mixes food and continues digestion? | Digestion. Swallowed food is churned and mixed with digestive juice. Which organ does this? |
| body_26 | en | tip | The stomach churns food and mixes it with digestive juices. | Use both clues. The answer is stomach. |
| body_26 | ru | prompt | Какой орган перемешивает пищу и продолжает пищеварение? | Пищеварение. Проглоченная пища перемешивается с пищеварительным соком. Какой орган это делает? |
| body_26 | ru | tip | Желудок перемешивает пищу с желудочным соком. | Учти обе подсказки. Ответ: желудок. |
| body_27 | de | prompt | Welcher Körperteil nimmt beim Essen Duftstoffe wahr? | Riechen. Ein Essen kann auch ohne Probieren appetitlich duften. Was nimmt den Duft auf? |
| body_27 | de | tip | Beim Essen arbeiten Geruchssinn und Geschmackssinn zusammen. | Überlege beide Hinweise. Gesucht ist: Nase. |
| body_27 | en | prompt | Which part of the body senses smells while you eat? | Smell. Food can smell inviting without tasting it. What detects the scent? |
| body_27 | en | tip | Smell and taste work together when you eat. | Use both clues. The answer is nose. |
| body_27 | ru | prompt | Какая часть тела чувствует запахи во время еды? | Запах. Еда может приятно пахнуть даже без пробы на вкус. Что воспринимает запах? |
| body_27 | ru | tip | Во время еды обоняние и вкус работают вместе. | Учти обе подсказки. Ответ: нос. |
| body_28 | de | prompt | Was nimmst du zum Händewaschen vor dem Essen? | Reinigen. Nach dem Toilettengang reicht kurzes Abwischen nicht. Was gehört zum Waschen mit Wasser? |
| body_28 | de | tip | Wasser und Seife helfen, Schmutz und viele Keime zu entfernen. | Überlege beide Hinweise. Gesucht ist: Seife. |
| body_28 | en | prompt | What do you use to wash your hands before eating? | Cleaning. A quick wipe after using the toilet is not enough. What belongs with water when washing? |
| body_28 | en | tip | Water and soap help remove dirt and many germs. | Use both clues. The answer is soap. |
| body_28 | ru | prompt | Чем моют руки перед едой? | Чистота. После туалета недостаточно быстро вытереть руки. Что нужно для мытья вместе с водой? |
| body_28 | ru | tip | Вода и мыло помогают смыть грязь и многие микробы. | Учти обе подсказки. Ответ: мыло. |
| body_29 | de | prompt | Was davon ist ein Lebensmittel? | Entdecken. Dein Körper braucht Nahrung, keine Reinigungsmittel oder Batterien. Was liefert ihm essbare Energie? |
| body_29 | de | tip | Ein gewaschener Apfel ist ein Lebensmittel. Batterien und Seife sind keines. | Überlege beide Hinweise. Gesucht ist: Apfel. |
| body_29 | en | prompt | Which of these is food? | Explore. Your body needs food, not cleaners or batteries. What provides edible energy? |
| body_29 | en | tip | A washed apple is food. Batteries and soap are not. | Use both clues. The answer is apple. |
| body_29 | ru | prompt | Что из этого является едой? | Открытие. Телу нужна пища, а не моющие средства или батарейки. Что даст ему пищевую энергию? |
| body_29 | ru | tip | Вымытое яблоко — еда. Батарейки и мыло не едят. | Учти обе подсказки. Ответ: яблоко. |
| body_30 | de | prompt | Was befindet sich im Fuß und gibt Halt? | Stützen. Muskeln bewegen den Fuß. Welche festen Teile geben ihnen im Fuß Halt? |
| body_30 | de | tip | Im Fuß liegen viele Knochen, die zusammen Halt geben. | Überlege beide Hinweise. Gesucht ist: Knochen. |
| body_30 | en | prompt | What is inside a foot and gives it support? | Support. Muscles move the foot. Which hard parts support them inside it? |
| body_30 | en | tip | A foot contains many bones that work together for support. | Use both clues. The answer is bone. |
| body_30 | ru | prompt | Что находится внутри стопы и даёт ей опору? | Опора. Мышцы двигают стопу. Какие твёрдые части дают им опору внутри неё? |
| body_30 | ru | tip | В стопе много костей, которые вместе создают опору. | Учти обе подсказки. Ответ: кость. |
| body_31 | de | prompt | Welches Organ verarbeitet die Signale der Ohren, damit du Geräusche erkennst? | Denken. Das Ohr empfängt Töne. Welches Organ macht daraus erkannte Wörter? |
| body_31 | de | tip | Die Signale gelangen zum Gehirn, das Geräusche verarbeitet. | Überlege beide Hinweise. Gesucht ist: Gehirn. |
| body_31 | en | prompt | Which organ processes signals from your ears so you recognize sounds? | Thinking. The ear receives sounds. Which organ turns them into recognised words? |
| body_31 | en | tip | The signals go to the brain, which processes sounds. | Use both clues. The answer is brain. |
| body_31 | ru | prompt | Какой орган обрабатывает сигналы от ушей, чтобы ты узнавал звуки? | Мысли. Ухо воспринимает звуки. Какой орган превращает их в узнанные слова? |
| body_31 | ru | tip | Сигналы поступают в мозг, где обрабатываются звуки. | Учти обе подсказки. Ответ: мозг. |
| body_32 | de | prompt | Wohin senden die Augen ihre Signale? | Denken. Die Augen liefern Lichtsignale. Welches Organ fügt sie zu einem erkannten Bild zusammen? |
| body_32 | de | tip | Die Augen senden Signale an das Gehirn. Dort werden Bilder verarbeitet. | Überlege beide Hinweise. Gesucht ist: Gehirn. |
| body_32 | en | prompt | Where do eyes send their signals? | Think. Eyes send light signals. Which organ combines them into a recognised image? |
| body_32 | en | tip | Eyes send signals to the brain, where images are processed. | Use both clues. The answer is brain. |
| body_32 | ru | prompt | Куда глаза посылают сигналы? | Думать. Глаза посылают световые сигналы. Какой орган собирает из них знакомый образ? |
| body_32 | ru | tip | Глаза посылают сигналы в мозг. Там обрабатываются изображения. | Учти обе подсказки. Ответ: мозг. |
| body_33 | de | prompt | Welches Organ bringt Sauerstoff aus der Luft ins Blut? | Atmen. Im Blut ist zu wenig Sauerstoff. Welche Organe nehmen neuen aus der Atemluft auf? |
| body_33 | de | tip | In den Lungenbläschen kann Sauerstoff ins Blut gelangen. | Überlege beide Hinweise. Gesucht ist: Lunge. |
| body_33 | en | prompt | Which organ brings oxygen from air into the blood? | Breathe. Blood needs more oxygen. Which organs take fresh oxygen from inhaled air? |
| body_33 | en | tip | Oxygen can enter the blood in the tiny air sacs of the lungs. | Use both clues. The answer is lungs. |
| body_33 | ru | prompt | Какой орган передаёт кислород из воздуха в кровь? | Дышать. Крови нужен кислород. Какие органы получают его из вдыхаемого воздуха? |
| body_33 | ru | tip | В лёгочных пузырьках кислород поступает в кровь. | Учти обе подсказки. Ответ: лёгкие. |
| body_34 | de | prompt | Welches Organ ist ein kräftiger Muskel in der Brust? | Antreiben. Dieses Organ ist ein Muskel und arbeitet auch im Schlaf. Was hält das Blut in Bewegung? |
| body_34 | de | tip | Das Herz ist ein Muskel und arbeitet auch, während du schläfst. | Überlege beide Hinweise. Gesucht ist: Herz. |
| body_34 | en | prompt | Which organ is a strong muscle in the chest? | Pumping. This organ is a muscle and works during sleep. What keeps blood moving? |
| body_34 | en | tip | The heart is a muscle that works even while you sleep. | Use both clues. The answer is heart. |
| body_34 | ru | prompt | Какой орган — сильная мышца в груди? | Движение. Этот орган состоит из мышечной ткани и работает даже во сне. Что поддерживает движение крови? |
| body_34 | ru | tip | Сердце — мышца. Оно работает даже во сне. | Учти обе подсказки. Ответ: сердце. |
| body_35 | de | prompt | Was fühlt sich meist weich und biegsam an? | Fühlen. Ein Verband soll sich um den Arm legen lassen. Welches Material ist weich und biegsam? |
| body_35 | de | tip | Ein weiches Tuch lässt sich mit der Hand fühlen und falten. | Überlege beide Hinweise. Gesucht ist: Stoff. |
| body_35 | en | prompt | What usually feels soft and bendy? | Touch. A bandage must wrap around an arm. Which material is soft and flexible? |
| body_35 | en | tip | You can feel and fold a soft cloth with your hand. | Use both clues. The answer is fabric. |
| body_35 | ru | prompt | Что обычно мягкое на ощупь и легко сгибается? | Осязание. Повязка должна обернуться вокруг руки. Какой материал мягкий и гибкий? |
| body_35 | ru | tip | Мягкую ткань можно ощупать и сложить рукой. | Учти обе подсказки. Ответ: ткань. |
| body_36 | de | prompt | Welchen Körperteil reinigst du mit einer Zahnbürste? | Pflegen. Ein Belag bleibt nach dem Essen zurück. Welchen Körperteil reinigst du deshalb mit einer Bürste? |
| body_36 | de | tip | Zähne brauchen regelmäßige Pflege. Ein Erwachsener kann beim Nachputzen helfen. | Überlege beide Hinweise. Gesucht ist: Zahn. |
| body_36 | en | prompt | Which body part do you clean with a toothbrush? | Care. A coating remains after eating. Which body part do you therefore clean with a brush? |
| body_36 | en | tip | Teeth need regular cleaning. An adult can help finish brushing. | Use both clues. The answer is tooth. |
| body_36 | ru | prompt | Что чистят зубной щёткой? | Уход. После еды остаётся налёт. Какую часть тела поэтому чистят щёткой? |
| body_36 | ru | tip | Зубы нужно регулярно чистить. Взрослый может помочь дочистить их. | Учти обе подсказки. Ответ: зуб. |
| body_37 | de | prompt | Wodurch kannst du beim ruhigen Atmen Luft einziehen? | Entdecken. Du atmest ruhig ein und hältst den Mund geschlossen. Wo strömt die Luft hinein? |
| body_37 | de | tip | Beim ruhigen Atmen kann Luft durch die Nase einströmen. | Überlege beide Hinweise. Gesucht ist: Nase. |
| body_37 | en | prompt | What can you breathe through when resting? | Explore. You breathe calmly with your mouth closed. Where does the air enter? |
| body_37 | en | tip | When resting, air can enter through your nose. | Use both clues. The answer is nose. |
| body_37 | ru | prompt | Через что можно вдыхать воздух в покое? | Открытие. Ты спокойно вдыхаешь с закрытым ртом. Куда поступает воздух? |
| body_37 | ru | tip | В покое воздух может поступать через нос. | Учти обе подсказки. Ответ: нос. |
| body_38 | de | prompt | Womit hörst du die Musik in diesem Spiel? | Hören. Eine Melodie bleibt erkennbar, obwohl es dunkel ist. Welcher Körperteil empfängt sie? |
| body_38 | de | tip | Die Ohren nehmen die Musik auf. Halte die Lautstärke angenehm leise. | Überlege beide Hinweise. Gesucht ist: Ohr. |
| body_38 | en | prompt | What helps you hear this game's music? | Hearing. You can recognise a tune in the dark. Which body part receives it? |
| body_38 | en | tip | The ears detect music. Keep it at a comfortable, quiet volume. | Use both clues. The answer is ear. |
| body_38 | ru | prompt | Что помогает слышать музыку в этой игре? | Слух. Мелодию можно узнать даже в темноте. Какая часть тела её воспринимает? |
| body_38 | ru | tip | Уши воспринимают музыку. Выбирай удобную негромкую громкость. | Учти обе подсказки. Ответ: ухо. |
| body_39 | de | prompt | Was braucht der Körper zum Trinken? | Trinken. Blut transportiert Stoffe in Flüssigkeit. Was muss der Körper deshalb regelmäßig trinken? |
| body_39 | de | tip | Trinkwasser versorgt den Körper mit Flüssigkeit. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| body_39 | en | prompt | What does the body need to drink? | Drink. Blood carries substances in fluid. What must the body therefore drink regularly? |
| body_39 | en | tip | Drinking water provides the body with fluid. | Use both clues. The answer is water. |
| body_39 | ru | prompt | Что нужно организму для питья? | Пить. Кровь переносит вещества в жидкости. Что поэтому нужно регулярно пить? |
| body_39 | ru | tip | Питьевая вода обеспечивает организм жидкостью. | Учти обе подсказки. Ответ: вода. |
| body_40 | de | prompt | Womit kannst du einen weichen Ball vorsichtig greifen? | Fühlen. Du willst einen Ball fangen, statt ihn wegzutreten. Welcher Körperteil greift zu? |
| body_40 | de | tip | Mit Hand und Fingern kannst du einen Ball greifen. Menschen nutzen auch Hilfsmittel. | Überlege beide Hinweise. Gesucht ist: Hand. |
| body_40 | en | prompt | What can gently hold a soft ball? | Touch. You want to catch a ball rather than kick it away. Which body part grasps it? |
| body_40 | en | tip | Hands and fingers can hold a ball. People also use helpful tools. | Use both clues. The answer is hand. |
| body_40 | ru | prompt | Чем можно осторожно взять мягкий мяч? | Осязание. Ты хочешь поймать мяч, а не пнуть его. Какая часть тела его возьмёт? |
| body_40 | ru | tip | Кистью и пальцами можно взять мяч. Люди также используют вспомогательные средства. | Учти обе подсказки. Ответ: кисть. |
| geography_01 | de | prompt | Was zeigt die Erde als kleine Kugel? | Orientieren. Du willst auch die Rückseite der Erde sehen und das Modell drehen. Was nimmst du? |
| geography_01 | de | tip | Ein Globus ist ein verkleinertes Modell der Erde. | Überlege beide Hinweise. Gesucht ist: Globus. |
| geography_01 | en | prompt | What shows Earth as a small sphere? | Direction. You want to turn a model to see Earth's far side too. What do you use? |
| geography_01 | en | tip | A globe is a small model of Earth. | Use both clues. The answer is globe. |
| geography_01 | ru | prompt | Что показывает Землю в виде маленького шара? | Ориентир. Нужно повернуть модель, чтобы увидеть обратную сторону Земли. Что выбрать? |
| geography_01 | ru | tip | Глобус — уменьшенная модель Земли. | Учти обе подсказки. Ответ: глобус. |
| geography_02 | de | prompt | Welche Zeichnung auf einem flachen Blatt zeigt Orte und Wege von oben? | Orientieren. Du brauchst Straßen und Orte von oben auf einem faltbaren Blatt. Welche Darstellung passt? |
| geography_02 | de | tip | Eine Karte zeigt einen Ausschnitt der Welt von oben und verkleinert. | Überlege beide Hinweise. Gesucht ist: Karte. |
| geography_02 | en | prompt | Which drawing on a flat sheet shows places and paths from above? | Direction. You need streets and places from above on a foldable sheet. Which representation fits? |
| geography_02 | en | tip | A map shows part of the world from above on a smaller scale. | Use both clues. The answer is map. |
| geography_02 | ru | prompt | Какой рисунок на плоском листе показывает места и дороги сверху? | Ориентир. Нужны улицы и места сверху на складывающемся листе. Какое изображение подходит? |
| geography_02 | ru | tip | Карта показывает часть мира сверху в уменьшенном виде. | Учти обе подсказки. Ответ: карта. |
| geography_03 | de | prompt | Welches Gerät hat eine Nadel, die nach Norden zeigt? | Orientieren. Die Karte zeigt Wege, aber du kennst Norden nicht. Welches Gerät ergänzt die Karte? |
| geography_03 | de | tip | Ein Kompass hilft, Norden und die anderen Himmelsrichtungen zu finden. | Überlege beide Hinweise. Gesucht ist: Kompass. |
| geography_03 | en | prompt | Which instrument has a needle that points north? | Direction. The map shows routes but you do not know north. Which instrument complements it? |
| geography_03 | en | tip | A compass helps you find north and the other directions. | Use both clues. The answer is compass. |
| geography_03 | ru | prompt | У какого прибора есть стрелка, показывающая на север? | Ориентир. Карта показывает пути, но ты не знаешь, где север. Какой прибор её дополнит? |
| geography_03 | ru | tip | Компас помогает находить север и другие стороны света. | Учти обе подсказки. Ответ: компас. |
| geography_04 | de | prompt | Was ragt hoch über seine Umgebung hinaus? | Entdecken. Ein Gipfel liegt weit über seinen Tälern. Welche Landschaftsform ist das? |
| geography_04 | de | tip | Ein Berg ist eine hohe Erhebung im Gelände. | Überlege beide Hinweise. Gesucht ist: Berg. |
| geography_04 | en | prompt | What rises high above the land around it? | Explore. A summit stands far above its valleys. Which landform is this? |
| geography_04 | en | tip | A mountain is a high landform. | Use both clues. The answer is mountain. |
| geography_04 | ru | prompt | Что высоко поднимается над окружающей местностью? | Открытие. Вершина находится намного выше своих долин. Какая это форма рельефа? |
| geography_04 | ru | tip | Гора — высокая возвышенность на поверхности земли. | Учти обе подсказки. Ответ: гора. |
| geography_05 | de | prompt | Was fließt in einem Bett durch die Landschaft? | Entdecken. Wasser bewegt sich von einer Quelle zwischen Ufern bergab. Welches Gewässer entsteht? |
| geography_05 | de | tip | Ein Fluss führt Wasser durch sein Flussbett. | Überlege beide Hinweise. Gesucht ist: Fluss. |
| geography_05 | en | prompt | What flows in a channel through the landscape? | Explore. Water moves downhill from a spring between banks. Which body of water forms? |
| geography_05 | en | tip | A river carries water along its riverbed. | Use both clues. The answer is river. |
| geography_05 | ru | prompt | Что течёт по руслу через местность? | Открытие. Вода течёт от источника вниз между берегами. Какой водоём образуется? |
| geography_05 | ru | tip | Река несёт воду по своему руслу. | Учти обе подсказки. Ответ: река. |
| geography_06 | de | prompt | Was ist ganz von Wasser umgebenes Land? | Entdecken. Du folgst dem Ufer ganz herum und kommst zum Start zurück. Welches Landstück passt? |
| geography_06 | de | tip | Eine Insel ist auf allen Seiten von Wasser umgeben. | Überlege beide Hinweise. Gesucht ist: Insel. |
| geography_06 | en | prompt | What is land surrounded by water on all sides? | Explore. You follow the shore all the way around and return to the start. Which landform fits? |
| geography_06 | en | tip | An island is surrounded by water on every side. | Use both clues. The answer is island. |
| geography_06 | ru | prompt | Как называется суша, со всех сторон окружённая водой? | Исследовать. Ты обходишь весь берег и возвращаешься к началу. Какой участок суши подходит? |
| geography_06 | ru | tip | Остров со всех сторон окружён водой. | Учти обе подсказки. Ответ: остров. |
| geography_07 | de | prompt | Wo findest du sehr viel Salzwasser? | Entdecken. Ein Fluss bringt Süßwasser zu einem sehr großen salzigen Gewässer. Wohin fließt er? |
| geography_07 | de | tip | Meere enthalten Salzwasser und bedecken große Teile der Erde. | Überlege beide Hinweise. Gesucht ist: Meer. |
| geography_07 | en | prompt | Where can you find a very large amount of salt water? | Explore. A river carries fresh water to a very large salty body. Where does it flow? |
| geography_07 | en | tip | Seas contain salt water and cover large parts of Earth. | Use both clues. The answer is sea. |
| geography_07 | ru | prompt | Где находится очень много солёной воды? | Исследовать. Река несёт пресную воду в очень большой солёный водоём. Куда она впадает? |
| geography_07 | ru | tip | Моря содержат солёную воду и покрывают большие части Земли. | Учти обе подсказки. Ответ: море. |
| geography_08 | de | prompt | Wo fällt über lange Zeit sehr wenig Niederschlag? | Beobachten. Nicht Hitze, sondern sehr wenig Niederschlag entscheidet. Welche Landschaft kann deshalb auch kalt sein? |
| geography_08 | de | tip | In einer Wüste fällt sehr wenig Niederschlag. Es gibt auch kalte Wüsten. | Überlege beide Hinweise. Gesucht ist: Wüste. |
| geography_08 | en | prompt | Where is there very little precipitation over a long time? | Observe. Very little precipitation, not heat, is decisive. Which landscape can therefore be cold too? |
| geography_08 | en | tip | Deserts get very little precipitation. Some deserts are cold. | Use both clues. The answer is desert. |
| geography_08 | ru | prompt | Где долгое время выпадает очень мало осадков? | Наблюдение. Решает не жара, а очень малое количество осадков. Какая местность поэтому бывает и холодной? |
| geography_08 | ru | tip | В пустынях выпадает очень мало осадков. Бывают и холодные пустыни. | Учти обе подсказки. Ответ: пустыня. |
| geography_09 | de | prompt | Wo wachsen viele Bäume zusammen? | Entdecken. Viele Baumkronen spenden Schatten, darunter liegt oft Laub. Welche Landschaft passt? |
| geography_09 | de | tip | In einem Wald stehen viele Bäume. Dort leben auch viele Tiere. | Überlege beide Hinweise. Gesucht ist: Wald. |
| geography_09 | en | prompt | Where do many trees grow together? | Explore. Many treetops provide shade and leaves often cover the ground. Which landscape fits? |
| geography_09 | en | tip | A forest has many trees and is home to many animals. | Use both clues. The answer is forest. |
| geography_09 | ru | prompt | Где много деревьев растёт вместе? | Открытие. Много крон дают тень, внизу часто опавшие листья. Какая местность подходит? |
| geography_09 | ru | tip | В лесу растёт много деревьев и обитает много животных. | Учти обе подсказки. Ответ: лес. |
| geography_10 | de | prompt | Was kann aus Wolken zum Boden fallen? | Beobachten. Tropfen wachsen in einer Wolke und fallen flüssig. Was kommt am Boden an? |
| geography_10 | de | tip | Aus manchen Wolken fällt Regen. Er bringt Wasser zum Boden. | Überlege beide Hinweise. Gesucht ist: Regen. |
| geography_10 | en | prompt | What can fall from clouds to the ground? | Observe. Drops grow in a cloud and fall as liquid. What reaches the ground? |
| geography_10 | en | tip | Rain falls from some clouds and brings water to the ground. | Use both clues. The answer is rain. |
| geography_10 | ru | prompt | Что может падать из облаков на землю? | Наблюдение. Капли растут в облаке и падают жидкими. Что достигает земли? |
| geography_10 | ru | tip | Из некоторых облаков идёт дождь, принося воду на землю. | Учти обе подсказки. Ответ: дождь. |
| geography_11 | de | prompt | Was fällt als Eiskristalle vom Himmel? | Entdecken. Wasser gefriert in einer Wolke zu Kristallen. Welcher Niederschlag entsteht? |
| geography_11 | de | tip | Schnee besteht aus Eiskristallen, die aus Wolken fallen. | Überlege beide Hinweise. Gesucht ist: Schnee. |
| geography_11 | en | prompt | What falls from the sky as ice crystals? | Explore. Water freezes into crystals in a cloud. Which precipitation forms? |
| geography_11 | en | tip | Snow consists of ice crystals that fall from clouds. | Use both clues. The answer is snow. |
| geography_11 | ru | prompt | Что падает с неба в виде кристалликов льда? | Открытие. В облаке вода замерзает кристалликами. Какие осадки получаются? |
| geography_11 | ru | tip | Снег состоит из кристалликов льда, выпадающих из облаков. | Учти обе подсказки. Ответ: снег. |
| geography_12 | de | prompt | Was versorgt die Erde mit Licht und Wärme? | Leuchten. Der Mond reflektiert, Wolken verdecken. Was liefert der Erde ursprünglich Licht und Wärme? |
| geography_12 | de | tip | Die Sonne liefert der Erde Licht und Wärme. | Überlege beide Hinweise. Gesucht ist: Sonne. |
| geography_12 | en | prompt | What gives Earth light and warmth? | Light. The Moon reflects and clouds block. What originally supplies Earth with light and warmth? |
| geography_12 | en | tip | The sun supplies Earth with light and warmth. | Use both clues. The answer is sun. |
| geography_12 | ru | prompt | Что даёт Земле свет и тепло? | Свет. Луна отражает, облака закрывают. Что изначально даёт Земле свет и тепло? |
| geography_12 | ru | tip | Солнце даёт Земле свет и тепло. | Учти обе подсказки. Ответ: Солнце. |
| geography_13 | de | prompt | Was umkreist die Erde? | Verändern. Ein Himmelskörper gehört zur Erde und umkreist sie. Welcher ist ihr natürlicher Begleiter? |
| geography_13 | de | tip | Der Mond bewegt sich um die Erde. | Überlege beide Hinweise. Gesucht ist: Mond. |
| geography_13 | en | prompt | What orbits Earth? | Change. A celestial body belongs with Earth and orbits it. Which is its natural companion? |
| geography_13 | en | tip | The moon moves around Earth. | Use both clues. The answer is moon. |
| geography_13 | ru | prompt | Что обращается вокруг Земли? | Изменение. Небесное тело связано с Землёй и обращается вокруг неё. Какой это естественный спутник? |
| geography_13 | ru | tip | Луна движется вокруг Земли. | Учти обе подсказки. Ответ: Луна. |
| geography_14 | de | prompt | Was verbindet zwei Ufer für einen Weg? | Entdecken. Die Ufer gehören zum selben Weg, aber Wasser liegt dazwischen. Welches Bauwerk verbindet sie? |
| geography_14 | de | tip | Eine Brücke führt über ein Hindernis wie einen Fluss. | Überlege beide Hinweise. Gesucht ist: Brücke. |
| geography_14 | en | prompt | What connects two banks so a path can cross? | Explore. Both banks belong to one route but water lies between. Which structure joins them? |
| geography_14 | en | tip | A bridge crosses an obstacle such as a river. | Use both clues. The answer is bridge. |
| geography_14 | ru | prompt | Что соединяет берега и позволяет перейти реку? | Открытие. Берега относятся к одному пути, но между ними вода. Какое сооружение их соединит? |
| geography_14 | ru | tip | Мост проходит через препятствие, например через реку. | Учти обе подсказки. Ответ: мост. |
| geography_15 | de | prompt | Wohin fließen viele große Flüsse schließlich? | Entdecken. Mehrere große Flüsse münden in dasselbe salzige Gewässer. Welches passt? |
| geography_15 | de | tip | Viele Flüsse münden ins Meer. Andere enden in Seen oder im Binnenland. | Überlege beide Hinweise. Gesucht ist: Meer. |
| geography_15 | en | prompt | Where do many large rivers eventually flow? | Explore. Several large rivers empty into the same salty body of water. Which fits? |
| geography_15 | en | tip | Many rivers flow into the sea. Others end in lakes or inland. | Use both clues. The answer is sea. |
| geography_15 | ru | prompt | Куда в конце концов впадают многие большие реки? | Открытие. Несколько больших рек впадают в один солёный водоём. Что подходит? |
| geography_15 | ru | tip | Многие реки впадают в море. Другие заканчиваются в озёрах или внутри суши. | Учти обе подсказки. Ответ: море. |
| geography_16 | de | prompt | Was kann als gefrorene weiße Schicht auch im Sommer auf hohen Bergen liegen? | Entdecken. Im Tal ist Sommer, am hohen Gipfel bleibt eine gefrorene weiße Schicht. Was ist es? |
| geography_16 | de | tip | Hoch oben ist es oft kälter. Deshalb kann dort Schnee liegen bleiben. | Überlege beide Hinweise. Gesucht ist: Schnee. |
| geography_16 | en | prompt | What can remain as a frozen white layer on high mountains even in summer? | Explore. It is summer in the valley but a frozen white layer remains high up. What is it? |
| geography_16 | en | tip | High up it is often colder, so snow can remain there. | Use both clues. The answer is snow. |
| geography_16 | ru | prompt | Что может лежать замёрзшим белым слоем на высоких горах даже летом? | Открытие. В долине лето, а высоко на вершине остаётся белый замёрзший слой. Что это? |
| geography_16 | ru | tip | На большой высоте часто холоднее, поэтому снег может не таять. | Учти обе подсказки. Ответ: снег. |
| geography_17 | de | prompt | Was ist auf Karten oft blau eingezeichnet? | Orientieren. Eine Karte benutzt Blau für Flüsse und Seen. Welchen Stoff meint diese Farbe? |
| geography_17 | de | tip | Blau steht auf vielen Karten für Wasser, etwa Flüsse und Meere. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| geography_17 | en | prompt | What is often coloured blue on maps? | Direction. A map uses blue for rivers and lakes. Which substance does this colour represent? |
| geography_17 | en | tip | On many maps, blue stands for water such as rivers and seas. | Use both clues. The answer is water. |
| geography_17 | ru | prompt | Что на картах часто обозначают синим цветом? | Ориентир. На карте реки и озёра синие. Какое вещество обозначает этот цвет? |
| geography_17 | ru | tip | На многих картах синий цвет обозначает воду: реки и моря. | Учти обе подсказки. Ответ: вода. |
| geography_18 | de | prompt | Was bedeutet ein Waldzeichen auf einer Karte? | Orientieren. Eine Kartenlegende zeigt viele Baumzeichen als zusammenhängende Fläche. Was bedeutet sie? |
| geography_18 | de | tip | Ein Waldzeichen zeigt, wo ein Wald liegt. Die Legende erklärt die Zeichen. | Überlege beide Hinweise. Gesucht ist: Wald. |
| geography_18 | en | prompt | What does a forest symbol on a map show? | Direction. A map key shows many tree symbols as one continuous area. What does it mean? |
| geography_18 | en | tip | A forest symbol shows where a forest is. The key explains the symbols. | Use both clues. The answer is forest. |
| geography_18 | ru | prompt | Что показывает знак леса на карте? | Ориентир. В условных знаках карты много деревьев образуют сплошной участок. Что это обозначает? |
| geography_18 | ru | tip | Знак леса показывает его расположение. Условные обозначения объясняются в легенде карты. | Учти обе подсказки. Ответ: лес. |
| geography_19 | de | prompt | Was zeigt ein Brückenzeichen auf einer Karte? | Orientieren. Ein Kartenzeichen verbindet einen Weg über einen Fluss. Welches Bauwerk ist gemeint? |
| geography_19 | de | tip | Das Zeichen zeigt einen Übergang über einen Fluss oder ein anderes Hindernis. | Überlege beide Hinweise. Gesucht ist: Brücke. |
| geography_19 | en | prompt | What does a bridge symbol on a map show? | Direction. A map symbol joins a route across a river. Which structure is meant? |
| geography_19 | en | tip | It shows a crossing over a river or another obstacle. | Use both clues. The answer is bridge. |
| geography_19 | ru | prompt | Что показывает знак моста на карте? | Ориентир. Знак карты соединяет путь через реку. Какое сооружение обозначено? |
| geography_19 | ru | tip | Он показывает переход через реку или другое препятствие. | Учти обе подсказки. Ответ: мост. |
| geography_20 | de | prompt | Was bedeckt den größten Teil der Erdoberfläche? | Entdecken. Vom Weltraum erscheint die Erde überwiegend blau. Welches große Gewässer bedeckt besonders viel Fläche? |
| geography_20 | de | tip | Die Meere bedecken mehr als die Hälfte der Erdoberfläche. | Überlege beide Hinweise. Gesucht ist: Meer. |
| geography_20 | en | prompt | What covers most of Earth’s surface? | Explore. From space Earth looks mostly blue. Which large body of water covers especially much area? |
| geography_20 | en | tip | Seas cover more than half of Earth's surface. | Use both clues. The answer is sea. |
| geography_20 | ru | prompt | Что покрывает большую часть поверхности Земли? | Открытие. Из космоса Земля в основном синяя. Какой большой водоём занимает особенно много места? |
| geography_20 | ru | tip | Моря покрывают больше половины поверхности Земли. | Учти обе подсказки. Ответ: море. |
| geography_21 | de | prompt | Wo entstehen Regentropfen am Himmel? | Beobachten. Wasser steigt als Dampf auf und kühlt ab. Wo wachsen daraus Regentropfen? |
| geography_21 | de | tip | Winzige Tropfen in Wolken können zusammenwachsen und als Regen fallen. | Überlege beide Hinweise. Gesucht ist: Wolke. |
| geography_21 | en | prompt | Where do raindrops form in the sky? | Observe. Water rises as vapour and cools. Where do raindrops grow from it? |
| geography_21 | en | tip | Tiny drops in clouds can join together and fall as rain. | Use both clues. The answer is cloud. |
| geography_21 | ru | prompt | Где в небе образуются дождевые капли? | Наблюдение. Вода поднимается паром и охлаждается. Где из неё растут дождевые капли? |
| geography_21 | ru | tip | Мелкие капли в облаках могут соединяться и выпадать дождём. | Учти обе подсказки. Ответ: облако. |
| geography_22 | de | prompt | Was erwärmt das Wasser im Wasserkreislauf vor allem? | Verändern. Ein nasser Stein trocknet draußen schneller im Licht. Was liefert dem Wasserkreislauf Wärmeenergie? |
| geography_22 | de | tip | Sonnenwärme hilft, Wasser verdunsten zu lassen. | Überlege beide Hinweise. Gesucht ist: Sonne. |
| geography_22 | en | prompt | What mainly warms water in Earth’s water cycle? | Change. A wet stone dries faster outside in light. What provides heat energy for the water cycle? |
| geography_22 | en | tip | Warmth from the sun helps water evaporate. | Use both clues. The answer is sun. |
| geography_22 | ru | prompt | Что в основном нагревает воду в круговороте воды на Земле? | Изменение. Мокрый камень на свету сохнет быстрее. Что даёт круговороту воды тепловую энергию? |
| geography_22 | ru | tip | Солнечное тепло помогает воде испаряться. | Учти обе подсказки. Ответ: Солнце. |
| geography_23 | de | prompt | Wie gelangt Wasser aus Wolken zurück zum Boden? | Beobachten. Eine Wolke verliert flüssige Tropfen, der Boden wird nass. Welcher Weg bringt das Wasser zurück? |
| geography_23 | de | tip | Niederschlag wie Regen bringt Wasser zurück zum Boden. | Überlege beide Hinweise. Gesucht ist: Regen. |
| geography_23 | en | prompt | How can water return from clouds to the ground? | Observe. A cloud loses liquid drops and the ground gets wet. What brings the water back? |
| geography_23 | en | tip | Precipitation such as rain returns water to the ground. | Use both clues. The answer is rain. |
| geography_23 | ru | prompt | Как вода из облаков возвращается на землю? | Наблюдение. Облако теряет жидкие капли, земля намокает. Что возвращает воду вниз? |
| geography_23 | ru | tip | Осадки, например дождь, возвращают воду на землю. | Учти обе подсказки. Ответ: дождь. |
| geography_24 | de | prompt | Wo kann ein Fluss hoch oben entspringen? | Entdecken. Eine Quelle liegt hoch, von dort fließt Wasser ins Tal. Welche Landschaft kann sie umgeben? |
| geography_24 | de | tip | Viele Flüsse entspringen in Bergen, aber nicht alle. | Überlege beide Hinweise. Gesucht ist: Berg. |
| geography_24 | en | prompt | Where can a river begin high above the plains? | Explore. A spring is high up and water flows to a valley. Which landscape may surround it? |
| geography_24 | en | tip | Many rivers begin in mountains, but not all do. | Use both clues. The answer is mountain. |
| geography_24 | ru | prompt | Где высоко над равниной может начинаться река? | Открытие. Источник высоко, от него вода течёт в долину. Какая местность может быть вокруг? |
| geography_24 | ru | tip | Многие реки начинаются в горах, но не все. | Учти обе подсказки. Ответ: гора. |
| geography_25 | de | prompt | Was liegt an vielen Stränden als kleine Körner? | Entdecken. Wellen zerkleinern Gestein. Was liegt als viele kleine Körner an vielen Stränden? |
| geography_25 | de | tip | An vielen Stränden liegt Sand. Es gibt auch Kies- und Felsstrände. | Überlege beide Hinweise. Gesucht ist: Sand. |
| geography_25 | en | prompt | What lies in little grains on many beaches? | Explore. Waves break down rock. What lies as many small grains on many beaches? |
| geography_25 | en | tip | Many beaches have sand. Others have pebbles or rocks. | Use both clues. The answer is sand. |
| geography_25 | ru | prompt | Что лежит мелкими крупинками на многих пляжах? | Открытие. Волны измельчают горные породы. Что лежит множеством мелких крупинок на многих пляжах? |
| geography_25 | ru | tip | На многих пляжах есть песок. Бывают также галечные и скалистые берега. | Учти обе подсказки. Ответ: песок. |
| geography_26 | de | prompt | Was ist in trockenen Wüsten besonders knapp? | Entdecken. Es regnet lange kaum. Was wird für Menschen, Tiere und Pflanzen in der Wüste knapp? |
| geography_26 | de | tip | Wasser ist in trockenen Wüsten knapp. Lebewesen sind daran angepasst. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| geography_26 | en | prompt | What is especially scarce in dry deserts? | Explore. There is little rain for a long time. What becomes scarce for people, animals and plants in a desert? |
| geography_26 | en | tip | Water is scarce in dry deserts. Living things there are adapted to this. | Use both clues. The answer is water. |
| geography_26 | ru | prompt | Чего особенно мало в сухих пустынях? | Открытие. Долго почти нет дождя. Чего в пустыне не хватает людям, животным и растениям? |
| geography_26 | ru | tip | В сухих пустынях мало воды. Обитатели приспособлены к таким условиям. | Учти обе подсказки. Ответ: вода. |
| geography_27 | de | prompt | Was siehst du rings um eine Meeresinsel? | Entdecken. Du stehst auf einer Meeresinsel. Welches Gewässer umgibt sie auf jeder Seite? |
| geography_27 | de | tip | Um eine Meeresinsel liegt auf allen Seiten Meerwasser. | Überlege beide Hinweise. Gesucht ist: Meer. |
| geography_27 | en | prompt | What surrounds an island in the sea? | Explore. You stand on a sea island. Which body of water surrounds every side? |
| geography_27 | en | tip | A sea island has seawater on every side. | Use both clues. The answer is sea. |
| geography_27 | ru | prompt | Что окружает морской остров? | Открытие. Ты стоишь на морском острове. Какой водоём окружает его со всех сторон? |
| geography_27 | ru | tip | Морской остров со всех сторон окружён морской водой. | Учти обе подсказки. Ответ: море. |
| geography_28 | de | prompt | Was gehört zu einem Wald? | Wachsen. Ein Wald enthält Pflanzen mit Stämmen und Kronen. Was davon gehört dorthin? |
| geography_28 | de | tip | Bäume sind ein wichtiger Teil eines Waldes. | Überlege beide Hinweise. Gesucht ist: Baum. |
| geography_28 | en | prompt | What belongs in a forest? | Grow. A forest contains plants with trunks and crowns. Which pictured thing belongs there? |
| geography_28 | en | tip | Trees are an important part of a forest. | Use both clues. The answer is tree. |
| geography_28 | ru | prompt | Что относится к лесу? | Расти. В лесу есть растения со стволами и кронами. Что из показанного там бывает? |
| geography_28 | ru | tip | Деревья — важная часть леса. | Учти обе подсказки. Ответ: дерево. |
| geography_29 | de | prompt | Was lässt sich zusammenfalten und zeigt deinen Spazierweg? | Entdecken. Du willst einen Spazierweg zeichnen und das Blatt einstecken. Welche Orientierungshilfe passt? |
| geography_29 | de | tip | Eine Papierkarte lässt sich zusammenfalten und unterwegs benutzen. | Überlege beide Hinweise. Gesucht ist: Karte. |
| geography_29 | en | prompt | What can be folded up and show your walking route? | Explore. You want to draw a walking route and pocket the sheet. Which navigation aid fits? |
| geography_29 | en | tip | A paper map folds up and can be used on a walk. | Use both clues. The answer is map. |
| geography_29 | ru | prompt | Что можно сложить и использовать для выбора маршрута прогулки? | Открытие. Нужно нарисовать прогулочный путь и убрать лист в карман. Что поможет ориентироваться? |
| geography_29 | ru | tip | Бумажную карту можно сложить и взять на прогулку. | Учти обе подсказки. Ответ: карта. |
| geography_30 | de | prompt | Welches Modell zeigt auch die Rückseite der Erde beim Drehen? | Orientieren. Auf einem Modell sind die Erdteile rundherum verteilt. Welches Modell lässt sich dafür drehen? |
| geography_30 | de | tip | Drehst du einen Globus, siehst du andere Teile der Erde. | Überlege beide Hinweise. Gesucht ist: Globus. |
| geography_30 | en | prompt | Which model shows Earth's other side when you turn it? | Direction. Continents are spread all around a model. Which model can be turned to see them? |
| geography_30 | en | tip | Turning a globe lets you see other parts of Earth. | Use both clues. The answer is globe. |
| geography_30 | ru | prompt | Какая модель показывает другую сторону Земли при повороте? | Ориентир. Материки распределены вокруг модели. Какую модель можно поворачивать, чтобы их увидеть? |
| geography_30 | ru | tip | Поворачивая глобус, можно увидеть другие части Земли. | Учти обе подсказки. Ответ: глобус. |
| geography_31 | de | prompt | Was kann die Sonne am Himmel verdecken? | Beobachten. Ein Schatten wandert über die Landschaft, obwohl die Sonne weiter scheint. Was kann sie verdecken? |
| geography_31 | de | tip | Wolken können Sonnenlicht teilweise oder ganz verdecken. | Überlege beide Hinweise. Gesucht ist: Wolke. |
| geography_31 | en | prompt | What can hide the sun in the sky? | Observe. A shadow moves over the landscape while the Sun still shines. What can block it? |
| geography_31 | en | tip | Clouds can partly or completely block sunlight. | Use both clues. The answer is cloud. |
| geography_31 | ru | prompt | Что может закрыть Солнце в небе? | Наблюдение. Тень движется по местности, хотя солнце продолжает светить. Что может его закрывать? |
| geography_31 | ru | tip | Облака могут частично или полностью закрывать солнечный свет. | Учти обе подсказки. Ответ: облако. |
| geography_32 | de | prompt | Was kann im Frühling Schnee schmelzen lassen? | Beobachten. Schnee schmilzt im Frühling auch ohne Regen. Welcher Himmelskörper liefert dafür Wärme? |
| geography_32 | de | tip | Wenn die Sonne den Boden erwärmt, kann Schnee schmelzen. | Überlege beide Hinweise. Gesucht ist: Sonne. |
| geography_32 | en | prompt | What can help melt snow in spring? | Observe. Snow melts in spring even without rain. Which celestial body supplies warmth? |
| geography_32 | en | tip | Snow can melt when the sun warms the ground. | Use both clues. The answer is sun. |
| geography_32 | ru | prompt | Что помогает снегу таять весной? | Наблюдение. Весной снег тает даже без дождя. Какое небесное тело даёт для этого тепло? |
| geography_32 | ru | tip | Когда солнце согревает землю, снег может таять. | Учти обе подсказки. Ответ: Солнце. |
| geography_33 | de | prompt | Was ist lang, fließt und hat zwei Ufer? | Entdecken. Ein langer Wasserlauf besitzt eine Quelle und zwei Ufer. Welcher passt? |
| geography_33 | de | tip | Ein Fluss fließt zwischen seinen beiden Ufern. | Überlege beide Hinweise. Gesucht ist: Fluss. |
| geography_33 | en | prompt | What is long, flows and has two banks? | Explore. A long watercourse has a source and two banks. Which fits? |
| geography_33 | en | tip | A river flows between its two banks. | Use both clues. The answer is river. |
| geography_33 | ru | prompt | Что длинное, течёт и имеет два берега? | Открытие. У длинного водного потока есть исток и два берега. Что подходит? |
| geography_33 | ru | tip | Река течёт между двумя берегами. | Учти обе подсказки. Ответ: река. |
| geography_34 | de | prompt | Welche Landschaft erkennst du an einem hohen Gipfel? | Entdecken. Höhenlinien liegen eng, ein Gipfel ist markiert. Welche Landschaftsform erwartet dich? |
| geography_34 | de | tip | Ein Berg hat einen Gipfel. Nicht jeder Gipfel ist spitz. | Überlege beide Hinweise. Gesucht ist: Berg. |
| geography_34 | en | prompt | Which landscape has a high peak? | Explore. Contour lines are close together and a summit is marked. Which landform should you expect? |
| geography_34 | en | tip | A mountain has a summit. Not every summit is pointed. | Use both clues. The answer is mountain. |
| geography_34 | ru | prompt | У какого элемента рельефа высокая вершина? | Открытие. Линии высот близко друг к другу, отмечена вершина. Какую форму рельефа ждать? |
| geography_34 | ru | tip | У горы есть вершина. Не каждая вершина острая. | Учти обе подсказки. Ответ: гора. |
| geography_35 | de | prompt | Welches große Gewässer ist normalerweise salzig? | Entdecken. Ein Gewässer ist viel größer als ein Fluss und normalerweise salzig. Welches passt? |
| geography_35 | de | tip | Meerwasser enthält gelöste Salze. Trinke kein Meerwasser. | Überlege beide Hinweise. Gesucht ist: Meer. |
| geography_35 | en | prompt | Which large body of water is normally salty? | Explore. A body of water is much larger than a river and normally salty. Which fits? |
| geography_35 | en | tip | Seawater contains dissolved salts. Do not drink it. | Use both clues. The answer is sea. |
| geography_35 | ru | prompt | Какой большой водоём обычно солёный? | Открытие. Водоём намного больше реки и обычно солёный. Что подходит? |
| geography_35 | ru | tip | В морской воде растворены соли. Морскую воду пить нельзя. | Учти обе подсказки. Ответ: море. |
| geography_36 | de | prompt | Welches Gerät zeigt mit einer Magnetnadel die Nordrichtung für deine Karte? | Orientieren. Der Weg auf der Karte ist klar, nur ihre Nordrichtung nicht. Welches Gerät hilft mit einer Magnetnadel? |
| geography_36 | de | tip | Mit einem Kompass kannst du die Nordrichtung der Karte passend ausrichten. | Überlege beide Hinweise. Gesucht ist: Kompass. |
| geography_36 | en | prompt | Which instrument uses a magnetic needle to show north for your map? | Direction. The map route is clear but its north direction is not. Which instrument helps using a magnetic needle? |
| geography_36 | en | tip | A compass helps you align the map's north direction. | Use both clues. The answer is compass. |
| geography_36 | ru | prompt | Какой прибор магнитной стрелкой показывает север для твоей карты? | Ориентир. Путь на карте понятен, но север неизвестен. Какой прибор поможет магнитной стрелкой? |
| geography_36 | ru | tip | Компас помогает повернуть карту так, чтобы её север совпал с направлением на север. | Учти обе подсказки. Ответ: компас. |
| geography_37 | de | prompt | Welcher Niederschlag ist flüssig? | Entdecken. Die Luft ist warm genug, dass Wolkentropfen nicht gefrieren. Welcher flüssige Niederschlag fällt? |
| geography_37 | de | tip | Regen fällt in flüssigen Wassertropfen, Schnee in festen Eiskristallen. | Überlege beide Hinweise. Gesucht ist: Regen. |
| geography_37 | en | prompt | Which kind of precipitation is liquid? | Explore. The air is warm enough that cloud drops do not freeze. Which liquid precipitation falls? |
| geography_37 | en | tip | Rain falls as liquid drops. Snow falls as solid ice crystals. | Use both clues. The answer is rain. |
| geography_37 | ru | prompt | Какие осадки жидкие? | Открытие. Воздух достаточно тёплый, капли облака не замерзают. Какие жидкие осадки выпадают? |
| geography_37 | ru | tip | Дождь выпадает жидкими каплями, а снег — твёрдыми кристалликами льда. | Учти обе подсказки. Ответ: дождь. |
| geography_38 | de | prompt | Was ist ein Stern: Sonne, Wolke oder Mond? | Beobachten. Ein Stern erzeugt eigenes Licht. Welcher dieser Himmelskörper ist deshalb ein Stern? |
| geography_38 | de | tip | Die Sonne ist ein Stern. Sie leuchtet selbst. | Überlege beide Hinweise. Gesucht ist: Sonne. |
| geography_38 | en | prompt | Which is a star: the sun, a cloud or the moon? | Observe. A star makes its own light. Which pictured celestial body is therefore a star? |
| geography_38 | en | tip | The sun is a star and gives off its own light. | Use both clues. The answer is sun. |
| geography_38 | ru | prompt | Что является звездой: Солнце, облако или Луна? | Наблюдение. Звезда сама излучает свет. Какое показанное небесное тело поэтому является звездой? |
| geography_38 | ru | tip | Солнце — звезда. Оно излучает собственный свет. | Учти обе подсказки. Ответ: Солнце. |
| geography_39 | de | prompt | Welcher Himmelskörper liefert das meiste Licht, das der Mond zurückwirft? | Leuchten. Der Mond erzeugt kein eigenes sichtbares Licht. Wessen Licht sehen wir von ihm zurückgeworfen? |
| geography_39 | de | tip | Der Mond leuchtet nicht selbst. Er reflektiert Sonnenlicht. | Überlege beide Hinweise. Gesucht ist: Sonne. |
| geography_39 | en | prompt | Which celestial body supplies most of the light reflected by the Moon? | Light. The Moon makes no visible light of its own. Whose light do we see reflected from it? |
| geography_39 | en | tip | The moon does not make its own light. It reflects sunlight. | Use both clues. The answer is sun. |
| geography_39 | ru | prompt | Какое небесное тело даёт большую часть света, отражаемого Луной? | Свет. Луна сама не излучает видимый свет. Чей отражённый свет мы от неё видим? |
| geography_39 | ru | tip | Луна не светится сама. Она отражает солнечный свет. | Учти обе подсказки. Ответ: Солнце. |
| geography_40 | de | prompt | Was bringen Regen und Flüsse vielen Pflanzen? | Wachsen. Pflanzen verdunsten Feuchtigkeit über Blätter. Was liefern Regen und Flüsse als Nachschub? |
| geography_40 | de | tip | Regen und Flüsse können Pflanzen mit Wasser versorgen. | Überlege beide Hinweise. Gesucht ist: Wasser. |
| geography_40 | en | prompt | What do rain and rivers bring to many plants? | Growing. Plants lose moisture through leaves. What do rain and rivers supply to replace it? |
| geography_40 | en | tip | Rain and rivers can supply plants with water. | Use both clues. The answer is water. |
| geography_40 | ru | prompt | Что дождь и реки приносят многим растениям? | Рост. Растения теряют влагу через листья. Что дождь и реки приносят взамен? |
| geography_40 | ru | tip | Дождь и реки могут снабжать растения водой. | Учти обе подсказки. Ответ: вода. |
