# help.py

def ait_help() -> None:
	""" explains each option avaiable to the user """

	# Main menu options explained 1-4
	print("Ping Prices:")
	print("    displays the name and price of each item added to this program")
	print("    by you\n")

	print("Configure:")
	print("    in here the user can add, remove and view the links to amazon")
	print("    items they've added.")
	print("    when adding a URL to track an item, you must specify whether")
	print("    the item is a book or not.\n")

	print("Monitor Prices:")
	print("    every hour the price of your specified items are compared")
	print("    to your desired price")
	print("    if an item falls below the desired price an email is sent")
	print("    to the user (you).")
	print("    For this to work you must add an email (gmail required)")
	print("    and password, to send the email.")
	print("    You must also add an email address to recieve this email")
	print("    which can be of any email service, yahoo, hotmail, etc.etc")
