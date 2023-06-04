import matplotlib.pyplot as mtp
import numpy as np
from sklearn.cluster import KMeans
df2 = pd.read_csv("Mall_Customers.csv")
x = df2.iloc[:,[3, 4]].values
y = df2["Spending Score (1-100)"]
print(df2.head())
#print(x)
wcss_list = []
for i in range(1, 11):  
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state= 42)  
    kmeans.fit(x)  
    wcss_list.append(kmeans.inertia_)  
mtp.plot(range(1, 11), wcss_list)  
mtp.title('The Elobw Method Graph')  
mtp.xlabel('Number of clusters(k)')  
mtp.ylabel('wcss_list')  
mtp.show()
kmeans = KMeans(n_clusters = 5, init = 'k-means++', random_state= 42) 
y_predict = kmeans.fit_predict(x)
mtp.scatter(x[y_predict == 0, 0], x[y_predict == 0, 1], s = 100, c = 'pink', label = 'Cluster 1')   
mtp.scatter(x[y_predict == 1, 0], x[y_predict == 1, 1], s = 100, c = 'violet', label = 'Cluster 2') 
mtp.scatter(x[y_predict== 2, 0], x[y_predict == 2, 1], s = 100, c = 'green', label = 'Cluster 3')
mtp.scatter(x[y_predict == 3, 0], x[y_predict == 3, 1], s = 100, c = 'blue', label = 'Cluster 4')
mtp.scatter(x[y_predict == 4, 0], x[y_predict == 4, 1], s = 100, c = 'black', label = 'Cluster 5') 
mtp.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 300, c = 'yellow', label = 'Centroid')   
mtp.title('Customer Cluster')  
mtp.xlabel('Annual Income (k$)')  
mtp.ylabel('Spending Score (1-100)')  
mtp.legend()  
mtp.show()  
