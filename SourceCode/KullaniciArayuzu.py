from carGuess_DesingerSourceCode import Ui_MainWindow
from tahmin import Tahminci
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
import pandas as pd
import sys
import os

class KullaniciArayuzu(QMainWindow):
    def __init__(self,dosyaAdi):
        super().__init__()
        self.ui = Ui_MainWindow()  # Assuming this is a generated UI class
        self.tahminci = Tahminci(dosyaAdi)
        self.ui.setupUi(self)
        self.load_car_brands()
        self.ui.cBox_CarBrand.currentIndexChanged.connect(self.load_car_models)
        self.ui.cBox_CarBrand.currentIndexChanged.connect(self.load_fuel_types)
        self.ui.cBox_CarBrand.currentIndexChanged.connect(self.update_company_choices)
        self.ui.cBox_CarBrand.currentIndexChanged.connect(self.update_Transmission_choices)
        
        self.ui.calculator_btn.clicked.connect(self.predict_car_price)
    def load_car_brands(self):
        dataset_folder = "dataSets"
        try:
            for filename in os.listdir(dataset_folder):
                if filename.endswith(".csv"):
                    brand_name = filename.replace(".csv", "")
                    self.ui.cBox_CarBrand.addItem(brand_name)
        except Exception :
           pass

    def load_car_models(self):
        selected_brand = self.ui.cBox_CarBrand.currentText() + ".csv"
        dataset_folder = "dataSets"
        filepath = os.path.join(dataset_folder, selected_brand)

        try:
            df = pd.read_csv(filepath)
            models = df["model"].unique()
            self.ui.cBox_CarModel.clear()  # Clear previous models
            for model in sorted(models):
                self.ui.cBox_CarModel.addItem(model)
        except Exception:
            pass
    
    def update_Transmission_choices(self):
        selected_brand = self.ui.cBox_CarBrand.currentText() + ".csv"
        dataset_folder = "dataSets"
        filepath = os.path.join(dataset_folder, selected_brand)
        
        try:
            df = pd.read_csv(filepath)
            models = df["transmission"].unique()
            self.ui.cBox_CarTransmission.clear()  # Clear previous models
            for model in sorted(models):
                self.ui.cBox_CarTransmission.addItem(model)
        except Exception:
            pass
    
    def load_fuel_types(self):
        selected_brand = self.ui.cBox_CarBrand.currentText() + ".csv"
        dataset_folder = "dataSets"
        filepath = os.path.join(dataset_folder, selected_brand)

        try:
            df = pd.read_csv(filepath)
            fuel_types = df["fuelType"].unique()
            self.ui.cbx_FuelType.clear()  # Clear previous fuel types
            for fuel_type in sorted(fuel_types):
                self.ui.cbx_FuelType.addItem(fuel_type)
        except Exception:
            pass

    def update_company_choices(self):
        self.ui.cBox_ChooseCompany.clear()
        company_choices = ["First_Company", "Second_Company", "Third_Company", "Fourth Company"]
        self.ui.cBox_ChooseCompany.addItems(company_choices)

    def predict_car_price(self):
        
        car_brand = self.ui.cBox_CarBrand.currentText()
        car_year = self.ui.date_CarYear.date().year()
        car_model = self.ui.cBox_CarModel.currentText()
        car_mileage = self.ui.sBox_Mileage.value()
        car_engine_size = self.ui.dSBox_EngineSize.value()
        car_fuel_type = self.ui.cbx_FuelType.currentText()
        car_tax = self.ui.sBox_Tax.value()
        car_mpg = self.ui.dSBox_MPG.value()
        car_Company = self.ui.cBox_ChooseCompany.currentText()
        car_Transmission = self.ui.cBox_CarTransmission.currentText()
        self.ui.CarGuessPrice_lbl.setText("")   
        predict_values = [car_brand, car_model,car_year,car_Transmission, car_mileage,car_fuel_type,car_tax,car_mpg,car_engine_size,car_Company]
        
        if car_model == "" or car_engine_size == 0 or car_year == 0 or car_mpg == 0:
            self.ui.info_lbl.setText("Tüm Bilgileri Doldurun") 
        else:
            self.ui.CarGuessPrice_lbl.setText(str(self.tahminci.tahminYap(predict_values)))  

        
      
        

app = QtWidgets.QApplication(sys.argv)
dosya_adi = "audi.csv"
win = KullaniciArayuzu(dosya_adi)
win.show()
sys.exit(app.exec_())