import bueroUtils, time, os, pyperclip

bü = bueroUtils.bueroUtils(packageName="BüroMail_backgroundAgent")
dLg = bü.dLg
py = bü.importPyautoguiCatched()

BPATH = "./programdata/buero/"
HPATH = "./programdata/mail/"

with open(BPATH+"username.txt", "r", encoding="utf-8") as f:
    USER = f.read()
with open(BPATH+"devid.txt", "r", encoding="utf-8") as f:
    DEVID = f.read()
    
try:
    with open("./premiumpass.txt", "r", encoding="utf-8") as f:
        premiumContent = f.read()
    PREMIUM = bü.checkPREMIUM(premiumContent)
except:
    PREMIUM = False
dLg.entrys("Bootdaten gesammelt", USER, DEVID, PREMIUM)

if not PREMIUM:
    PREGET = (bü.buttonLog("Sie benötigen Büro PREMIUM, um BüroMail nutzen zu können.\nGratis-Modus zum Erhalten von PREMIUM nutzen?", "BüroMail nicht verfügbar") == "Fortfahren")
else:
    PREGET = False
dLg.entry(PREGET)
    
if PREMIUM or PREGET:
    py.alert("BüroMail BackgroundAgent überprüft Ihren Posteingang nun im Hintergrund.", "BüroMail BackgroundAgent V1.2.10")

    BETA = str(bü.checkBETA(USER))

    while True:
        with open(HPATH+"/runAgent.txt", "r", encoding="utf-8") as f:
            stop = f.read()
        if stop == "stop":
            with open(HPATH+"/runAgent.txt", "w", encoding="utf-8") as f:
                f.write("run")
            break
        code = bü.web_content("https://lkunited.pythonanywhere.com/getCode", {"username": USER,\
                              "id": BETA, "devid": DEVID, "password": "lkunited"})
        count = bü.web_content("https://lkunited.pythonanywhere.com/getMailCount", {"username": USER, "code": code})
        dLg.entrys(code, count)
        if count == "Authentification failed":
            py.alert("Ein Fehler ist beim Authentifizieren Ihrer Identität aufgetreten.\n"+\
                     "Wenden Sie sich an den Kundenservice.", "Authentifizierung fehlgeschlagen")
        elif count != "0" and not "<html>" in count:
            if not PREGET:
                py.alert(f"Sie haben {count} neue Mails in Ihrem BüroMail-Posteingang.", "Neue Mail")
            else:
                py.alert("Es befinden sich ungelesene Mails in Ihrem Posteingang.\nSie können diese lesen, sobald PREMIUM geliefert wurde.", "PREMIUM benötigt")
            code = bü.web_content("https://lkunited.pythonanywhere.com/getCode", {"username": USER,\
                                     "id": "True" if bü.web_content("https://lkunited.pythonanywhere.com/cB",\
                                     {"message": USER, "pw": "lkunited"}) == "registered" else "False", "devid": DEVID, "password": "lkunited"})
            content = bü.web_content("https://lkunited.pythonanywhere.com/getMail", {"username": USER, "code": code})
            dLg.entrys(code, count)
            if content == "Authentification failed":
                py.alert("Ein Fehler ist beim zweiten Authentifizieren Ihrer Identität aufgetreten.\n"+\
                         "Wenden Sie sich an den Kundenservice.", "Authentifizierung fehlgeschlagen")
            else:
                for i in content.split("#***#"):
                    mailList = i.split("#**#")
                    while mailList[0]+".txt" in os.listdir(HPATH+"inbox/unread") or mailList[0]+".txt" in os.listdir(HPATH+"inbox/archive"):
                        mailList[0] = mailList[0] + "_"
                    with open(HPATH+"inbox/unread/"+mailList[0]+".txt", "w", encoding="utf-8") as f:
                        f.write(mailList[1]+"#**#"+mailList[2])
                    dLg.entry(mailList[0])
                    if PREGET:
                        if mailList[1] == "The Creator" and ("PremiumPass" in mailList[2] or "y!" in mailList[2]) and ("PREMIUM" in mailList[0] or "PremiumPass" in mailList[0]):
                            py.alert("Ihr PREMIUM-Pass ist angekommen. Sie können ihn in Büro hinzufügen.", "PREMIUM")
                            py.alert("The Creator hat Ihnen die folgende Nachricht diesbezüglich geschickt:\n"+mailList[0]+"\n"+mailList[2], "PREMIUM")
                            pyperclip.copy(mailList[2])
                            py.alert("Der Inhalt der Mail wurde in die Zwischenablage kopiert.", "PREMIUM erhalten")
                            py.alert("BüroMail BackgroundAgent wurde beendet.", "Ende")
                            dLg.finalsave_log()
                            quit()
        else:
            if count != "0":
                py.alert("Ein Fehler ist auf unseren Servern aufgetreten.\nBitte versuchen Sie es zu einem späteren Zeitpunkt erneut.\nDer BackgroundAgent bleibt aktiv.", "Serverfehler")
                dLg.entry(count); dLg.presave_log()
                py.alert("Falls dieser Fehler wiederholt auftritt, melden Sie sich bitte beim Kundenservice.\nEin DebugLog wurde erstellt.", "Serverfehler")
        time.sleep(60)
    py.alert("BüroMail BackgroundAgent wurde beendet.", "Ende")
    dLg.finalsave_log()
    quit()
else:
    dLg.finalsave_log()
    quit()
