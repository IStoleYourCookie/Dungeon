import msvcrt
ch = str(msvcrt.getch())
ch = (ch.replace("b'", "")).strip("'")
print()
if ch == 'q':
    print("q was pressed")