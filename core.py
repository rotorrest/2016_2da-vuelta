from bs4 import BeautifulSoup
import pandas as pd
import lxml
from html_table_extractor.extractor import Extractor

class web:
    def ACTA_ELECTORAL(s):
        """
        Return 
        Numero de mesa      -> y1
        Numero de copia     -> y2 
        """
        x = s.find('table', attrs={'class':'table13'})
        x = str(x)
        extractor = Extractor(x)
        extractor.parse()
        x = extractor.return_list()    
        x_r = x[1]
        x_r = [w.strip() for w in x_r]
        
        y1 = x_r[0]
        y2 = x_r[1]
        return(y1, y2)

    def INFO_UBIGEO(s):
        """
        Return 
        DEPARTAMENTO	      -> y1
        PROVINCIA           -> y2 
        DISTRITO            -> y3
        LOCAL DE VOTACIÓN   -> y4
        DIRECCIÓN           -> y5
        """
        x = s.find('table', attrs={'class':'table14'})
        x = str(x)
        extractor = Extractor(x)
        extractor.parse()
        x = extractor.return_list()
        x_r = x[1]
        x_r = [w.strip() for w in x_r]  
        y1 = x_r[0]
        y2 = x_r[1]
        y3 = x_r[2]
        y4 = x_r[3]
        y5 = x_r[4]

        return(y1, y2, y3, y4,y5)


    def INFORMACION_MESA(s):
        """
        ELECTORES HÁBILES     -> y1
        TOTAL VOTANTES        -> y2
        ESTADO DEL ACTA       -> y3
        """
        x = s.find('table', attrs={'class':'table15'})
        x = str(x)
        extractor = Extractor(x)
        extractor.parse()
        x = extractor.return_list()  
        x_r = x[1]
        x_r = [w.strip() for w in x_r]  
        
        y1 = x_r[0]
        y2 = x_r[1]
        y3 = x_r[2]

        return(y1, y2, y3)

    def INFO_ACTA(s):
        """
        PERUANOS POR EL KAMBIO        -> y1
        FUERZA POPULAR                -> y2
        VOTOS EN BLANCO               -> y3
        VOTOS NULOS                   -> y4
        VOTOS IMPUGNADOS              -> y5
        TOTAL DE VOTOS EMITIDOS       -> y6
        """
        x = s.find('table', attrs={'class':'table06'})
        x = str(x)
        extractor = Extractor(x)
        extractor.parse()
        x = extractor.return_list()  
        x = pd.DataFrame(x)
        x = x[2]
        x = x.tolist()
        x = x[1:]
        x_r = [w.strip() for w in x]  

        y1 = x_r[0]
        y2 = x_r[1]
        y3 = x_r[2]
        y4 = x_r[3]
        y5 = x_r[4]
        y6 = x_r[5]
    
        return(y1, y2, y3, y4, y5, y6)

    def run(s):
        """
        Numero de mesa                -> y1
        Numero de copia               -> y2 
        DEPARTAMENTO	                -> y3
        PROVINCIA                     -> y4 
        DISTRITO                      -> y5
        LOCAL DE VOTACIÓN             -> y6
        DIRECCIÓN                     -> y7
        ELECTORES HÁBILES             -> y8
        TOTAL VOTANTES                -> y9
        ESTADO DEL ACTA               -> y10
        PERUANOS POR EL KAMBIO        -> y11
        FUERZA POPULAR                -> y12
        VOTOS EN BLANCO               -> y13
        VOTOS NULOS                   -> y14
        VOTOS IMPUGNADOS              -> y15
        TOTAL DE VOTOS EMITIDOS       -> y16
        """

        num_mesa, num_copia = web.ACTA_ELECTORAL(s)
        departamento, provincia, distrito, local, diraccion = web.INFO_UBIGEO(s)
        electores_habiles, total_votantes, estado_acta = web.INFORMACION_MESA(s)
        ppk, fp, votos_blanco, voto_nulos, votos_impugnados, votos_emitidos  = web.INFO_ACTA(s)
                
        return (num_mesa, num_copia, departamento, provincia, distrito, local, diraccion, electores_habiles, total_votantes, estado_acta, ppk, fp, votos_blanco, voto_nulos, votos_impugnados, votos_emitidos)