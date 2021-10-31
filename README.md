# Axie Infinity Sniper Bot #axieinfinity
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R5R56SOT1)



This project helps you collect data from axie.zone about the top 100 players, and match their most used axies against the marketplace in realtime, matches that are found are then stored in Firebase Firestore. 

## Installation

### Video Tutorial

[![IMAGE ALT TEXT HERE](https://i.imgur.com/baDtWpr.png)](https://youtu.be/LijzwzcuIKo)


### Instructions

1. Create a Firebase account & Project

2. Enable Firestore

3. (optional) Enable Authentication using Google.

4. (optional) Update security rules to enable any authenticated user to read data (this setup is assuming usage with the provided Web GUI, if used within your own project tailor your security rules to the given project).

Example:
```python
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read: if (request.auth.uid != null);
    }
  }
}
```

5. Within Firebase, navigate to Project Settings > Service Accounts, select Python and click on "Generate new private key"

6. Rename the file to serviceAccountKey.json and import it into the project directory ./database/serviceAccountKey.json (this file is included in .gitignore)

7. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies from requirements.txt file.

```bash
pip3 install -r requirements.txt
```

8. Run main.py, after script finishes, your data will be loaded into two collections, leaderboards (top 100 players at the runtime, multiple documents) and on_sale (all axies matching one of the most used axies by top 100 players, including their price, which top 100 player it matches, ID, class & parts, see example json below).

####  Example JSON:

```
{
    "player_rank": 44,
    "image": "https://storage.googleapis.com/assets.axieinfinity.com/axies/7751721/axie/axie-full-transparent.png",
    "time": {
        "seconds": 1635428026,
        "nanoseconds": 751095000
    },
    "axie": {
        "class": "Bird",
        "player_mmr": "3312",
        "player_rank": 44,
        "axie_zone_score": "Excellent",
        "title": "",
        "matching_player": "#44 youtube.com de-hi games 3312 0 0%",
        "id": "7751721",
        "__typename": "Axie",
        "name": "Axie #7751721",
        "breedCount": 3,
        "battleInfo": {
            "banned": false,
            "__typename": "AxieBattleInfo"
        },
        "parts": [
            {
                "name": "Mavis",
                "specialGenes": null,
                "id": "eyes-mavis",
                "class": "Bird",
                "__typename": "AxiePart",
                "type": "Eyes"
            },
            {
                "type": "Ears",
                "specialGenes": null,
                "class": "Bird",
                "id": "ears-peace-maker",
                "__typename": "AxiePart",
                "name": "Peace Maker"
            },
            {
                "name": "Pigeon Post",
                "__typename": "AxiePart",
                "specialGenes": null,
                "id": "back-pigeon-post",
                "class": "Bird",
                "type": "Back"
            },
            {
                "specialGenes": null,
                "type": "Mouth",
                "__typename": "AxiePart",
                "class": "Bug",
                "id": "mouth-cute-bunny",
                "name": "Cute Bunny"
            },
            {
                "type": "Horn",
                "specialGenes": null,
                "class": "Bird",
                "name": "Eggshell",
                "id": "horn-eggshell",
                "__typename": "AxiePart"
            },
            {
                "id": "tail-post-fight",
                "class": "Bird",
                "specialGenes": null,
                "type": "Tail",
                "name": "Post Fight",
                "__typename": "AxiePart"
            }
        ],
        "stage": 4,
        "image": "https://storage.googleapis.com/assets.axieinfinity.com/axies/7751721/axie/axie-full-transparent.png",
        "player_url": "https://axie.zone/profile?ron_addr=0x1b246e446336f55b4150294ccd39693fb4a8aa9b",
        "matching_axie_name": "obasan",
        "auction": {
            "currentPrice": "40000000000000000",
            "__typename": "Auction",
            "currentPriceUSD": "165.82"
        }
    },
    "currentPriceUSD": 165.82,
    "id": "7751721",
    "class": "Bird"
}
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
