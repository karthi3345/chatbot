import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from .vector_db import collection


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



def import_games():

    documents = []
    embeddings = []
    ids = []
    metadatas = []

    games_folder = Path(__file__).parent / "data"

    counter = 0


    for json_file in games_folder.glob("*.json"):

        print("Loading:", json_file.name)

        try:

            with open(
                json_file,
                "r",
                encoding="utf-8"
            ) as f:

                games = json.load(f)



            # dict format
            if isinstance(games, dict):

                games = list(
                    games.values()
                )



            for game in games:
                print(game)


                # skip invalid data
                if not isinstance(game, dict):

                    print(
                        "Skipping invalid:",
                        game
                    )

                    continue



                text = f"""
Game: {game.get('game_name','')}

Provider: {game.get('provider','')}

Category: {game.get('category','')}

RTP: {game.get('rtp','')}

Description:
{game.get('description','')}
"""


                embedding = model.encode(
                    text
                ).tolist()



                documents.append(
                    text.strip()
                )


                embeddings.append(
                    embedding
                )


                ids.append(
                    str(counter)
                )


                metadatas.append(
                    game
                )


                counter += 1



        except Exception as e:

            print(
                "Error:",
                json_file.name,
                e
            )

            continue



    if documents:

        collection.add(

            ids=ids,

            documents=documents,

            embeddings=embeddings,

            metadatas=metadatas

        )


    print(
        f"✅ Imported {len(documents)} games"
    )