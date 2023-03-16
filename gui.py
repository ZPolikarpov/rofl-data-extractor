import PySimpleGUI as sg
import extractor as ex

def settings_window():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.T("")], 
                [sg.Text("Choose your replay folder: "), sg.Input(key="inputReplayPath"), sg.FolderBrowse(key="browseReplayPath")],
                [sg.Text("Choose your json folder: "), sg.Input(key="inputJsonPath"), sg.FolderBrowse(key="browseJsonPath")],
                [sg.Button("Submit Config"), sg.Button("Cancel")] ]

    # Create the Window
    window = sg.Window('Config Edit', layout, finalize=True)

    return window

def main_window(config):
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    
    layout = [  [sg.T("")], 
                [sg.Text("Replay folder: "), sg.Text(config["replay_path"])],
                [sg.Text("Json folder: "), sg.Text(config["json_path"])],
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
                window1, window2 = main_window(config), None
            elif window == window1:     # if closing win 1, exit program
                break

        elif event == 'Change Settings' and not window2:
            window.close()
            window1, window2 = None, settings_window()

        if event == "Submit Config":
            ex.write_json(configPath, configFileName, {"replay_path": values["inputReplayPath"], "json_path": values["inputJsonPath"]})
            window.close()
            window1, window2 = main_window(config), None

        if event == "Rofl2Json":
            ex.onRofl2Json(config["replay_path"], config["json_path"])
