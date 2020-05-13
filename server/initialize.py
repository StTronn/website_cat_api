import pickle
import numpy as np
def load_obj(filename):
  with open('server/Dump_obj/'+filename,'rb') as obj_file:
    obj = pickle.load(obj_file)
    return obj

def store_object(obj,filename):
  with open(filename,'wb') as obj_file:
    pickle.dump(obj,obj_file)

kmeans=load_obj("kmeans")
print("kmeans loaded")
modelg=load_obj("modelg50")
print("modelg50 loaded")

def sent_vectorizer(sent, modelg=modelg):
    print("sent vectorizer function called")
    try:
        sent_vec =[]
        numw = 0
        for w in sent:

            try:
                if numw == 0:
                    sent_vec = modelg[w]
                else:
                    sent_vec = np.add(sent_vec, modelg[w])
                numw+=1
            except:
                pass
        return np.asarray(sent_vec) / numw
    except Exception as e:
        print("Sent Vectorizer Error",e)
        return e


