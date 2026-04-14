"""
Fact database for the AI Hallucination Quiz.

Each entry is a statement that is either REAL (true) or HALLUCINATED (false
but plausible — the kind of thing an AI might confidently make up).

Organized by category. Every entry has:
  - "statement": The claim presented to the player
  - "answer": True if real, False if hallucinated
  - "explanation": Why it's real or how the hallucination works
  - "category": Topic area
"""

FACTS = [
    # --- History ---
    {
        "statement": "Napoleon Bonaparte was once attacked by a horde of rabbits during a hunting party.",
        "answer": True,
        "explanation": "In 1807, Napoleon organized a rabbit hunt. Hundreds of rabbits were released but instead of fleeing, they charged at Napoleon and his party, forcing him to retreat to his carriage.",
        "category": "History",
    },
    {
        "statement": "The Great Wall of China is visible from the Moon with the naked eye.",
        "answer": False,
        "explanation": "This is a common myth. The Great Wall is far too narrow to be seen from the Moon. Even from low Earth orbit, it's extremely difficult to spot without aid. Astronauts have confirmed this.",
        "category": "History",
    },
    {
        "statement": "Oxford University is older than the Aztec Empire.",
        "answer": True,
        "explanation": "Teaching at Oxford began around 1096, while the Aztec Empire was founded in 1428. Oxford predates it by over 300 years.",
        "category": "History",
    },
    {
        "statement": "Cleopatra lived closer in time to the first Moon landing than to the construction of the Great Pyramid.",
        "answer": True,
        "explanation": "The Great Pyramid was built around 2560 BC. Cleopatra lived around 30 BC. The Moon landing was 1969 AD. She was about 2530 years after the pyramid and about 2000 years before the Moon landing.",
        "category": "History",
    },
    {
        "statement": "Benjamin Franklin proposed the turkey as the national bird of the United States in an official letter to Congress.",
        "answer": False,
        "explanation": "Franklin never formally proposed the turkey to Congress. In a private letter to his daughter, he expressed that the bald eagle had poor moral character and jokingly praised the turkey, but he never made an official proposal.",
        "category": "History",
    },
    {
        "statement": "During WWII, the US military developed a plan to attach incendiary bombs to bats.",
        "answer": True,
        "explanation": "Project X-Ray was a real WWII plan to use Mexican free-tailed bats carrying tiny napalm bombs. The idea was that they'd roost in Japanese buildings and start fires. It was tested but never deployed.",
        "category": "History",
    },
    {
        "statement": "Albert Einstein failed his university entrance exam on his first attempt.",
        "answer": True,
        "explanation": "In 1895, Einstein took the entrance exam for the Swiss Federal Polytechnic in Zurich and failed the general portion, though he excelled in math and physics. He enrolled at a different school first, then was admitted the next year.",
        "category": "History",
    },
    {
        "statement": "Vikings wore horned helmets in battle.",
        "answer": False,
        "explanation": "There is no historical evidence that Vikings wore horned helmets. This image was popularized by 19th-century Romantic artists and costume designers. Actual Viking helmets were simple rounded caps, sometimes with nose guards.",
        "category": "History",
    },

    # --- Science ---
    {
        "statement": "Octopuses have three hearts and blue blood.",
        "answer": True,
        "explanation": "Octopuses have two branchial hearts that pump blood through the gills and one systemic heart for the rest of the body. Their blood is blue because it uses copper-based hemocyanin instead of iron-based hemoglobin.",
        "category": "Science",
    },
    {
        "statement": "Glass is actually a very slow-moving liquid, which is why old windows are thicker at the bottom.",
        "answer": False,
        "explanation": "Glass is an amorphous solid, not a liquid. Old windows are thicker at the bottom because of how they were manufactured — crown glass production created uneven panes, and glaziers placed the thicker edge at the bottom for stability.",
        "category": "Science",
    },
    {
        "statement": "A teaspoon of neutron star material would weigh about 6 billion tons.",
        "answer": True,
        "explanation": "Neutron stars are incredibly dense. Their matter is compressed so tightly that a teaspoonful would indeed weigh around 6 billion tons on Earth.",
        "category": "Science",
    },
    {
        "statement": "Humans use only 10% of their brains.",
        "answer": False,
        "explanation": "This is a persistent myth. Brain imaging shows that virtually all parts of the brain are active, just not all at the same time. Even during sleep, more than 10% of the brain is active.",
        "category": "Science",
    },
    {
        "statement": "There are more possible iterations of a game of chess than there are atoms in the observable universe.",
        "answer": True,
        "explanation": "The Shannon number estimates about 10^120 possible chess games, while the observable universe contains roughly 10^80 atoms. Chess possibilities vastly outnumber atoms.",
        "category": "Science",
    },
    {
        "statement": "Lightning never strikes the same place twice.",
        "answer": False,
        "explanation": "Lightning frequently strikes the same place, especially tall or isolated structures. The Empire State Building gets struck about 20-25 times per year.",
        "category": "Science",
    },
    {
        "statement": "Tardigrades can survive in the vacuum of space.",
        "answer": True,
        "explanation": "In 2007, tardigrades were exposed to the vacuum and radiation of space aboard the FOTON-M3 mission. Many survived, making them one of the most resilient known organisms.",
        "category": "Science",
    },
    {
        "statement": "Water conducts electricity well because of the hydrogen and oxygen molecules.",
        "answer": False,
        "explanation": "Pure water is actually a poor conductor of electricity. It's the dissolved ions (salts, minerals) in water that make it conductive. Ultra-pure water is nearly an insulator.",
        "category": "Science",
    },

    # --- Technology ---
    {
        "statement": "The first computer bug was an actual bug — a moth found in the Harvard Mark II computer.",
        "answer": True,
        "explanation": "In 1947, operators found a moth trapped in a relay of the Harvard Mark II computer. Grace Hopper's team taped it in the logbook with the note 'First actual case of bug being found.' The term 'bug' predated this, but it popularized it.",
        "category": "Technology",
    },
    {
        "statement": "The QWERTY keyboard layout was designed to slow typists down to prevent typewriter jams.",
        "answer": False,
        "explanation": "While commonly repeated, this is an oversimplification. QWERTY was designed to separate frequently used letter pairs to reduce jamming, but this doesn't necessarily slow typing — it was about mechanical reliability, not speed reduction.",
        "category": "Technology",
    },
    {
        "statement": "The entire text of Wikipedia can fit on a 22 GB file when compressed.",
        "answer": True,
        "explanation": "The text content of English Wikipedia (without images or metadata) compresses to roughly 22 GB. The full database dump with all history and metadata is much larger.",
        "category": "Technology",
    },
    {
        "statement": "The average smartphone today has more computing power than all of NASA had during the Apollo 11 Moon landing.",
        "answer": True,
        "explanation": "The Apollo Guidance Computer had about 74 KB of memory and ran at 0.043 MHz. A modern smartphone has billions of times more processing power and memory.",
        "category": "Technology",
    },
    {
        "statement": "The term 'artificial intelligence' was first coined by Alan Turing in his 1950 paper.",
        "answer": False,
        "explanation": "The term was coined by John McCarthy in 1956 for the Dartmouth Conference. Turing's 1950 paper introduced the concept of the 'imitation game' (Turing Test) but didn't use the phrase 'artificial intelligence.'",
        "category": "Technology",
    },
    {
        "statement": "The first webcam was created to monitor a coffee pot at Cambridge University.",
        "answer": True,
        "explanation": "In 1991, researchers at Cambridge set up a camera pointed at the Trojan Room coffee pot so they could check if coffee was ready without walking to the room. It went online in 1993.",
        "category": "Technology",
    },

    # --- Geography & Nature ---
    {
        "statement": "Honey never spoils. Edible honey has been found in Egyptian tombs thousands of years old.",
        "answer": True,
        "explanation": "Honey's low moisture, acidity, and natural hydrogen peroxide make it inhospitable to bacteria. Archaeologists have found 3000-year-old honey in Egyptian tombs that was still edible.",
        "category": "Geography & Nature",
    },
    {
        "statement": "The Amazon River is the longest river in the world.",
        "answer": False,
        "explanation": "The Nile River, at about 6,650 km, is generally considered the longest river. The Amazon is the largest by volume and drainage area, and some measurements dispute the ranking, but the Nile traditionally holds the title.",
        "category": "Geography & Nature",
    },
    {
        "statement": "A group of flamingos is called a 'flamboyance.'",
        "answer": True,
        "explanation": "The collective noun for flamingos is indeed a 'flamboyance,' fitting their vibrant pink coloring and dramatic group behavior.",
        "category": "Geography & Nature",
    },
    {
        "statement": "Goldfish have a 3-second memory.",
        "answer": False,
        "explanation": "Goldfish can actually remember things for months. Studies have shown they can be trained to navigate mazes, respond to signals, and remember feeding times over long periods.",
        "category": "Geography & Nature",
    },
    {
        "statement": "There is a lake in Australia that is naturally bright pink.",
        "answer": True,
        "explanation": "Lake Hillier on Middle Island in Western Australia is bright pink. The exact cause isn't fully confirmed but is likely due to the algae Dunaliella salina and halobacteria.",
        "category": "Geography & Nature",
    },
    {
        "statement": "Bananas are berries, but strawberries are not.",
        "answer": True,
        "explanation": "Botanically, a berry develops from a single ovary and has seeds embedded in the flesh. Bananas qualify. Strawberries are 'accessory fruits' — the fleshy part comes from the receptacle, not the ovary.",
        "category": "Geography & Nature",
    },

    # --- Literature & Culture ---
    {
        "statement": "Dr. Seuss wrote 'Green Eggs and Ham' after being bet he couldn't write a book using 50 or fewer distinct words.",
        "answer": True,
        "explanation": "Publisher Bennett Cerf bet Dr. Seuss (Theodor Geisel) $50 that he couldn't write a book with 50 or fewer different words. Seuss won the bet — the book uses exactly 50 unique words.",
        "category": "Literature & Culture",
    },
    {
        "statement": "Shakespeare invented the word 'assassination.'",
        "answer": False,
        "explanation": "While Shakespeare coined many English words, 'assassination' appeared in print before his use of it in Macbeth. He did popularize many words, but this specific attribution is incorrect.",
        "category": "Literature & Culture",
    },
    {
        "statement": "The word 'robot' comes from a Czech play written in 1920.",
        "answer": True,
        "explanation": "The word 'robot' was introduced in Karel Capek's 1920 play 'R.U.R.' (Rossum's Universal Robots). It derives from the Czech word 'robota,' meaning forced labor.",
        "category": "Literature & Culture",
    },
    {
        "statement": "The Mona Lisa has no eyebrows because it was fashionable to shave them in Renaissance Italy.",
        "answer": False,
        "explanation": "While some claim this fashion explanation, high-resolution scans in 2007 revealed that da Vinci originally painted eyebrows and eyelashes, but they gradually disappeared over time due to cleaning and fading.",
        "category": "Literature & Culture",
    },
    {
        "statement": "The shortest war in history lasted 38 minutes, between Britain and Zanzibar.",
        "answer": True,
        "explanation": "The Anglo-Zanzibar War of August 27, 1896, lasted between 38 and 45 minutes, making it the shortest recorded war in history.",
        "category": "Literature & Culture",
    },
    {
        "statement": "Fortune cookies were invented in China.",
        "answer": False,
        "explanation": "Fortune cookies were likely invented in California by Japanese-American immigrants in the early 1900s. They are largely unknown in China and are an American creation associated with Chinese-American restaurants.",
        "category": "Literature & Culture",
    },

    # --- AI-specific hallucination traps ---
    {
        "statement": "GPT-3 was trained on a dataset that included the complete text of every book in the Library of Congress.",
        "answer": False,
        "explanation": "This is the kind of plausible-sounding claim an AI might generate. GPT-3 was trained on internet text (Common Crawl, WebText2, books corpora, Wikipedia), not the Library of Congress collection specifically.",
        "category": "AI & Computing",
    },
    {
        "statement": "The term 'hallucination' in AI refers to models generating confident but factually incorrect information.",
        "answer": True,
        "explanation": "AI hallucination is the widely used term for when language models produce statements that sound plausible and confident but are factually wrong — exactly what this quiz is about!",
        "category": "AI & Computing",
    },
    {
        "statement": "In 2016, Microsoft's chatbot Tay was taken offline within 24 hours after it began posting offensive tweets.",
        "answer": True,
        "explanation": "Microsoft launched Tay on Twitter in March 2016. Users quickly manipulated it into posting inflammatory content, and Microsoft took it offline within about 16 hours.",
        "category": "AI & Computing",
    },
    {
        "statement": "Google's DeepMind AI 'AlphaFold' solved the complete protein folding problem in 2020, predicting all possible protein structures.",
        "answer": False,
        "explanation": "AlphaFold made a major breakthrough in protein structure prediction in 2020, but it did not solve the 'complete' problem. It predicts structures with high accuracy for many proteins, but challenges remain for protein complexes, dynamics, and certain categories.",
        "category": "AI & Computing",
    },
    {
        "statement": "The first neural network was built in 1943 as a computational model by McCulloch and Pitts.",
        "answer": True,
        "explanation": "Warren McCulloch and Walter Pitts published 'A Logical Calculus of Ideas Immanent in Nervous Activity' in 1943, creating the first mathematical model of a neural network.",
        "category": "AI & Computing",
    },
    {
        "statement": "IBM's Watson won Jeopardy! in 2011 by accessing the internet during the game.",
        "answer": False,
        "explanation": "Watson was not connected to the internet during its Jeopardy! matches. It relied on 200 million pages of content stored locally, including encyclopedias, dictionaries, and other reference materials loaded before the game.",
        "category": "AI & Computing",
    },
]

# Pre-compute category list
CATEGORIES = sorted(set(f["category"] for f in FACTS))
