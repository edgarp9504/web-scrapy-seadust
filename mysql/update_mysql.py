import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from conection_sql.model import TripAdvisorTable, FacebookTable,GoogleTable, BookingTable, ExpediaTable
from conection_sql.conection import Base, engine, SessionLocal


class CargaSQL:
    
    def __init__(self):
        Base.metadata.create_all(engine)
        self.db = SessionLocal()

        self.date_inter = datetime.strftime(datetime.now() - timedelta(20), '%d/%m/%Y')
        self.load_tripadvisor()
        self.load_facebook()
        self.load_google()
        self.load_booking()
        self.load_expedia()
    
    def validate_data(self, dataframe, query):
        df_query = pd.DataFrame(query)
        df = dataframe.merge(df_query, on='nombre', how = 'left') 
        df = df[df['review_y'].isnull()]        
        df.rename(columns = {'review_x' : 'review'}, inplace = True)
        df = df.reset_index()
        return df
    
    
    def load_tripadvisor(self):
        
        df_tripadvisor = pd.read_csv("./csv_file/seadust-tripadvisor.csv")
        
        try:
            query = self.db.query(TripAdvisorTable.nombre, TripAdvisorTable.review ).filter(TripAdvisorTable.date_extract >= self.date_inter).all()
        except Exception(e):
            print(e)
        
        
        # Validando comentarios repetidos
        print('Validando datos')
        df_tripadvisor = self.validate_data(df_tripadvisor, query)

        
        print('Cargando al BD MYSQL Trip...', len(df_tripadvisor.index) )
        for index in range(len(df_tripadvisor.index)):
            db_tripadvisor = TripAdvisorTable(
                                        nombre       = df_tripadvisor['nombre'][index] ,
                                        titulo       = df_tripadvisor['titulo'][index] ,
                                        review       = df_tripadvisor['review'][index] ,
                                        estadia      = df_tripadvisor['estadia'][index] ,
                                        rating       = df_tripadvisor['rating'][index] ,
                                        date_extract = df_tripadvisor['date_extract'][index] ,
                                        )
            try:
                self.db.add(db_tripadvisor)
                self.db.commit()
                self.db.refresh(db_tripadvisor)
            finally:
                self.db.close()
        print('Insertando a MYSQL Expedia...')
    
        
    def load_facebook(self):
        
        df_facebook = pd.read_csv("./csv_file/seadust-facebook.csv")
        
        try:
            query = self.db.query(FacebookTable.nombre,FacebookTable.review ).filter(FacebookTable.date_extract >= self.date_inter).all()
        except Exception(e):
            print(e)
        

        # Validando comentarios repetidos
        print('Validando datos')
        df_facebook = self.validate_data(df_facebook, query)
        
        print('Cargando al BD Facebook...', len(df_facebook.index) )
        for index in range(len(df_facebook.index)):
            db_facebook = FacebookTable(
                                        nombre       = df_facebook['nombre'][index] ,
                                        review       = df_facebook['review'][index] ,
                                        date_extract = df_facebook['date_extract'][index] ,
                                        )
            try:
                self.db.add(db_facebook)
                self.db.commit()
                self.db.refresh(db_facebook)
            finally:
                self.db.close()
        print('Insertando a MYSQL Facebook...')
        
    
    def load_google(self):
        
        df_google = pd.read_csv("./csv_file/seadust-google.csv")
        
        try:
            query = self.db.query(GoogleTable.nombre,GoogleTable.review ).filter(GoogleTable.date_extract >= self.date_inter).all()
        except Exception(e):
            print(e)


        # Validando comentarios repetidos
        print('Validando datos')
        df_google = self.validate_data(df_google, query)
        
        print('Cargando al BD Google...', len(df_google.index) )
        for index in range(len(df_google.index)):
            db_google = GoogleTable(
                                        nombre       = df_google['nombre'][index] ,
                                        ranking      = df_google['ranking'][index] ,
                                        fecha        = df_google['fecha'][index] ,
                                        review       = df_google['review'][index] ,
                                        date_extract = df_google['date_extract'][index] ,
                                        )
            try:
                self.db.add(db_google)
                self.db.commit()
                self.db.refresh(db_google)
            finally:
                self.db.close()
        print('Insertando a MYSQL Google...')
        

    def load_booking(self):
        
        df_booking = pd.read_csv("./csv_file/seadust-booking.csv")
        
        try:
            query = self.db.query(BookingTable.nombre, BookingTable.review ).filter(BookingTable.date_extract >= self.date_inter).all()
        except Exception(e):
            print(e)


        # Validando comentarios repetidos
        print('Validando datos')
        df_booking = self.validate_data(df_booking, query)
        
        
        print('Cargando al BD Booking...', len(df_booking.index) )
        
        for index in range(len(df_booking.index)):
            db_booking = BookingTable(
                                        nombre            = df_booking['nombre'][index] ,
                                        Fecha_comentario  = df_booking['Fecha_comentario'][index] ,
                                        rating            = df_booking['rating'][index] ,
                                        titulo            = df_booking['titulo'][index] ,
                                        review_good       = df_booking['review_good'][index] ,
                                        review            = df_booking['review'][index] ,
                                        date_extract      = df_booking['date_extract'][index] ,
                                        )
            try:
                self.db.add(db_booking)
                self.db.commit()
                self.db.refresh(db_booking)
            finally:
                self.db.close()
        print('Insertando a MYSQL Booking...')


    def load_expedia(self):
        
        df_expediaC = pd.read_csv("./csv_file/seadust-expediaCOM.csv")
        df_expediaM = pd.read_csv("./csv_file/seadust-expediaMX.csv")
        
        df_expedia  = pd.concat([df_expediaC,df_expediaM], axis=0)
        df_expedia.to_csv('csv_file/seadust-expedia.csv',index = False, header=True)
        
        
        df_expedia = pd.read_csv("./csv_file/seadust-expedia.csv")

        
        try:
            query = self.db.query(ExpediaTable.nombre, ExpediaTable.review ).filter(ExpediaTable.date_extract >= self.date_inter).all()
        except Exception(e):
            print(e)


        # Validando comentarios repetidos
        print('Validando datos')
        df_expedia = self.validate_data(df_expedia, query)
        
        
        print('Cargando al BD Expedia...', len(df_expedia.index) )
        
        for index in range(len(df_expedia.index)):
            db_expedia = ExpediaTable(
                                        nombre       = df_expedia['nombre'][index] ,
                                        conceptop    = df_expedia['conceptop'][index] ,
                                        fecha_review = df_expedia['fecha_review'][index] ,
                                        critica      = df_expedia['critica'][index] ,
                                        review       = df_expedia['review'][index] ,
                                        estadia      = df_expedia['estadia'][index] ,
                                        date_extract = df_expedia['date_extract'][index] ,
                                        )
            try:
                self.db.add(db_expedia)
                self.db.commit()
                self.db.refresh(db_expedia)
            finally:
                self.db.close()
        print('Insertando a MYSQL Expedia...')
        

        
        
        
