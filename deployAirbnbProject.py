import pandas as pd
import streamlit as st
import joblib

class PageItens:

    def __init__(self):

        self.numeric = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bedrooms': 0,
                        'bathrooms': 0,'beds': 0, 'extra_people': 0, 'minimum_nights': 0,
                        'month': 0, 'year': 0,'n_amenities': 0, 'host_listings_count': 0}
        self.boolean    = {'host_is_superhost': 0, 'instant_bookable': 0}
        self.build_categories_dict()
        self.build_categories_dummies()
    
    def build_categories_dict(self):

        property_subitens = ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite',
                             'Guesthouse', 'Hostel', 'House', 'Loft', 'Others', 'Serviced apartment']
        room_subitens     = ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room']
        cancellation_policy_subitens = ['Others', 'flexible', 'moderate', 'strict_14_with_grace_period']

        self.categories = {'property_type': property_subitens,
                           'room_type': room_subitens,
                           'cancellation_policy': cancellation_policy_subitens}

    def build_categories_dummies(self):

        self.categories_dummies = {}

        for item in self.categories:
            for subitem in self.categories[item]:
                self.categories_dummies[f'{item}_{subitem}'] = 0

class StreamLitPage:
    def __init__(self):
        self.PageItensValues = {}
        self.PageItensBoxes = PageItens()
        self.PredictButtonStatus = False

    def build_SreamLite_Page(self):

        self.add_Numeric_Boxes()
        self.add_Boolean_Boxes()
        self.add_Categories_Boxes()
        self.add_PredictButton()

    def add_Numeric_Boxes(self):
        for item in self.PageItensBoxes.numeric:
            if item == 'latitude' or item == 'longitude':
                inserted_value = self.add_Latitude_Longitude_Box(item)
            elif item == 'extra_people':
                inserted_value = self.add_Extra_People_Box(item)
            else:
                inserted_value = self.add_General_Numeric_Box(item)
            self.PageItensBoxes.numeric[item] = inserted_value

    def add_Latitude_Longitude_Box(self,item):
        return st.number_input(f'{item}', step=0.00001, value=0.0, format='%.5f')
    
    def add_Extra_People_Box(self,item):
        return st.number_input(f'{item}', step=0.01, value=0.0)
    
    def add_General_Numeric_Box(self,item):
        return st.number_input(f'{item}', step= 1, value= 0)
    
    def add_Boolean_Boxes(self):
        for item in self.PageItensBoxes.boolean:
            inserted_value = st.selectbox(f'{item}', ('Yes','No'))
            if inserted_value == 'Yes':
                self.PageItensBoxes.boolean[item] = True
            else:
                self.PageItensBoxes.boolean[item] = False

    def add_Categories_Boxes(self):
        for item in self.PageItensBoxes.categories:
            subitens_list = self.PageItensBoxes.categories[item]
            selected_subitem = st.selectbox(f'{item}', subitens_list)
            self.PageItensBoxes.categories_dummies[f'{item}_{selected_subitem}'] = 1
            
    def add_PredictButton(self):
            self.PredictButtonStatus = st.button('Predict Book Value')

    def predictButtonClick(self):
        if self.PredictButtonStatus:
            self.create_DataFrame()
            self.sort_DataToPredict()
            self.predict_Price()
            self.write_Prediction()

    def create_DataFrame(self):
        self.update_PageItensValues()
        self.DataToPredict = pd.DataFrame(self.PageItensValues, index=[0])

    def update_PageItensValues(self):
        self.PageItensValues.update(self.PageItensBoxes.numeric)
        self.PageItensValues.update(self.PageItensBoxes.boolean)
        self.PageItensValues.update(self.PageItensBoxes.categories_dummies)

    def sort_DataToPredict(self):
        model_ColumnsOrder = ['host_is_superhost', 'host_listings_count', 'latitude', 'longitude',
                              'accommodates', 'bathrooms', 'bedrooms', 'beds', 'extra_people',
                              'minimum_nights', 'instant_bookable', 'month', 'year', 'n_amenities',
                              'property_type_Apartment', 'property_type_Bed and breakfast',
                              'property_type_Condominium', 'property_type_Guest suite',
                              'property_type_Guesthouse', 'property_type_Hostel',
                              'property_type_House', 'property_type_Loft', 'property_type_Others',
                              'property_type_Serviced apartment', 'room_type_Entire home/apt',
                              'room_type_Hotel room', 'room_type_Private room',
                              'room_type_Shared room', 'cancellation_policy_Others',
                              'cancellation_policy_flexible', 'cancellation_policy_moderate',
                              'cancellation_policy_strict_14_with_grace_period']
        self.DataToPredict = self.DataToPredict[model_ColumnsOrder]

    def predict_Price(self):
        model = joblib.load('ExtraTrees_Model.joblib')
        arrayIndex = 0
        self.PredictedValue = model.predict(self.DataToPredict)[arrayIndex]

    def write_Prediction(self):
        text = 'Model Prediction: R$ {:.2f}'.format(self.PredictedValue)
        st.write(text)

if __name__ == '__main__':
    pass