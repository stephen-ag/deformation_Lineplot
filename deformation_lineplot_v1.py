import glob
import os
import xlsxwriter
import openpyxl
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
from openpyxl import load_workbook


#fpath = ('C:\\Users\\arpuste\\Downloads\\case2\\displ_edge4.txt')
#path = os.getcwd()
path= filedialog.askdirectory()
files = glob.glob(os.path.join(path, "*.txt"))
print(files)

dfs = []

for file in files:
    df = pd.read_csv(file, sep='\t')
    df['source'] = os.path.basename(file)
    dfs.append(df)

df_master= pd.concat(dfs, axis=0)
filename = 'dataframe.csv'
#my_list = ['Node Number','Directional Deformation (mm)','source']
#for item in my_list:
df_node_disp= df_master.filter(['Node Number', 'Directional Deformation (mm)', 'source'])


path2= filedialog.askdirectory()
files2 = glob.glob(os.path.join(path2, "*.txt"))
print(files2)

dfnodes = []

for filee in files2:
    df = pd.read_csv(filee, sep='\t',encoding='ISO-8859-1')
    df['Location'] = os.path.basename(filee)
    dfnodes.append(df)
# append all the sheet data to one dataframe:
dfn= pd.concat(dfnodes, axis=0)
filename2 = 'nodes_dataframe.csv'
dfn = dfn[dfn.filter(regex='^(?!Unnamed)').columns]
dfnf= dfn.filter(['Node ID', 'Theta(°)', 'Location'])

sorted_df = dfnf.sort_values(by=['Location','Theta(°)'], ascending=True)
#renane the column heading to be common between the two dataframe where merge can be done
df_rename = sorted_df.rename(columns={'Node ID': 'Node Number'})
print(df_rename)
##The pandas .merge() method allows us to merge two DataFrames together.##
##VLOOKUP is essentially a left join between two tables, that is,
# the output consists of all the rows in the left table and only the matched rows from the right table.#

df33= pd.merge(df_node_disp,df_rename, how='left')
df3 = df33.sort_values(by=['source','Theta(°)'], ascending=True)
# unique names from the dataframe
uniqueNames = df3['source'].unique().tolist()
print(uniqueNames)
df_names = dict()
for k, v in df3.groupby('source'):
    df_names[k] = v


#define number of rows and columns for subplots

# writing all the dictionary data to one excel group
for df_name, df in df_names.items():

     # df.sort_values(by=['Theta(°)'], ascending=True)
     values = df[['Theta(°)','Directional Deformation (mm)']]
     #values = df_names['disp_edge3XAxis.txt'][['Theta(°)', 'Directional Deformation (mm)']]
    #print(values)
     ax= values.plot.line(x='Theta(°)',y='Directional Deformation (mm)',rot=0)
     plt.savefig(str(df_name)+'.jpg',bbox_inches='tight', dpi=100)
    #plt.show()
     plt.close()

with pd.ExcelWriter('results1.xlsx',engine="xlsxwriter") as writer:

#writer.sheets = dict((ws.title, ws) for ws in book1.worksheets)
    for df_name, df in df_names.items():
       # df.sort_values(by=['Theta(°)'], ascending=True)
        df.to_excel(writer, sheet_name=str(df_name))


#for elem in uniqueNames:
print(df_names)
df_stack = pd.concat(df_names, axis=0)

#df_master.to_csv(path +'_'+filename,index=False)


#print(df_names)
print(df_names['disp_edge1XAxis.txt'])
df_stack.to_csv(path +'_'+filename2,index=False)


"""$df2 = pd.read_csv(fpath, sep='\t' )
df2 = df2[df2.filter(regex='^(?!Unnamed)').columns]
print(df2)
print(df2.shape)
print(df2.columns)
# execute(fpath)
print(fpath)"""