#!/usr/bin/env python3
"""Compile authored multilingual exercises; preserve all 24 foundation tasks."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path(__file__).parent
LOCALES=('de','en','ru')
languages=json.loads((SOURCE/'languages-source.json').read_text())
objects=languages['objects']
tasks=json.loads((SOURCE/'foundation-tasks.json').read_text())['tasks']

def local(task,questions,hints):
    task['texts']={lang:{'prompt':q,'tip':h} for lang,q,h in zip(LOCALES,questions,hints)}
    task['prompt']=questions[0];task['tip']=hints[0]
    return task

def add(subject,kind,question,hint,**values):
    index=sum(t['subject']==subject for t in tasks)+1
    data={'id':f'{subject}_{index:02d}','subject':subject,'kind':kind,**values}
    local(data,question,hint)
    tasks.append(data)

def names(ids,lang):return ', '.join(objects[i][lang] for i in ids)
def opt(answer,index=0):
    # Distinct nearby numeric distractors, all inside the 0..20 number range.
    wrong=[n for n in [answer-1,answer+1,answer+2,answer-2] if 0<=n<=20 and n!=answer][:2]
    values=[answer,*wrong];shift=index%3;return values[shift:]+values[:shift]

logic_old={
'logic_repeat':('Apple, leaf. What comes next?','Яблоко, лист. Что дальше?','Apple and leaf alternate. The next picture is a leaf.','Яблоко и лист чередуются. Дальше будет лист.'),
'logic_triple':('How does this pattern continue?','Как продолжается узор?','Two stars, then a moon. The next picture is a moon.','Две звезды, затем Луна. Дальше будет Луна.'),
'logic_odd':('Which does not grow like these plants?','Что не растёт, как эти растения?','Apples, leaves and flowers grow. A ball does not grow.','Яблоки, листья и цветы растут. Мяч не растёт.'),
'logic_shadow':('What matches the shadow?','Что подходит к тени?','Compare the outlines. The shadow shows a tree.','Сравни контуры. Это тень дерева.'),
'logic_size':('Which tree is the tallest?','Какое дерево самое высокое?','Choose the tallest tree.','Выбери самое высокое дерево.'),
'logic_double':('What comes in the gap?','Что поставить в пропуск?','One sun, then two moons. The pattern repeats.','Одно Солнце, затем две Луны. Узор повторяется.'),
'logic_shape':('What matches the shadow?','Что подходит к тени?','Look for the square head and two arms of the robot.','Найди квадратную голову и две руки робота.'),
'logic_rule':('Which does not belong with the objects in the sky?','Что лишнее среди небесных тел?','The sun, moon and stars are in the sky. A flower grows on the ground.','Солнце, Луна и звёзды находятся в небе. Цветок растёт на земле.')}

# Explicit plurals avoid dropping the pictured object in translations.
PLURALS={
 'apple':('Äpfel','apples','яблок'), 'star':('Sterne','stars','звёзд'),
 'bee':('Bienen','bees','пчёл'), 'fish':('Fische','fish','рыб'),
 'leaf':('Blätter','leaves','листьев'), 'flower':('Blumen','flowers','цветов')}
def math_text(t):
    k=t['kind'];o=t.get('object','star');de,en,ru=PLURALS[o]
    if k=='count':
        return ([f'Wie viele {de} siehst du?',f'How many {en} can you see?',f'Сколько {ru} ты видишь?'],['Tippe jedes Bild einmal an und zähle mit.','Tap each picture once and count.','Коснись каждой картинки один раз и посчитай.'])
    if k=='add':
        a,b=t['left'],t['right'];return ([f'{a} und {b}. Wie viele zusammen?',f'{a} and {b}. How many altogether?',f'{a} и {b}. Сколько всего?'],['Zähle zuerst links und dann rechts weiter.','Count the left group, then keep counting the right group.','Сначала посчитай слева, затем продолжи считать справа.'])
    if k=='subtract':
        a,b=t['left'],t['right'];return ([f'{a} sind da. {b} gehen weg. Wie viele bleiben?',f'There are {a}. Take away {b}. How many remain?',f'Было {a}. Убрали {b}. Сколько осталось?'],['Zähle die Bilder ohne Kreuz.','Count only the pictures without a cross.','Считай только картинки без крестика.'])
    if k=='complete':
        a,b=t['left'],t['right'];return ([f'{a} sind da. Wie viele fehlen bis {b}?',f'There are {a}. How many more make {b}?',f'Есть {a}. Сколько не хватает до {b}?'],['Zähle die leeren Sternplätze.','Count the empty star spaces.','Посчитай пустые места для звёзд.'])
    if k=='compare':return (['Wo sind mehr?','Which group has more?','Где больше?'],['Zähle beide Mengen. Tippe die größere an.','Count both groups and tap the larger one.','Посчитай обе группы. Коснись той, где больше.'])
    if k=='sequence':
        delta=t['sequence'][1]-t['sequence'][0];return (['Welche Zahl kommt als Nächstes?','Which number comes next?','Какое число следующее?'],[f'Es kommen jedes Mal {delta} dazu.',f'Add {delta} each time.',f'Каждый раз прибавляй {delta}.'])
    raise ValueError(k)

def german_text(t):
    word=t['word'];k=t['kind'];target=word.capitalize()
    if k=='initial':return ([f'{target}. Mit welchem Buchstaben schreibt man das deutsche Wort am Anfang?',f'German word: {target}. Which letter does it start with?',f'Немецкое слово: {target}. С какой буквы его пишут?'],[f'{target} beginnt mit {t["answer"]}. Suche diesen Buchstaben.',f'{target} starts with the letter {t["answer"]}. Choose that letter.',f'{target} начинается с буквы {t["answer"]}. Выбери эту букву.'])
    if k=='syllables':
        parts='. '.join(x.capitalize() for x in t['syllables']);count=t['answer'];ru_count='слог' if count==1 else ('слога' if count in [2,3,4] else 'слогов')
        return ([f'{target}. Wie viele Silben hörst du?',f'German word: {target}. How many syllables can you hear?',f'Немецкое слово: {target}. Сколько слогов ты слышишь?'],[f'Sprich und klatsche: {parts}. Das sind {count} Silben.',f'Say and clap: {parts}. That is {count} '+('syllable.' if count==1 else 'syllables.'),f'Произнеси и хлопай: {parts}. Это {count} {ru_count}.'])
    if k=='word':
        letters='. '.join(word)+'.'
        return (['Welches deutsche Wort passt zum Bild?','Which German word matches the picture?','Какое немецкое слово подходит к картинке?'],[f'Suche die Buchstaben von {target}: {letters}',f'Find the letters of {target}: {letters}',f'Найди буквы слова {target}: {letters}'])
    if k=='rhyme':return (['Was reimt sich auf Haus?','Which German word rhymes with Haus?','Какое немецкое слово рифмуется со словом Haus?'],['Haus und Maus klingen am Ende gleich.','Haus and Maus sound the same at the end.','Haus и Maus звучат одинаково в конце.'])
    raise ValueError(k)

# Preserve the original German wording while retaining every named object,
# number, spelling and action in its localized instruction.
FOUNDATION_TRANSLATIONS={
 'math_count':('How many apples can you see?','Сколько яблок ты видишь?','Tap each apple once. Count as you go.','Коснись каждого яблока один раз. Считай при этом.'),
 'math_add':('Three apples and two apples. How many altogether?','Три яблока и два яблока. Сколько всего?','Count the left group first. Then keep counting on the right.','Сначала посчитай слева. Затем продолжи считать справа.'),
 'math_take':('Seven leaves. Three fly away. How many remain?','Семь листьев. Три улетают. Сколько осталось?','Count only the leaves without a cross.','Считай только листья без крестика.'),
 'math_ten':('Four stars are already there. How many more make ten?','Уже есть четыре звезды. Сколько не хватает до десяти?','Count the empty star spaces.','Посчитай пустые места для звёзд.'),
 'math_compare':('Where are there more apples?','Где больше яблок?','Compare both groups. Tap the larger group.','Сравни обе группы. Коснись той, где больше.'),
 'math_steps':('Two, four, six. Which number comes next?','Два, четыре, шесть. Какое число следующее?','Add two each time.','Каждый раз прибавляй два.'),
 'math_twenty':('Ten and four. How many altogether?','Десять и четыре. Сколько всего?','The first group has ten. Count on four more.','В первой группе десять. Отсчитай ещё четыре.'),
 'math_split':('Five stars are already there. How many more make eight?','Уже есть пять звёзд. Сколько не хватает до восьми?','Count the empty star spaces.','Посчитай пустые места для звёзд.'),
 'german_read':('Which German word belongs to the ball?','Какое немецкое слово подходит к мячу?','B. A. L. L. Find the word Ball.','B. A. L. L. Найди слово Ball.')}

# Translations change instructions only. German subject keeps German words and answers.
for t in tasks:
    de=(t['prompt'],t['tip'])
    if t['subject']=='math':q,h=math_text(t)
    elif t['subject']=='german':q,h=german_text(t)
    else:
        en,ru,eh,rh=logic_old[t['id']];q=[de[0],en,ru];h=[de[1],eh,rh]
    if t['id'] in FOUNDATION_TRANSLATIONS:
        en,ru,eh,rh=FOUNDATION_TRANSLATIONS[t['id']];q[1:]=[en,ru];h[1:]=[eh,rh]
    q[0],h[0]=de
    local(t,q,h)

# 32 additional concrete maths exercises, deliberately bounded to 0..20.
math_specs=[('count',dict(count=n,object=o,answer=n)) for n,o in [(3,'bee'),(4,'fish'),(5,'flower'),(8,'leaf'),(9,'star'),(10,'apple')]]
math_specs += [('add',dict(left=a,right=b,object=o,answer=a+b)) for a,b,o in [(2,2,'apple'),(4,3,'leaf'),(5,4,'star'),(6,2,'flower'),(8,3,'fish'),(10,5,'apple'),(9,6,'star'),(12,7,'leaf')]]
math_specs += [('subtract',dict(left=a,right=b,object=o,answer=a-b)) for a,b,o in [(5,2,'apple'),(8,4,'leaf'),(9,2,'star'),(10,1,'flower'),(12,3,'fish'),(14,4,'apple'),(16,6,'star'),(20,5,'leaf')]]
math_specs += [('complete',dict(left=a,right=b,object='star',answer=b-a)) for a,b in [(2,5),(6,10),(7,10),(8,12),(10,15),(14,20)]]
math_specs += [('compare',dict(left=a,right=b,object=o,answer='left' if a>b else 'right')) for a,b,o in [(4,2,'apple'),(3,6,'star'),(9,7,'leaf'),(6,8,'flower')]]
assert len(math_specs)==32
for i,(kind,v) in enumerate(math_specs):
    v['options']=['left','right'] if kind=='compare' else opt(v['answer'],i)
    q,h=math_text({'kind':kind,**v});add('math',kind,q,h,**v)

words=[]
for line in (SOURCE/'german-words.tsv').read_text().splitlines():
    if line and not line.startswith('#'):
        o,w,parts=line.split('|');words.append((o,w,parts.split()))
for i,(o,w,parts) in enumerate(words):
    kind='initial' if i<12 else ('syllables' if i<24 else 'word')
    if kind=='initial':
        answer=w[0];options=[answer,*[x for x in 'MSLFBAHNKZ' if x!=answer][:2]]
    elif kind=='syllables':answer=len(parts);options=opt(answer,i)
    else:
        answer=w;options=[w,words[(i+1)%len(words)][1],words[(i+3)%len(words)][1]]
    shift=i%3;options=options[shift:]+options[:shift]
    t=dict(kind=kind,word=w,syllables=parts,options=options,answer=answer,object=o)
    q,h=german_text(t);t.pop('kind');add('german',kind,q,h,**t)

patterns=[['apple','star'],['sun','leaf','leaf'],['fish','flower'],['moon','star','star'],['bee','leaf','flower'],['ball','ball','robot'],['tree','sun'],['egg','bird','bird']]
for i,p in enumerate(patterns):
    length=4+i%3;seq=[p[j%len(p)] for j in range(length)];answer=p[length%len(p)]
    options=list(dict.fromkeys([answer,*p,*['apple','moon','ball']]))[:3];shift=i%3;options=options[shift:]+options[:shift]
    hint_de='Das Muster wiederholt sich: '+names(p,'de')+'. Danach kommt '+objects[answer]['de']+'.'
    q=['Was kommt als Nächstes?','What comes next?','Что дальше?'];h=[hint_de,'The pattern repeats: '+names(p,'en')+'. Next comes '+objects[answer]['en']+'.','Узор повторяется: '+names(p,'ru')+'. Дальше: '+objects[answer]['ru']+'.']
    add('logic','pattern',q,h,sequence=seq,options=options,answer=answer)
for i,o in enumerate(['bird','cat','butterfly','hammer','helmet','frog','hand','wheel']):
    options=[o,*[x for x in ['flower','robot','tree'] if x!=o][:2]];shift=i%3;options=options[shift:]+options[:shift]
    add('logic','shadow',['Was passt zum Schatten?','What matches the shadow?','Что подходит к тени?'],['Vergleiche die Umrisse. Gesucht ist: '+objects[o]['de']+'.','Compare the outlines. Find the '+objects[o]['en']+'.','Сравни контуры. Найди: '+objects[o]['ru']+'.'],object=o,options=options,answer=o)
categories=[(['leaf','tree','flower'],'ball'),(['cat','bird','frog'],'glass'),(['eye','ear','nose'],'hammer'),(['hammer','scissors','screwdriver'],'fish'),(['sun','cloud','rain'],'tooth'),(['water','ice','steam'],'wood'),(['bird','bee','butterfly'],'bone'),(['glass','wood','metal'],'cat')]
for i,(seq,answer) in enumerate(categories):
    options=[seq[0],answer,seq[1]];shift=i%3;options=options[shift:]+options[:shift]
    reasons=[('Pflanzen und Pflanzenteile','plants and plant parts','растения и части растений'),('Tiere','animals','животные'),('Sinnesorgane','sense organs','органы чувств'),('Werkzeuge','tools','инструменты'),('Dinge am Himmel','things in the sky','явления в небе'),('Zustände von Wasser','forms of water','состояния воды'),('Tiere mit Flügeln','animals with wings','животные с крыльями'),('Werkstoffe','materials','материалы')][i]
    add('logic','odd',['Welches Bild passt nicht zur gezeigten Gruppe?','Which picture does not belong with this group?','Какая картинка не подходит к этой группе?'],['Die Gruppe zeigt '+reasons[0]+'. '+objects[answer]['de']+' passt nicht dazu.','The group shows '+reasons[1]+'. '+objects[answer]['en']+' does not belong.','В группе: '+reasons[2]+'. '+objects[answer]['ru']+' сюда не относится.'],sequence=seq,options=options,answer=answer)
for i,(start,step) in enumerate([(1,1),(2,1),(3,1),(5,1),(1,2),(3,2),(0,5),(2,5)]):
    seq=[start+step*j for j in range(3)];answer=start+step*3
    add('logic','sequence',['Welche Zahl kommt als Nächstes?','Which number comes next?','Какое число следующее?'],[f'Es kommen jedes Mal {step} dazu.',f'Add {step} each time.',f'Каждый раз прибавляй {step}.'],sequence=seq,options=opt(answer,i),answer=answer)

for subject in ['physics','biology','chemistry','body','geography']:
    lines=[s for s in (SOURCE/(subject+'.tsv')).read_text().splitlines() if s and not s.startswith('#')]
    assert len(lines)==40,(subject,len(lines))
    for i,line in enumerate(lines):
        fields=line.split('|');assert len(fields)==7,(subject,i)
        cue,answer,*wrong=fields[0].split();assert len(wrong)==2
        for image in [cue,answer,*wrong]:assert image in objects,(subject,i,image)
        options=[answer,*wrong];assert len(set(options))==3
        shift=i%3;options=options[shift:]+options[:shift]
        add(subject,'discovery',fields[1:4],fields[4:7],object=cue,options=options,answer=answer)

assert len(tasks)==320 and len({t['id'] for t in tasks})==320
for subject in ['math','german','logic','physics','biology','chemistry','body','geography']:
    assert sum(t['subject']==subject for t in tasks)==40
for t in tasks:
    assert t['answer'] in t['options'] and len(set(t['options']))==len(t['options'])
    assert set(t['texts'])==set(LOCALES)
    for lang in LOCALES:assert t['texts'][lang]['prompt'] and t['texts'][lang]['tip']
(ROOT/'games/quest/tasks.json').write_text(json.dumps({'schema':2,'authorship':'Original Kinderwelt tasks; multilingual authored subject bank, no copied commercial exercises.','tasks':tasks},ensure_ascii=False,indent=2)+'\n')
(ROOT/'games/quest/languages.json').write_text(json.dumps(languages,ensure_ascii=False,indent=2)+'\n')
print('320 exercises: 40 each in eight subjects; German, English and Russian instructions.')
