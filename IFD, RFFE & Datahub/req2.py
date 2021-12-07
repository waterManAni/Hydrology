import requests
import pandas as pdd

def get_rffe(rfferesults):
    lines=rfferesults.replace(' ','')
    #reading xml (weird syntax hence string instead of parsing)
    dfrffe=pdd.DataFrame (columns=['aep','upper_limit','lower_limit','flow'])
    lines=lines.split('results=[{')[1].split('}]')[0]
    lines=(lines.replace('},{','};{')).replace('{','').replace('}','').split(';')
    for line in lines:
        m=line.split(',')
        k=[]
        for i in m:
           test=float((i.split(':')[1]).replace("'",''))
           k.append(test)
        dfrffe.loc[len(dfrffe)] = k
    return dfrffe

def get_datahub(dhubresult):
    ###to convert the json to pandas
    dhubjson= dhubresult.json()
    IL=pdd.DataFrame(dhubjson['layers']['BurstIL']['data'],columns=dhubjson['layers']['BurstIL']['columns'],index=dhubjson['layers']['BurstIL']['index'])
    IL.index.names = ['Duration']
    PB=pdd.DataFrame(dhubjson['layers']['Preburst50']['data'],columns=dhubjson['layers']['Preburst50']['columns'],index=dhubjson['layers']['Preburst50']['index'])
    PB.index.names = ['Duration']
    return IL,PB

def fetch_datahub(lonc,latc):
    datahub="https://data.arr-software.org/?lon_coord="+str(lonc)+"&lat_coord="+str(latc)+"&type=json&All=1"
    dhubresponse=requests.get(datahub)
    return dhubresponse

def fetch_rffe (lono,lato,lonc,latc,area):
    rffe="http://rffe.arr-software.org"
    args={
          "catchment_name":"catchment1",
          "lato":str(lato),
          "lono":str(lono),
          "latc":str(latc),
          "lonc":str(lonc),
          "area":str(area)
          }
    rfferespond=requests.post(rffe,data=args)
    return rfferespond

def fetch_IFD (latc,lonc,Name):
    url = r'http://www.bom.gov.au/water/designRainfalls/revised-ifd/?coordinate_type=dd&latitude={0}&longitude={1}&user_label={2}&design=ifds&sdmin=true&sdhr=true&sdday=true&nsd%5B%5D=&nsdunit%5B%5D=m&values=depths&update='.format(str(latc),str(lonc),Name)
    #Request data
    page = requests.get(url,
                    headers={'User-agent': 'Mozilla/5.0'},
                    #proxies={"http":"http://GATEWAY.GHD.ZSCALER.NET:80"}##proxies may be required if connected in the office
                    ).text
    #-----Remove '%' symbols which mess with formatting
    df = pdd.read_html(page.replace('%',''))[0]
    #-----Change from multilevel to single level columns
    df.columns = df.columns.droplevel()
    #---------Removed unnamed columns and columns for winter factors etc... so only IFD data remains
    df = df.loc[:,~df.columns.str.contains('^Unnamed')]
    df = df[~df['Duration'].str.contains('factor')]
    #------Remove # and * symbols from columns names
    df.columns=df.columns.str.replace('#','')
    df.columns=df.columns.str.replace('*','')
    df.set_index('Duration', inplace=True)
    df = df.apply(pdd.to_numeric)
    return df, page, url


def save_results_to_files (catchment,folderpath,ifdresponse,dhubresponse,rfferesponse):
    import os
    with open(os.path.join (folderpath,catchment+"_data-hub.txt"), "w") as dhubfile:
        dhubfile.write(dhubresponse.text)
    
    with open(os.path.join (folderpath,catchment+"_rffe.txt"), "w") as rffefile:
        rffefile.write(rfferesponse.text)
    
    with open (os.path.join(folderpath,catchment+"_ifd.html"),"w") as ifdfile:
        ifdfile.write (ifdresponse)

def main (lato,lono,latc,lonc,area,Name,outfolder):
    # lato, lono,latc,lonc,area,Name= -33.8783,150,-33.9607,150.752,88,'Catchment1'
    # outfolder= r'C:\Users\Animesh.Paudel\Desktop\Temp\Python training- web access'
    
    dhubresponse=fetch_datahub(lonc,latc)
    rfferesponse=fetch_rffe (lono,lato,lonc,latc,area)
    ifd=fetch_IFD(latc,lonc,Name)
    
    
    #SAVE TO FILES-----------
    save_results_to_files(Name, outfolder, ifd[1],dhubresponse,rfferesponse)
    
    #process results to tables
    rffe=get_rffe (rfferesponse.text)
    initialloss,preburst=get_datahub(dhubresponse)
    ifd=ifd[0]
    return rffe, initialloss,preburst,ifd
