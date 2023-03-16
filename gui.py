import PySimpleGUI as sg
import extractor as ex

def settings_window():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.T("")], 
                [sg.Text("Choose your replay folder: "), sg.Input(key="-IN2-", enable_events=True), sg.FolderBrowse(key="-IN-")],
                [sg.Button("Submit Config"), sg.Button("Cancel")] ]

    # Create the Window
    window = sg.Window('Config Edit', layout, finalize=True)

    return window

def main_window(configPath, configFileName):
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    config = ex.read_json(configPath, configFileName)
    layout = [  [sg.T("")], 
                [sg.Text("Replay folder: "), sg.Text(config["replay_path"])],
                [sg.Button("Change Settings")],
                [sg.Button("Exit")] ]

    # Create the Window
    window = sg.Window('Main Window', layout, finalize=True)
    
    return window

if __name__ == "__main__":
    window1, window2 = main_window("data\\Configs", "defaultConfig.json"), None

    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel':
            window.close()
            if window == window2:  
                window1 = main_window("data\\Configs", "defaultConfig.json")     
                window2 = None          # if closing win 2, mark as closed
            elif window == window1:     # if closing win 1, exit program
                break

        elif event == 'Change Settings' and not window2:
            window.close()
            window1 = None
            window2 = settings_window()

        if event == "-IN2-":
            print(values["-IN2-"])

        if event == "Submit Config":
            ex.write_json("data/Configs", "defaultConfig.json", {"replay_path": values["-IN2-"]})
            window.close()
            window1 = main_window("data\\Configs", "defaultConfig.json")
            window2 = None
