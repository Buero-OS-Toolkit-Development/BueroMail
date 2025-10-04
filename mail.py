import bueroUtils

try:
    bü = bueroUtils.bueroUtils(packageName="BüroMail")
    dLg = bü.dLg
    py = bü.importPyautoguiCatched()
except ImportError:
    import pyautogui as py
    py.alert("Sie wurden deautorisiert.\nWenden Sie sich an den Kundenservice.", "Fehler beim Laden der bueroUtils")
    quit(code="Unautorisiertes Plugin")

BPATH = "./programdata/buero/"
HPATH = "./programdata/mail/"

dLg.entry("Daten initialisiert")

with open(BPATH+"username.txt", "r", encoding="utf-8") as f:
    USER = f.read()
with open(BPATH+"devid.txt", "r", encoding="utf-8") as f:
    DEVID = f.read()
dLg.entrys("USER und DEVID ausgelesen", USER, DEVID)
    
try:
    with open("./premiumpass.txt", "r", encoding="utf-8") as f:
        premiumContent = f.read()
    PREMIUM = bü.checkPREMIUM(premiumContent)
except:
    PREMIUM = False

dLg.entry(PREMIUM)
    
if PREMIUM:
    from tkinter import *
    from tkinter.filedialog import askopenfilename
    import shutil, os

    BETA = str(bü.checkBETA(USER))
    
    def load_mail():
        global USER
        try:
            filename = askopenfilename(filetypes=[("*.txt", "TXT BüroMail file")], initialdir=HPATH+"inbox/unread")
            sbj = filename.split("/")[-1].rstrip(".txt")
            with open(filename, "r", encoding="utf-8") as f:
                ct = f.read()
            sender, content = ct.split("#**#")
            for i in c.textlist:
                i.delete("1.0", END)
            c.inhalt.insert(END, content.rstrip())
            c.sender.insert(END, sender)
            c.empfänger.insert(END, USER)
            c.betreff.insert(END, sbj)
            if "/unread/" in filename:
                if filename.split("/")[-1] not in os.listdir(HPATH+"/inbox/archive"):
                    shutil.move(HPATH+"/inbox/unread/"+sbj+".txt", HPATH+"/inbox/archive/"+sbj+".txt")
                else:
                    shutil.move(HPATH+"/inbox/unread/"+sbj+".txt", HPATH+"/inbox/archive/"+sbj+"_.txt")
            c.itemconfig(c.benachrichtigung, text="Mail geöffnet")
        except:
            py.alert("Invalide Mail!", "Fehler")
            c.itemconfig(c.benachrichtigung, text="Fehler beim Öffnen")
    
    def send_mail():
        global USER, DEVID
        c.itemconfig(c.benachrichtigung, text="Mail wird gesendet...")
        root.update()
        toSend = True
        if c.sentRecently:
            toSend = bü.buttonLog("Sie haben bereits sehr kürzlich eine Mail gesendet.\nWollen Sie diese Mail wirklich senden?") == "Fortfahren"
        if toSend:
            if c.sender.get("1.0", END).rstrip() == USER:
                sbj = c.betreff.get("1.0", END).rstrip()
                cnt = c.inhalt.get("1.0", END)
                rcps = c.empfänger.get("1.0", END).rstrip().split("; ")
                for rcp in rcps:
                    if rcp != "":
                        while sbj+".txt" in os.listdir(HPATH+"sent"):
                            sbj += "_"
                        with open(HPATH+"sent/"+sbj+".txt", "x", encoding="utf-8") as f:
                            f.write(USER+"#**#"+cnt)
                        code = bü.web_content("https://lkunited.pythonanywhere.com/getCode", {"username": USER,\
                                              "id": BETA, "devid": DEVID, "password": "lkunited"})
                        c.itemconfig(c.benachrichtigung, text="Code generiert: "+code)
                        root.update()
                        send = bü.web_content("https://lkunited.pythonanywhere.com/sendMail",\
                                              {"username": USER, "code": code, "subject": sbj, "content": cnt, "recipient": rcp})
                        c.itemconfig(c.benachrichtigung, text="Mail gesendet: "+send)
                        root.update()
                    else:
                        c.itemconfig(c.benachrichtigung, text="Invalider Empfänger: "+rcp)
                        root.update()
                c.after(1000, setMailSentRecpText)
                c.sentRecently = True
                c.after(5000, removeSentRecentlyTombstone)
            else:
                py.alert("Invalider Absendername!", "Fehler")
                c.itemconfig(c.benachrichtigung, text="Fehler beim Senden")
        else:
            c.itemconfig(c.benachrichtigung, text="Senden abgebrochen")

    def setMailSentRecpText():
        c.itemconfig(c.benachrichtigung, text="Mail an alle Empfänger gesendet")

    def removeSentRecentlyTombstone():
        c.sentRecently = False
    
    def redirect():
        global USER
        sender_before = c.sender.get("1.0", END)
        c.inhalt.insert("1.0", "\n\n"+sender_before.rstrip("\n")+" schrieb:\n")
        c.betreff.insert("1.0", "Wg- ")
        c.empfänger.delete("1.0", END)
        c.sender.delete("1.0", END)
        c.sender.insert(END, USER)
        c.itemconfig(c.benachrichtigung, text="Weiterleitung konfiguriert")
    
    def reply():
        global USER
        sender_before = c.sender.get("1.0", END)
        c.inhalt.insert("1.0", "\n\n"+sender_before.rstrip("\n")+" schrieb:\n")
        c.betreff.insert("1.0", "Aw- ")
        c.empfänger.delete("1.0", END)
        c.sender.delete("1.0", END)
        c.sender.insert(END, USER)
        c.empfänger.insert(END, sender_before)
        c.itemconfig(c.benachrichtigung, text="Antwort konfiguriert")

    def insert_person():
        global USER
        c.sender.delete("1.0", END)
        c.sender.insert(END, USER)
        c.itemconfig(c.benachrichtigung, text="Sender validiert")

    def format_multi_rcp():
        c.empfänger.insert(END, "; ")
        c.itemconfig(c.benachrichtigung, text="Multiple Empfänger initialisiert")

    def format_start():
        c.sender.delete("1.0", END)
        c.betreff.delete("1.0", END)
        c.empfänger.delete("1.0", END)
        c.inhalt.delete("1.0", END)
        c.inhalt.insert(END, "Öffne eine Mail oder setze eine neue Mail auf, um zu beginnen."+\
                             "\n\nTastenkombinationen:\nEnter: neue Zeile\nTab: Zum nächsten Textfeld")
        c.itemconfig(c.benachrichtigung, text="Textfelder zurückgesetzt")
    
    def quit_():
        c.itemconfig(c.benachrichtigung, text="BüroMail beenden...")
        root.update()
        dLg.finalsave_log()
        quit()
    
    def quit_agent():
        with open(HPATH+"runAgent.txt", "w", encoding="utf-8") as f:
            f.write("stop")
        c.itemconfig(c.benachrichtigung, text="BackgroundAgent beendet")

    def tabJump():
        for idx in range(len(c.fields)):
            if "\t" in c.fields[idx].get("1.0", END):
                content = c.fields[idx].get("1.0", END)
                c.fields[idx].delete("1.0", END)
                c.fields[idx].insert("1.0", content.replace("\t", "").rstrip("\n"))
                if idx != len(c.fields)-1:
                    c.fields[idx+1].focus_set()
                else:
                    if bü.buttonLog("Mail senden?", "Senden?") == "Fortfahren":
                        send_mail()
        c.after(1000, tabJump)

    root = Tk()
    root.title("BüroMail")
    
    c = Canvas(root, width=650, height=850)
    c.configure(bg="light blue")
    c.pack()

    c.create_text(325, 30, text="BüroMail", font=("Verdana", "30", "bold"))
    c.create_text(20, 100, text="Sender:", font=("Verdana", "20"), anchor="w")
    c.create_text(20, 140, text="Empfänger:", font=("Verdana", "20"), anchor="w")
    c.create_text(20, 200, text="Betreff:", font=("Verdana", "20"), anchor="w")
    c.create_text(325, 270, text="Inhalt:", font=("Verdana", "25"))

    c.inhalt = Text(root, wrap=WORD, font=("Verdana", "16"))
    c.create_window(10, 325, height=325, width=630, window=c.inhalt, anchor="nw")
    c.sender = Text(root, wrap="none", font=("Verdana", "16"))
    c.create_window(230, 100, height=35, width=370, window=c.sender, anchor="w")
    c.empfänger = Text(root, wrap="none", font=("Verdana", "16"))
    c.create_window(230, 140, height=35, width=370, window=c.empfänger, anchor="w")
    c.betreff = Text(root, wrap="none", font=("Verdana", "18"))
    c.create_window(230, 200, height=40, width=370, window=c.betreff, anchor="w")
    
    c.fields = [c.sender, c.empfänger, c.betreff, c.inhalt]

    c.sentRecently = False

    c.benachrichtigung = c.create_text(325, 820, text="BüroMail gestartet", font=("Verdana", "17"))
    
    c.create_text(325, 845, text="Copyright Leander Kafemann 2024-2025  -  Version 1.2.10", font=("Verdana", "5"))
    
    c.create_window(15, 675, anchor="nw", window=Button(master=root, command=load_mail, text="📂", background="light blue", relief="ridge", height=2, width=15))
    c.create_window(325, 675, anchor="n", window=Button(master=root, command=quit_agent, text="BackgroundAgent beenden", background="light blue", relief="ridge", height=2, width=27))
    c.create_window(635, 675, anchor="ne", window=Button(master=root, command=send_mail, text="➢", background="light blue", relief="ridge", height=2, width=15))
    c.create_window(325, 770, window=Button(master=root, command=quit_, text="Quit", background="light blue", relief="ridge", height=2, width=30))

    c.create_window(605, 100, anchor="w", window=Button(master=root, command=insert_person, relief="sunken", height=1, width=2, text="👤", background="silver"))
    c.create_window(605, 140, anchor="w", window=Button(master=root, command=format_multi_rcp, relief="sunken", height=1, width=2, text="➕", background="silver"))
    c.create_window(605, 200, anchor="w", window=Button(master=root, command=format_start, relief="sunken", height=1, width=2, text="❌", background="silver"))

    c.create_window(125, 270, anchor="w", window=Button(master=root, command=reply, text="⮪", background="light blue", relief="sunken", height=1, width=3))
    c.create_window(525, 270, anchor="e", window=Button(master=root, command=redirect, text="⮫", background="light blue", relief="sunken", height=1, width=3))

    c.textlist = [c.inhalt, c.sender, c.empfänger, c.betreff]

    if "pre_mail.txt" in os.listdir("./programdata/mail"):
        with open(HPATH+"pre_mail.txt", "r", encoding="utf-8") as f:
            content = f.read()
        os.remove(HPATH+"pre_mail.txt")
        #Empfänger, Betreff, Inhalt
        content_ = content.split("#**#")
        c.empfänger.insert(END, content_[0])
        c.betreff.insert(END, content_[1])
        c.inhalt.insert(END, content_[2])
        c.sender.insert(END, USER)
        c.itemconfig(c.benachrichtigung, text="Vorgespeicherte Mail geladen")
    else:
        format_start()

    dLg.entry("BüroMail gestartet.")
    c.itemconfig(c.benachrichtigung, text="BüroMail gestartet")

    c.after(2000, tabJump)

    root.mainloop()
else:
    py.alert("Sie benötigen Büro PREMIUM, um BüroMail nutzen zu können.", "BüroMail nicht verfügbar")
    dLg.finalsave_log()
    quit(code="Büro PREMIUM fehlt")