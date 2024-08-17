import customtkinter as ctk
from client_back import client_back

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

#Build UI
root = ctk.CTk()
root.geometry("600x500")
root.resizable(False, False)

frame = ctk.CTkFrame(master=root)
frame.pack(padx=0, pady=0, fill="both", expand=True)

txt_box = ctk.CTkEntry(master=frame, placeholder_text="Message...", width=500, height=50, font=("", -15))
txt_box.place(relx=0.45, rely=0.85, anchor="center")

send_btn = ctk.CTkButton(master=frame, text="▷", width=50, height=50, font=("", -30), command=lambda: send_message())
send_btn.place(relx=0.925, rely=0.85, anchor="center")

message_display = ctk.CTkTextbox(master=frame, width=500, height=300)
message_display.place(relx=0.5, rely=0.35, anchor="center")
#Read only, state="normal" means editable
message_display.configure(state="disabled")

def send_message():
    msg = txt_box.get()
    client_back.send_msg(client_back.client_sock, msg)
    #Clear the text entry after sending
    txt_box.delete(0, "end")


#Update disply to show all messages
all_msgs_cache = []
def update_screen():
    global all_msgs_cache
    if len(all_msgs_cache) != len(client_back.all_msgs):
        all_msgs_cache = client_back.all_msgs.copy()
        message_display.configure(state="normal")
        message_display.delete("1.0", "end")
        for m in all_msgs_cache:
            message_display.insert("end", m + "\n")
            message_display.see("end")
        message_display.configure(state="disabled")
    #Schedule the next check in 100ms
    root.after(100, update_screen)

    if client_back.exited:
        root.destroy()

update_screen()

root.mainloop()
