
from Szyfrowanie.SzyfrowaniePubliczne import SzyfrowaniePubliczne
from Szyfrowanie.SzyfrowaniePrywatne import SzyfrowaniePrywatne
from Szyfrowanie.Szyfrowanie import Szyfrowanie

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    szyfrowanie_publiczne = SzyfrowaniePrywatne()
    print_hi('PyCharm')
