import json
import os

def get_metadata(filename):
    with open(filename, "rb") as f:
        # Magic
        magic = str(f.read(4), encoding="utf-8")

        # Length fields
        lengths_buffer = []
        f.seek(262)
        length_field_buffer = f.read(26)
        metadata_offset = length_field_buffer[6:10]
        metadata_length = length_field_buffer[10:14]

        metadata_offset = int.from_bytes(metadata_offset, byteorder='little')
        metadata_length = int.from_bytes(metadata_length, byteorder='little')

        # Metadata
        f.seek(metadata_offset)
        replay_metadata = f.read(metadata_length)
        replay_metadata = json.loads(str(replay_metadata, encoding="utf-8"))
        stats_json = json.loads(replay_metadata["statsJson"])

        #champs = [s["SKIN"] for s in stats_json]

        return replay_metadata, stats_json

def insert_game(cur, org, metadata, game_id):
    surrender = any([m["GAME_ENDED_IN_SURRENDER"] for m in metadata])
    surrender = 1 if surrender else 0
    early_surrender = any([m["GAME_ENDED_IN_EARLY_SURRENDER"] for m in metadata])
    early_surrender = 1 if early_surrender else 0

    cur.execute(f"""INSERT INTO games VALUES(
        {game_id},
        {org["gameLength"]},
        {org["gameLength"] / (1000 * 60)},
        {surrender},
        {early_surrender})""")

    for i, player in enumerate(metadata):
        player_id = player["ID"]
        champ = player["SKIN"]
        win = player["WIN"]
        team = player["TEAM"]
        team_position = POSITIONS[i % 5]
        name = player["NAME"]
        assists = player["ASSISTS"]
        kills = player["CHAMPIONS_KILLED"]
        exp = player["EXP"]
        early_surrender = player["GAME_ENDED_IN_EARLY_SURRENDER"]
        surrender = player["GAME_ENDED_IN_SURRENDER"]
        gold_earned = player["GOLD_EARNED"]
        gold_spent = player["GOLD_SPENT"]
        level = player["LEVEL"]
        longest_time_spent_living = player["LONGEST_TIME_SPENT_LIVING"]
        cs = player["MINIONS_KILLED"] + player["NEUTRAL_MINIONS_KILLED"]
        deaths = player["NUM_DEATHS"]
        dmg_dealt = player["TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"]
        vision_score = player["VISION_SCORE"]
        
        cur.execute(f"""INSERT INTO playerGame VALUES(
            {player_id},
            '{game_id}',
            '{champ}',
            {1 if win == "Win" else 0},
            '{team}',
            '{team_position}',
            '{name}',
            {assists},
            {kills},
            {exp},
            {1 if early_surrender == "1" else 0},
            {1 if surrender == "1" else 0},
            {gold_earned},
            {gold_spent},
            {level},
            {longest_time_spent_living},
            {cs},
            {deaths},
            {dmg_dealt},
            {vision_score})""")
        
def write_json(target_path, target_file, data):
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception as e:
            print(e)
            raise
    with open(os.path.join(target_path, target_file), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # root_dir = "D:\\LoL Replays\\11.21\\Replays\\"
    root_dir = "C:\\Users\\polik\\Desktop\\Visual Studio Code\\Replays"
    json_dir = "C:\\Users\\polik\\Desktop\\Visual Studio Code\\Replays in JSON"
    
    counts = {}

    i = 0
    total = len(os.listdir(root_dir))

    """
    for root_dir in root_dirs[0:]:
        files = os.listdir(root_dir)[0:]
        for f in files:
            game_id = f.split(".")[0].split("-")[1]
            fname = os.path.join(root_dir, f)
            for c in get_champs(fname):
                if not c in counts:
                    counts[c] = 0
                counts[c] += 1
            print(f'{i}/{total}', i)
            i += 1
        counts = {k: v
                for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}
    """

    files = [os.path.join(root_dir, f) for f in os.listdir(root_dir)]
    print(files)
    for fname in files:
        game_id = os.path.basename(fname).split(".")[0].split("-")[1]
        org, metadata = get_metadata(fname)
        write_json(json_dir, str(i)+".json", metadata)
        print(fname, i)
        i+= 1


    print(counts)