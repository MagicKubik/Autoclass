from GUI import TitlePage

test = TitlePage()
test.start()


# команда для компиляции в EXE
# pyinstaller
# pyinstaller -w --onedir --add-data "data_source/picture/*.png;data_source/picture" --add-data "data_source/test.csv;data_source" main.py
