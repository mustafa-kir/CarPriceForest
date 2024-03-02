from modelEgitici import ModelEgitici
import matplotlib.pyplot as plt
import pandas as pd

class Tahminci(ModelEgitici):
    def __init__(self, dosyaAdi):
        super().__init__(dosyaAdi)

    def tahminYap(self, girdi_verisi):
        # Girdi verisi için tahmin yapma işlemleri
        print(girdi_verisi) # Çıktı ['A1', 2017, 'Manual', 15000, 'Petrol', 150, 55.4, 1.4]

        arabaMarkasi = girdi_verisi.pop(0)
        sirket_adi = girdi_verisi.pop()
        Xcolumns = self.x.columns.tolist()
        
        girdi_verisiDF = pd.DataFrame([girdi_verisi], columns=['model', 'year', 'transmission', 'mileage', 'fuelType', 'tax', 'mpg', 'engineSize'])
        
        # Kategorik ve sayısal özellikleri ayırt et
        categorical_features = girdi_verisiDF.select_dtypes(include=[object]).columns.tolist()
        numerical_features = girdi_verisiDF.select_dtypes(exclude=[object]).columns.tolist()
    
        # One-hot encoding için boş bir DataFrame oluştur
        encoded_df = pd.DataFrame(columns=Xcolumns)
        
        # Kategorik özellikler için one-hot encoding uygula
        for feature in categorical_features:
            # Her kategorik özelliğin değerini sütun adı olarak kullan
            encoded_feature = f"{feature}_{girdi_verisiDF.loc[0, feature]}"
            if encoded_feature in Xcolumns:
                encoded_df[encoded_feature] = [1]
            else:
                print(f"{encoded_feature} is not in the columns.")
        
        # Sayısal özellikleri kopyala
        for feature in numerical_features:
            if feature in Xcolumns:
                encoded_df[feature] = girdi_verisiDF[feature]
            else:
                print(f"{feature} is not in the columns.")
        
        # Eksik sütunları doldur
        for col in encoded_df.columns:
            if encoded_df[col].isnull().all():
                encoded_df[col] = [0]
        
        
        print(encoded_df)
        self.modelSec(sirket_adi,arabaMarkasi) # burada sadece şirket adını ve araba markası veriyorsun
        
        tahmin = self.model.predict(encoded_df)
        
        return tahmin[0]
        
            


