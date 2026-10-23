"""Compile native literacy, indirect visual clues and optional reasoning challenges.

Stable parent IDs preserve existing progress. Bonus records are nested so world
routes stay at forty stations per subject; rewards are independently identified.
"""
from copy import deepcopy
from pathlib import Path
import json

LOCALES=('de','en','ru')
SOURCE=Path(__file__).parent
NATIVE={
 'sun':('SUN','SUN','СОЛНЦЕ','СОЛН ЦЕ'),
 'mouse':('MOUSE','MOUSE','МЫШЬ','МЫШЬ'),
 'apple':('APPLE','AP PLE','ЯБЛОКО','Я БЛО КО'),
 'house':('HOUSE','HOUSE','ДОМ','ДОМ'),
 'robot':('ROBOT','RO BOT','РОБОТ','РО БОТ'),
 'ball':('BALL','BALL','МЯЧ','МЯЧ'),
 'flower':('FLOWER','FLOW ER','ЦВЕТОК','ЦВЕ ТОК'),
 'fish':('FISH','FISH','РЫБА','РЫ БА'),
 'bee':('BEE','BEE','ПЧЕЛА','ПЧЕ ЛА'),
 'frog':('FROG','FROG','ЛЯГУШКА','ЛЯ ГУШ КА'),
 'cat':('CAT','CAT','КОШКА','КОШ КА'),
 'nest':('NEST','NEST','ГНЕЗДО','ГНЕЗ ДО'),
 'worm':('WORM','WORM','ЧЕРВЯК','ЧЕР ВЯК'),
 'water':('WATER','WA TER','ВОДА','ВО ДА'),
 'salt':('SALT','SALT','СОЛЬ','СОЛЬ'),
 'sand':('SAND','SAND','ПЕСОК','ПЕ СОК'),
 'wood':('WOOD','WOOD','ДЕРЕВО','ДЕ РЕ ВО'),
 'nose':('NOSE','NOSE','НОС','НОС'),
 'hand':('HAND','HAND','РУКА','РУ КА'),
 'heart':('HEART','HEART','СЕРДЦЕ','СЕРД ЦЕ'),
 'butterfly':('BUTTERFLY','BUT TER FLY','БАБОЧКА','БА БОЧ КА'),
 'turtle':('TURTLE','TUR TLE','ЧЕРЕПАХА','ЧЕ РЕ ПА ХА'),
 'battery':('BATTERY','BAT TER Y','БАТАРЕЙКА','БА ТА РЕЙ КА'),
 'paper':('PAPER','PA PER','БУМАГА','БУ МА ГА'),
 'soap':('SOAP','SOAP','МЫЛО','МЫ ЛО'),
 'eye':('EYE','EYE','ГЛАЗ','ГЛАЗ'),
 'brain':('BRAIN','BRAIN','МОЗГ','МОЗГ'),
 'stomach':('STOMACH','STOM ACH','ЖЕЛУДОК','ЖЕ ЛУ ДОК'),
 'cloud':('CLOUD','CLOUD','ОБЛАКО','ОБ ЛА КО'),
 'rain':('RAIN','RAIN','ДОЖДЬ','ДОЖДЬ'),
 'island':('ISLAND','IS LAND','ОСТРОВ','ОС ТРОВ'),
 'hammer':('HAMMER','HAM MER','МОЛОТОК','МО ЛО ТОК'),
 'bird':('BIRD','BIRD','ПТИЦА','ПТИ ЦА'),
 'moon':('MOON','MOON','ЛУНА','ЛУ НА'),
 'tree':('TREE','TREE','ДЕРЕВО','ДЕ РЕ ВО'),
 'tooth':('TOOTH','TOOTH','ЗУБ','ЗУБ'),
 'foot':('FOOT','FOOT','СТОПА','СТО ПА'),
 'egg':('EGG','EGG','ЯЙЦО','ЯЙ ЦО'),
 'sea':('SEA','SEA','МОРЕ','МО РЕ'),
}

def words(task,locale):
    if task.get('native_words'): return task['native_words'][locale],[task['native_words'][locale]]
    if locale=='de': return task['word'],task.get('syllables',[task['word']])
    row=NATIVE[task['object']];offset=0 if locale=='en' else 2
    return row[offset],row[offset+1].split()

def choices(answer,alphabet,index):
    options=[answer]+[letter for letter in alphabet if letter!=answer][:2]
    shift=index%3
    return options[shift:]+options[:shift]

def numeric(answer,index=0):
    options=[answer,answer+1,answer-1 if answer>0 else answer+2]
    shift=index%3
    return options[shift:]+options[:shift]

def texts(prompts,hints):
    return {lang:{'prompt':q,'tip':h} for lang,q,h in zip(LOCALES,prompts,hints)}

def literacy(task,index):
    task['variants']={}
    for locale in LOCALES:
        word,parts=words(task,locale)
        if locale=='de':continue
        variant={'word':word,'syllables':parts}
        if task['kind']=='initial':
            variant.update(answer=word[0],options=choices(word[0],'АМОСТРКБЛ' if locale=='ru' else 'AMSBTCLRO',index))
            q=f'{word.capitalize()}. Which letter comes first?' if locale=='en' else f'{word.capitalize()}. Какая первая буква?'
            h=f'{word.capitalize()} starts with {word[0]}.' if locale=='en' else f'В слове {word.capitalize()} первая буква {word[0]}.'
        elif task['kind']=='syllables':
            n=len(parts);variant.update(answer=n,options=numeric(n,index))
            if locale=='en' and task['object'] in ('flower','battery'):
                variant['accepted_answers']=[1,2] if task['object']=='flower' else [2,3]
            q=f'{word.capitalize()}. How many syllables?' if locale=='en' else f'{word.capitalize()}. Сколько слогов?'
            h=('Say and clap: ' if locale=='en' else 'Произнеси и хлопай: ')+'. '.join(p.capitalize() for p in parts)+'.'
        elif task['kind']=='rhyme':
            if locale=='en':
                variant.update(answer='mouse',options=['mouse','ball','tree'],option_labels={'mouse':'MOUSE','ball':'BALL','tree':'TREE'})
                q='House. Which word rhymes?';h='House and mouse have the same ending sound.'
            else:
                variant.update(answer='fish',options=['fish','ball','cat'],option_labels={'fish':'СОМ','ball':'МЯЧ','cat':'КОТ'})
                q='Дом. Какое слово рифмуется?';h='Дом и сом звучат похоже в конце.'
        else:
            other=list(dict.fromkeys(row[0 if locale=='en' else 2] for row in NATIVE.values()))
            pool=[w for w in other if w!=word]
            options=[word,pool[index%len(pool)],pool[(index+5)%len(pool)]]
            shift=index%3;options=options[shift:]+options[:shift]
            variant.update(answer=word,options=options)
            q='Which word matches the picture?' if locale=='en' else 'Какое слово подходит к картинке?'
            h=('The word is '+word.capitalize()+'.' if locale=='en' else 'Это слово '+word.capitalize()+'.')
        task['variants'][locale]=variant
        task['texts'][locale]={'prompt':q,'tip':h}

def language_bonus(parent,index,level):
    bonus={'kind':'word','object':parent['object'],'variants':{},'texts':{}}
    for locale in LOCALES:
        word,_=words(parent,locale)
        alphabet='АМОСТРКБЛЕИ' if locale=='ru' else 'AEIMONRSTUL'
        positions=[(index+level+j)%len(word) for j in range(min(len(word),level+2))]
        positions=sorted(set(positions))
        answer=''.join(word[p] for p in positions)
        from advanced import letter_distractors
        wrong=letter_distractors(answer,alphabet,index+level)
        opts=[answer,*wrong];shift=index%3;opts=opts[shift:]+opts[:shift]
        masked=''.join('_' if p in positions else c for p,c in enumerate(word))
        variant={'word':word,'display':masked,'answer':answer,'options':opts,'missing_positions':positions,
                 'option_displays':{o:''.join(o[positions.index(p)] if p in positions else '_' for p in range(len(word))) for o in opts}}
        from pedagogy import STRATEGIES
        if locale=='de':
            from advanced import word_title
            q='Welche Buchstaben fehlen?'
        elif locale=='en':q='Which letters are missing?'
        else:q='Какие буквы пропущены?'
        h=STRATEGIES['german'][LOCALES.index(locale)]
        from advanced import word_title
        bonus['texts'][locale]={'prompt':q,'tip':h,'spoken_prompt':word_title(word,locale)+'. '+q}
        if locale=='de':bonus.update(variant)
        else:bonus['variants'][locale]=variant
    return bonus

def math_bonus(index,level):
    a=5+index%10;b=1+index//10;c=1+index%4
    if level==1:
        answer=a+b-c;display=f'{a} + {b} − {c} = ?'
        q=[f'Erst {b} zu {a} dazu, dann {c} weg. Wie viele bleiben?',f'Add {b} to {a}, then take away {c}. How many remain?',f'К {a} прибавь {b}, затем вычти {c}. Сколько осталось?']
        h=[f'{a} plus {b} sind {a+b}. Nun {c} abziehen.',f'{a} plus {b} is {a+b}. Now subtract {c}.',f'{a} плюс {b} — это {a+b}. Теперь вычти {c}.']
    else:
        a=2+index%9;b=1+index//9;c=1+index%4;answer=b;display=f'{a} + ? + {c} = {a+b+c}'
        q=['Welche Zahl fehlt zwischen den beiden Pluszeichen?','Which number is missing between the plus signs?','Какого числа не хватает между знаками плюс?']
        h=[f'Ziehe {a} und dann {c} von {a+b+c} ab.',f'Subtract {a}, then {c}, from {a+b+c}.',f'Из {a+b+c} вычти {a}, затем {c}.']
    return {'kind':'equation','display':display,'answer':answer,'options':numeric(answer,index),'texts':texts(q,h)}

def logic_bonus(parent,index,level):
    a=1+index%5;step=2+index//5
    if level==1:
        sequence=[a,a+step,a+step+1,a+2*step+1]
        continuation=[a+2*step+2,a+3*step+2];answer=sum(continuation)
        display=' → '.join(map(str,sequence))+' → ? → ?'
        numbers=', '.join(map(str,sequence))
        q=[f'{numbers}. Zwei Schritte wechseln. Wie groß ist die Summe der nächsten beiden Zahlen?',f'{numbers}. Two steps alternate. What is the sum of the next two numbers?',f'Продолжи ряд: {numbers}. Найди сумму двух следующих чисел.']
        h=[f'Abwechselnd {step} und eins dazu. Setze zweimal fort und addiere beide neuen Zahlen.',f'Alternate adding {step} and one. Continue twice, then add the two new numbers.',f'Чередуй прибавление {step} и одного. Продолжи дважды и сложи два новых числа.']
        rule={'steps':[step,1],'given':sequence,'continuation':continuation,'operation':'sum-next-two'}
    else:
        extra=1+index//5;answer=a+2;output=2*answer+extra
        examples=[[a,2*a+extra],[a+1,2*(a+1)+extra]]
        display=f'{a} → {examples[0][1]}\n{a+1} → {examples[1][1]}\n? → {output}'
        q=[f'Aus {a} wird {examples[0][1]}, aus {a+1} wird {examples[1][1]}. Welche Startzahl ergibt {output}?',f'{a} becomes {examples[0][1]}, {a+1} becomes {examples[1][1]}. Which starting number gives {output}?',f'{a} превращается в {examples[0][1]}, {a+1} — в {examples[1][1]}. Какое начальное число даёт {output}?']
        h=[f'Vorwärts: verdoppeln, danach {extra} addieren. Gehe für die gesuchte Startzahl rückwärts.',f'Forward: double, then add {extra}. Work backwards to find the starting number.',f'Вперёд: удвой, затем прибавь {extra}. Найди начальное число обратными действиями.']
        rule={'multiply':2,'add':extra,'examples':examples,'output':output,'operation':'inverse-function'}
    return {'kind':'equation','display':display,'answer':answer,'options':numeric(answer,index),'texts':texts(q,h),'logic_rule':rule}

def expand(tasks,languages):
    ui=languages['ui']
    for key,values in {
        'german':('Deutsch','English','Русский'),
        'points':('Gesamtpunkte','Total points','Всего очков'),
        'bonus':('Bonusaufgabe','Bonus challenge','Бонусное задание'),
        'skip_bonus':('Überspringen →','Skip →','Пропустить →'),
        'equation':('Knobelaufgabe','Think it through','Подумай'),
        'initial':('Wie fängt das Wort an?','Which letter comes first?','Какая первая буква?'),
        'syllables':('Wie viele Silben?','How many syllables?','Сколько слогов?'),
        'word':('Welches Wort passt?','Which word matches?','Какое слово подходит?'),
        'rhyme':('Was reimt sich?','Which words rhyme?','Какие слова рифмуются?'),
        'privacy':('400 Aufgaben und jeweils zwei freiwillige Bonusaufgaben. Keine Konten, Werbung oder Netzwerkverbindungen. Dein Gesamtpunktestand bleibt auf diesem Gerät.','400 tasks, each with two optional bonus challenges. No accounts, adverts or network connections. Your total score stays on this device.','400 заданий, в каждом два необязательных бонусных задания. Нет аккаунтов, рекламы и сетевых соединений. Общий счёт сохраняется на этом устройстве.'),
    }.items():ui[key]=dict(zip(LOCALES,values))
    cues=json.loads((SOURCE/'riddle-cues.json').read_text())
    for subject in ['math','german','logic','physics','biology','chemistry','body','geography']:
        parents=[t for t in tasks if t['subject']==subject]
        for index,parent in enumerate(parents):
            parent['points']=10
            if subject=='german' and not parent.get('advanced_native'):literacy(parent,index)
            if parent['kind']=='discovery':
                clue=cues[parent['id']]
                parent['riddle_scene']=clue['scene']
                parent['keyword']=clue['keywords'][0]
                for j,locale in enumerate(LOCALES):
                    q=parent['texts'][locale]['prompt'] if parent.get('content_revision')==2 else clue.get('questions',[parent['texts'][lang]['prompt'] for lang in LOCALES])[j]
                    parent['texts'][locale]['prompt']=clue['keywords'][j]+'. '+q
                    parent.setdefault('variants',{}).setdefault(locale,{})['keyword']=clue['keywords'][j]
            bonuses=[]
            for level in [1,2]:
                if subject=='math':
                    from advanced import maths
                    bonus=maths(index,level)
                elif subject=='german':bonus=language_bonus(parent,index,level)
                elif subject=='logic':bonus=logic_bonus(parent,index,level)
                else:
                    # The complete scientific comparisons are compiled below
                    # after the common ID/reward wrapper exists, never returned
                    # as unfinished tasks.
                    bonus={'kind':'discovery','answer':parent['answer'],'options':list(parent['options']),
                           'object':parent['object'],'texts':deepcopy(parent['texts'])}
                bonus.update(id=parent['id']+'_bonus_'+str(level),parent_id=parent['id'],subject=subject,points=50 if level==1 else 100,optional=True,reasoning_level=level,content_revision=2)
                bonus['prompt']=bonus['texts']['de']['prompt'];bonus['tip']=bonus['texts']['de']['tip']
                bonuses.append(bonus)
            parent['bonuses']=bonuses
    from pedagogy import science_bonuses
    tasks=science_bonuses(tasks,languages)
    # Stable per-task shuffling prevents solving a whole round by the old
    # repeating left/middle/right answer-position cycle.
    import hashlib
    for parent in tasks:
        for task in [parent,*parent['bonuses']]:
            for locale in LOCALES:
                target=task if locale=='de' else task.get('variants',{}).get(locale)
                if target is None or 'options' not in target:continue
                target['options']=sorted(target['options'],key=lambda choice:hashlib.sha256(
                    (task['id']+'|2|'+locale+'|'+json.dumps(choice,ensure_ascii=False)).encode()).digest())
    return tasks
