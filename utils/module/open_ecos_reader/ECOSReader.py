import requests
import json
import pandas as pd
import logging
from collections import namedtuple

class ECOSReader():
    """_summary_
    #TODO : doc string
    """
    def __init__(self, api_key, language='kr'):
        with open(api_key, 'r') as f:
            api_key = json.load(f)
            key = api_key['key']
        self.api_key = key
        self.language = language

    # def _request(self, service, start_date, end_date, code, cycle, offset, start=1, end=1000):
    def _request(self, service, **kwargs):

        
        url = f'http://ecos.bok.or.kr/api/{service}/{self.api_key}/json/{self.language}/'
        
        if kwargs.get('start'):
            start = kwargs['start']
            url += f'{start}/'
        if kwargs.get('end'):
            end = kwargs['end']
            url += f'{end}/'
        if kwargs.get('code'):
            code = kwargs['code']
            url += f'{code}/'
        if kwargs.get('cycle'):
            cycle = kwargs['cycle']            
            url += f'{cycle}/'        
        if kwargs.get('start_date'):
            start_date = kwargs['start_date']
            url += f'{start_date}/'
        if kwargs.get('end_date'):
            end_date = kwargs['end_date']
            url += f'{end_date}/'
        assert((end - start) > 0)

        ret = requests.get(url)

        if ret.status_code != 200:
            print({'status_code' : ret.status_code, 'text' : ret.text})
            raise Exception("not response")

        try:
            ret_json = json.loads(ret.text)
            # print(ret_json)
            if ret_json.get(service) == None:                
                raise Exception('No service')
            total_size = ret_json[service]['list_total_count']            
            return total_size, pd.DataFrame(ret_json[service]['row'])

        except Exception as e:
            print(f"{ret_json['RESULT']['CODE']}, {ret_json['RESULT']['MESSAGE']}", e)

    def statistic_list(self, start = 1, end = 1000):
        """_summary_
        #TODO : doc string
        """        
        service = 'StatisticTableList'
        
        total_size, df = self._request(service, 
                                       start = start, 
                                       end = end)
        
        return total_size, df
    
    
    def statiscic_search(self, start_date, end_date, code, cycle, start = 1, end = 1000):
        """_summary_
        #TODO : doc string
        """                
        service = 'StatisticSearch'      
        offset = 1000
            
        total_size, df = self._request(service, 
                                       start_date = start_date, 
                                       end_date = end_date, 
                                       code = code, 
                                       cycle = cycle, 
                                       offset = offset, 
                                       start = start, 
                                       end = end)
        
        for index in range(end+1, total_size, offset):
            start = index
            end = index+offset
            _, temp_df = self._request(service, 
                                        start_date = start_date, 
                                        end_date = end_date, 
                                        code = code, 
                                        cycle = cycle, 
                                        offset = offset, 
                                        start = start, 
                                        end = end)

            df = pd.concat([df, temp_df], axis=0)

        return df
        