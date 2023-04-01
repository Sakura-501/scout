predict_result=[1,1,0,1,1,1,0,1,0,0,0,1,1,0,0,0,1,0]
label_value=   [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]

TP,TN,FP,FN=0,0,0,0
for i in range(len(predict_result)):
    if (label_value[i]==1 and predict_result[i]==1):
        TP+=1
    elif (label_value[i]==0 and predict_result[i]==0):
        TN+=1
    elif (label_value[i]==0 and predict_result[i]==1):
        FP+=1
    elif (label_value[i]==1 and predict_result[i]==0):
        FN+=1
accuracy=(TP+TN)/(TP+TN+FP+FN)
precision=TP/(TP+FP)
recall=TP/(TP+FN)
F1=(2*precision*recall)/(precision+recall)
print(accuracy)
print(precision)
print(recall)
print(F1)