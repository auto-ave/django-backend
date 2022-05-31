import re


def getVehicleTypeFromBody(body):
    """
    Return vehicle type from body
    """
    if body == 'MPV':
        return 'SUV'
    else:
        return body

def getDataFromMotorcheckResponse(content):
    """
    Return data format
    {
        'reg': 'DK18RMO', 
        'make': 'Volkswagen', 
        'model': 'Caddy Maxi', 
        'version': 'C20 Life TDI', 
        'body': 'MPV', 
        'doors': '5', 
        'seats': '7', 
        'reg_date>2018-04-16</reg_date>': '', 
        'sale_date>0000-00-00</sale_date>': '', 
        'engine_cc': '1968', 
        'colour': 'White', 
        'fuel': 'Diesel', 
        'transmission': 'A', 
        'year_of_manufacture': '2018', 
        'tax_class': '', 
        'tax_expiry_date': '0000-00-00', 
        'NCT_expiry_date>0000-00-00</NCT_expiry_date>': '', 
        'nct_pass_date': '', 
        'no_of_owners': '1', 
        'chassis_no': 'WV2ZZZ2KZJX118127', 
        'engine_no': 'DFSD233694', 
        'co2_emissions': '132', 
        'crwExpDate': '0000-00-00'
    }
    """
    res=re.findall("<(?P<var>\S*)(?P<attr>[^/>]*)(?:(?:>(?P<val>.*?)</(?P=var)>)|(?:/>))",content)
    if len(res)>=1:
        if len(res) > 1:
            return {
                i[0]: getDataFromMotorcheckResponse(i[2]) for i in res
            }
        else:
            return {
                res[0]: getDataFromMotorcheckResponse(res[2])
            }
    else:
        return content


def getWheelTypeFromReg(reg):
    """
    Return vehicle type from reg
    """
    return 'four_wheeler'
    try:
        if len(reg) == 7:
            return 'two_wheeler'
        elif len(reg) == 8:
            return 'three_wheeler'
        elif len(reg) == 9:
            return 'four_wheeler'
        else:
            return 'Commercial'
    except:
        return 'Commercial'