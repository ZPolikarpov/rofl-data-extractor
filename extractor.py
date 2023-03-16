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
    if not os.path.exists(target_path):
        return
    with open(os.path.join(target_path, target_file)) as f:
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

    replay_files = [os.path.join(root_dir, f) for f in os.listdir(root_dir)]

    return replay_files

if __name__ == "__main__":

    gc = gspread.service_account()

    # root_dir = "D:\\LoL Replays\\11.21\\Replays\\"
    root_dir = "C:\\Users\\polik\\Desktop\\Visual Studio Code\\Replays"
    json_dir = "C:\\Users\\polik\\Desktop\\Visual Studio Code\\Replays in JSON"
    xlsx_dir = "C:\\Users\\polik\\Desktop\\Visual Studio Code\\Replays in Excel"
    

    i = 0
    j = 0


    replay_files = get_replay_file_paths(root_dir)
    for fname in replay_files:
        game_id = os.path.basename(fname).split(".")[0].split("-")[1]
        org, metadata = get_metadata(fname)
        write_json(json_dir, str(i)+".json", metadata)
        print(fname, i)
        i+= 1

    json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir)]
    json_to_excel(xlsx_dir, json_files)

    sh = gc.open("Bot Test")

    print(sh.sheet1.get('A1'))
