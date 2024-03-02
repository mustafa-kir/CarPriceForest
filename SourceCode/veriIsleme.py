import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

class VeriIsleme:
    
    def __init__(self, dosyaAdi ):
        self.veriler = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.x = None
        self.y = None
        self.dosyaAdi = dosyaAdi
        # burada dosya yolu ile verileri okuyacak ve daha sonra eğitim, test olarak ayırarak atama işlemi yapılcak    
    
    def veriYukle(self):
        dosyaAdi = "dataSets/" + self.dosyaAdi 
        # Veri setini yükleme işlemleri
        self.veriler = pd.read_csv(dosyaAdi)
        self.y = self.veriler["price"].values
        self.x = self.veriler.drop("price", axis=1)
               
        # veri temizleme işlemi
        self.veriTemizleme()
        
        # Kategorik sütunları sayısal değerlere dönüştürme
        self.x = self.kategorikVerileriDönüştür(self.x)
        
        # Eksik veri var mı ?
        if self.veriler.isnull().any().any():
            self.eksikVeriDoldur()

        self.verileriAyır()
        
        # scaler işelmi yap
        self.verileriScalerIslemi()
        
        
    def eksikVeriDoldur(self, strategy='mean'):
        # Eksik verileri doldurma işlemleri
        imputer = SimpleImputer(missing_values=np.nan, strategy=strategy)
        self.x = imputer.fit_transform(self.x)
        
    def veriTemizleme(self):
        # verilerde en yüksek olan verilerin %1'i çıkarma
        temizlenmisVeriler = self.veriler.sort_values("price", ascending= False).iloc[131:] 
        self.veriler = temizlenmisVeriler
    
    def kategorikVerileriDönüştür(self, X):
        # Kategorik ve sayısal sütunları işleme
        categorical_features = X.select_dtypes(include=[object]).columns
        
        ohe = OneHotEncoder(sparse_output=False, drop='first')
        encoded_features = pd.DataFrame(ohe.fit_transform(X[categorical_features]))
        encoded_features.columns = ohe.get_feature_names_out(categorical_features)
        
        X = X.drop(categorical_features, axis=1)
        X= pd.concat([X.reset_index(drop=True), encoded_features.reset_index(drop=True)], axis=1)
        
        return X
    
    def verileriScalerIslemi(self):
        
        scaler = MinMaxScaler()
        self.x_train = scaler.fit_transform(self.x_train)
        self.x_test = scaler.transform(self.x_test)
        

    def verileriAyır(self, test_boyutu=0.2, random_state=0):
        # Veriyi eğitim ve test setlerine ayırma işlemleri
        self.x_train, self.x_test,self.y_train,self.y_test = train_test_split(self.x,self.y,test_size=test_boyutu, random_state=random_state)
        

dosya_adi = "audi.csv"  # Dosya adını belirtiniz
vi = VeriIsleme(dosya_adi)
vi.veriYukle()
