import pandas as pd
import socket
import datetime
from tkinter import *



def gen_raport(test_case: str, rezultat: str) -> None:
    data: str = datetime.datetime.now().strftime("%d/%m/%Y")
    ora: str = datetime.datetime.now().strftime("%H:%M:%S")

    try:
        fisier = open(f"./rapoarte/{test_case}.csv", "r")
        fisier.close()
    except FileNotFoundError:
        data_brut: dict = {
            "Dispozitiv": [socket.gethostname()],
            "Data": [data],
            "Ora": [ora],
            "Tester": ["FMI".upper()],
            "Status": [rezultat]

        }
        datele = pd.DataFrame(data_brut)
        datele.to_csv(f"./rapoarte/{test_case}.csv", index=False)
    else:
        datele1 = pd.read_csv(f"./rapoarte/{test_case}.csv")

        new_list_disp: list = datele1.Dispozitiv.to_list()
        new_list_disp.append(socket.gethostname())

        new_list_data: list = datele1.Data.to_list()
        new_list_data.append(data)

        new_list_ora: list = datele1.Ora.to_list()
        new_list_ora.append(ora)

        new_list_tester: list = datele1.Tester.to_list()
        new_list_tester.append("FMI".upper())

        new_list_status: list = datele1.Status.to_list()
        new_list_status.append(rezultat)

        new_dates = {
            "Dispozitiv": new_list_disp,
            "Data": new_list_data,
            "Ora": new_list_ora,
            "Tester": new_list_tester,
            "Status": new_list_status
        }
        df = pd.DataFrame(new_dates)
        df.to_csv(f"./rapoarte/{test_case}.csv", index=False)


def pop_up(nr_test: str, rezultat: str, last: bool) -> None:
    while True:
        try:
            from tkinter import messagebox
            break
        except TclError:
            continue
    if last is True:
        messagebox.showinfo(title=f"{nr_test}",
                            message=f"Am incheiat ultimul {nr_test}\nTestul este: {rezultat}\nApasa \"OK\" pt. a inchide driverul")
    else:
        messagebox.showinfo(title=f"{nr_test}",
                            message=f"Am incheiat {nr_test}\nTestul este: {rezultat}\nApasa \"OK\" pt. a continua")
