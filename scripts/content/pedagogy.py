"""KW-QA-01 editorial layer. Content only; stable routing and rewards unchanged.

Classification bonuses require checking factual statements for every candidate,
then applying an exact-count rule. Different fact sets are different content,
not a station-name substitution. Facts/labels are reviewed source data.
"""
import hashlib,itertools,json
from pathlib import Path
SOURCE=Path(__file__).parent
LOCALES=('de','en','ru')

def facts():
    result={}
    for line in (SOURCE/'science-properties.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        subject,key,members,*clauses=line.split('|');assert len(clauses)==3
        result.setdefault(subject,[]).append({'id':key,'members':members.split(),'texts':dict(zip(LOCALES,clauses))})
    return result

def science_bonuses(parents,languages):
    all_facts=facts();models=json.loads((SOURCE/'science-models.json').read_text())['labels']
    for subject,properties in all_facts.items():
        pool=sorted({member for p in properties for member in p['members']})
        target_parents=[p for p in parents if p['subject']==subject];used={1:set(),2:set()}
        choices={}
        for level,count in [(1,3),(2,4)]:
            target=count-1;records=[]
            intros=(['2 Aussagen stimmen. ','2 clues are true. ','Верны 2 признака. '] if level==1 else ['3 Aussagen stimmen. ','3 clues are true. ','Верны 3 признака. '])
            for indexes in itertools.combinations(range(len(properties)),count):
                selected=[properties[j] for j in indexes]
                prompts={lang:intro+' '.join(f['texts'][lang] for f in selected) for lang,intro in zip(LOCALES,intros)}
                if any(len(q)>(130 if lang=='ru' else 155) for lang,q in prompts.items()):continue
                scores={obj:sum(obj in f['members'] for f in selected) for obj in pool}
                correct=[obj for obj in pool if scores[obj]==target]
                wrong=[obj for obj in pool if scores[obj]!=target and scores[obj]>0]
                for answer in correct:
                    for wrongs in itertools.combinations(wrong,2):
                        options=[answer,*wrongs]
                        # Each fact discriminates; no padding with irrelevant or
                        # universally true sentences to manufacture uniqueness.
                        if not all(0<sum(o in f['members'] for o in options)<3 for f in selected):continue
                        records.append((indexes,answer,options,prompts))
            assert records,(subject,level,'no reviewed candidates')
            choices[level]=records
        for index,parent in enumerate(target_parents):
            previous={parent['answer']}
            for level in [1,2]:
                candidates=sorted(choices[level],key=lambda row:hashlib.sha256((parent['id']+str(level)+repr(row[:3])).encode()).digest())
                row=next((r for r in candidates if r[0] not in used[level] and r[1] not in previous),None)
                assert row is not None,(parent['id'],level,'not enough unique scientific comparisons')
                indexes,answer,options,prompts=row;used[level].add(indexes);previous.add(answer)
                bonus=parent['bonuses'][level-1]
                hint=['Prüfe jede Aussage für jedes Bild. Zähle erst danach die passenden Aussagen.','Check every statement for each picture. Then count the matching statements.','Проверь каждый признак для каждой картинки. Затем посчитай совпадения.'] if level==1 else ['Ein Merkmal darf nicht passen. Prüfe alle vier, bevor du dich entscheidest.','One feature must not fit. Check all four before choosing.','Один признак не должен подходить. Перед выбором проверь все четыре.']
                bonus.update(kind='discovery',answer=answer,options=options,object=answer,riddle_scene={'physics':'tools','biology':'life','chemistry':'materials','body':'support','geography':'navigation'}[subject],keyword='2/3' if level==1 else '3/4',texts={lang:{'prompt':prompts[lang],'tip':h} for lang,h in zip(LOCALES,hint)},comparison={'property_ids':[properties[j]['id'] for j in indexes],'required_matches':2 if level==1 else 3,'model':subject},thinking='apply scientific facts, reject nonmatches and count exactly; not a measured difficulty certificate')
                bonus['option_labels']={o:models.get(subject,{}).get(o,[languages['objects'][o][l] for l in LOCALES])[0] for o in options}
                bonus['variants']={lang:{'option_labels':{o:models.get(subject,{}).get(o,[languages['objects'][o][l] for l in LOCALES])[i] for o in options}} for i,lang in enumerate(LOCALES)}
                bonus['prompt']=bonus['texts']['de']['prompt'];bonus['tip']=bonus['texts']['de']['tip']
    return parents

# Strategies deliberately avoid spelling the answer or every missing letter.
STRATEGIES={
 'math':['Rechne die Schritte der Reihe nach. Prüfe am Ende durch Rückwärtsrechnen.','Work through the steps in order. Check by working backwards.','Выполни действия по порядку. Проверь обратными действиями.'],
 'german':['Sprich das Wort langsam. Vergleiche jeden fehlenden Laut mit den Buchstabengruppen.','Say the word slowly. Match each missing sound to the groups of letters.','Медленно произнеси слово. Сравни каждый пропущенный звук с группами букв.']}
CONCEPT_HINTS={
 'apple':['Welche essbare Frucht kann aus einer Baumblüte entstehen?','Which edible fruit can develop from a tree blossom?','Какой съедобный плод может появиться из цветка дерева?'],
 'wheel':['Was bewegt sich beim Fahren immer im Kreis?','What keeps going round when you ride?','Что при езде всё время движется по кругу?'],
 'gear':['Welche Form kann in die Zähne eines anderen Teils greifen?','Which shape can mesh with the teeth of another part?','Какая форма сцепляется с зубцами другой детали?'],
 'lever':['Suche die starre Stange, die um eine feste Stütze kippt.','Look for a stiff bar that tilts about a fixed support.','Найди твёрдую доску, которая качается на неподвижной опоре.'],
 'pulley':['Verfolge den Weg des Seils. Wo ändert es seine Richtung?','Follow the rope. Where does its direction change?','Проследи за верёвкой. Где меняется её направление?'],
 'hammer':['Welche Form kann einen Schlag auf einen Nagel übertragen?','Which shape can deliver a blow to a nail?','Какая форма передаёт удар на гвоздь?'],
 'screwdriver':['Achte auf den Schlitz im Kopf der Schraube. Was passt hinein?','Look at the slot in the screw head. What fits it?','Посмотри на прорезь в головке шурупа. Что в неё подходит?'],
 'scissors':['Vergleiche, wie zwei Klingen sich gegeneinander bewegen.','Compare how two blades move against each other.','Сравни, как два лезвия движутся навстречу друг другу.'],
 'magnet':['Nicht die Form allein zählt. Welche Kraft wirkt schon aus der Nähe?','Shape alone is not enough. Which force acts from nearby?','Важна не только форма. Какая сила действует на расстоянии?'],
 'battery':['Trenne die Energiequelle von dem Teil, das die Energie verbraucht.','Distinguish the energy source from the part that uses it.','Отличи источник энергии от детали, которая её расходует.'],
 'bulb':['Wo wird elektrische Energie in sichtbares Licht umgewandelt?','Where is electrical energy changed into visible light?','Где электрическая энергия превращается в видимый свет?'],
 'helmet':['Überlege, was vor dem Losfahren passend auf den Kopf gesetzt wird.','Think about what is fitted onto the head before riding.','Подумай, что надевают на голову перед поездкой.'],
 'bridge':['Der Weg soll über die Lücke führen und Menschen tragen.','The path must cross the gap and support people.','Дорога должна пройти над промежутком и выдержать людей.'],
 'sun':['Unterscheide selbst erzeugtes Licht von zurückgeworfenem Licht.','Distinguish light produced by a source from reflected light.','Отличи собственный свет от отражённого.'],
 'water':['Vergleiche flüssigen, festen und gasförmigen Zustand.','Compare the liquid, solid and gaseous states.','Сравни жидкое, твёрдое и газообразное состояния.'],
 'ice':['Überlege, ob es wärmer oder kälter geworden ist. Was ändert seine Form?','Think about whether it became warmer or colder. What changes shape?','Подумай, стало теплее или холоднее. Что меняет форму?'],
 'steam':['Manches Gas ist unsichtbar. Sichtbare Tröpfchen sind etwas anderes.','Some gases are invisible. Visible droplets are different.','Некоторые газы невидимы. Видимые капельки — другое.'],
 'salt':['Überlege, welche Körnchen sich im Wasser lösen können. Nicht probieren.','Think about which grains dissolve in water. Do not taste them.','Подумай, какие крупинки растворяются в воде. Не пробуй их.'],
 'sand':['Unterscheide Auflösen von bloßem Verteilen kleiner Körner.','Distinguish dissolving from just spreading small grains.','Отличи растворение от распределения мелких крупинок.'],
 'oil':['Beobachte, ob die Flüssigkeiten sich mischen oder Schichten bilden.','Consider whether the liquids mix or form layers.','Подумай, смешиваются жидкости или образуют слои.'],
 'metal':['Nicht alle Metalle werden angezogen. Vergleiche die Stoffeigenschaften.','Not all metals are attracted. Compare the properties of the materials.','Не все металлы притягиваются. Сравни свойства материалов.'],
 'glass':['Vergleiche Lichtdurchlässigkeit und feste Form.','Compare transparency and solid shape.','Сравни прозрачность и твёрдую форму.'],
 'wood':['Überlege, welcher Werkstoff aus einem Baumstamm stammt.','Think about which material comes from a tree trunk.','Подумай, какой материал получают из ствола дерева.'],
 'paper':['Überlege, welcher flache Werkstoff aus Fasern besteht.','Think about which flat material is made of fibres.','Подумай, какой плоский материал состоит из волокон.'],
 'fabric':['Vergleiche weiche Fasern mit harten, geschlossenen Oberflächen.','Compare soft fibres with hard sealed surfaces.','Сравни мягкие волокна с твёрдыми сплошными поверхностями.'],
 'soap':['Überlege, was beim Waschen hilft, Fett zu entfernen.','Think about what helps remove grease when washing.','Подумай, что помогает смывать жир при мытье.'],
 'flower':['Suche den Teil, der mit Farbe und Duft Insekten anlocken kann.','Look for the part that can attract insects with colour and scent.','Найди часть, которая привлекает насекомых цветом и запахом.'],
 'roots':['Verfolge den Weg vom Boden in die Pflanze.','Trace the route from soil into the plant.','Проследи путь из почвы внутрь растения.'],
 'seed':['Denke an ein kleines Korn, aus dem eine neue Pflanze wachsen kann.','Think about a small grain that can grow into a new plant.','Подумай о маленьком зёрнышке, из которого вырастает новое растение.'],
 'leaf':['Achte auf die flache grüne Fläche am Zweig.','Look for the flat green surface on a twig.','Обрати внимание на плоскую зелёную поверхность на ветке.'],
 'tree':['Welche Pflanze bildet mit den Jahren einen dicken Stamm?','Which plant grows a thick trunk over the years?','У какого растения с годами появляется толстый ствол?'],
 'nest':['Welche Form wird aus Halmen gebaut und hält die Eier zusammen?','What is built from grass stems and holds eggs together?','Что строят из травинок, чтобы яйца лежали вместе?'],
 'egg':['Überlege, welche schützende Hülle vor dem Schlüpfen da ist.','Think about the protective covering before hatching.','Подумай о защитной оболочке перед вылуплением.'],
 'worm':['Suche ein Tier ohne Beine, das Gänge im Boden macht.','Look for a legless animal that makes tunnels in soil.','Найди безногое животное, которое делает ходы в почве.'],
 'mushroom':['Nicht alles, was aus dem Boden wächst, ist eine Pflanze.','Not everything growing from soil is a plant.','Не всё, что растёт из почвы, является растением.'],
 'bee':['Vergleiche Körperbau und Besuch an nektarreichen Pflanzenteilen.','Compare body structure and visits to nectar-rich plant parts.','Сравни строение тела и посещение частей растения с нектаром.'],
 'butterfly':['Denke die Entwicklung nach Raupe und Puppe weiter.','Continue the life cycle after caterpillar and chrysalis.','Продолжи развитие после гусеницы и куколки.'],
 'bird':['Welche Körperbedeckung unterscheidet diese Tiergruppe?','Which body covering distinguishes this animal group?','Какой покров тела отличает эту группу животных?'],
 'cat':['Überlege, welche Tiere ihre Jungen mit Milch versorgen.','Think about which animals feed their young with milk.','Подумай, какие животные кормят детёнышей молоком.'],
 'fish':['Wo können Kiemen den nötigen Sauerstoff aufnehmen?','Where can gills take up the oxygen they need?','Где жабры получают нужный кислород?'],
 'frog':['Verbinde die schwimmende Jugendform mit dem späteren Tier.','Connect the swimming young form to the adult animal.','Свяжи плавающего детёныша со взрослым животным.'],
 'turtle':['Überlege, welches Tier einen festen Panzer am Körper hat.','Think about which animal has a hard shell on its body.','Подумай, у какого животного есть твёрдый панцирь.'],
 'mouse':['Vergleiche, was wächst, Nahrung braucht und sich fortpflanzen kann.','Compare what grows, needs food and can reproduce.','Сравни, что растёт, нуждается в пище и размножается.'],
 'eye':['Verfolge den Weg des Lichts, nicht den des Schalls.','Follow the path of light rather than sound.','Проследи путь света, а не звука.'],
 'ear':['Überlege, wo Schwingungen der Luft aufgenommen werden.','Think about where air vibrations are received.','Подумай, где воспринимаются колебания воздуха.'],
 'nose':['Vergleiche Riechen mit Schmecken. Was nimmt Duftstoffe aus der Luft auf?','Compare smelling and tasting. What receives scents from air?','Сравни обоняние и вкус. Что улавливает запахи из воздуха?'],
 'tongue':['Denke an die Sinneswahrnehmung im Mund.','Think about the sense used inside the mouth.','Подумай об ощущении внутри рта.'],
 'hand':['Vergleiche Greifen, Gehen und Kauen. Welche Bewegung ist gefragt?','Compare gripping, walking and chewing. Which action is needed?','Сравни хватание, ходьбу и жевание. Какое действие нужно?'],
 'foot':['Überlege, welcher Körperteil mit seiner Sohle auftritt.','Think about which body part steps on its sole.','Подумай, какая часть тела наступает подошвой.'],
 'heart':['Eine Pumpe drückt Flüssigkeit weiter. Welches Organ tut das im Körper?','A pump pushes liquid along. Which organ does that in the body?','Насос проталкивает жидкость. Какой орган делает это в теле?'],
 'lungs':['Verfolge den Weg der eingeatmeten Luft.','Trace the path of the air you breathe in.','Проследи путь вдыхаемого воздуха.'],
 'brain':['Wo werden Signale mit Erinnerungen verglichen?','Where are signals compared with memories?','Где сигналы сравниваются с воспоминаниями?'],
 'stomach':['Denke den Weg des Essens nach dem Schlucken weiter.','Follow the path of food after swallowing.','Продолжи путь пищи после глотания.'],
 'bone':['Vergleiche die weiche Haut mit der festen Stütze darunter.','Compare soft skin with the hard support underneath.','Сравни мягкую кожу с твёрдой опорой под ней.'],
 'tooth':['Was berührt das Essen beim Abbeißen und Zerkleinern?','What touches food when biting and breaking it up?','Что касается пищи при откусывании и измельчении?'],
 'map':['Welche Darstellung zeigt Wege flach von oben?','Which representation shows routes flat from above?','Какое изображение показывает дороги сверху на плоскости?'],
 'globe':['Vergleiche eine flache Zeichnung mit einem drehbaren Kugelmodell.','Compare a flat drawing with a rotating spherical model.','Сравни плоский рисунок с вращающейся моделью шара.'],
 'compass':['Welche drehbare Nadel richtet sich nach dem Erdmagnetfeld aus?','Which rotating needle aligns with Earth’s magnetic field?','Какая подвижная стрелка ориентируется по магнитному полю Земли?'],
 'mountain':['Suche die hohe Geländeform mit einem Gipfel.','Look for the high landform with a summit.','Найди высокую форму рельефа с вершиной.'],
 'river':['Verfolge das fließende Gewässer von seiner Quelle aus.','Follow the flowing body of water from its source.','Проследи течение от истока.'],
 'sea':['Vergleiche Salzgehalt und Größe der Gewässer.','Compare the salt content and size of bodies of water.','Сравни солёность и размеры водоёмов.'],
 'island':['Gehe in Gedanken die Küste ganz herum.','Imagine following the coast all the way round.','Мысленно обойди весь берег.'],
 'forest':['Vergleiche einzelne Pflanzen mit vielen dicht stehenden Stämmen.','Compare individual plants with many closely spaced trunks.','Сравни отдельные растения с множеством близких стволов.'],
 'desert':['Entscheidend ist die Niederschlagsmenge, nicht bloß die Wärme.','The amount of precipitation matters, not just warmth.','Важны осадки, а не только жара.'],
 'cloud':['Unterscheide schwebende Tröpfchen von fallenden Tropfen.','Distinguish floating droplets from falling drops.','Отличи висящие в воздухе капельки от падающих капель.'],
 'rain':['Achte darauf, ob Wasser flüssig oder gefroren vom Himmel fällt.','Notice whether water falls from the sky as liquid or ice.','Заметь, вода падает с неба жидкой или замёрзшей.'],
 'snow':['Vergleiche feste Kristalle mit flüssigen Tropfen.','Compare solid crystals with liquid drops.','Сравни твёрдые кристаллы с жидкими каплями.'],
 'moon':['Unterscheide einen Begleiter der Erde von selbst leuchtenden Sternen.','Distinguish Earth’s companion from stars that make their own light.','Отличи спутник Земли от звёзд, которые светят сами.'],
 'star':['Unterscheide weit entfernte leuchtende Himmelskörper von nahen Gegenständen.','Distinguish distant shining bodies from nearby objects.','Отличи далёкие светящиеся небесные тела от близких предметов.']}

def apply(tasks,languages):
    by_id={t['id']:t for t in tasks}
    for line in (SOURCE/'pedagogy-base.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        id,options,*tail=line.split('|');questions=tail[:3];assert len(tail)==4
        task=by_id[id];task['options']=options.split();task['pedagogical_review']=tail[-1]
        for lang,q in zip(LOCALES,questions):
            task['texts'][lang]['prompt']=task['variants'][lang]['keyword']+'. '+q
        task['prompt']=task['texts']['de']['prompt']
    for parent in tasks:
        for task in [parent,*parent['bonuses']]:
            if task['subject']=='german':hints=STRATEGIES['german']
            elif task['subject']=='math':
                # Keep useful first-step arithmetic hints; remove explicit final
                # solutions from the 50-point multi-step problems only.
                if task.get('reasoning_level')!=1:continue
                hints=STRATEGIES['math']
            elif task['kind']=='discovery' and 'comparison' not in task:hints=CONCEPT_HINTS[task['answer']]
            else:continue
            for locale,hint in zip(LOCALES,hints):task['texts'][locale]['tip']=hint
            task['tip']=task['texts']['de']['tip']
    for line in (SOURCE/'science-hints.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        id,*hints=line.split('|');task=by_id[id]
        for lang,hint in zip(LOCALES,hints):task['texts'][lang]['tip']=hint
        task['tip']=task['texts']['de']['tip']
    # The new term is linked to the familiar seesaw instead of left unexplained.
    for lang,label in zip(LOCALES,['Hebel (Wippe)','lever (seesaw)','рычаг (качели)']):
        by_id['physics_11'].setdefault('variants',{}).setdefault(lang,{}).setdefault('option_labels',{})['lever']=label
    by_id['physics_11']['option_labels']={'lever':'Hebel (Wippe)'}
    # Plant-part terminology is local to these tasks; generic flower words in
    # native literacy do not silently change into a different concept.
    for parent in tasks:
        if parent['subject']=='biology':
            for task in [parent,*parent['bonuses']]:
                if 'flower' not in task['options'] or 'comparison' in task:continue
                for lang,name in zip(LOCALES,['Blüte','blossom','цветок']):
                    task.setdefault('variants',{}).setdefault(lang,{}).setdefault('option_labels',{})['flower']=name
                task.setdefault('option_labels',{})['flower']='Blüte'
    for parent in tasks:
        for task in [parent,*parent['bonuses']]:
            task['options']=sorted(task['options'],key=lambda choice:hashlib.sha256((task['id']+'|2|de|'+json.dumps(choice,ensure_ascii=False)).encode()).digest())
    return tasks
