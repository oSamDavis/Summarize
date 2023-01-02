import transformers
import numpy as np
import torch
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *


df_1 = pd.read_csv('./dataset1-news/articles1.csv')
df_2 = pd.read_csv('./dataset1-news/articles2.csv')
df_3 = pd.read_csv('./dataset1-news/articles3.csv')
dfs = [df_1, df_2, df_3]
for frame in dfs:
    frame.drop(columns=['Unnamed: 0', 'publication', 'author', 'date', 'month', 'url'], axis=1, inplace=True)
df = pd.concat(dfs)

# Creating GUI window using tkinter
window = tk.Tk()
window.title("Article to Abstarct")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

# Adding a label GUI window
label = tk.Label(text="Please select an article:")
label.grid(column = 1, row = 4)

# Bind  variables when the selected value changes
def article_changed(event):
    text_example = df.iloc[articlechoosen.get()]['content']
    txt_edit.insert(text_example)

# Creating of a combobox drop down list
articlechoosen = ttk.Combobox(window, width = 27, values =[0,1,2,3,4,5] )
articlechoosen.set(0)
articlechoosen.current(0)


# Main function to generate abstract for selected article using Pegasus
def show_summary():    
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    model = AutoModelForSeq2SeqLM.from_pretrained('google/pegasus-xsum')
    tokenizer = AutoTokenizer.from_pretrained('google/pegasus-xsum')
    i = int(articlechoosen.get())
    text_example = df.iloc[i]['content']
    tokens_input = tokenizer.encode("Abstarct: "+ text_example, return_tensors='pt', max_length=512, truncation=True)
    ids = model.generate(tokens_input, min_length=80, max_length=120)
    summary = tokenizer.decode(ids[0], skip_special_tokens=True)
    print(summary)
    txt_edit.delete("1.0","end")
    txt_edit.insert('1.0',summary)

txt_edit = tk.Text()

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_abstract = tk.Button(frm_buttons, text="Show Abstract",command=show_summary )
btn_abstract.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
articlechoosen.grid(column = 1, row = 1)
frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
