from PIL import Image
import customtkinter as ctk
from client_back import client_back
from time import sleep

ctk.set_appearance_mode(client_back.user_prefs["theme"])
ctk.set_default_color_theme(client_back.user_prefs["tint"])

#Build UI
root = ctk.CTk()
root.geometry("600x500")
root.resizable(False, False)
root.title("OIN")
root.iconbitmap("assets/paper_plane_send_message_icon_185989.ico")

frame = ctk.CTkFrame(master=root)
frame.pack(padx=0, pady=0, fill="both", expand=True)

txt_box = ctk.CTkEntry(master=frame, placeholder_text="Message...", width=500, height=50, font=("", -15))
txt_box.place(relx=0.45, rely=0.85, anchor="center")

send_btn = ctk.CTkButton(master=frame, text="▷", width=50, height=50, font=("", -40), command=lambda: send_message())
send_btn.place(relx=0.925, rely=0.85, anchor="center")

message_display = ctk.CTkTextbox(master=frame, width=500, height=300)
message_display.place(relx=0.5, rely=0.35, anchor="center")
#Read only, state="normal" means editable
message_display.configure(state="disabled")

title_lab = ctk.CTkLabel(master=frame, text="OIN", font=("", -35))
title_lab.place(relx=0.5, rely=0.725, anchor="center")

def send_message():
    global current_user_prefs
    msg = txt_box.get()
    if msg == "" or str.isspace(msg) or not msg:
        return
    client_back.send_msg(client_back.client_sock, msg)

    #Clear the text entry after sending
    txt_box.delete(0, "end")


#Update disply to show all messages
all_msgs_cache = []
def update_screen():
    global all_msgs_cache

    # Check for new messages
    if len(all_msgs_cache) != len(client_back.all_msgs):
        new_msgs = [item for item in client_back.all_msgs if item not in all_msgs_cache]

        message_display.configure(state="normal")
        for m in new_msgs:
            message_display.insert("end", m + "\n")
            message_display.see("end")
        message_display.configure(state="disabled")
        all_msgs_cache = client_back.all_msgs.copy()

    # Apply theme and tint dynamically
    ctk.set_appearance_mode(client_back.user_prefs["theme"])
    send_btn.configure(fg_color=client_back.user_prefs["tint"])
    send_btn.update()

    # Check if client exited
    if client_back.exited:
        sleep(0.5)
        root.destroy()

    # Schedule the next check in 100ms
    root.after(100, update_screen)

update_screen()

root.mainloop()
