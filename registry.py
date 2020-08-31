# registry.py
from typing import List
from typing import Tuple


URL_FILE = 'urls.txt'


class Registry:
    def __init__(self):
        self.view = False
        pass


    def __repr__(self) -> str:
        return f"<class Registry, path={URL_FILE}>"


    def __len__(self) -> int:
        return len(self.load_links())


    def set_view_false(self) -> None:
        """ sets attribute 'view' to false to close menu """

        self.view = False
        pass


    def reg_menu_text(self) -> None:
        print("\n_______________________________")        
        print("[Please type 1, 2, 3, or 4]")
        print("_______________________________")
        print("1 -> [View]   Registry")
        print("2 -> [Add]    URL to registry")
        print("3 -> [Remove] URL from registry")
        print("4 -> [Exit]   Return to main menu")
        print("_______________________________")
        pass


    def load_links(self) -> Tuple[List[str], List[str]]:
        """ extract each line of text from the specified text file
    
            :return: tuple(lines: List[str], urls: List[str])"""

        with open(URL_FILE, 'r') as txt_file:
            lines = txt_file.read().split()

        urls = []
        for line in lines:
            urls.append(line.split(',')[0])
            
        return lines, urls


    def view_registry(self) -> None:
        """ prints out index, url link """

        arr = self.load_links()[0]
        for i,v in enumerate(arr):
            print(f"<{i}: {v}>\n")
        pass


    def input_item_category(self) -> str:
        inp = ""
        while(inp != "y" and inp != "n"):
            inp = str(input("Is this item a book? (y/n): ")).lower()
        return inp


    def inp_item_price(self) -> List[str]:
        """ this method is called if the item is not a book

            return cannot be of type str, as later on an iterator incorrectly
            iterates through each char instead of the string as a whole
        """
        
        return [str(input("Enter desired price for item: "))]


    def format_string(self, url: str, prices) -> str:
        """ :param:  prices -> can be either string or tuple of two strings
            :return: str    -> line of string to write to URL text file
        """

        sep = ','
        return f"{url}{sep}{prices[0]}\n" if(len(prices)!=2) else\
               url+sep+sep.join(prices)+'\n'


    def inp_book_prices(self) -> Tuple[str]:
        print("[!] Enter 10000 if wish to ignore one of the prices [!]")
        paper_price, kindle_price = '', ''
        while(paper_price == ''):
            paper_price  = str(input("Enter desired paperback price: "))
        while(kindle_price == ''):
            kindle_price = str(input("Enter desired kindle price: "))
        return paper_price, kindle_price


    def add_registry(self) -> None:
        """ appends entry to text document """

        # inits functions corresponding to user input and takes in url input
        item_options = {'n': self.inp_item_price, 'y': self.inp_book_prices}
        url = str(input("Enter URL to amazon item: "))
        # validates url input - prevents inputting duplicate and/or blank URLs
        if(url == "" or url in self.load_links()[1]):
            print("Item not added - URL already exists or is blank")
            return
        # user-input price(s) -> then -> validates price input        
        prices = item_options.get(self.input_item_category())()
        try:
            for price in prices:
                float(price)
        except ValueError:
            print("Do not include any letters or symbols other than '.' - Item not added!")
            return
        # writes input as a line of text to text file
        with open(URL_FILE, 'a') as text_file:
            text_file.write(self.format_string(url, prices))
        pass


    def delete_registry(self) -> None:
        """ user enters an integer and the corresponding link is deleted """
        
        self.view_registry()
        links = self.load_links()[0]
        try:
            url_to_delete = links[abs(int(input("Enter no. of URL to delete: ")))]
        except IndexError:
            print('Item not found - Nothing was deleted')
            return
        with open(URL_FILE, 'w') as f:
            for link in links:
                if(link != url_to_delete):
                    f.write(link+'\n')
                    

    def reg_menu(self) -> None:
        self.view = True
        options = { 1: self.view_registry, 
                    2: self.add_registry,
                    3: self.delete_registry,
                    4: self.set_view_false}
        
        while(self.view is True):
            self.reg_menu_text()
            links = self.load_links()  # links: List[str] -> contains specified urls
            try:
                options.get(int(input("\nEnter option: ")))()
            except (ValueError, TypeError):
                print("[Invalid option! :(]")


if __name__ == "__main__":
    Registry().reg_menu()
