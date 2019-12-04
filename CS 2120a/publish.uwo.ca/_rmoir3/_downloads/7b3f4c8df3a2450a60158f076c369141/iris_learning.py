# Load iris data
from sklearn import datasets
iris = datasets.load_iris()
data = iris.data
labels = iris.target
import time

### VISUALIZATION IN 2 DIMENSIONS

from sklearn.decomposition import PCA
pca = PCA(n_components=2)

start = time.time()
transformed_pca = pca.fit_transform(data)
print("PCA transformation time: {}s".format(time.time()-start))

transformed_pca0 = transformed_pca[:50]
transformed_pca1 = transformed_pca[50:100]
transformed_pca2 = transformed_pca[100:150]

plt.scatter(transformed_pca0.T[0].T, transformed_pca0.T[1].T, color='red', label='Iris Setosa')
plt.scatter(transformed_pca1.T[0].T, transformed_pca1.T[1].T, color='green', label='Iris Versicolour')
plt.scatter(transformed_pca2.T[0].T, transformed_pca2.T[1].T, color='blue', label='Iris Virginica')

plt.title('Iris Type Clusters By PCA')
plt.legend()
plt.savefig('Iris Type Clusters By PCA.png')
plt.show()

from sklearn.manifold import TSNE
tsne = TSNE()

start = time.time()
transformed = tsne.fit_transform(data)
print("TSNE transformation time: {}s".format(time.time()-start))

import matplotlib.pyplot as plt

transformed0 = transformed[:50]
transformed1 = transformed[50:100]
transformed2 = transformed[100:150]

plt.scatter(transformed0.T[0].T, transformed0.T[1].T, color='red', label='Iris Setosa')
plt.scatter(transformed1.T[0].T, transformed1.T[1].T, color='green', label='Iris Versicolour')
plt.scatter(transformed2.T[0].T, transformed2.T[1].T, color='blue', label='Iris Virginica')

plt.title('Iris Type Clusters By t-SNE')
plt.legend()
plt.savefig('Iris Type Clusters By t-SNE.png')
plt.show()

####################################

### K Nearest Neighbours Classifier and Data Partitioning ###
# Fit (train) using kNN algorithm
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()

start = time.time()
knn.fit(data, labels)
print("KNN first fit time: {}s".format(time.time()-start))

# Compute accuracy
correct = 0
for i in range(len(data)):
    prediction = knn.predict([data[i]])
    label = labels[i]
    if prediction[0] == label:
        correct += 1
accuracy = correct / len(data)

# Accuracy
print('Accuracy: {:.1f}%'.format(accuracy*100))



#################################

### Partition into Training and Testing Sets ###

import numpy as np
data_training = np.array(data[0:40].tolist() + data[50:90].tolist() + data[100:140].tolist())
data_testing = np.array(data[40:50].tolist() + data[90:100].tolist() + data[140:150].tolist())
labels_training = np.array(labels[0:40].tolist() + labels[50:90].tolist() + labels[100:140].tolist())
labels_testing = np.array(labels[40:50].tolist() + labels[90:100].tolist() + labels[140:150].tolist())

# Refit model using separate training set
start = time.time()
knn.fit(data_training, labels_training)
print("KNN second fit time: {}s".format(time.time()-start))

# Compute training accuracy
correct = 0
for i in range(len(data_training)):
    prediction = knn.predict([data_training[i]])
    label = labels_training[i]
    if prediction[0] == label:
        correct += 1
accuracy = correct / len(data_training)

# Training accuracy
print('kNN Training accuracy: {:.1f}%'.format(accuracy*100))

# Compute testing accuracy
correct = 0
for i in range(len(data_testing)):
    prediction = knn.predict([data_testing[i]])
    label = labels_testing[i]
    if prediction[0] == label:
        correct += 1
accuracy = correct / len(data_testing)

# Testing accuracy
print('kNN Testing accuracy: {:.1f}%'.format(accuracy*100))



#################################


### SUPPORT VECTOR CLASSIFIER ###
from sklearn import svm
svc = svm.SVC(kernel='linear')

start = time.time()
svc.fit(data_training, labels_training)
print("SVC fit time: {}s".format(time.time()-start))

# Compute training accuracy
correct = 0
for i in range(len(data_training)):
    prediction = svc.predict([data_training[i]])
    label = labels_training[i]
    if prediction[0] == label:
        correct += 1
accuracy = correct / len(data_training)

# Training accuracy
print('SVC Training accuracy: {:.1f}%'.format(accuracy*100))

# Compute testing accuracy
correct = 0
for i in range(len(data_testing)):
    prediction = svc.predict([data_testing[i]])
    label = labels_testing[i]
    if prediction[0] == label:
        correct += 1
accuracy = correct / len(data_testing)

# Testing accuracy
print('SVC Testing accuracy: {:.1f}%'.format(accuracy*100))



#################################

### K Means Clustering ###
from sklearn import cluster
k_means = cluster.KMeans(4)

start = time.time()
k_means.fit(data)
print("K-Means fit time: {}s".format(time.time()-start))

# Use model to predict cluster membership
print(k_means.predict(data))
print(labels)

# Visualize the clusters
tsne = TSNE()
transformed = tsne.fit_transform(data)
colors = ['red', 'green', 'blue', 'purple']
for index, (x, y) in enumerate(transformed):
    predicted_label = k_means.predict([data[index]])
    plt.scatter(x, y, color=colors[predicted_label[0]])
plt.title('K-Means Clusters')
plt.figure()
for index, (x, y) in enumerate(transformed):
    predicted_label = [labels[index]]
    plt.scatter(x, y, color=colors[predicted_label[0]])
plt.title('Ground Truth')
plt.show()

# How else can we quantify the quality of this model?


#################################

### Automated Partitioning ###
from sklearn.model_selection import train_test_split
data_training, data_testing, labels_training, labels_testing = train_test_split(data, labels, test_size=0.4, random_state=0)
svc = svm.SVC(kernel='linear')
svc.fit(data_training, labels_training)
print(svc.score(data_testing, labels_testing))


# Automated cross validation
from sklearn.model_selection import cross_val_score
svc = svm.SVC(kernel='linear')
scores = cross_val_score(svc, data, labels, cv=5)
print(scores)

##############################