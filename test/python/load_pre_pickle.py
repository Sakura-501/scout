import pickle


prefeature_pickleload_name=r"C:\Users\Lenovo\Desktop\python3Project\school\works\scout\traindata\pre_feature-default.pkl"
fileopen=open(prefeature_pickleload_name,"rb")
pickle_loaddata=pickle.load(fileopen)
fileopen.close()
print(pickle_loaddata.feature_value)
print(len(pickle_loaddata.feature_value))
print(pickle_loaddata.label_value)
print(len(pickle_loaddata.label_value))