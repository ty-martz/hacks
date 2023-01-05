from urllib.request import urlopen
from tabula import read_pdf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pdf = urlopen("https://nsaa.org/webdocs/Media_Public/IndustryStats/Historical_Skier_Days_1979_2022.pdf")
dflist = read_pdf(pdf)

df = dflist[0]
df.columns = [x.strip().lower().replace(" ", "_").replace("(", "").replace(")", "") for x in df.iloc[1]]
df = df.drop([0,1], axis=0)
df['season'] = (df.season.str[:2] + df.season.str[-2:]).astype(int)

badrows = []
for row in range(len(df)):
    val_list = df.iloc[row]['midwest_mtn._southwest_northwest'].strip().split(" ")[:4]
    badrows.append(val_list)

add_cols = pd.DataFrame(np.array(badrows), columns=['midwest', 'rocky_mtn', 'pacific_southwest', 'pacific_northwest'])
df = df.join(add_cols)
df = df.drop(['midwest_mtn._southwest_northwest'], axis=1)
df['pacific_southwest'] = df['pacific_southwest'].str.replace('Not', '0').str.replace('NaN', '0')

for col in df.columns:
    if col != 'season':
        df[col] = df[col].str.strip().replace('Not', '0').replace('NaN', '0').replace('avail.', '0')
        df[col] = df[col].astype(float)
        df[col] = df[col].replace(0, np.nan)
df.loc[df.season == 1900, 'season'] = 2000

df = df[['season', 'northeast', 'southeast','midwest', 'rocky_mtn', 'pacific_southwest',
         'pacific_northwest', 'west_total', 'total', 'rank']]

df2 = df.copy()[['season', 'northeast', 'southeast','midwest', 'rocky_mtn', 'pacific_southwest',
         'pacific_northwest', 'west_total']]

print(df)
#print(df.info())

plt.plot(df2['season'], df2[['northeast', 'southeast','midwest', 'rocky_mtn', 'pacific_southwest','pacific_northwest']])
plt.legend(['northeast', 'southeast','midwest', 'rocky_mtn', 'pacific_southwest','pacific_northwest'])
plt.axvline(2008, color='blue', alpha=0.3, linestyle='--')
plt.show()