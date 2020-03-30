import os
import json
import requests
import config


class Holdings():

    def __init__(self):
        try:
            config.API_KEY
        except NameError, err:
            print(err)
            config.API_KEY = 'dummy_token'

        token = 'Bearer ' + config.API_KEY
        self.nmax = 2000
        self.header = {'Authorization': token}
        self.base_url = "https://api.adsabs.harvard.edu/v1/search/query"

    def fetch(self, bibstem, getyear):

        # make sure query params are URL encoded (esp. bibstems w/ampersand)
        if isinstance(bibstem, str):
            bibstem = requests.utils.quote(bibstem)
        else:
            # bibstem must be a string -- if it's not, just return
            print("Holdings.fetch: Bad type for bibstem: %s" % type(bibstem))
            return []
        # getyear can be an integer (1994) or str ('1990-1994')
        if isinstance(getyear, str):
            getyear = requests.utils.quote(getyear)
        try:
            query = "?q=bibstem:" + bibstem + \
                    "+year:" + str(getyear) + \
                    "&fl=year,volume,page,esources&rows=" + str(self.nmax)
            url = self.base_url + query
            nstart = 0
            total_results = 1
            output_array = list()
            while nstart < total_results:
                qstart = url + "&start=" + str(nstart)
                r = requests.get(qstart, headers=self.header)
                query_data = r.json()

                response_hdr = query_data['responseHeader']

                response = query_data['response']
                total_results = response['numFound']
                docs = response['docs']
                output_array = output_array + docs
                nstart = nstart + self.nmax
        except Exception, err:
            print("Error in Holdings.fetch: %s" % err)
            return []
        else:
            return output_array

    def load_json(self,infile):
        output_array = []
        if not os.path.exists(infile):
            print "file does not exist:",infile
        else:
            with open(infile,'rU') as fhold:
                json_data = json.load(fhold)
                if json_data['responseHeader']['status'] == 0:
                    output_array = json_data['response']['docs']
                else:
                    print "problem loading json:",json_data['responseHeader']
        return output_array
        

    def process_output(self, output_array):

        try:
            holdings_list = dict()
            for paper in output_array:
                try:
                    vol = paper['volume']
                    pg = paper['page'][0]
                    bs = paper['bibstem'][0]
                    yr = int(paper['year'])
                    try:
                        eso = self.convert_esources_to_int(paper['esources'])
                    except Exception, err:
                        # print "Error:", err
                        eso = 0
                    outdict = {'page': pg, 'year': yr, 'esources': eso}
                    if bs in holdings_list:
                        holdings_list[bs].append(outdict)
                    else:
                        holdings_list[bs] = [outdict]
                except Exception, err:
                    # print("Paper: %s" % paper)
                    # print("Error in Holdings.process_output: %s" % err)
                    pass
        except Exception, err:
            print("Error in Holdings.process_output: %s" % err)
            return {}
        else:
            return holdings_list

    def convert_esources_to_int(self, esource_array):
        try:
            bin_int_string = ''
            for p in config.ESOURCE_LIST:
                if p in esource_array:
                    bin_int_string = bin_int_string + '1'
                else:
                    bin_int_string = bin_int_string + '0'
            bin_int_string = '0b' + bin_int_string
            esources_out = int(bin_int_string, 2)
        except Exception, err:
            print 'Error:', err
            esources_out = 0
        return esources_out
