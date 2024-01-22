import os

# Dla każdego pliku w bieżącym folderze
for filename in os.listdir():
    if filename.endswith(".csv"):  # Dodatkowa warunek, aby działać tylko na plikach CSV
        # Otwórz plik w trybie odczytu
        print(filename)
        with open(filename, 'r') as f:
            lines = f.readlines()
            print(lines[0])
        # Zmień wartość w pierwszym wierszu
        lines[0] = "Date,Inflation\n"

        # Otwórz plik w trybie zapisu i zapisz zmienione linie
        with open(filename, 'w') as f:
            f.writelines(lines)

print("Zmieniono wartość pierwszej kolumny dla wszystkich plików.")
