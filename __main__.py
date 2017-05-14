# !/usr/bin/env python3

import tkinter as tk
from main_app import App
import logging

if __name__ == '__main__':
	logging.basicConfig(filename='console.log', level=logging.INFO)
	
	logging.info("\n==Application starting==\n")
	root = tk.Tk()
	
	App(root)

	root.mainloop()