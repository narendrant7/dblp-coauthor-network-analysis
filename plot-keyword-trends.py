import sys
from urllib.parse import quote
import mysql.connector
import networkx as nx
import pandas as pd
import pylab as plt2
import matplotlib.pyplot as plt
import numpy as np

def get_prolific_aids(items):
        items.sort(reverse=True, key=lambda x: x[1])
        return map(lambda x: x[0], items)


cnx = mysql.connector.connect(user='username', password='password',
                              host='host.ip.address.here',
                              port=3306,
                              database='database_name')
cursor = cnx.cursor()

keyword = sys.argv[1]
get_trends = '''SELECT x.publYear, COALESCE(COUNT,0) FROM (SELECT DISTINCT publYear FROM papers WHERE  publYear IS NOT NULL)x LEFT JOIN (SELECT publYear, COUNT(*) AS COUNT FROM papers WHERE title LIKE '%''' + keyword + '''%' AND publYear IS NOT NULL GROUP BY publYear)y ON x.publYear = y.publYear WHERE x.publYear <= 2019 ORDER BY publYear'''
trends_df = pd.read_sql(sql = get_trends, con = cnx)
x = trends_df.iloc[:,0]
y = trends_df.iloc[:,1]

plt.plot(x, y, color = 'blue')
title = 'Trends - ' + keyword
plt.title(title)
plt.xlabel('Year')
plt.ylabel('Publications')
plt.savefig('./output/graphs/Trends.png', dpi = 200)
print(title + " created")
