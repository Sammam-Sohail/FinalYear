
values = [i for i in range(30,0,-1)]
values = np.reshape(values, (-1,1))
scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit(values)
print(scaler.transform(values))
