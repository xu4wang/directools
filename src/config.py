
url = "http://localhost:8055"
token = "32Qj2q_1-dBaUxxx-Z-fm1oGRmujaXVt"

src_url = "http://localhost:8055"
src_token = "32Qj2q_1-dBaUxxx-Z-fm1oGRmujaXVt"

dst_url = "https://b2b-dev-api.ksher.cn"
dst_token = "xK0kDEGxAJaSSLK2Xyjnb7IqvgNRJIdc"

flow_list = [
"Business INT FX下单",
"Business INT FX取消",
"Business INT FX确认",
"Business INT Rate Query",
"Business INT 同币种提现下单",
"Business: Rate Query",
"Business：FX下单",
"Business：FX取消",
"Business：FX确认",
"Business：Withdraw下单",
"Business：Withdraw取消",
"Business：Withdraw确认"
]

folder = "/Users/austin/Documents/coding/b2b-backend/export"

################################### No need to change below this line ######################################################

config_data = {
    "directus": {
        "url": url,
        "token": token,
        "src_url": src_url,
        "src_token": src_token,
        "dst_url": dst_url,
        "dst_token": dst_token,
        "flow_list": flow_list
    },
        "system": {
           "folder": folder,
    }
}

def get_config():
    return config_data
