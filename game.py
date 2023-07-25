import customtkinter
import csv
import traceback
import tkinter as tk

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("900x480")
app.title("ExMo Game App")

def focus_on_input(inp):
    error_label.pack_forget()

def refresh_leaderboard(sorted_entries):
    for i in range(len(sorted_entries)):
        line = str(i+1) + ". " + '{:15.15}'.format(sorted_entries[i][0])  + " : " + '{:4.4}'.format(str(sorted_entries[i][7]))
        if (i < 5):
            name_labels[i].configure(text=line)

def read_entries():
    entries = []
    with open('entries.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            entry = []
            for i,value in  enumerate(row):
                if i == 0 or i == 3:
                    entry.append(value)
                else:
                    entry.append(float(value))
            entries.append(entry)
    return entries

def submit_callback():
    length = length.get().strip()
    name = name_textbox.get().strip()
    time = time_textbox.get().strip()
    
    if (name == "") or (time == ""):
        error_label.configure(text="Invalid values in entry")
        error_label.pack(pady=2, padx=0)
    else :
        error_label.pack_forget()

        try:
            time = float(time)
            distance = routes[route_name]
            utility_of_route = distance / route_sum

            entries = read_entries()
            entries.append([name, time, 0, route_name, distance, utility_of_route, 0, 0, 0])

            time_sum = sum([value[1] for value in entries])

            for entry in entries:
                entry[2] = entry[1]/time_sum
                entry[6] = entry[2]/entry[5]
                entry[7] = 1/entry[6]

            sorted_entries = sorted(entries, key = lambda x: x[7], reverse=True)
            ranks = [sorted_entries.index(x) for x in entries]

            for i in range(len(entries)):
                entries[i][8] = ranks[i] + 1
            
            with open('entries.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name","Time","Utility of time","Route","Route Distance","Utility of route","Incorporated utility 1","IU 2","rank"])
                writer.writerows(entries)

            refresh_leaderboard(sorted_entries)

            name_textbox.delete(0, customtkinter.END)
            time_textbox.delete(0, customtkinter.END)

        except Exception as e:
            traceback.print_exc()
            error_label.configure(text="Error saving entry")
            error_label.pack(pady=2, padx=0)


right_frame = customtkinter.CTkFrame(master=app)
right_frame.pack(pady=20, padx=20, fill="both", expand=True, side=customtkinter.RIGHT)

left_heading_label = customtkinter.CTkLabel(master=right_frame, justify=customtkinter.CENTER, text="NEW ENTRY", font=customtkinter.CTkFont(size=20, weight="bold"))
left_heading_label.pack(pady=10, padx=10)

name_label = customtkinter.CTkLabel(master=right_frame, width=300, text="Enter Name")
name_label.pack(pady=2, padx=0, anchor="w")

name_textbox = customtkinter.CTkEntry(master=right_frame, width=300, height=40)
name_textbox.pack(pady=10, padx=10)
name_textbox.bind("<1>", focus_on_input)

# select_route_label = customtkinter.CTkLabel(master=right_frame, width=300, text="Select Route")
# select_route_label.pack(pady=2, padx=0, anchor="w")

# routes = dict()
# with open('routes.csv', newline='') as f:
#     reader = csv.reader(f)
#     next(reader)
#     for row in reader:
#         routes[row[0]] = float(row[1])
# route_sum = sum(routes.values())
# route_option_selector = customtkinter.CTkComboBox(right_frame, width=300, height=40, values=list(routes.keys()))
# route_option_selector.pack(pady=10, padx=10)
# route_option_selector.bind("<1>", focus_on_input)

name_label = customtkinter.CTkLabel(master=right_frame, width=300, text="Enter Length")
name_label.pack(pady=2, padx=0, anchor="w")

name_textbox = customtkinter.CTkEntry(master=right_frame, width=300, height=40)
name_textbox.pack(pady=10, padx=10)
name_textbox.bind("<1>", focus_on_input)

time_label = customtkinter.CTkLabel(master=right_frame, width=300, text="Enter Time")
time_label.pack(pady=2, padx=0, anchor="w")

time_textbox = customtkinter.CTkEntry(master=right_frame, width=300, height=40)
time_textbox.pack(pady=10, padx=10)
time_textbox.bind("<1>", focus_on_input)

submit_button = customtkinter.CTkButton(master=right_frame,  height=40, command=submit_callback, text="Submit")
submit_button.pack(pady=10, padx=10)

error_label = customtkinter.CTkLabel(master=right_frame, width=300, text_color="red", font=customtkinter.CTkFont(size=15, weight="bold"))
error_label.pack_forget()

left_frame = customtkinter.CTkFrame(master=app)
left_frame.pack(pady=20, padx=20, fill="both", expand=True, side=customtkinter.LEFT)

right_heading_label = customtkinter.CTkLabel(master=left_frame, justify=customtkinter.CENTER, text="Leaderboard", font=customtkinter.CTkFont(size=20, weight="bold"))
right_heading_label.pack(pady=10, padx=10)

leaderboard_container = customtkinter.CTkFrame(master=left_frame)
leaderboard_container.pack(pady=20, padx=20, fill="both", expand=True)

name_labels = []
for i in range(5):
    name_label = customtkinter.CTkLabel(master=leaderboard_container, text = str(i+1) + ".", font=customtkinter.CTkFont(family="Courier", size=20, weight="bold"))
    name_label.pack(pady=10, padx=20, anchor="w")
    name_labels.append(name_label)
refresh_leaderboard(sorted(read_entries(), key = lambda x: x[7], reverse=True))

app.mainloop()
