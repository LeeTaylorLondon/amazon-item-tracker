# registry.py
from typing import List

URL_FILE = 'urls.txt'

class Registry:
    def __init__(self):
        self.view = False
        pass


    def __repr__(self):
        return f"<class Registry, path={URL_FILE}>"


    def __len__(self) -> int:
        return len(self.load_links())


    def set_view_false(self) -> None:
        """ sets attribute 'view' to false to close menu """

        self.view = False
        pass


    def reg_menu_text(self) -> None:
        print("\n_______________________________")        
        print("[Please type 1, 2, or 3...]")
        print("_______________________________")
        print("1 -> [View] Registry")
        print("2 -> [Add] URL to registry")
        print("3 -> [Remove] URL from registry")
        print("4 -> [Exit] Return to main menu")
        print("_______________________________")
        pass


    def load_links(self) -> List[str]:
        """ returns -> array of string links """

        with open(URL_FILE, 'r') as txt_file:
            urls = txt_file.read().split()
        return urls


    def view_registry(self) -> None:
        """ prints out url and index in array """

        arr = self.load_links()
        for i,v in enumerate(arr):
            print(f"<{i}: {v}>\n")
        pass


    def add_registry(self) -> None:
        """ appends entry to text document """

        url = str(input("Enter URL to amazon item: "))
        price = str(input("Enter desired price for item: "))
        # prevents invalid desired price value
        try:
            float(price)
        except ValueError:
            print("Do not include any letters or symbols other than '.' - Item not added!")
            return
        # prevents inputting duplicate and/or blank URLs
        if(not url == "" and url not in self.load_links()):
            with open(URL_FILE, 'a') as text_file:
                text_file.write(url+','+price+'\n')
        pass


    def delete_registry(self):
        """ user enters an integer and the corresponding link is deleted """
        
        self.view_registry()
        links = self.load_links()
        try:
            url_to_delete = links[int(input("Enter no. of URL to delete: "))]
        except IndexError:
            print('Item not found - Nothing was deleted')
            return
        with open(URL_FILE, 'w') as f:
            for link in links:
                if(link != url_to_delete):
                    f.write(link+'\n')
                    

    def reg_menu(self) -> None:
        self.view = True
        options = {1: self.view_registry, 2: self.add_registry,
                   3: self.delete_registry, 4: self.set_view_false}
        
        while(self.view is True):
            self.reg_menu_text()
            links = self.load_links()  # links: List[str] -> contains specified urls
            try:
                options.get(int(input("\nEnter option: ")))()
            except (ValueError, TypeError):
                print("[Invalid option! :(]")


if __name__ == "__main__":
    Registry().reg_menu()
