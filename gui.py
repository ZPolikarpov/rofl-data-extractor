import PySimpleGUI as sg
import extractor as ex

def settings_window(config):
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.T("")], 
                [sg.Text("Your Google Sheet URL: "), sg.Input(config["gsheet_link"], key="inputGsheetURL")],
                [sg.Text("Choose your replay folder: "), sg.Input(config["replay_path"], key="inputReplayPath"), sg.FolderBrowse(key="browseReplayPath")],
                [sg.Text("Choose your json folder: "), sg.Input(config["json_path"], key="inputJsonPath"), sg.FolderBrowse(key="browseJsonPath")],
                [sg.T("Player Names")],
                [sg.Text("Top: "), sg.Input(config["player_names"]["top"], key="inputTopName")],
                [sg.Text("Jungle: "), sg.Input(config["player_names"]["jng"], key="inputJungleName")],
                [sg.Text("Mid: "), sg.Input(config["player_names"]["mid"], key="inputMidName")],
                [sg.Text("Bottom: "), sg.Input(config["player_names"]["bot"], key="inputBottomName")],
                [sg.Text("Support: "), sg.Input(config["player_names"]["sup"], key="inputSupportName")],
                [sg.Button("Submit Config"), sg.Button("Cancel")] ]

    # Create the Window
    window = sg.Window('Config Edit', layout, finalize=True)

    return window

def main_window(config):
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    
    layout = [  [sg.T("")], 
                [sg.Text("Google Sheet URL: "), sg.Text(config["gsheet_link"])],
                [sg.Text("Replay folder: "), sg.Text(config["replay_path"])],
                [sg.Text("Json folder: "), sg.Text(config["json_path"])],
                [sg.T("Player Names")], 
                [sg.Text("Top: "), sg.Text(config["player_names"]["top"])],
                [sg.Text("Jungle: "), sg.Text(config["player_names"]["jng"])],
                [sg.Text("Mid: "), sg.Text(config["player_names"]["mid"])],
                [sg.Text("Bottom: "), sg.Text(config["player_names"]["bot"])],
                [sg.Text("Support: "), sg.Text(config["player_names"]["sup"])],
                [sg.Button("Change Settings")],
                [sg.Button("Rofl2Json"), sg.Button("Exit")] ]

    # Create the Window
    window = sg.Window('Main Window', layout, finalize=True)
    
    return window

if __name__ == "__main__":
    configPath, configFileName = "data\\Configs", "defaultConfig.json"
    config = ex.read_json(configPath, configFileName)
    window1, window2 = main_window(config), None

    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel':
            window.close()
            if window == window2:
                config = ex.read_json(configPath, configFileName)
                window1, window2 = main_window(config), None
            elif window == window1:     # if closing win 1, exit program
                break

        elif event == 'Change Settings' and not window2:
            window.close()
            config = ex.read_json(configPath, configFileName)
            window1, window2 = None, settings_window(config)

        if event == "Submit Config":
            ex.write_json(configPath, configFileName,
                {
                    "replay_path": values["inputReplayPath"], 
                    "json_path": values["inputJsonPath"],
                    "gsheet_link": values["inputGsheetURL"],
                    "player_names": {
                        "top": values["inputTopName"],
                        "jng": values["inputJungleName"],
                        "mid": values["inputMidName"],
                        "bot": values["inputBottomName"],
                        "sup": values["inputSupportName"]
                    }
                }
            )
            window.close()
            config = ex.read_json(configPath, configFileName)
            window1, window2 = main_window(config), None


        if event == "Rofl2Json":
            ex.onRofl2Json(config["replay_path"], config["json_path"])
            gc = ex.initGspread()
            ex.pushGameStatsToSheet(gc, config)
