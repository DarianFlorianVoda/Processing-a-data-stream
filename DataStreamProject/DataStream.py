import requests
import getpass
import pandas as pd
import operator

from matplotlib import pyplot as plt
#importarea tuturor pachetelor


#functia de descarcare a fisierului
def download_file():
    #copiere URL
    file_url = 'https://data.gov.ro/dataset/b86a78a3-7f88-4b53-a94f-015082592466/resource/d0b60b45-fb08-4980-a34c-8cbb4a43cad3/download/transparenta_martie_2021.xlsx'

    print('Beginning file download with urllib2...')
    #descarcare URL
    file_object = requests.get(file_url)

    #scriere URL in adresa locala
    with open('COVID-19.xlsx', 'wb') as local_file:
        local_file.write(file_object.content)

download_file()

#definirea utilizatorului
username = getpass.getuser()

#functie pentru calcularea cerintelor
def calcul_alerta_prevalenta(valoare):
    #alocarea de date pentru pagina 'incidenta' din fisierul Excel
    incidenta = pd.read_excel('Covid-19.xlsx', sheet_name='incidenta', header=1)

    #scrierea datelor sub forma CSV
    rate_incidenta = incidenta.to_csv(index=False)

    # preprocesarea datelor de tip csv (convertirea lor din string in lista si stergerea ultimului element ce este gol)
    new_rate_incidenta = rate_incidenta.split("\r\n")
    del new_rate_incidenta[-1]

    #definirea prevalentei pe judet, numarului oraselor pe judet si a judetelor in sine
    prevalenta_judet = dict()
    nr_orase_judet = dict()
    judete = list()

    #parcurgerea datelor
    for i in new_rate_incidenta[1:]:

        #divizarea datelor mai explicit (initial fiind toate datele intr-un singur sir de caractere
        explicit_rate_incidenta = i.split(",")

        #definirea localitatii
        localitate_alerta = explicit_rate_incidenta[0]

        #calcularea diferentei dintre ultima rata de incidenta din localitate si verificarea ei cu valoarea configurabila
        diferenta = float(explicit_rate_incidenta[-1]) - float(explicit_rate_incidenta[-2])

        #se afiseaza o alerta daca diferenta este mai mare decat valoarea
        if diferenta > valoare:
            print(f"Alerta! Localitatea {localitate_alerta} are o crestere a valorilor mai mare decat {valoare}")

        #definirea ultimelor 10 zile
        ultimele_zece_zile = explicit_rate_incidenta[-11:-1]

        s = 0
        #calcularea ratelor de incidenta din cele 10 zile
        for j in ultimele_zece_zile:
            s = s + float(j)

        #calcularea prevalentei pe baza ratei de incidenta
        #FORMULA: Rata de prevalenţă = Rata de incidenţă * Durata bolii (Durata bolii: 10 zile)
        s = s * 10

        #alocarea judetelor si a ratei de prevalenta in dictionar
        if explicit_rate_incidenta[1] in prevalenta_judet:
            prevalenta_judet[explicit_rate_incidenta[1]] = prevalenta_judet[explicit_rate_incidenta[1]] + s
        else:
            prevalenta_judet[explicit_rate_incidenta[1]] = s

        #alocarea judetelor si a numarului de localitati din judet in dictionar
        if explicit_rate_incidenta[1] in nr_orase_judet:
            nr_orase_judet[explicit_rate_incidenta[1]] = nr_orase_judet[explicit_rate_incidenta[1]] + 1
        else:
            nr_orase_judet[explicit_rate_incidenta[1]] = 1

        #alocarea de judete intr-o lista
        if explicit_rate_incidenta[1] in judete:
            pass
        else:
            judete.append(explicit_rate_incidenta[1])

    #parcurgerea fiecarui judet si calcularea finala a ratei de prevalenta prin media prevalentei pe judet (prevalenta/nr. de localitati)
    for i in judete:
        prevalenta_judet[i] = prevalenta_judet[i]/nr_orase_judet[i]

    #sortarea descrescatoare a prevalentelor
    prevalenta_judet= dict(sorted(prevalenta_judet.items(), key=operator.itemgetter(1), reverse=True))
    print(prevalenta_judet)

    # Crearea de spatiu si de figura
    fig, ax = plt.subplots(figsize=(10, 10))

    # Adaugarea de X si Y
    ax.bar(prevalenta_judet.keys(),
           prevalenta_judet.values(),
           color='purple')

    # Modificarea titlului si a textelor de pe liniile X si Y
    ax.set(xlabel="Judet",
           ylabel="Prevalenta",
           title="Prevalenta in ultimele 10 zile\nMartie, 2021, Romania")

    # Rotirea numelor de localitati la 60 de grade pentru a fi vizibile
    plt.setp(ax.get_xticklabels(), rotation=60)

    #afisarea plotului
    plt.show()


#valoare configurabila
valoare = 0.3

#calcularea cerintelor
calcul_alerta_prevalenta(valoare)

