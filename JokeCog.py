import discord
from discord.ext import commands
import random
import asyncio

jokes = [
    "A man escapes from a prison where he's been locked up for 15 years. He breaks into a house to look for money and guns. "
    "Inside, he finds a young couple in bed. He orders the guy out of bed and ties him to a chair.  "
    "While tying the homeowner's wife to the bed, the convict gets on top of her, kisses her neck, then gets up and goes into the bathroom.  "
    "While he's in there, the husband whispers over to his wife: 'Listen, this guy is an escaped convict. "
    "Look at his clothes! He's probably spent a lot of time in jail and hasn't seen a woman in years. I saw how he kissed your neck. "
    "If he wants sex, don't resist, don't complain... do whatever he tells you. Satisfy him no matter how much he nauseates you. "
    "This guy is obviously very dangerous. If he gets angry, he'll kill us both. Be strong, honey. I love you!' "
    "His wife responds: 'He wasn't kissing my neck. He was whispering in my ear. He told me that he's gay, thinks you're cute, and asked if we had any Vaseline. "
    "I told him it was in the bathroom. Be strong honey. I love you, too!'",

    "So, there's this guy at his apartment and he smoking weed for his therapy session. "
    "Well his neighbors dispice him and call the cops after smelling a batch cause he refuses to share. "
    "As the police appear and smell this outside his door, they bang on the door. BANG! BANG! 'Open up, it's the police.' "
    "Calmly he goes to the door, douses his light and puts his magic bag of weed into his back pocket. "
    "Opening the door, the officer demands to search the place, as he goes, he find his magic bag of weed and says. "
    "'AH HA! Caught you red handed', the officer snickers. His neighbors boil with laughter inside thinking he will go to jail until the man speaks. "
    "'Ahem, I have a reason for this.' With the officer rolling his eyes to hear the story he lets him proceed. "
    "'You see officer this is is a magic bag of weed, I can't keep it off me because every time I flush it down the toilet, it jumps right back out again and into my back pocket.'  "
    "Frowning the officer is laughing with a argument back and forth on finding this whole story ridiculous. "
    "'Fine I'll prove it to you!' The man shouts. The officer gives him the bag confidently and watches him empty it into the toilet were he flushes it down the toilet. "
    "When nothing appears the officer goes. 'Well?' Smirking the man goes 'Well what?' With the neighbors mouths gaped opened the officer becomes annoyed. "
    "'Where the hells the drugs at?' The man smirks again. 'What drugs?'",

    '''A successful businessman flew to Vegas for the weekend to gamble. He lost the shirt off his back, and had nothing left but a quarter and the second half of his round trip ticket. All he needed to do was somehow get to the airport, and then he'd be home-free.
So he went out to the front of the casino where there was a cab waiting. He got in and explained his situation to the cabbie. He promised to send the driver money from home. He offered him his credit card numbers, his drivers license number, his address, etc...
The cabbie said, ''If you don't have fifteen dollars, get the hell out of my cab!''
So the businessman was forced to hitchhike to the airport and was barely in time to catch his flight.
One year later the businessman, having worked long and hard to regain his financial success, returned to Vegas and this time he won big. Feeling pretty good about himself, he went out to the front of the casino to get a cab ride back to the airport. Well who should he see out there, at the end of a long line of cabs, but his old buddy who had refused to give him a ride when he was down on his luck.
The businessman thought for a moment about how he could make the guy pay for his lack of charity, and he hit on a plan.
The businessman got in the first cab in the line, ''How much for a ride to the airport,'' he asked?
''Fifteen bucks,'' came the reply.
''And how much for you to give me a blowjob on the way?''
''What?! Get the hell out of my cab.''
The businessman got into the back of each cab in the long line and asked the same questions, with the same result.
When he got to his old friend at the back of the line, he got in and asked, ''How much for a ride to the airport?''
The cabbie replied, ''Fifteen bucks.''
The businessman said, ''OK,'' and off they went. Then, as they drove slowly past the long line of cabs, the businessman gave a big smile and thumbs up sign to each of the other drivers. ''',

    '''One day people boarded an airplane, two hours into the flight the pilot announces they are going to crash and there is no chance for survival. 
         Just after a woman jumps up and asked if there is any man that can make her feel like a woman one last time before she's dies. 
         A man gets up rips off his shirt throws it at her an says here iron this.''',

    '''A contestant on Who Wants to be a Millionaire? had reached the final plateau. If she answered the next question correctly, she would win the million dollars. If she answered incorrectly, she would pocket only the $32,000 milestone money.

And as she suspected it would be, the million-dollar question was no pushover. It was, "Which of the following species of birds does not build its own nest, but instead lays its eggs in the nests of other birds? Is it A) the condor; B) the buzzard; C) the cuckoo; or D) the vulture?"

The woman was on the spot. She did not know the answer. And she was doubly on the spot because she had used up her 50/50 Lifeline and her Audience Poll Lifeline. All that remained was her Phone-a-Friend Lifeline, and the woman had hoped against hope that she would not have to use it. Mainly because the only friend that she knew would be home happened to be a blonde.

But the contestant had no alternative. She called her friend and gave her the question and the four choices. The blonde responded unhesitatingly: "That's easy. The answer is 'C' -- the cuckoo."

The contestant had to make a decision and make it fast. She considered employing a reverse strategy and giving Regis any answer except the one that her friend had given her. And considering that her friend was a blonde, that would seem to be the logical thing to do.

On the other hand, the blonde had responded with such confidence, such certitude, that the contestant could not help but be persuaded.

Time was up. "I need an answer," said Regis.

Crossing her fingers, the contestant said, "C) the cuckoo."

"Is that your final answer?" asked Regis.

"Yes, that is my final answer," she said, breaking into a sweat.

After the usual foot-dragging delay Regis said, "I regret to inform you that that answer is ... absolutely correct. You are now a millionaire!"

Three days later, the contestant hosted a party for her family and friends, including the blonde who had helped her win the million dollars.

"Jenny, I just do not know how to thank you," said the contestant. "Because of your knowing the answer to that final question, I am now a millionaire. And do you want to know something? It was the assuredness with which you answered the question that convinced me to go with your choice."

"You're welcome!" the blonde said.

"By the way," the winner said, not being able to contain the question anymore. "How did you happen to know the right answer?"

"Oh, come on," said the blonde. "Everybody knows that cuckoos don't build nests. They live in clocks."''',

    '''Before Marriage:
Boy: Ah at last. I can hardly wait.
Girl: Do you want me to leave?
Boy: No don't even think about it.
Girl: Do you love me?
Boy: Of Course. Always have and always will.
Girl: Have you ever cheated on me?
Boy: Never. Why are you even asking?
Girl: Will you kiss me?
Boy: Every chance I get.
Girl: Will you hit me?
Boy: Hell no. Are you crazy?
Girl: Can I trust you?
Boy: Yes.
Girl: Darling!
After Marrige:
Read bottom to top''',
    '''A father passing by his son's bedroom was astonished to see the bed was nicely made and everything was picked up. Then, he saw an envelope, propped up prominently on the pillow. It was addressed, 'Dad'. With the worst premonition, he opened the envelope and read the letter, with trembling hands.

Dear, Dad. It is with great regret and sorrow that I'm writing you. I had to elope with my new girlfriend, because I wanted to avoid a scene with Mum and you.

I've been finding real passion with Stacy. She is so nice, but I knew you would not approve of her because of all her piercing's, tattoos, her tight Motorcycle clothes, and because she is so much older than I am.

But it's not only the passion, Dad. She's pregnant. Stacy said that we will be very happy. She owns a trailer in the woods, and has a stack of firewood for the whole winter. We share a dream of having many more children.

Stacy has opened my eyes to the fact that marijuana doesn't really hurt anyone. We'll be growing it for ourselves and trading it with the other people in the commune for all the cocaine and ecstasy we want.

In the meantime, we'll pray that science will find a cure for AIDS so that Stacy can get better. She sure deserves it!

Don't worry Dad, I'm 15, and I know how to take care of myself. Someday, I'm sure we'll be back to visit so you can get to know your many grandchildren.

Love, your son, Joshua.

P.S . Dad, none of the above is true. I'm over at Jason's house. I just wanted to remind you that there are worse things in life than the school report that's on the kitchen table. Call when it is safe for me to come home!''',

    '''Little April was not the best student in Sunday school. Usually she slept through the class. 
One day the teacher called on her while she was napping, "Tell me, April, who created the universe?" 
When April didn't stir, little Johnny, a boy seated in the chair behind her, took a pin and jabbed her in the rear. 
"GOD ALMIGHTY!" shouted April and the teacher said, "Very good" and April fell back asleep. A while later the teacher asked April, 
"Who is our Lord and Saviour," But, April didn't even stir from her slumber. Once again, Johnny came to the rescue and stuck her again. 
"JESUS CHRIST!" shouted April and the teacher said, "very good," and April fell back to sleep. Then the teacher asked April a third question. 
"What did Eve say to Adam after she had her twenty-third child?" And again, Johnny jabbed her with the pin. This time April jumped up and shouted, 
"JOHNNY IF YOU STICK THAT FUCKING THING IN ME ONE MORE TIME, I'LL BREAK IT IN HALF AND STICK IT UP YOUR ASS!" The teacher fainted.''',

    '''A dad buys a lie detector robot that slaps you if you lie.

Dad: Son, where were you at school hours?
Son: At school. The robot slaps the son.
Son: Okay I was watching KungFu Panda! The robot slaps his son again.
Son: Okay I was watching porn!
Dad: What?! When I was your age I never watched that kind of stuff! The robot slaps the dad.
Mom: Haha, after all, he is your son. The robot slaps the mom.''',

    '''Four guys are at a high school reunion and one of them goes to the restroom.
The other three guys start talking about how succesful their sons are.
Guy 1: My son is so successful he owns a cardealership and just gave his best friend a Ferarri.
Guy 2: Thats nothing, my son owns an airliner and just gave his best friend a private jet
Guy 3: Well my son is more success than that, he owns an architecture firm and just gave his best friend a castle
Guy 4 walks out of the bathroom and walks over to the other 3 guys
Guy 4: Hey guys what are we talking about
Guy 1: Oh, we are talking about how successful our sons are
Guy 4:Well, my son is a Gay stripper
Guy 2: You must be so dissappointed with what he's done with his life
Guy 4: Actually, he is doing very well for himself. He just got a Ferrari, a jet, and a caste from his three boyfriends.''',

    '''There once was this guy who was going on a date to the movies with a beautiful girl. Before he went, he made the mistake of eating a jumbo can of beans. Right after he picked her up, he felt the need to fart, but he figured he could wait until they got to the movies.
When they got there, he asked her if she wanted some popcorn and Coke. She said sure, so he went to the restroom. The line was long, so he went back to the lobby, got the food, and went back into the theatre.
When the movie was over, he goes to the bathroom again, still with a tremondously long line. So he figures he can wait until he drops her off.
When they pull up into her driveway, she exclaims, ''Oh goodie. My grandparents are here. Come on in and meet them.''
He agrees, although his A-hole is about to cry at this point.
They go in and sit down at the table. Finally, he couldn't hold it in any longer a tried to let it seep out a little at a time. As he squeezed out a toxic blast, he aimed it towards the family's hound dog Duke, in hopes that they might blame the pooch for the horrendous fart. The girl's father stands up and hollers ''Duke!!'' and sits back down.
''Great!'' he thought. ''They really think it's the dog!'' So, he starts bombarding the room with a couple, more powerful, louder stinkers.
Once again, the girl's father stands up, shouts ''Duke!!'' and sits back down.
Finally, he lets it all go and the loudest most hair-curling fart you've ever heard or smelt rippled through the dining room. The girl's father stands up again. ''Duke, get the hell out from under him before he shits on you!!''',

    '''This is a story about the girl that didn't know what cursing was. It was Thanksgiving evening and the young girl was sleeping in her bedroom and she heard her parents having sex in the next bedroom over. 
She hears the dad say, "oh honey I love your luscious tits" and she hears the mom say, "oh baby I love your slim dick". 
So the next morning, the daughter walks up to the dad and says, "Hey dad, what are luscious tits?" the dad panics and says, "It's a fine coat". 
She then walks up to the mom and says, "Hey mom, what's a slim dick?". The mom panics and says, "It's a pair of boots". 
Later on that day, everybody's getting ready for the Holiday. The girl walks past the bathroom and sees her dad shaving. 
He cuts himself on the cheek and shouts, "Shit!". The daughter then asks,"What does shit mean" and the dad replies, "I'm shaving right now sweety". 
The girl walks into the kitchen and sees her mom trying to cook the turkey. The mom accidentally drops the turkey and shouts, "Fuck". 
The daughter then asks, "hey mom, what does f*ck mean" and the mom replies, "I'm cooking the turkey sweety". About an hour later friends and family arrive at the door. 
The girl answers the door and says, "Hello everyone hang up your luscious tits and drop your slim dicks, my dad is upstairs shitting and my mom's f*cking the turkey".''',

    '''Mr. Bear and Mr. Rabbit didn't like each other very much. One day, while walking through the woods, they came across a golden frog.

They were amazed when the frog talked to them. The golden frog admitted that he didn't often meet anyone, but, when he did, he always gave them six wishes. He told them that they could have 3 wishes each.

Mr. Bear immediately wished that all the other bears in the forest were females. The frog granted his wish. Mr. Rabbit, after thinking for a while, wished for a crash helmet. One appeared immediately, and he placed it on his head. 

Mr. Bear was amazed at Mr. Rabbit's wish, but carried on with his second wish. He wished that all the bears in the neighboring forests were females as well, and the frog granted his wish.

Mr. Rabbit then wished for a motorcycle. It appeared before him, and he climbed on board and started revving the engine. Mr. Bear could not believe it and Complained that Mr. Rabbit had wasted two wishes that he could have had for himself. 

Shaking his head, Mr. Bear made his final wish, that all the other bears in the world were females as well, leaving him as the only male bear in the world.

The frog replied that it had been done, and they both turned to Mr. Rabbit for his last wish. Mr. Rabbit revved the engine, thought for a second, then said, "I wish that Mr. Bear was gay!" and rode off as fast as he could!''',

    '''A gorilla dies of old age at a zoo right before the zoo opens. It is the only gorilla at the zoo since they are not very profitable.

However, the gorilla is their most popular attraction by far, and they cannot afford to go a day without it. So the zoo owner asks one of his workers to wear a gorilla suit they have in storage for an extra $100 a day if he will go in the gorilla cage and pretend to be the gorilla until the zoo can afford a new one.

Quickly, the new "gorilla" becomes the most popular craze at the zoo. People from all over are coming to see the "Human-like" gorilla.

About a month in, the craze has started to wear off. So, to get peoples' attention back, he decides to climb over his enclosure and hang from the net ceiling above the lions den next to him. 

A large crowd of people gather watching the spectacle in awe and terror. Suddenly the man loses his grip and falls to the floor of the lion's den. The man starts screaming "HELP!! HELP!!!" 

Suddenly a lion pounces him from behind and whispers in his ear, "Shut the fuck up right now or you're going to get us both fired."''',

    '''There was this guy at a bar, just looking at his drink. He stays like that for half of an hour.

Then, this big trouble-making truck driver steps next to him, takes the drink from the guy, and just drinks it all down. The poor man starts crying. The truck driver says, "Come on man, I was just joking. Here, I'll buy you another drink. I just can't stand to see a man cry."

"No, it's not that. This day is the worst of my life. First, I fall asleep, and I go late to my office. My boss, outrageous, fires me. When I leave the building, to my car, I found out it was stolen. The police said that they can do nothing. I get a cab to return home, and when I leave it, I remember I left my wallet and credit cards there. The cab driver just drives away."

"I go home, and when I get there, I find my wife in bed with the gardener. I leave home, and come to this bar. And just when I was thinking about putting an end to my life, you show up and drink my poison.''',

    '''Bob was in trouble. He forgot his wedding anniversary. His wife was really pissed.

She told him, "Tomorrow morning, I want to see a gift in the driveway that goes from 0 to 200 in 6 seconds AND IT BETTER BE THERE!"

The next morning he got up early and left for work. When his wife woke up, she looked out the window and sure enough there was a box gift-wrapped in the middle of the driveway.

Confused, the wife put on her robe and ran out to the driveway, brought the box back in the house.

She opened it and found a brand new bathroom scale.''',

    '''One day, Little Johnny saw his grandpa smoking his cigarettes. Little Johnny asked, "Grandpa, can I smoke some of your cigarettes?" 

His grandpa replied, "Can your penis reach your asshole?" "No", said Little Johnny. His grandpa replied, "Then you're not old enough."

The next day, Little Johnny saw his grandpa drinking beer. He asked, "Grandpa, can I drink some of your beer?" 

His grandpa replied, "Can your penis reach your asshole?" "No" said Little Johhny. "Then you're not old enough." his grandpa replied.

The next day, Little Johnny was eating cookies. His grandpa asked, "Can I have some of your cookies?" Little Johnny replied, "Can your penis reach your asshole?" 

His grandpa replied, "It most certainly can!" Little Johnny replied, "Then go fuck yourself. These are my cookies!"''',

    '''How fast can you guess these words?
1. `_ _ _k`
2. `_ _ndom`
3. `d_ck`
Answers:
1. `book`
2. `random`
3. `duck`
You didn't get them right you dirty minded shit''',
    
    '''Little Girl: Mom what's this *she pulled down her pants*
Mom: That's your garage, don't let boys put their car into your garage
She nods and hops off

Next door
Little Boy: Dad whats this? *he pulls down his pants*
Dad: That's your car, you need to put that into a girls garage
He nods and hops off
Little girl walks in with her hands covered with blood
Mom: WHAT HAPPENED!?
Little Girl: The little boy from next door tried to put his car into my garage so I pulled its wheels off''',

    '''Guy: Wanna suck my dick?
Girl: No.
Guy: Probably for the best. I mean, it has a label-Warning! Choking Hazard!
Girl: Isn't that the warning put on tiny objects?''',

    '''Teacher: And therefore, sperm cells are made up of glucose.
Student: So you're saying that sperm has sugar in it?
Teacher: Technically. Yes.
Student: But it doesn't even taste like that...
Teacher: what?
Student: what?''',

    '''Who's the biggest prostitute in history? Ms. Pacman, for 25 cents that b*tch swallowed balls till she died.''',

    '''What gets longer when pulled, fits between breasts, inserts neatly in a hole, and works best when jerked?
It's a fucking seatbelt, you shitty minded perverts.''',

    '''After having failed his exam, a student goes and confronts his lecturer about it.
Student:
“Sir, do you really understand anything about the subject?”

Professor:
“Surely I must. Otherwise I would not be a professor!”

Student:
“Great, well then I would like to ask you a question. If you can give me the correct answer, I will accept my mark as is and go. If you however do not know the answer, I want you to give me an “A” for the Exam.”

Professor:
“Okay, it’s a deal. So what is the question?”

Student:
“What is legal but not logical, logical but not legal, and neither logical nor legal?”

Even after some long and hard consideration, the professor cannot give the student an answer, and therefore changes his exam mark into an “A”, as agreed.
Afterwards, the professor calls on his best student and asks him the same question.

He immediately answers:
“Sir, you are 63 years old and married to a 35 year old woman, which is legal, but not logical. Your wife has a 17 Year old lover, which is logical but not legal. 

The fact that you have given your wife’s lover an “A”, although he really should have failed, is neither legal nor logical.”
''',

    '''A husband had to leave his wife for 3 months while he attended business in Africa. 
    
To prevent her loneliness and to lower the temptations of her being unfaithful he gave his wife a magic dildo before he left. 

The reason it was called a magic dildo was because no matter where the wife was all she would have to do is say, "magic dildo" and then the place she wanted the magic dildo to be and it would appear there.

Well a week after her husband left the wife decided to give the magic dildo a try. She left it in the garage and then went up into her bed and said, "magic dildo, vagina." 

Instantly it appeared where it was called and satisfied the wife. The wife was very excited about her magic dildo and started to use it everywhere. 

She called to it at work when no one was looking, in the wooded part of the park, at the movie theater, when she was dancing, everywhere. 

No matter where she was it would appear and make her squirm with pleasure.
One day on her way to work the wife hit bad traffic. She looked up ahead and saw there was an accident and realized it would be a while and decided to call the magic dildo. 

The wife was feeling really confident and called out "magic dildo, vagina." She became overwhelmed and hit the accelerator slamming into the car in front of her. As it turned out that car was a cop.

The cop came up to the car seeing the woman squirming and suspected she was on drugs.

"Get out of the car now and put your hands on the hood!" The wife tried to comply but ended up just falling to the pavement. 

The officer was quite alright and asked the wife what she was on. The wife told him "Officer I'm not on any drugs, my husband gave me a magic dildo and its causing me to lose control!"

The officer, not buying it, simply replied "Magic dildo, my ass."''',

    '''Son:Mum i got suspended today
Mum: Why?!!
Son: It was pajama day at school today
Mum: So?!?!
Son: I sleep naked''',

    '''A dad sees his son swatting a honeybee. He says, "For that, no honey for a month. 
The next day, he sees his son killing a butterfly. He says, "For that no butter for a month." 
The next day, he sees his wife kill a cockroach. The son says, "Dad you want to tell her or should I?"''',

    '''A pregnant woman got shot 3 times and recovered, but the bullets were never found. Later she had triplets, two girls and one boy.

Many years later, the first girl came up to her mom and told about how she peed out a bullet.

The next day the second came up and the mother said, "Lemme guess, you peed out a bullet too." She was right.

The next day her young boy came up to his mom and says, "Mom, I'm so ashamed of what just happened" The mother replied, "Aw, honey, it's alright, your sisters peed out a bullet too, it's nothing to be ashamed of."

"No, that's not it" he said. "I was rubbing myself, and I think I shot the dog"''',

    '''A man walks into a library and asks for a book on suicide. The librarian replies " Fuck off, you won't bring it back!".''',

    '''A small boy asks his Dad, "Daddy, what is politics?" Dad says, "Well son, let me try to explain it this way: I'm the breadwinner of the family, so let's call me Capitalism. 
    
Your mom, she's the administrator of the money, so we'll call her the Government. We're here to take care of your needs, so we'll call you the People. 

The nanny, we'll consider her the Working Class. And your baby brother, we'll call him the Future. Now, think about that and see if that makes sense." 

So the little boy goes off to bed thinking about what Dad has said. Later that night, he hears his baby brother crying, so he gets up to check on him. 

He finds that the baby has severely soiled his diaper. The little boy goes to his parents' room and finds his mother sound asleep. 

Not wanting to wake her, he goes to the nanny's room. Finding the door locked, he peeks in the keyhole and sees his father having sex with the nanny. 

He gives up and goes back to bed. The next morning, the little boy says to his father, "Dad, I think I understand the concept of politics now." 

The father says, "Good, son, tell me in your own words what you think politics is all about." 

The little boy replies, "Well, while Capitalism is screwing the Working Class, the Government is sound asleep, the People are being ignored and the Future is in Deep Shit.''',

    '''A doctor and his wife were having a big argument at breakfast. He shouted at her, "You aren't so good in bed either!" 
    
Then stormed off to work. By mid-morning, he decided he'd better make amends and called home. "What took you so long to answer?" he asked. 

"I was in bed," she replied. "What were you doing in bed this late?" "Getting a second opinion.''',

    '''Two guys sneak into a farmer's orchard and start eating the fruit. The farmer sees them and comes out with a shotgun. 
    
"Since you guys like fruit so much go pick 100 of whatever fruit you want," said the farmer. The first guy decides to pick grapes. 

When he gets 100 he goes back to the farmer. The farmer says, "Now shove 'em all up your ass." The guy gets all 100 up his ass. 

He feels really bad, but then he starts to laugh. "Why are you laughing?" asks the farmer. And the guy replies, "My friend is out picking watermelons!''',

    '''A little boy and his grandfather are raking leaves in the yard. The little boy sees an earthworm trying to get back into its hole. 
    
He says, "Grandpa, I bet I can put that worm back in that hole." The grandfather replies, "I'll bet you five dollars you can't. 

It's too wiggly and limp to put back in that tiny hole." The little boy runs into the house and comes back out with a can of hair spray. 

He sprays the worm until it is straight and stiff as a board. The boy then proceeds to slip the dying worm back into the hole. 

The grandfather hands the little boy five dollars, grabs the hair spray and runs into the house. 

Thirty minutes later the grandfather comes back out and hands the boy another five dollars. 

The little boy says, "Grandpa, you already gave me five dollars." The grandfather replies, "I know. That's from Grandma.''',

    '''Little Johnny goes home from his first day of 1st grade with one assignment - learning the first 5 letters of the alphabet. 
    
First, he asks his mom, who is resting in bed. "Mom, what is the first letter of the alphabet?" She responds, "Shut up, I'm too tired right now."

Next, he goes to his dad, who is working on fixing the car's radiator, and asks him the same question. He says,

"Could you hand me some glue to seal 'er shut? She won't keep quiet." The boy walks away, feeling pretty good about his progress on his assignment thus far.

He finds his sister in the next room, who is watching wrestling on TV. Her response is, "HIT HER WITH THE FUCKING CHAIR! SHOVE IT UP HER ASS!"

The boy is a little surprised by her very enthusiastic response, but goes with it anyways. He goes to find his brother, who is making strange noises in his room.

He walks in and sees him watching some kind of video with VERY happy people in it. He asks his question, and the brother starts yelling.

"WHAT ARE YOU FUCKING DOING IN HERE? GO THE FUCK AWAY RIGHT NOW!" He jots it down on a slip of paper and continues on his way. 

Finally, he goes to his grandpa, who answers very softly, so softly that Johnny can barely hear it. But he does, and is finished with his assignment.

The next day at school, Johnny is called up first to recite his part of the alphabet. So, standing at the front of the class, he says to the teacher,

"Ugh, shut up, I'm too tired right now." "Excuse me?" The teacher is taken aback at his response. He continues confidently, this time addressing the whole class.

"Could you hand me some glue to seal her shut? She won't keep quiet." Now the rest of the class is staring in astonishment, and the teacher orders him outside.

As the teacher takes him there, pulling him by the hand, he shouts, "HIT HER WITH THE FUCKING CHAIR! SHOVE IT UP HER ASS!" Now, the teacher changes course and instead heads to the principals office.

Once they get there, he recites his fourth letter to the principal: "WHAT ARE YOU FUCKING DOING IN HERE? GO THE FUCK AWAY RIGHT NOW!" The principal says,

"Ok, that's it. I'm calling your parents right now. When they pick up the phone, the principal hands it to little Johnny. He says one thing: "E".'''



]

embedColors = [discord.Color.blue(), discord.Color.blurple(), discord.Color.dark_blue(), discord.Color.dark_gold(),
               discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_grey(),
               discord.Color.dark_magenta(),
               discord.Color.blue(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(),
               discord.Color.dark_teal(), discord.Color.darker_grey(), discord.Color.default(), discord.Color.gold(),
               discord.Color.green(), discord.Color.greyple(), discord.Color.light_grey(), discord.Color.magenta(),
               discord.Color.orange(), discord.Color.purple(), discord.Color.teal(),
               discord.Color.red()]


class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jokes = jokes
        self.spam = False

    @commands.command()
    async def joke(self, ctx):
        joke = random.choice(self.jokes)
        embed = discord.Embed(description=f"**{joke}**", color=random.choice(embedColors))
        embed.set_footer(text="Credit for joke goes to: https://kickasshumor.com")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(JokeCog(bot))


""""[Text To Click](https://www.youtube.com/)"
- Needs to be a full url
- Only works in embeds, duh
- This won't work in the title, footer or field titles
If you want to hyperlink a title, you can use the url kwarg"""
