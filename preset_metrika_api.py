#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#Таймер

import time

#Для загрузок
import json
import requests
from pprint import pprint
from yaml import load
        


class metrika_preset:
    
    def __init__ (self, data_type, preset, date):
        
        
        #Хранилище данных
        
        self.data = []
        
        
        
        #Настройки сбора информации
        
        self.data_type = data_type
        
        self.preset = preset  
        
        self.date = date
        

            
            
        
    
    def upload (self, data):
        
        
        print ('Библиотека Preset_Metrika. Разработка - IMVO.site.')
        print ('Последнее обновление - 23.05.2019.')
        print ('Скорректирована архитектура программы, повышена точность и устойчивость, настроены метки прохода')
        print ('')
        print ('Набор доступных команд в запросе: 1 - Custom, Preset, 2 - Preset, Custom_Upload, 3 - Mounth, Year')
        


        #Загрузка конфига

        f = open('config.yaml', 'r')
        config = load(f)
        token2 = config['token']
        
        
        API_URL = 'https://api-metrika.yandex.ru/stat/v1/data'
        headers = {'Authorization': 'OAuth ' + token2}
        
        
        if self.date == 'mounth':
            startDate = str(config['start_date'])
            endDate = str(config['end_date'])
            
            
        if self.date == 'year':
            startDate = str(config['year_start_date'])
            endDate = str(config['year_end_date'])
            
        
        counter = str(config['yandex_counter'])
        


        #Функция запроса
        
        def vigryzka(offset, n_rows):
    
            params = {
            'date1': startDate,
            'date2': endDate,
            'id': counter,
            'offset': offset,
            'limit': n_rows,
            'accuracy': 'full',
            }
        
            if self.data_type == 'preset':
                params.update({'preset':self.preset, })
                
            else:

                params.update({'dimensions':self.preset[0], })
                params.update({'metrics':self.preset[1], })
                
                
            r = requests.get(API_URL, params=params, headers=headers) 
            data = r.json()
            return r.json()
        
        
        
        
        
        #Вызов функции запроса

        n_rows = 500
        offset = 1
        
        
        try:
            dataset = vigryzka(offset, n_rows)
            self.data += dataset['data']
            
        except:
            print ('Ошибка в получении данных')
            
        timer = 1
        
        
        
        #Цикл получения данных
        
        while len (dataset['data']) > 0:
            
            
            offset += n_rows            
            dataset = vigryzka(offset, n_rows)  
            self.data += dataset['data']
            
            timer += 1
            
            if timer / 10 == int (timer / 10):
                print ('Завершен проход данных {}, следующая строка - {}'.format(timer, offset))
      
            
            time.sleep(1)
            
            
            
            
            
        print ('Успешно завершено. Тип отчета - {}, длина отчета - {}'.format(self.data_type, len(self.data)))
        

