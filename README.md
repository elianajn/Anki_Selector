# Anki_Selector


## Original Workflow
1. Create a personal OpenAI account, and obtain an API key.
2. In Anki, export the deck you wish to tag as an anki_deck.apkg.
3. In Anki, export the deck using the Notes as plain text funcion, and select to include a unique identifier: `anki.txt`
4. `$ python embed_anki_deck.py` <anki.txt> Returns: anki_embeddings.csv This will create the embeddings of your deck: These are required for a first pass crude search of your deck to minimize API costs.
5. `$ python make_learning_objectives.py` <learning_guide.pdf> or <folder_of_pdfs> Returns: anki_learning_objectives.csv Create a list of summary learning objectives, the filename of the pdf will be the tag for the learning objective. Generally one lecture guide results in 10-30 questions.
6. `$ python select_cards.py` <deck_embeding> <learning_objectives> Returns: anki_cards.csv This will create a list of cards from your deck scoring them on their relevance to each learning objective.
7. `$ python tag_deck.py` <anki_cards.csv> <anki_deck.apkg> Will tag the deck, and return the original deck apkg file.
8. Import into Anki and enjoy!