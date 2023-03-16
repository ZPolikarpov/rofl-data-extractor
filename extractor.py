import json
import os
import pandas as pd
import gspread

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
        
def write_json(target_path, target_file, data):
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception as e:
            print(e)
            raise
    with open(os.path.join(target_path, target_file), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_json(target_path, target_file):
    if not os.path.exists(os.path.join(target_path, target_file)):
        return
    with open(os.path.join(target_path, target_file), 'r', encoding='utf-8') as f:
        return json.load(f)

def json_to_excel(excel_path, json_files):
    j = 0
    for fname in json_files:
        with open(fname) as json_file:
            df = pd.read_json(json_file)
            df.to_excel(excel_path + "\\" + str(j) + '.xlsx')
        j+= 1

def get_replay_file_paths(replay_dir):
    counts = {}

    i = 0
    
    total = len(os.listdir(replay_dir))

    """
    for replay_dir in replay_dirs[0:]:
        files = os.listdir(replay_dir)[0:]
        for f in files:
            game_id = f.split(".")[0].split("-")[1]
            fname = os.path.join(replay_dir, f)
            for c in get_champs(fname):
                if not c in counts:
                    counts[c] = 0
                counts[c] += 1
            print(f'{i}/{total}', i)
            i += 1
        counts = {k: v
                for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}
    """

    replay_files = [os.path.join(replay_dir, f) for f in os.listdir(replay_dir)]

    return replay_files

def rofl_to_json(json_dir, replay_files):
    i = 0
    for fname in replay_files:
        game_id = os.path.basename(fname).split(".")[0].split("-")[1]
        org, metadata = get_metadata(fname)
        write_json(json_dir, str(i)+".json", metadata)
        i+= 1

def onRofl2Json(root_dir, json_dir):
    replay_files = get_replay_file_paths(root_dir)
    rofl_to_json(json_dir, replay_files)

def initGspread():
    return gspread.service_account()

def pushGameStatsToSheet(gspreadAccount, config):
    replay_json = read_json(config["json_path"], "0.json")
    sheet = gspreadAccount.open_by_url(config["gsheet_link"])
    worksheetTop = sheet.worksheet(config["player_names"]["top"])
    worksheetJungle = sheet.worksheet(config["player_names"]["jng"])
    worksheetMid = sheet.worksheet(config["player_names"]["mid"])
    worksheetBottom = sheet.worksheet(config["player_names"]["bot"])
    worksheetSupport = sheet.worksheet(config["player_names"]["sup"])
    insertPlayerStats(worksheetTop, config["player_names"]["top"], replay_json)
    insertPlayerStats(worksheetJungle, config["player_names"]["jng"], replay_json)
    insertPlayerStats(worksheetMid, config["player_names"]["mid"], replay_json)
    insertPlayerStats(worksheetBottom, config["player_names"]["bot"], replay_json)
    insertPlayerStats(worksheetSupport, config["player_names"]["sup"], replay_json)



def insertPlayerStats(worksheet, player_name, replay_json):

    for player in replay_json:
        if player["NAME"] == player_name:
            champ = player["SKIN"]
            kills = player["CHAMPIONS_KILLED"]
            deaths = player["NUM_DEATHS"]
            assists = player["ASSISTS"]
            damage_dealt = player["TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"]
            damage_taken = player["TOTAL_DAMAGE_TAKEN"]
            wards_placed = player["WARD_PLACED"]
            wards_destroyed = player["WARD_KILLED"]
            control_wards = player["VISION_WARDS_BOUGHT_IN_GAME"]
            gold_earned = player["GOLD_EARNED"]
            cs = player["MINIONS_KILLED"] + player["NEUTRAL_MINIONS_KILLED"]
            
    dataframe = pd.DataFrame(worksheet.get_all_values())
    rowToFill = findFirstEmptyCellInColumn(dataframe, 3, 23)
    dataframe.iloc[rowToFill, 3] = champ
    dataframe.iloc[rowToFill, 4] = kills
    dataframe.iloc[rowToFill, 5] = deaths
    dataframe.iloc[rowToFill, 6] = assists
    dataframe.iloc[rowToFill, 9] = damage_dealt
    dataframe.iloc[rowToFill, 11] = damage_taken
    dataframe.iloc[rowToFill, 12] = wards_placed
    dataframe.iloc[rowToFill, 13] = wards_destroyed
    dataframe.iloc[rowToFill, 14] = control_wards
    dataframe.iloc[rowToFill, 15] = gold_earned
    dataframe.iloc[rowToFill, 16] = cs

    worksheet.update(dataframe.values.tolist())

def findFirstEmptyCellInColumn(dataframe, column, startRow):
    currentRow = startRow
    print(dataframe)
    print(dataframe.loc[currentRow][column])
    while True:
        print(currentRow, dataframe.iloc[currentRow][column])
        if dataframe.iloc[currentRow][column] == "":
            return currentRow
        currentRow+= 1


if __name__ == "__main__":

    gc = gspread.service_account()
    sh = gc.open("Bot Test")

    print(sh.sheet1.get('A1'))

    # root_dir = "D:\\LoL Replays\\11.21\\Replays\\"
    root_dir = "C:\\Users\\polik\\Desktop\\Visual Studio Code\\Replays"
    json_dir = "C:\\Users\\polik\\Desktop\\Visual Studio Code\\Replays in JSON"
    xlsx_dir = "C:\\Users\\polik\\Desktop\\Visual Studio Code\\Replays in Excel"
    
    j = 0


    replay_files = get_replay_file_paths(root_dir)
    rofl_to_json(json_dir, replay_files)

    # json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir)]
    # json_to_excel(xlsx_dir, json_files)

