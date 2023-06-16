import pandas as pd
import os
import time


def gl_to_bg(folder_path):
    start_time = time.time()
    pd.set_option('display.max_rows', None)

    # Liste pour stocker les dataframes
    dfs = []

    # récupérer les noms des fichiers
    files = [f for f in os.listdir(folder_path)]

    # Boucle pour itérer sur l'ensemble des fichiers
    for i, file in enumerate(files):
        file_path = os.path.join(folder_path, file)

        # Pour le premier fichier, on charge toutes les lignes
        # à adapter en fonction des besoins (of course)
        if i == 0:
            dfs.append(
                pd.read_csv(file_path, sep="|", dtype=str, on_bad_lines='skip', encoding='ISO-8859-1',
                            usecols=range(18)))
        # Pour les autres on charge les fichiers sans les "a nouveau"
        else:
            df = pd.read_csv(file_path, sep="|", dtype=str, on_bad_lines='skip', encoding='ISO-8859-1',
                             usecols=range(18))
            dfs.append(df[df['JournalCode'] != "ANOUVEAU"])

    # Concaténer tous les dataframes dans la liste
    combined_df = pd.concat(dfs, ignore_index=True)

    #Rajouter notre colonne débit et crédit puis solde (la différence des deux)
    combined_df['Debit'] = combined_df['Debit'].str.replace(',', '.').astype(float)
    combined_df['Debit'] = combined_df['Debit'].round(2)

    combined_df['Credit'] = combined_df['Credit'].str.replace(',', '.').astype(float)
    combined_df['Credit'] = combined_df['Credit'].round(2)

    combined_df['Solde'] = combined_df['Debit'] - combined_df['Credit']

    combined_df['mois'] = combined_df['EcritureDate'].str.slice(start=4, stop=6)

    print(combined_df.groupby(by='mois')['Solde'].sum().round(2))

    print(f'Le solde de mon FEC est de : {combined_df["Solde"].sum(axis=0).round(2)}')

    end_time = time.time()

    print(f'Temps d\'exécution : {end_time - start_time} secondes.')


if __name__ != '__main__':
    pass
# Press the green button in the gutter to run the script.
else:
    gl_to_bg(
        r"chemin à mettre ici")
