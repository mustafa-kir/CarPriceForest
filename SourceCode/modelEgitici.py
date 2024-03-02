import numpy as np
from sklearn.metrics import mean_squared_error
from veriIsleme import VeriIsleme
from keras.layers import Dense
from keras.models import Sequential
from keras.models import load_model
import os
import pickle 

class ModelEgitici(VeriIsleme):
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    def __init__(self, dosyaAdi):
        super().__init__(dosyaAdi)
        self.veriYukle()
        self.model = None
        self.model_dosya_yolu = "saveLearning/"

    def modelSec(self, sirket_adi,arabaMarkasi):
        model_dosya_adi = self.model_dosya_yolu + arabaMarkasi+ "_" + sirket_adi + ".h5"
        
        # Eğer model dosyası mevcutsa, modeli yükle
        if os.path.exists(model_dosya_adi):
            self.model = self.modeliYukle(model_dosya_adi)
        else:
            print("geldi: modelSec/else")
            # Modeli oluştur ve eğit
            if sirket_adi == "First_Company":
                print("geldi: modelSec/else/first_company")
                konfig = {'katmanlar': [12, 12, 12, 12], 'aktivasyon': 'relu', 'optimizer': 'adam'}
                print("geldi: modelSec/else/first_company/konfig : ", konfig)
            elif sirket_adi == "Second_Company":
                konfig = {'katmanlar': [128, 64, 32], 'aktivasyon': 'sigmoid', 'optimizer': 'sgd'}
            elif sirket_adi == "Third_Company":
                konfig = {'katmanlar': [128, 128], 'aktivasyon': 'tanh', 'optimizer': 'rmsprop'}
            elif sirket_adi == "fourth_Company":
                konfig = {'katmanlar': [128, 128], 'aktivasyon': 'elu', 'optimizer': 'adamax'}
            
            self.model = self.modelOlustur(konfig)
            self.modelEgit(self.model, 300, 150)
            self.modelKaydet(self.model, sirket_adi, arabaMarkasi)
        return self.model
    
    def modelOlustur(self, konfig):              
        model = Sequential()
        for katman in konfig['katmanlar']:     
            if model.layers:
                model.add(Dense(katman, activation=konfig['aktivasyon']))
            else:
                model.add(Dense(katman, activation=konfig['aktivasyon'], input_dim=self.x_train.shape[1]))
        model.add(Dense(1))
        model.compile(optimizer=konfig['optimizer'], loss='mse')
        return model
    
    def modelEgit(self, model, epochs=10, batch_size=10):
               
        model.fit(x = self.x_train, y = self.y_train, epochs=epochs, batch_size=batch_size)
        y_pred = model.predict(self.x_test)
        # print(self.y_test, y_pred)
        # hata = mean_squared_error(self.y_test, y_pred)
        
      
    def modelKaydet(self,model, sirket_adi, arabaMarkasi):
        # Eğitilmiş modeli dosyaya kaydetme işlemleri
        dosya = "saveLearning/" + arabaMarkasi+ "_" + sirket_adi + ".h5"  
        model.save(dosya)
        
    
    def modeliYukle(self, dosya_adi):
        dosya =  dosya_adi 
        return load_model(dosya)