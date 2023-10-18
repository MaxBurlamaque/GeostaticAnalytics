import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import tkinter
from tkinter import *
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# making pandas float numbers show y.xx (2 decimals places)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

"""
0.1 Crutial Variables
1.0 Database
1.1 Data Manipulation
2.0 Charts
3.0 Visualization
"""
# 0.1 Variables
global training
training = 5 # Starts in 5 because that's my currently training

# 1.0 Connect to the database and get data
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="" # Add password
)
cursor = mydb.cursor()
cursor.execute("use geo;")

cursor.execute("SELECT * FROM uniaoTabelas;")
results = cursor.fetchall()

cursor.execute("SELECT * FROM training;")
results_training = cursor.fetchall()

# 1.1 Data Manipulation

df = pd.DataFrame(results, columns=['guessed','answer','date','category'])
df_training = pd.DataFrame(results_training, columns=['id', 'desc', 'cg'])

def getCorrect(row):
    if row.guessed == row.answer:
        return 1
    return 0

df2 = df
df2['correct'] = df2.apply(getCorrect, axis=1)

total_rounds = len(df2)

currently_country_group = df_training[df_training.id == training].iloc[0]['cg']
currently_country_group_rounds = len(df2[df2.category == currently_country_group])
df2 = df2[df2.category == currently_country_group] # df2 is the database that it's going to be used

df_acumulative_percentage = []
for i in df2.index:
    df_acumulative_percentage.append(df2.iloc[0:i].correct.sum()/(i+1)*100)
df2['percentage'] = df_acumulative_percentage

# 2.0 Charts and Data

# WINRATE CHART
fig6, ax6 = plt.subplots()
chart = sns.lineplot(y="percentage", x=df2.index, data=df2, ax=ax6) 
ax6.set_ylim(1, 100)
ax6.set_title("Training Winrate")
nmr = (len(df2)-1 )/ 4
l_nmr = [round(nmr), round(nmr*2), round(nmr*3), round(nmr*4)]
for line in l_nmr:
     ax6.text(line, df2.percentage[line], "{:.2f}".format(df2.percentage[line]), horizontalalignment='left', size='medium', color='black', weight='semibold')
fig6.set_figheight(3)
fig6.set_figwidth(4)
fig6.tight_layout()
# END WINRATE CHART

# INCIDENCE CHART
fig7, ax7 = plt.subplots()
chart_incidence = sns.countplot(x="answer", data= df2, order = df2.answer.value_counts().iloc[:5].index)
ax7.set_title("Countries Incidence")
fig7.set_figheight(3)
fig7.set_figwidth(4)
fig7.tight_layout()
# END INCIDENCE CHART

# COUNTRY WINRATE CHART
winrate_country_list = [] # country, winrate
for i in df2.groupby("answer"):
    if i[1].correct.sum() == 0:
        winrate_country_list.append([i[0], 0])
    else : winrate_country_list.append([i[0], (len(i[1]) / i[1].correct.sum()) * 100])
winrate_country_list = sorted(winrate_country_list, key= lambda row:row[0], reverse=1)
fig8, ax8 = plt.subplots()
ctr = []
winrate = []
for i in winrate_country_list:
    ctr.append(i[0])
    winrate.append(i[1])
chart_winrate = sns.barplot(x=ctr[:5], y=winrate[:5])
ax8.set_title("Best Winrate Countries")
fig8.set_figheight(3)
fig8.set_figwidth(4)
fig8.tight_layout()
# END COUNTRY WINRATE CHART

# COUNTRY LOSERATE CHART
fig9, ax9 = plt.subplots() 
chart_loserate = sns.barplot(x=ctr[len(ctr)-5:], y=winrate[len(winrate)-5:])
ax9.set_title("Worst Winrate Countries")
fig9.set_figheight(3)
fig9.set_figwidth(4)
fig9.tight_layout()
# END COUNTRY LOSERATE CHART

# 3.0 Visualization

root = tkinter.Tk()
root.title("Dashboard")
root.state("zoomed") # Fullscreen
root.resizable(False, False) # Not resizable

# Side frame for utilities
side_frame = tkinter.Frame(root, bg="#4C2A85")
side_frame.pack(side="left", fill="y")

label = tkinter.Label(side_frame, text="Dashboard", bg="#4C2A85", fg="#FFF", font=25)
label.pack(pady=50, padx=20)

# Global variables such as vard are used to be able to delete labels created in the function bellow
global vard
vard = 0
# Function to show specific country charts with the user input
def country_stats(country):
    # Global variables as explained 5 code lines before
    global vard 
    global label_plc
    global label_prct
    global label_plc_guess
    # Delete old labels to reduce memory usage
    if vard == 1:
        root.after(1000, label_plc.destroy)
        root.after(1000, label_prct.destroy)

    # Creating databases for the country
    df_cstat = df2[df2.answer == country]
    df_cstatguess = df2[df2.guessed == country]
    
    percentage_answer = 0
    if df_cstat.correct.sum() != 0:
        percentage_answer = (df_cstat.correct.sum()/len(df_cstat))*100

    # Chart for when the country is the answer
    values2 = df_cstatguess[df_cstatguess.correct == 0].guessed.value_counts().tolist()
    index2 = df_cstatguess[df_cstatguess.correct == 0].guessed.value_counts().index.tolist()

    country_stat_figguess, country_stat_axguess = plt.subplots()
    chart2 = sns.barplot(x = index2, y = values2)
    country_stat_axguess.set_title("Most guessed countries for {}".format(country))
    country_stat_figguess.set_figheight(3)
    country_stat_figguess.set_figwidth(4)
    country_stat_figguess.tight_layout()
    canvass2 = FigureCanvasTkAgg(figure=country_stat_figguess, master=root)
    canvass2.draw()
    canvass2.get_tk_widget().place(x=960, y=80)

    # Chart for when the country is the guess
    values = df_cstat[df_cstat.correct == 0].guessed.value_counts().tolist()
    index = df_cstat[df_cstat.correct == 0].guessed.value_counts().index.tolist()

    country_stat_fig, country_stat_ax = plt.subplots()
    chart1 = sns.barplot(x=index, y=values)
    country_stat_ax.set_title("Wrong guessed countries with {}".format(country))
    country_stat_fig.set_figheight(3)
    country_stat_fig.set_figwidth(4)
    country_stat_fig.tight_layout()
    canvass1 = FigureCanvasTkAgg(figure=country_stat_fig, master=root)
    canvass1.draw()
    canvass1.get_tk_widget().place(x=960, y=400)

    # Showing other stats
    total_rounds_country = "Rounds Played in this Country: {}".format(len(df_cstat))

    label_plc = tkinter.Label(root, text=total_rounds_country, fg="black", font=25)
    label_plc.place(x=1000, y=7)

    total_rounds_country_guess = "Rounds Guessing this Country: {}".format(len(df_cstatguess))

    label_plc_guess = tkinter.Label(root, text=total_rounds_country_guess, fg="black", font=25)
    label_plc_guess.place(x=1000, y=28)

    percentage_country = "Country Winrate: {:.2f}%".format(percentage_answer)

    label_prct = tkinter.Label(root, text=percentage_country, fg="black", font=25)
    label_prct.place(x=1000, y=49)
    # Updating vard variable to delete old labels
    vard = 1

# Function to call the country charts
def changeCountry():
    country_stats(new_country.get())

# Function to change training - NOT WORKING AS SHOULD RIGHT NOW
def changeTraining():
    global training
    training = new_training.get()

# Change country chart functionality
new_country = tkinter.Entry(root, width=18)
new_country.place(x=5, y=200)
tkinter.Button(root, width=13, text="Country", command=changeCountry).place(x=5, y=220)

# Change training functionality
new_training = tkinter.Entry(root, width=18)
new_training.place(x=5, y=150)
tkinter.Button(root, width=13, text="Training", command=changeTraining).place(x=5, y=170)

# Basic stats
text_total_rounds = "Total Rounds Played Ever: {}".format(total_rounds)

label2 = tkinter.Label(root, text=text_total_rounds, fg="black", font=25)
label2.place(x=200, y=30)

total_training_rounds = "Total Rounds Played in this Training: {}".format(currently_country_group_rounds)

label2 = tkinter.Label(root, text=total_training_rounds, fg="black", font=25)
label2.place(x=450, y=30)

# Basic charts
canvas = FigureCanvasTkAgg(figure=fig6, master=root)
canvas.draw()
canvas.get_tk_widget().place(x=140, y=80)

canvas = FigureCanvasTkAgg(figure=fig7, master=root)
canvas.draw()
canvas.get_tk_widget().place(x=550, y=80)

canvas = FigureCanvasTkAgg(figure=fig8, master=root)
canvas.draw()
canvas.get_tk_widget().place(x=550, y=400)

canvas = FigureCanvasTkAgg(figure=fig9, master=root)
canvas.draw()
canvas.get_tk_widget().place(x=140, y=400)

# Initialization
root.mainloop()