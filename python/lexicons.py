'''
Created on May 27, 2014

@author: lusisi
'''
beforeSeq='''afore | aforesaid | aforetime | ahead | ahead of | already | and then | ante | ante- |  
antecedent | antecedently | before | before present | beforehand | by the time | earlier | 
early | ere | first | firstly | fore | foregoing | former | formerly | heretofore | in advance | 
in advance of | in days of yore | in old days | on the eve of | once | past | pre- | precede | 
preceded | precedent | precedes | preceding | preceding the time when | precipitate |  
precipitated | precipitates | precipitating | precursive | precursory | preliminary | preop | 
preoperatively | preparatory | preprandial | previous | previous to | previously | prior |
prior to | since | sooner | sooner than | then | to come | until | up front | up to now '''

afterSeq='''a while later | after | after that | after this | afterward | afterwards | at a later time | 
behind | by and by | consequently | ensuingly | eventually | follow | followed | following 
| follows | from that day forward | from that day on | from there forward | from there on 
| hereafter | in a while | later | latterly | next | on the next day | post | post- | 
postoperative | postoperatively | since | soon | subsequent | subsequently | then | 
thenceforth | thenceforward | thereafter | thereon | ultimately '''

causesSeq='''accordingly | account for | accounted for | accounting for | accounts for | affect | 
affected | affecting | affects | are responsible for | arouse | aroused | arouses | arousing | 
as a consequence | as a result | as expected | became | because | because of | become | 
becomes | becoming | block | blocked | blocking | blocks | bring about | brings about | 
brought about | can generate | can lead to | cause | cause of | cause these symptoms | 
caused | caused by | causes | causing | change | changed | changes | changing | 
consequently | contribute to | contributed to | contributes to | contributing to | could 
generate | create | created | creates | creating | develop | developed | developing | 
develops | due to | effect | enable | enabled | enables | enabling | evoke | evoked | evokes 
| evoking | for | for this reason | force | forced forces | forcing | form | formed | 
forming | forms | gave rise to | generate | generated | generates | generating | give rise to 
| given | gives rise to | giving rise to | had an effect | hamper | hampered | hampering | 
hampers | has an effect | have an effect | having an effect | impede | impeded | impedes | 
impeding | in consequence | in effect | incite | incited | incites | inciting | increase | 
increased | increases | increasing | indicate | indicated | indicates | indicating | induce | 
induced | induces | inducing | influence | influenced | influences | influencing | interfere 
with | interfered with | interferes with | interfering with | is blamed for | is responsible 
for | lead to | leading to | leads to | leave | leaves | leaving | led to | left | made | made 
possible | make | make possible | makes | makes possible | making | making possible | 
motivate | motivated | motivates | motivating | perpetuate | perpetuated |perpetuates | 
perpetuating | play a role in | played a role in | playing a role in | plays a role in | 
precipitate | precipitated | precipitates | precipitating | prerequisite | prerequisites | 
prevent | prevented | preventing | prevents | produce | produced | produces | producing | 
promote | promoted | promotes | promoting | prompt | prompted | prompting | prompts | 
provoke | provoked | provokes | provoking | raise | raised | raises | raising | reduce | 
reduced | reduces | reducing | render | rendered | rendering | renders | require | required | 
requires | requiring | restrain | restrained | restraining | restrains | result | result in | 
resulted | resulted in | resulting | resulting in | results | results in | since | slow | slowed | 
slowing | slows | so | so that | spark | sparked | sparking | sparks | stimulate | stimulated 
| stimulates | stimulating | such that | the reason for | trigger | triggered | triggering | 
triggers | was responsible for | yield | yielded | yielding | yields'''

causedBySeq='''as soon as | attributed to | because | because of | derive from | derived from | deriving 
from | due to | effect of | follow from | followed from | following from | follows from | 
is attributed to | is a result of | is a consequence of | now that | occur from | occurred 
from | occurring from | occurs from | on account of | originate from | originate in | 
originate with | originated from | originated in | originated with | originates from | 
originates in | originates with | originating from | originating in | originating with | 
owing to | result from | result of | resulted from | resulting from | results from | stem 
from | stemmed from | stemming from | stems from | thanks to'''

duringSeq='''accompanied | accompanies | accompanying | ad interim | all along | all the time | all 
the while | all through | amid | at that same time | at that time | at the same time | at the 
time | at this same time | at this time as well | attendant | coexist | coexisted | coexisting 
| coincide | coincided | coincident | coincidentally | coincides | coinciding | coinciding | 
concomitant | concomitantly | concurrent | concurrently | conjoint | conjointly | 
contemporaneous | contemporaneously | during | during the interval | for now | for the 
duration | for the moment | for the time being | from beginning to end | from start to 
finish | in conjunction | in the course of | in the interim | in the interval | in the 
meantime | in the meanwhile | in the middle of | in the time of | inextricably | 
inseparably | intraoperatively | jointly | linked | meantime | meanwhile | mid | midst | 
over | pending | simultaneous | simultaneously | synchronically | synchronous | 
synchronously | the time between | the whole time | through the whole of | throughout | 
throughout the | together | when | when the patient | while '''

startingSeq='''at first | at the start | began | beginning | begins | begun | commence | commenced | 
commences | commencing | embark on | embarked on | embarking on | embarks on | 
first of all | get started | gets started | getting started | got started | in the beginning | 
initial | initially | initiate | initiated | initiates | initiating | lead off | leading off | leads off 
| led off | onset | recommence | recommenced | recommences | recommencing | restart | 
restarted | restarting | restarts | set out | sets out | setting out | start | start out | started | 
started out | starting | starting out | starts | starts out'''

continuingSeq='''continually | continue | continues | continuing | continuous | lasting | lasts | ongoing | 
persisting | persists | prolonged | recurrence | recurring | remain | remained | remaining | 
resumed | still | sustained | sustaining | unchanged | unchanging | undergoing '''

endingSeq='''after all | at last | at length | at long last | at the close | at the end of the day | 
conclusively | eventually | finally | in due time | in the end | in the long run | lastly | 
someday | ultimately'''

suddenlySeq='''abruptly | all at once | all of a sudden | asudden | immediately | instantly | just then | on 
spur of moment | precipitately | straightaway | sudden | suddenly | tout de suite | 
unexpectedly | without warning'''

nowSeq='''at this point | currently | now | right away | right now | soon '''

saysSeq='''says | said | note | notes | noted | told | tells | presents | presented | describes | described | 
states | stated | denied | denies | complains | complained | report | reports | reported '''

