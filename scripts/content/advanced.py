"""Authored second learning round: new problems, not a reset of lifetime rewards.

The previous station IDs remain routing identifiers. Save revision 2 distinguishes
new completions from the archived achievements earned in the first round.
"""
from pathlib import Path
SOURCE=Path(__file__).parent
LANGS=('de','en','ru')

def localized(q,h):return {lang:{'prompt':a,'tip':b} for lang,a,b in zip(LANGS,q,h)}
def numeric(n,i):
    values=[n-1,n,n+1];k=i%3
    return values[k:]+values[:k]

def maths(i,level=0):
    a=9+i%10;b=4+i//4;c=2+i%4
    if level:
        a=14+i%12;b=5+i//5;c=3+i%5
        if level==1:
            d=2+i%3;answer=a+b-c-d;display=f'{a} + {b} − {c} − {d} = ?'
            q=[f'Erst {b} zu {a}, dann {c} und {d} weg. Wie viel bleibt?',f'Add {b} to {a}, then subtract {c} and {d}. How much remains?',f'Сложи {a} и {b}, затем вычти {c} и {d}. Сколько осталось?']
            h=[f'Erst {a+b}, dann {a+b-c}, zuletzt {answer}.',f'First {a+b}, then {a+b-c}, finally {answer}.',f'Сначала {a+b}, потом {a+b-c}, в конце {answer}.']
        else:
            target=a+b-c;answer=b;display=f'{a} + ? − {c} = {target}'
            q=['Welche Zahl fehlt? Denke die beiden Schritte rückwärts.','Which number is missing? Think backwards through both steps.','Какого числа не хватает? Пройди оба шага в обратном порядке.']
            h=[f'Zu {target} kommen {c} zurück. Von {target+c} ziehst du {a} ab.',f'Add {c} back to {target}. Subtract {a} from {target+c}.',f'Сначала сложи {target} и {c}. Затем вычти {a}.']
    elif i%4==0:
        answer=a+b-c;display=f'{a} + {b} − {c} = ?'
        q=[f'Zu {a} kommen {b}, dann gehen {c}. Wie viele bleiben?',f'{b} join {a}, then {c} leave. How many remain?',f'Было {a}. Добавили {b}, убрали {c}. Сколько осталось?']
        h=[f'{a} plus {b} sind {a+b}. Dann {c} weg.',f'{a} plus {b} is {a+b}. Then take away {c}.',f'{a} плюс {b} — это {a+b}. Потом убери {c}.']
    elif i%4==1:
        target=a+b;answer=b;display=f'{a} + ? = {target}'
        q=[f'Ergänze {a} bis {target}. Welche Zahl fehlt?',f'Complete {a} up to {target}. Which number is missing?',f'Было {a}, стало {target}. Сколько добавили?']
        h=[f'Gehe zuerst zum nächsten Zehner, dann bis {target}.',f'Go to the next ten first, then up to {target}.',f'Сначала дойди до следующего десятка, потом до {target}.']
    elif i%4==2:
        n=3+(i//4)%5;groups=2+i//20;gone=1+(i//4)%3;answer=n*groups-gone
        display=' + '.join([str(n)]*groups)+f' − {gone} = ?'
        q=[f'{groups} Körbe mit je {n} Äpfeln. Du verschenkst {gone}. Wie viele bleiben?',f'{groups} baskets have {n} apples each. You give away {gone}. How many remain?',f'Корзин: {groups}. В каждой яблок: {n}. Отдали {gone}. Сколько осталось?']
        h=[f'Alle Körbe zusammen: {groups*n}. Nun {gone} abziehen.',f'All baskets together: {groups*n}. Now subtract {gone}.',f'Во всех корзинах вместе {groups*n}. Теперь вычти {gone}.']
    else:
        a=17+i%9;b=2+i%7;c=3+i//10;answer=b;target=a-b+c
        display=f'{a} − ? + {c} = {target}'
        q=['Eine Zahl wird weggenommen, dann kommt etwas dazu. Wie viel ging weg?','A number is taken away, then some is added. How much was taken away?','Сначала число убрали, потом немного добавили. Сколько убрали?']
        h=[f'Nimm die {c} zuerst wieder weg. Vergleiche {target-c} mit {a}.',f'Undo the added {c} first. Compare {target-c} with {a}.',f'Сначала отмени прибавление {c}. Сравни {target-c} и {a}.']
    return {'kind':'equation','display':display,'answer':answer,'options':numeric(answer,i),'texts':localized(q,h),'thinking':'multi-step arithmetic or missing quantity'}

def logic(i,languages):
    a=2+i%6;s=2+i//8
    if i%4==0:
        seq=[a,a+s,a+s+1,a+2*s+1];answer=a+2*s+2;display=' → '.join(map(str,seq))+' → ?'
        q=['Zwei Schritte wechseln sich ab. Welche Zahl folgt?','Two steps alternate. Which number follows?','Два шага чередуются. Какое число дальше?']
        h=[f'Abwechselnd {s} dazu, dann eins dazu.',f'Alternate adding {s}, then adding one.',f'Чередуй: прибавь {s}, потом один.']
    elif i%4==1:
        answer=a+3*s;display=f'{a}   {a+s}\n{a+2*s}   ?'
        q=['Nach rechts und nach unten gilt ein fester Schritt. Was fehlt unten rechts?','A fixed step goes right and another goes down. What is missing at bottom right?','Вправо и вниз действуют постоянные шаги. Чего не хватает внизу справа?']
        h=[f'Nach rechts {s} dazu, nach unten {2*s} dazu.',f'Add {s} going right, add {2*s} going down.',f'Вправо прибавь {s}, вниз прибавь {2*s}.']
    elif i%4==2:
        k=i//4;cycle=['sun','moon','star'];sequence=[cycle[(j+k)%3] for j in range(5)]
        start=1+k;counts=[start,start+2,start+3,start+5,start+6]
        image=cycle[(5+k)%3];number=start+8;answer=f'{image}:{number}'
        options=[f'{cycle[(6+k)%3]}:{number}',answer,f'{image}:{number+1}']
        q=['Bild und Zahl haben eigene Regeln. Welches Paar setzt beide fort?','Picture and number have separate rules. Which pair continues both?','У картинок и чисел свои правила. Какая пара продолжает оба ряда?']
        h=['Die drei Bilder wiederholen sich. Bei den Zahlen wechseln plus zwei und plus eins.','The three pictures repeat. The numbers alternate adding two and adding one.','Три картинки повторяются. У чисел чередуются прибавления двух и одного.']
        return {'kind':'dual_pattern','sequence':sequence,'counts':counts,'answer':answer,'options':options,'texts':localized(q,h),'thinking':'combine a three-image cycle with alternating numeric steps'}
    else:
        k=i//4;animals=['cat','frog','bird','mouse','turtle','bee','fish'];pool=[animals[(k+j)%len(animals)] for j in range(3)]
        x,y,z=pool;front=k%2==0;answer=z if front else y
        q=[];h=[]
        for lang in LANGS:
            nx,ny,nz=[languages['objects'][id][lang] for id in pool]
            if lang=='de':
                q.append(f'{nx} steht vor {ny}. {nz} steht vor {nx}. Wer steht '+('ganz vorn?' if front else 'ganz hinten?'))
                h.append(f'Von vorn nach hinten: {nz}, {nx}, {ny}.')
            elif lang=='en':
                q.append(f'The {nx} is before the {ny}. The {nz} is before the {nx}. Who is '+('first?' if front else 'last?'))
                h.append(f'From first to last: {nz}, {nx}, {ny}.')
            else:
                q.append(f'{nx} раньше, чем {ny}. {nz} раньше, чем {nx}. Кто '+('самый первый?' if front else 'самый последний?'))
                h.append(f'От первого к последнему: {nz}, {nx}, {ny}.')
        return {'kind':'reasoning_choice','riddle_scene':'navigation','keyword':'?',
                'answer':answer,'options':pool,'order':[z,x,y],'ask_first':front,
                'texts':localized(q,h),'thinking':'compose two ordering constraints'}
    return {'kind':'equation','display':display,'answer':answer,'options':numeric(answer,i),'texts':localized(q,h),'thinking':'infer and transfer a two-part rule'}

def literacy(parent,i,word_row):
    result={'kind':'word','advanced_native':True,'native_words':dict(zip(LANGS,word_row)),'variants':{},'texts':{},'thinking':'auditory spelling and reconstructing missing letter pairs'}
    for locale,word in zip(LANGS,word_row):
        positions=sorted({i%len(word),(i+max(1,len(word)//2))%len(word)})
        answer=''.join(word[p] for p in positions)
        alphabet='АЕИКЛМНОРСТ' if locale=='ru' else 'AEIKLMNORST'
        wrong=[x+answer[1:] for x in alphabet if x!=answer[0]][:2]
        options=[wrong[0],answer,wrong[1]];shift=i%3;options=options[shift:]+options[:shift]
        variant={'word':word,'display':''.join('＿' if p in positions else c for p,c in enumerate(word)),'answer':answer,'options':options}
        q={'de':f'{word.capitalize()}. Welche beiden Buchstaben fehlen?','en':f'{word.capitalize()}. Which two letters are missing?','ru':f'{word.capitalize()}. Какие две буквы пропущены?'}[locale]
        h={'de':'Lies von links nach rechts. Die Lücken brauchen '+'. '.join(answer)+'.','en':'Read from left to right. The gaps need '+'. '.join(answer)+'.','ru':'Читай слева направо. В пропусках: '+'. '.join(answer)+'.'}[locale]
        result['texts'][locale]={'prompt':q,'tip':h}
        if locale=='de':result.update(variant)
        else:result['variants'][locale]=variant
    return result

def renew(tasks,languages):
    word_rows=[line.split('|') for line in (SOURCE/'advanced-words.tsv').read_text().splitlines() if line]
    assert len(word_rows)==40
    questions={}
    for subject in ['physics','biology','chemistry','body','geography']:
        rows=[line.split('|') for line in (SOURCE/f'advanced-{subject}.tsv').read_text().splitlines() if line]
        assert len(rows)==40 and all(len(row)==4 for row in rows),subject
        questions.update({row[0]:row[1:] for row in rows})
    for subject in ['math','german','logic','physics','biology','chemistry','body','geography']:
        for i,task in enumerate(t for t in tasks if t['subject']==subject):
            if subject in ('math','logic','german'):
                result=maths(i) if subject=='math' else logic(i,languages) if subject=='logic' else literacy(task,i,word_rows[i])
                for key in ['left','right','count','sequence','syllables','accepted_answers','word','variants']:task.pop(key,None)
                task.update(result)
            else:
                for lang,q in zip(LANGS,questions[task['id']]):
                    answer=languages['objects'][task['answer']][lang]
                    task['texts'][lang]={'prompt':q,'tip':{'de':'Überlege beide Hinweise. Gesucht ist: '+answer+'.','en':'Use both clues. The answer is '+answer+'.','ru':'Учти обе подсказки. Ответ: '+answer+'.'}[lang]}
                task['thinking']='combine context with function, cause, contrast or sequence'
            task['prompt']=task['texts']['de']['prompt'];task['tip']=task['texts']['de']['tip']
            task['content_revision']=2
    return tasks
