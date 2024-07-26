import numpy as np
import pandas as pd
import os
import argparse
from module import data_module

class GraphData():

    def __init__(self):
        self.module_functions = {
            'kospi_mdd': data_module.make_kospi_MDD,
            'sp500_mdd': data_module.make_sp500_MDD,
            'kospi_monthly_returns' : data_module.monthly_returns,
            'sp500_monthly_returns' : data_module.monthly_returns,
            'korea_nsi' : data_module.load_korea_nsi,
        }

    def run(self):
        d = vars(self.args)

        if d['list'] == 'all':
            for g in self.module_functions.keys():
                print(f"- {g}")
            return

        graph_name = d['graph_name']
        _key = d['key']
        if  graph_name == 'korea_nsi':
            print("Korea News Sentiment Index Data generate")
            dstfile = "../website/dashboard_blog/posts/nsi/result_korea_NSI.csv"
            self.module_functions[graph_name](dstfile, _key)

        if graph_name == 'sp500_mdd':
            dstfile = "../website/dashboard_blog/posts/sp500_mdd/result_sp500_mdd.csv"
            self.module_functions[graph_name](dstfile, _key)

        elif graph_name == 'kospi_mdd':
            dstfile = "../website/dashboard_blog/posts/kospi_mdd/result_kospi_mdd.csv"
            self.module_functions[graph_name](dstfile, _key)

        elif graph_name == 'kospi_monthly_returns':
            dstfile = "../website/dashboard_blog/posts/kospi_monthly_returns/result_kospi_monthly_returns.csv"
            data_module.monthly_returns(name = 'KS11', dstfile = dstfile, key= _key)

        elif graph_name == 'sp500_monthly_returns':
            dstfile = "../website/dashboard_blog/posts/sp500_monthly_returns/result_sp500_monthly_returns.csv"
            data_module.monthly_returns(name = 'US500', dstfile = dstfile, key= _key)



    def get_arguments(self):
        parser = argparse.ArgumentParser(prog='Graph Data Generator',
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        description=' each graph name has necessary data.\n use -l option to check all graph names',
                                        epilog='There are several graph names')
        parser.add_argument('-filename', help=': a filename of the new dataframe')
        parser.add_argument('-list', help=": list all graph names")
        parser.add_argument('-graph_name', type=str)
        parser.add_argument('-key', type=str)
        self.args = parser.parse_args()


if __name__ == '__main__':
    graphs = GraphData()
    graphs.get_arguments()
    graphs.run()






