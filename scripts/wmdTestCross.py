import spacy
import wmd
from rouge import Rouge
'''used in conjunction with Template excel file, the results of this, which is
 found in rougeWMD.txt in the same forlder, get pasted in
the first column as data'''
nlp = spacy.load('en', create_pipeline=wmd.WMD.create_spacy_pipeline)

clusters = [[
"After Sandy hit the East Coast Monday night, more than 2 million New Jersey residents were left without power and feeling powerless",
"Superstorm Sandy crashed ashore this week, cutting a path of destruction several hundred miles long. Here are some numbers that help put it in perspective.",
"Hurricane Sandy struck the Northeast hard when it made landfall in New Jersey Tuesday night. New York Magazine's cover reflects the damage.",
"Hurricane Sandy is poised to become an “unprecedented” superstorm that could leave millions of people in the Northeast without power for days or even weeks, experts said Saturday.",
"One of the largest and fiercest storms to menace the East Coast in years caused widespread flooding, power outages and damage. At least 16 have died, AP reports.",
"The hurricane continued its march north, with powerful winds already affecting the region on Sunday and landfall expected on Monday or Tuesday.",
]
,[
"A shooting at a gay nightclub in Orlando killed at least 50 people on Sunday, June 12. Orlando police said they shot and killed the gunman.",
"Approximately 20 people have died after an attacker opened fire inside a gay nightclub in the Florida city of Orlando, police say.",
"Officials say at least 49 people were killed and dozens were injured in the shooting.",
"A terrorist opened fire inside a popular Orlando gay club near closing time early Sunday.",
"At least 42 people were taken to hospitals with injuries, police said. The shooter was killed in an exchange of gunfire with police.",
"Police in the US city of Orlando are telling people to stay away from a gay nightclub where a shooting has broken out and people are injured.'",
"Unconfirmed reports have emerged of a shooting at a nightclub in Orlando, Florida.'",
"At least 50 people are dead and dozens injured after a gunman opened fire at a gay nightclub in Orlando. What exactly happened?'",
"For three harrowing hours, as Omar Mateen carried out his rampage inside the Pulse nightclub in Orlando, clubgoers hid in bathrooms, in air-conditioning vents, under tables.'",
"It's the worst terror attack on American soil since 9/11, and the deadliest mass shooting in U.S. history.'",
"The gun massacre Sunday at an Orlando nightclub is the worst in the history of the U.S., where mass shootings are frighteningly common.'",
]
,[
"Nelson Mandela, who rose from militant antiapartheid activist to become the unifying president of a democratic South Africa and a global symbol of racial reconciliation, died at his Johannesburg home on Thursday. He was 95.",
"He was the country’s most potent symbol of unity, using the power of forgiveness and reconciliation.",
"The South African leader, who passionately fought apartheid, dies at age 95",
"Nelson Mandela, the anti-apartheid crusader and former South African president, died Dec. 5 at 95. We’re bringing you live updates here.",
"In a symbol befitting a nation in mourning, a dark gray cloud swept over Johannesburg on Friday as news spread that Nelson Mandela is dead.",
"The people of South Africa reacted Friday with deep sadness at the loss of a man considered by many to be the father of the nation, while mourners said it was also a time to celebrate the achievements of the anti-apartheid leader who emerged from prison to become South Africa's first black president.",
"When Nelson Mandela died on Thursday, people around the globe gathered to memorialize the man widely recognized as a beacon of courage, hope and freedom.",
"Mandela transformed his nation from oppressive regime to one of the most inclusive democracies on the planet.",
"In an extraordinary life that spanned the rural hills where he was groomed for tribal leadership, anti-apartheid activism, guerrilla warfare, 27 years of political imprisonment and, ultimately, the South African presidency, Mandela held a unique cachet that engendered respect and awe in capitals around the globe.'",
]
,[
"At least two dead and dozens injured when bombs go off near finish line.",
"Two explosions rocked the finish line at the Boston Marathon on Monday, killing three and wounding at least 144 people",
"Pressure cookers are believed to have been used to make the crude bombs that sent torrents of deadly shrapnel hurling into a crowd of onlookers and competitors at Monday’s Boston Marathon, experts told Fox News",
"Two deadly bomb blasts, seconds apart, turned the 117th Boston Marathon – the nation’s premier event for elite and recreational runners – into a tragedy on Monday. Here is a timeline of how the day’s events unfolded: 9 a.m. ET — Race …",
"When two bombs detonated in the final stretch of the Boston Marathon on Monday afternoon, runners, spectators and people across the country and around the world were stunned by the public nature of",
"Mayhem descended on the Boston marathon Monday afternoon, when an explosion at the finish line killed at least two and injured at least 23. TIME is tracking the breaking news from the scene in downtown Boston. Follow here for constant updates. 5:45 p.m.",
"Two bombs exploded in the packed streets near the finish line of the Boston Marathon on Monday, killing two people and injuring more than 100 in a terrifying scene of shattered glass, billowing smoke, bloodstained pavement and severed limbs, authorities said",
"Blasts near the finish line of the renowned race caused dozens of injuries and scattered crowds.",
"Two deadly explosions brought the Boston Marathon and much of this city to a chaotic halt Monday, killing at least three people, injuring about 140 and once again raising the specter of terrorism on American soil.",
]]
rouge = Rouge()
file1 = open("rougeWMD.txt","w+")
for sentences in clusters:
    for ind1, sentence1 in enumerate(sentences, start = 0):
        vals = []
        for ind2, sentence2 in enumerate(sentences, start = 0):
            #doc1 = nlp(sentence1)
            #doc2 = nlp(sentence2)
            scores = rouge.get_scores(sentence2, sentence1)
            if(ind1 != ind2):
                file1.write(str(scores[0]["rouge-1"]["f"])+"\n")
                #file1.write(str(doc1.similarity(doc2))+"\n")
