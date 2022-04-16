#!/usr/dbt/bin/env python3

import os
import sys
import re
import pdfplumber
import pandas as pd
from collections import namedtuple

Inv = namedtuple('Inv', ['vendor', 'invoice', 'date','currency', 'amount', 'vat','units','picking_cost', 'goodsin_cost'])

def get_files(folder):
    """ Get PDF files from folder""" 

    os.chdir(folder)
    files = os.listdir()
    files = [os.path.join(folder,x) for x in files if x.endswith(".pdf")]
    return files 

def load_patterns(vendor):
    """ Load patterns for invoice number, date, amount, units and picking cost"""

    patterns = {'currency': re.compile(r'(Amount\s?)(USD|EUR|GBP)', re.IGNORECASE)}

    if vendor == 'PackShack Limited':
        packshack = {
            'inv_num_re': re.compile(r'(inv-).*\d+$', re.IGNORECASE),
            'inv_date_re':re.compile(r'(\d{2}/\d{2}/\d{4}|\d\d?\w{3}\d{4}$)'),
            'inv_amt_re': re.compile(r'(AmountDue)\s*(\d[\d,]+\.?\d+)', re.IGNORECASE),
            'pick_cost_re': re.compile(r'(^Picking\s?Cost).+[^\\n]', re.IGNORECASE),
            'goodsin_cost_re': re.compile(r'(^goodsin\s?Cost).+[^\\n]', re.IGNORECASE),
        }
    
        patterns.update(packshack)
    return patterns.values()

def search_patters (pattern, text, gr=0):
    """ Search for pattern in text"""

    search = [ pattern.search(line) for line in text.split('\n')]
    res = next (( item for item in search if item is not None), 'Not Found')
    return res.group(gr) if isinstance(res, re.Match) else res


def process_text(file, vendor ):
    with pdfplumber.open(file) as pdf:

        text = ""
        cur_re, inv_num_re , inv_date_re, inv_amt_re, pick_cost_re, goodsin_cost_re  = load_patterns(vendor)

        for page in pdf.pages:
            text += page.extract_text()

        # Invoice Currency
        cur = search_patters(cur_re, text, 2)
        # Invoice Amount
        inv_amt = search_patters(inv_amt_re, text, 2)
        # Invoice Number
        inv_num = search_patters(inv_num_re, text, 0)
        # Invoice Date
        inv_date = search_patters(inv_date_re, text, 0)

        # Picking Cost
        pick_cost = search_patters(pick_cost_re, text, 0).replace('Zero Rated','0')
        pick_cost = pick_cost.replace('Zero Rated','0').strip()
        try:
            _ , qt, pk_unit_price, vat, pick_total = pick_cost.split()
        except:
            qt, pk_unit_price, vat, pick_total = '0', '0', '0', '0'

        # Goods In Cost
        goodsin_cost = search_patters(goodsin_cost_re, text, 0).replace('Zero Rated','')
        try:
            _ , qt, gi_unit_price, vat, gi_total = goodsin_cost.split()
        except:
            gi_unit_price, vat, gi_total = '0', '0', '0'

    return Inv( vendor, 
                inv_num, 
                inv_date, 
                cur,
                inv_amt, 
                vat, 
                qt, 
                pk_unit_price, 
                gi_unit_price )


def main():
    folder = sys.argv[1]
    files = get_files(folder)
    invs = [process_text(file, file.split('/')[-1].split('-')[0].strip()) for file in files]
    
    # Create DataFrame and format columns for visualization
    df = pd.DataFrame(invs)
    df['date'] = pd.to_datetime(df['date'], format='%d%b%Y')
    df['amount'] = df['amount'].str.replace(',','').astype(float)
    df['picking_cost'] = df['picking_cost'].str.replace(',','').astype(float)
    df['goodsin_cost'] = df['goodsin_cost'].str.replace(',','').astype(float)

    # save Excel file to local directory
    df.to_excel('invoices.xlsx',index=False)
    

#usage python pdfreader.py /home/rribeiro/pdfs/ 

if __name__ == '__main__':

    if len(sys.argv) > 1:
        main()
    else:
        print("Usage: python3 pdfreader.py <folder>")

