m_files_rest_url = 'https://mfiles.xxxxxxxx.com/REST/server/authenticationtokens.aspx'
auth_body = {"Username" : "*********", "Password" : "***********", "VaultGuid" : "{********-****-****-****-************}"}

auth_res = requests_post(m_files_rest_url, json=auth_body)

if auth_res.status_code == 200:
  data = auth_res.json()
  token = auth_res.json().get('Value')
  
  if token:
    not_exist_ids = []
    
    for employee in model.search([]):
      
      headers = {'X-Authentication': token}
      url = "https://mfiles.xxxxxxxx.com/REST/objects/122?p1133=" + str(employee.x_sicil_no)
      resp = requests_get(url, headers=headers).json().get('Items')
      
      try:
        birinci_yonetici = requests_get("https://mfiles.xxxxxxxx.com/REST/objects/122?p1133=" + str(employee.parent_id.x_sicil_no), headers=headers,timeout=10).json().get('Items')
        by_int_id = birinci_yonetici[0].get('ObjVer').get('ID')
      except Exception as e:
        by_int_id = False
        log("An error occured while creating or updating a partner (Birinci Yönetici): %s" % (str(e),), level='error')
      
      try:
        ikinci_yonetici = requests_get("https://mfiles.xxxxxxxx.com/REST/objects/122?p1133=" + str(employee.x_ikinci_amir_id.x_sicil_no), headers=headers,timeout=10).json().get('Items')
        iy_int_id = ikinci_yonetici[0].get('ObjVer').get('ID')
      except Exception as e:
        iy_int_id = False
        log("An error occured while creating or updating a partner (İkinci Yönetici): %s" % (str(e),), level='error')
        
      try:
        ust_birim = requests_get("https://mfiles.xxxxxxxx.com/REST/objects/262?p2973=" + str(employee.department_id.x_mfiles_id), headers=headers,timeout=10).json().get('Items')
        ub_int_id = ust_birim[0].get('ObjVer').get('ID')
      except Exception as e:
        ub_int_id = False
        log("An error occured while creating or updating a partner (Üst Birim): %s" % (str(e),), level='error')
        
      try:
        birim = requests_get("https://mfiles.xxxxxxxx.com/REST/objects/134?p2972=" + str(employee.department_id.x_m_files_birim_id), headers=headers,timeout=10).json().get('Items')
        b_int_id = ust_birim[0].get('ObjVer').get('ID')
      except Exception as e:
        b_int_id = False
        log("An error occured while creating or updating a partner (Üst Birim): %s" % (str(e),), level='error')
        
      try:
        is_gorevi = requests_get("https://mfiles.xxxxxxxx.com/REST/objects/224?p2974=" + str(employee.job_id.x_mfiles_id), headers=headers,timeout=10).json().get('Items')
        ig_int_id = is_gorevi[0].get('ObjVer').get('ID')
      except Exception as e:
        ig_int_id = False
        log("An error occured while creating or updating a partner (İş Görevi): %s" % (str(e),), level='error')
      
      if not resp:
        
        create_url = "https://mfiles.xxxxxxxx.com/REST/objects/122?checkIn=true"
    
        payload = {
          
          "PropertyValues": [
            {
              "PropertyDef": 100,
              "TypedValue": {
                "DataType": 9,
                "Lookup": {
                  "Item": 27,
                  "Version": -1
                }
              }
            },
            {
              "PropertyDef": 1133, # Sicil No
              "TypedValue": {
                "DataType": 1, # text
                "Value": str(employee.x_sicil_no) if employee.x_sicil_no else False
              }
            },
            {
              "PropertyDef": 1474, # Ad
              "TypedValue": {
                "DataType": 1, # text
                "Value": str(employee.firstname) if employee.firstname else False
              }
            },
            {
              "PropertyDef": 1475, # Soyad
              "TypedValue": {
                "DataType": 1, # text
                "Value": str(employee.lastname) if employee.lastname else False
              }
            },
            {
              "PropertyDef": 1079, # Ad Soyad
              "TypedValue": {
                "DataType": 1, # text
                "Value": str(employee.firstname) + " " + str(employee.lastname) if employee.firstname and employee.lastname else False
              }
            },
            {
              "PropertyDef": 1078, # E-Posta
              "TypedValue": {
                "DataType": 1, # text
                "Value": str(employee.work_email) if employee.work_email else False
              }
            },
            {
              "PropertyDef": 1082, # Mobil
              "TypedValue": {
                "DataType": 1, # text
                "Value": str(employee.x_work_mobil) if employee.x_work_mobil else False
              }
            },
            {
              "PropertyDef": 1472, # İşe Giriş Tarihi
              "TypedValue": {
                "DataType": 5, # date
                "Value": str(employee.start_date) if employee.start_date else False
              }
            },
            {
              "PropertyDef": 1753, # Birinci Yönetici
              "TypedValue": {
                "DataType": 9, # selection
                "Lookup": {
                  "Item": int(by_int_id)
                }
              }
            },
            {
              "PropertyDef": 1754, # İkinci Yönetici
              "TypedValue": {
                "DataType": 9, # selection
                "Lookup": {
                  "Item": int(iy_int_id)
                }
              }
            },
            {
              "PropertyDef": 2051, # Direktörlük
              "TypedValue": {
                "DataType": 9, # selection
                "Lookup": {
                  "Item": int(ub_int_id)
                }
              }
            },
            {
              "PropertyDef": 1473, # Direktörlük
              "TypedValue": {
                "DataType": 10, # selection
                "Lookups": [
                  {"Item": int(b_int_id)}
                ]
              }
            },
            {
              "PropertyDef": 1469,  # İş Pozisyonu
              "TypedValue": {
                "DataType": 9,  # selection
                "Value": int(ig_int_id)
              }
            }
          ]
        }

        try:
          resp = requests_post(create_url, json=payload, headers=headers)
          
        except Exception as e:
          log("An error occured while creating or updating a partner: %s" % (str(e),), level='error')
        
