#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 20:58:37 2017

@author: milad
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 20:33:20 2017

@author: Milad
"""

from enum import Enum
import BShelper as soup
import browser as br

class Period (Enum):
    Annual = 0,
    Quarter = 1
         
class Financial_Info():
    def __init__(self, period, shareKey):
        self.period = period
        self.shareKey = shareKey
        self.Revenue = None
        self.GrossProfit = None
        self.NetIncome = None
        self.Assets = None
        self.Liabilities = None
        self.Equity = None
        self.LiabilitiesAndEquity = None
        self.EPS = None
        self.NetProfitMargin  = None
        self.BookValue = None
        
    def crawl(self):
        self.set1()
        self.set2()
        self.set3()
        return
        
    def navigation(self, key):
        if key in ["Revenue", "GrossProfit", "NetIncome", "Assets", "Liabilities", "LiabilitiesAndEquity", "Equity", "EPS"]:
            if key in ["Revenue", "GrossProfit", "NetIncome", "EPS"]:
                # call https://www.msn.com/en-us/money/stockdetailsvnext/financials/income_statement/annual/{shareKey}
                _url = "{}{}".format("https://www.msn.com/en-us/money/stockdetailsvnext/financials/income_statement/annual/", self.shareKey)
                _pageSource = br.url_request(_url)
                return _pageSource
            # Balance sheet tab
            elif key in ["Assets", "Liabilities", "LiabilitiesAndEquity", "Equity"]:
                # call https://www.msn.com/en-us/money/stockdetailsvnext/financials/balance_sheet/annual/{shareKey}
                _url = "{}{}".format("https://www.msn.com/en-us/money/stockdetailsvnext/financials/balance_sheet/annual/", self.shareKey)
                _pageSource = br.url_request(_url)
                return _pageSource
        elif key in ["NetProfitMargin", "BookValue"]:
            # call https://www.msn.com/en-us/money/stockdetails/analysis/{shareKey}
            _url = "{}{}".format("https://www.msn.com/en-us/money/stockdetails/analysis/", self.shareKey)
            _pageSource = br.url_request(_url)
            return _pageSource
        return

    def extractUlLi(self, block, indicator):
        _rec = list()
        _found = False
        _output = list()
        for _ultag in block.find_all("ul"):
            for _litag in _ultag.find_all("li"):
                # if the first li value equals the indicator
                if not _found and indicator not in _litag.text.strip():
                    _rec.append(_litag.text.strip())
                    break # next ul
                elif not _found:
                    _found = True
                    continue # next li
                _output.append(_litag.text.strip())
            if _found: # leave the loops
                break
        if len(_output) == 0:
            _output.append(None)
            print (_rec)
        return _output
        
    def set1(self):
        _page_source = self.navigation("Revenue")
        _soup = soup.Helper()
        _block = _soup.elemSelector( "div", {"class": "table-data-rows"}, _page_source )
        
        _ls = self.extractUlLi( _block, "Total Revenue" )
        self.Revenue = _ls[ len(_ls) - 1 ] # keep the last record
        
        _ls = self.extractUlLi(_block, "Gross Profit")
        self.GrossProfit = _ls[ len(_ls) - 1 ] # keep the last record
        
        _ls = self.extractUlLi( _block, "Net Income" )
        self.NetIncome = _ls[ len(_ls) - 1 ] # keep the last record
        
        _ls = self.extractUlLi( _block, "Basic EPS" )
        self.EPS = _ls[ len(_ls) - 1 ] # keep the last record
        return
        
    def set2(self):
        _page_source = self.navigation("Assets")
        _soup = soup.Helper()
        _block = _soup.elemSelector( "div", {"class": "table-data-rows"}, _page_source )
        _ls = self.extractUlLi(_block, "Total Assets")
        self.Assets = _ls[ len(_ls) - 1 ] # keep the last record
        
        _ls = self.extractUlLi(_block, "Total Liabilities")
        self.Liabilities = _ls[ len(_ls) - 1 ] # keep the last record
        
        _ls = self.extractUlLi(_block, "Total Equity")
        self.Equity = _ls[ len(_ls) - 1 ] # keep the last record
        
        _ls = self.extractUlLi(_block, "Total Liabilities and Equity")
        self.LiabilitiesAndEquity = _ls[ len(_ls) - 1 ] # keep the last record
        return
        
    def set3(self):
        _page_source = self.navigation("BookValue")
        _soup = soup.Helper()
        _block = _soup.elemSelector( "div", {"class": "stock-highlights-right-container"}, _page_source )
        _ls = self.extractUlLi(_block, "Book Value/Share")
        self.BookValue = _ls[ len(_ls) - 1 ] # keep the last record
        
        _ls = self.extractUlLi(_block, "Net Profit Margin")
        self.NetProfitMargin = _ls[ len(_ls) - 1 ] # keep the last record
        return
    
finObj = Financial_Info( "Per", "fi-126.1.GOOGL.NAS" )
finObj.crawl()

print (finObj.NetIncome, finObj.Revenue, finObj.EPS, finObj.GrossProfit)
print (finObj.Assets, finObj.Equity, finObj.Liabilities, finObj.LiabilitiesAndEquity)
print (finObj.BookValue, finObj.NetProfitMargin)


# http://www.msn.com/en-us/money/stockdetails/fi-200.1.{symbol}.FRA


#import cProfile
#import re
#import pstats
#cProfile.run('finObj.crawl()', 'restats')
#p = pstats.Stats('restats')
#p.strip_dirs().sort_stats(-1).print_stats()