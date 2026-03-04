# MES API 規格書

## 取得布廠主機報表資料
- API URL: /api/Spunlace/GetSPMainReport
- Method: GET
- Query Parameters:
  - table: 固定帶 TB_SP_MAIN
  - organization_code: WPN/楠梓 WPT/樹谷 WPD/同奈
  - startdate: 查詢起始日期，格式為 YYYY-MM-DD
  - enddate: 查詢結束日期，格式為 YYYY-MM-DD

- Response:
  - JSON格式
    ```
    [
        {
            "wip_entity_name": "string",
            "data": "json string"
        }
    ]
    ```
  - data欄位的json string格式如下:
    ```
{
  "ebs_workorder": {
    "assembly_item_id": 5590,
    "assembly_lot_control": 1,
    "organization_code": "WPN",
    "organization_id": 84,
    "wip_entity_name": "A00686-02",
    "wip_entity_id": 1884004,
    "wip_supply_type": 1,
    "status": "Released",
    "job_type": "STANDARD",
    "assembly_item": "53.DL538.O20",
    "description": "NDR538-F6 442.6cm",
    "class_code": "PROD",
    "schedule_start_date": "2026-01-30T16:38:46Z",
    "schedule_end_date": "2026-01-30T16:38:46Z",
    "start_quantity": 67094.016,
    "primary_uom_code": "kg",
    "primary_secondary_uom": "kg",
    "primary_secondary_qty": 67094,
    "routing": "SP03",
    "routing_desc": "製布主機 SP3 (楠梓廠)",
    "so_no": "11126010096",
    "so_line": "1.1",
    "warehouse": "NLS3",
    "quantity_completed": 0,
    "quantity_scrapped": 0,
    "component": [
      {
        "componenet_item": "36.ST85D.220",
        "component_item_id": 2244,
        "componenet_lot_control": 2,
        "componenet_description": "PET 2.0D*51mm NANYA(南亞) 無銻",
        "componenet_required_quantity": 8922.0766,
        "componenet_issue_quantity": 0,
        "componenet_primary_uom": "kg",
        "componenet_secondary_uom": "bag",
        "componenet_secondary_qty": "28.7",
        "wip_supply_type": 1
      }
    ]
  },
  "so": {},
  "order_status": "InProcess",
  "machine": "SP3",
  "own_date": "2026-02-04",
  "running_time": "00:00:00",
  "order_start_date": "2026-02-04 19:51",
  "order_end_date": "",
  "workers": "0",
  "recycleCotton": 0,
  "rebuildCotton": "570",
  "ebs_split_workorder": {
    "assembly_item_id": 6940,
    "assembly_lot_control": 2,
    "organization_code": "WPN",
    "organization_id": 84,
    "wip_entity_name": "A00686-01",
    "wip_entity_id": 1884003,
    "wip_supply_type": 1,
    "status": "Released",
    "job_type": "STANDARD",
    "assembly_item": "93.DL538.D33",
    "description": "NDR538-F6 133cm*4400M(贈30M)",
    "class_code": "PROD",
    "schedule_start_date": "2026-01-30T16:38:46Z",
    "schedule_end_date": "2026-01-30T16:38:46Z",
    "start_quantity": 42696.192,
    "primary_uom_code": "kg",
    "primary_secondary_uom": "rol",
    "primary_secondary_qty": 192,
    "routing": "SLN0",
    "routing_desc": "製布分條 (楠梓廠)",
    "so_no": "11126010096",
    "so_line": "1.1",
    "warehouse": null,
    "quantity_completed": 0,
    "quantity_scrapped": 0,
    "component": [
      {
        "componenet_item": "53.DL538.O20",
        "component_item_id": 5590,
        "componenet_lot_control": 1,
        "componenet_description": "NDR538-F6 442.6cm",
        "componenet_required_quantity": 42696.192,
        "componenet_issue_quantity": 0,
        "componenet_primary_uom": "kg",
        "componenet_secondary_uom": "kg",
        "componenet_secondary_qty": "42696.2",
        "wip_supply_type": 1
      }
    ]
  },
  "additional": [],
  "H1": [
    {
      "hopper": "H1",
      "item_name": "",
      "material": {
        "component_item": "36.SR54X.010",
        "component_description": "Rayon 1.5D*40mm Lenzing SPV(印尼)",
        "component_item_id": 2267,
        "color": "yellow"
      },
      "cotton_lot_no": "EMPTY_LOTNO",
      "BarcodeID": "P048389236-01",
      "cotton_weight": "180",
      "inout": "in",
      "date": "2026-02-04",
      "class": "晚",
      "worker": "1090202",
      "id": "1770238753452",
      "toEBS": 1,
      "recordtime": "2026-02-05 04:59"
    }
  ],
  "H2": [
    {
      "hopper": "H2",
      "item_name": "",
      "material": {
        "component_item": "36.ST85D.220",
        "component_description": "PET 2.0D*51mm NANYA(南亞) 無銻",
        "component_item_id": 2244,
        "color": "orange"
      },
      "cotton_lot_no": "EMPTY_LOTNO",
      "BarcodeID": "01315188310.0-01",
      "cotton_weight": "20",
      "inout": "in",
      "date": "2026-02-04",
      "class": "晚",
      "worker": "1090202",
      "id": "1770238754964",
      "toEBS": 1,
      "recordtime": "2026-02-05 04:59"
    }
  ],
  "H3": [
    {
      "hopper": "H3",
      "item_name": "",
      "material": {
        "component_item": "36.SR54X.010",
        "component_description": "Rayon 1.5D*40mm Lenzing SPV(印尼)",
        "component_item_id": 2267,
        "color": "purple"
      },
      "cotton_lot_no": "EMPTY_LOTNO",
      "BarcodeID": "P048390646",
      "cotton_weight": 294.655,
      "inout": "in",
      "date": "2026-02-04",
      "class": "晚",
      "worker": "1090202",
      "id": "1770241237970",
      "toEBS": 1,
      "recordtime": "2026-02-05 05:40"
    }
  ],
  "H4": [
    {
      "hopper": "H4",
      "item_name": "",
      "material": {
        "component_item": "36.ST43D.220",
        "component_description": "PET 1.4D*38mm NANYA(南亞) 無銻",
        "component_item_id": 2255,
        "color": "gray"
      },
      "cotton_lot_no": "EMPTY_LOTNO",
      "BarcodeID": "01365010310.0-01",
      "cotton_weight": "60",
      "inout": "in",
      "date": "2026-02-04",
      "class": "晚",
      "worker": "1090202",
      "id": "1770238756308",
      "toEBS": 1,
      "recordtime": "2026-02-05 04:59"
    }
  ],
  "H5": [
    {
      "hopper": "H5",
      "item_name": "",
      "material": {
        "component_item": "36.SR54X.010",
        "component_description": "Rayon 1.5D*40mm Lenzing SPV(印尼)",
        "component_item_id": 2267,
        "color": "yellow"
      },
      "cotton_lot_no": "EMPTY_LOTNO",
      "BarcodeID": "P048387586-01",
      "cotton_weight": "180",
      "inout": "in",
      "date": "2026-02-04",
      "class": "晚",
      "worker": "1090202",
      "id": "1770238757724",
      "toEBS": 1,
      "recordtime": "2026-02-05 04:59"
    }
  ],
  "BOX": [],
  "output": [
    {
      "item_number": "53.DL538.O20",
      "description": "NDR538-F6 442.6cm",
      "subinventory": "NLS3",
      "class": "晚",
      "own_date": "2026-02-06",
      "worker": "1120802",
      "hand": "2",
      "meter": "0",
      "type": "Jumbo",
      "lotno": "3G020619",
      "down_time": "2026-02-06T22:16",
      "speed": "180",
      "width": "4420",
      "total_length": "8840",
      "gross_weight": "1837",
      "axis": "3",
      "effective_width": "4180",
      "standard_meter": "8800",
      "regain": 1.02,
      "import_button_A_1": "3.10",
      "import_button_A_2": "0",
      "import_button_B_1": "3.10",
      "import_button_B_2": "0",
      "metal": "0",
      "strange": "48",
      "cotton_point": "0",
      "regain_AC_1": "0",
      "regain_AC_2": "0",
      "remark": "",
      "control_basic_weight": 37.2549,
      "real_net_weight": "1441.63465",
      "real_basic_weight": 36.93874,
      "standard_basic_weight": 38,
      "standard_net_weight": 1397.792,
      "total_net_weight": 1443.3,
      "good_length": 8830,
      "good_weight": "0",
      "scrap_length": 10,
      "scrap_weight": 1.6327,
      "initial_process_length": 0,
      "initial_process_weight": 0,
      "moisture_content": "0",
      "qc": [
        {
          "defectType": {
            "label": "品保取樣",
            "value": "AF4",
            "type": "AF",
            "hasDecay": false,
            "hasHandle": true,
            "hasNext": false,
            "hasDefectType": false
          },
          "handle": "割除",
          "length": 0,
          "length2": 10,
          "site": "Jumbo",
          "sn": 1,
          "loss": 1.6327,
          "loss_length": 10
        }
      ],
      "toEBS": 1
    },
    {
      "item_number": "53.DL538.O20",
      "description": "NDR538-F6 442.6cm",
      "subinventory": "NLS3",
      "class": "晚",
      "own_date": "2026-02-06",
      "worker": "1120802",
      "hand": "2",
      "meter": "0",
      "type": "Jumbo",
      "lotno": "3G020617",
      "down_time": "2026-02-06T20:38",
      "speed": "180",
      "width": "4425",
      "total_length": "8840",
      "gross_weight": "1864",
      "axis": "22",
      "effective_width": "4180",
      "standard_meter": "8800",
      "regain": 1.02,
      "import_button_A_1": "3.15",
      "import_button_A_2": "0",
      "import_button_B_1": "3.15",
      "import_button_B_2": "0",
      "metal": "0",
      "strange": "42",
      "cotton_point": "0",
      "regain_AC_1": "0",
      "regain_AC_2": "0",
      "remark": "",
      "control_basic_weight": 37.2549,
      "real_net_weight": 1464.04874,
      "real_basic_weight": 37.46982,
      "standard_basic_weight": 38,
      "standard_net_weight": 1397.792,
      "total_net_weight": 1465.74,
      "good_length": 8830,
      "good_weight": "0",
      "scrap_length": 10,
      "scrap_weight": 1.6581,
      "initial_process_length": 0,
      "initial_process_weight": 0,
      "moisture_content": "0",
      "qc": [
        {
          "defectType": {
            "label": "品保取樣",
            "value": "AF4",
            "type": "AF",
            "hasDecay": false,
            "hasHandle": true,
            "hasNext": false,
            "hasDefectType": false
          },
          "handle": "割除",
          "length": 0,
          "length2": 10,
          "site": "Jumbo",
          "sn": 1,
          "loss": 1.6581,
          "loss_length": 10
        }
      ],
      "toEBS": 1
    }
  ],
  "records": [
    {
      "serial_number": 2,
      "class": "晚",
      "own_date": "2026-02-04",
      "stage": "Z8",
      "illustrate": "others",
      "reason": "others",
      "start_time": "2026-02-05T04:12",
      "end_time": "2026-02-05T05:18",
      "remark": "",
      "duration": "66",
      "worker": "1031006",
      "running": true
    }
  ],
  "ebs_status": "Open",
  "ebs_salesorder": {
    "org_code": "WPN",
    "order_type_id": 1002,
    "org_id": 84,
    "order_number": 11126010096,
    "request_date": "2026/01/13",
    "schedule_ship_date": "2026/02/12",
    "ship_to_customer_name": "PIGEON MANUFACTURING IBARAKI CORPORATION(PHP-I)",
    "ship_to_customer_number": "OJP9218",
    "cust_po_number": null,
    "component": [
      {
        "so_line": "1.1",
        "so_item": "93.DL538.D33",
        "inventory_item_id": 6940,
        "description": "NDR538-F6 133cm*4400M(贈30M)",
        "ordered_quantity": 42696.192,
        "uom": "kg",
        "so_note": "每櫃最大量裝1330+1520共32捲(1330*2R+1520*1R)手",
        "customer_item_number": null
      },
      {
        "so_line": "2.1",
        "so_item": "93.DL538.F22",
        "inventory_item_id": 148146,
        "description": "NDR538-F6 152cm*4400M(贈30M)",
        "ordered_quantity": 24397.824,
        "uom": "kg",
        "so_note": "每櫃最大量裝1330+1520共32捲(1330*2R+1520*1R)手",
        "customer_item_number": null
      }
    ]
  },
  "component_list": [
    {
      "component_item": "36.ST85D.220",
      "component_description": "PET 2.0D*51mm NANYA(南亞) 無銻",
      "component_item_id": 2244,
      "color": "red"
    },
    {
      "component_item": "36.ST43D.220",
      "component_description": "PET 1.4D*38mm NANYA(南亞) 無銻",
      "component_item_id": 2255,
      "color": "green"
    },
    {
      "component_item": "36.ST25D.220",
      "component_description": "PET 1.2D*51mm NANYA(南亞) 無銻",
      "component_item_id": 2231,
      "color": "blue"
    },
    {
      "component_item": "36.ST23D.220",
      "component_description": "PET 1.2D*38mm NANYA(南亞) 無銻",
      "component_item_id": 2230,
      "color": "yellow"
    },
    {
      "component_item": "36.SR54X.010",
      "component_description": "Rayon 1.5D*40mm Lenzing SPV(印尼)",
      "component_item_id": 2267,
      "color": "purple"
    }
  ],
  "assembly_item_info": [
    {
      "ELEMENT_NAME": "產品分類",
      "ELEMENT_VALUE": "D:NDR"
    },
    {
      "ELEMENT_NAME": "產品特徵",
      "ELEMENT_VALUE": "L:-F6"
    },
    {
      "ELEMENT_NAME": "棉比",
      "ELEMENT_VALUE": "5:5"
    },
    {
      "ELEMENT_NAME": "實際棉比",
      "ELEMENT_VALUE": "50"
    },
    {
      "ELEMENT_NAME": "基重(X0)",
      "ELEMENT_VALUE": "3:3"
    },
    {
      "ELEMENT_NAME": "基重(0X)",
      "ELEMENT_VALUE": "8:8"
    },
    {
      "ELEMENT_NAME": "實際基重",
      "ELEMENT_VALUE": "38"
    },
    {
      "ELEMENT_NAME": "幅寬(XX00)",
      "ELEMENT_VALUE": "O:44"
    },
    {
      "ELEMENT_NAME": "幅寬(00XX)",
      "ELEMENT_VALUE": "2:20~29"
    },
    {
      "ELEMENT_NAME": "幅寬說明",
      "ELEMENT_VALUE": "4426"
    },
    {
      "ELEMENT_NAME": "米長",
      "ELEMENT_VALUE": "8919"
    },
    {
      "ELEMENT_NAME": "Remark",
      "ELEMENT_VALUE": "442.6cm"
    }
  ]
}
    ```