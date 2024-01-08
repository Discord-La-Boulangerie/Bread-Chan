import json

# Votre JSON
json_data = {
   "errors":[
      {
         "message":"CatalogNamespace/mappings: CatalogNamespace/mappings: timeout of 5000ms exceeded",
         "locations":[
            {
               "line":68,
               "column":19
            }
         ],
         "correlationId":"8403daed-933d-40d1-bf39-ce188e1f28e5",
         "serviceResponse":"{\"errorStatus\":500}",
         "stack":"None",
         "path":[
            "Catalog",
            "searchStore",
            "elements",
            0,
            "catalogNs",
            "mappings"
         ]
      },
      {
         "message":"CatalogNamespace/mappings: CatalogNamespace/mappings: timeout of 5000ms exceeded",
         "locations":[
            {
               "line":68,
               "column":19
            }
         ],
         "correlationId":"8403daed-933d-40d1-bf39-ce188e1f28e5",
         "serviceResponse":"{\"errorStatus\":500}",
         "stack":"None",
         "path":[
            "Catalog",
            "searchStore",
            "elements",
            1,
            "catalogNs",
            "mappings"
         ]
      }
   ],
   "data":{
      "Catalog":{
         "searchStore":{
            "elements":[
               {
                  "title":"A Plague Tale: Innocence",
                  "id":"f0fd2cc8fe3048978ac407d99d81a58d",
                  "namespace":"d5241c76f178492ea1540fce45616757",
                  "description":"A Plague Tale: Innocence",
                  "effectiveDate":"2024-01-03T16:00:00.000Z",
                  "offerType":"OTHERS",
                  "expiryDate":"2024-01-04T16:00:00.000Z",
                  "viewableDate":"2024-01-02T15:25:00.000Z",
                  "status":"ACTIVE",
                  "isCodeRedemptionOnly":"true",
                  "keyImages":[
                     {
                        "type":"DieselStoreFrontWide",
                        "url":"https://cdn1.epicgames.com/offer/d5241c76f178492ea1540fce45616757/Free-Game-16_1920x1080-705a8e15d078ee00f6476491b374ff2e"
                     },
                     {
                        "type":"VaultClosed",
                        "url":"https://cdn1.epicgames.com/offer/d5241c76f178492ea1540fce45616757/Free-Game-16-teaser_1920x1080-988a5d75946464cea876eb17e4326f9f"
                     }
                  ],
                  "seller":{
                     "id":"o-ufmrk5furrrxgsp5tdngefzt5rxdcn",
                     "name":"Epic Dev Test Account"
                  },
                  "productSlug":"a-plague-tale-innocence",
                  "urlSlug":"mysterygame-16",
                  "url":"None",
                  "items":[
                     {
                        "id":"8341d7c7e4534db7848cc428aa4cbe5a",
                        "namespace":"d5241c76f178492ea1540fce45616757"
                     }
                  ],
                  "customAttributes":[
                     {
                        "key":"com.epicgames.app.freegames.vault.close",
                        "value":"[]"
                     },
                     {
                        "key":"com.epicgames.app.blacklist",
                        "value":"[]"
                     },
                     {
                        "key":"com.epicgames.app.freegames.vault.slug",
                        "value":"sales-and-specials/holiday-sale"
                     },
                     {
                        "key":"com.epicgames.app.freegames.vault.open",
                        "value":"[]"
                     },
                     {
                        "key":"com.epicgames.app.productSlug",
                        "value":"a-plague-tale-innocence"
                     }
                  ],
                  "categories":[
                     {
                        "path":"freegames/vaulted"
                     },
                     {
                        "path":"freegames"
                     },
                     {
                        "path":"games"
                     },
                     {
                        "path":"applications"
                     }
                  ],
                  "tags":[
                     
                  ],
                  "catalogNs":{
                     "mappings":"None"
                  },
                  "offerMappings":[
                     
                  ],
                  "price":{
                     "totalPrice":{
                        "discountPrice":0,
                        "originalPrice":0,
                        "voucherDiscount":0,
                        "discount":0,
                        "currencyCode":"USD",
                        "currencyInfo":{
                           "decimals":2
                        },
                        "fmtPrice":{
                           "originalPrice":"0",
                           "discountPrice":"0",
                           "intermediatePrice":"0"
                        }
                     },
                     "lineOffers":[
                        {
                           "appliedRules":[
                              
                           ]
                        }
                     ]
                  },
                  "promotions":{
                     "promotionalOffers":[
                        {
                           "promotionalOffers":[
                              {
                                 "startDate":"2024-01-03T16:00:00.000Z",
                                 "endDate":"2024-01-04T16:00:00.000Z",
                                 "discountSetting":{
                                    "discountType":"PERCENTAGE",
                                    "discountPercentage":0
                                 }
                              }
                           ]
                        }
                     ],
                     "upcomingPromotionalOffers":[
                        
                     ]
                  }
               },
               {
                  "title":"Mystery Game Day 17",
                  "id":"b8cc7e2f33f74361a241f13887508a31",
                  "namespace":"d5241c76f178492ea1540fce45616757",
                  "description":"Mystery Game Day 17",
                  "effectiveDate":"2099-01-01T16:00:00.000Z",
                  "offerType":"OTHERS",
                  "expiryDate":"None",
                  "viewableDate":"2024-01-03T15:25:00.000Z",
                  "status":"ACTIVE",
                  "isCodeRedemptionOnly":"true",
                  "keyImages":[
                     {
                        "type":"DieselStoreFrontWide",
                        "url":"https://cdn1.epicgames.com/offer/d5241c76f178492ea1540fce45616757/Free-Game-17-teaser_1920x1080-4fe4dc39667a1bbd6e61bc170adc777d"
                     },
                     {
                        "type":"VaultClosed",
                        "url":"https://cdn1.epicgames.com/offer/d5241c76f178492ea1540fce45616757/Free-Game-17-teaser_1920x1080-4fe4dc39667a1bbd6e61bc170adc777d"
                     }
                  ],
                  "seller":{
                     "id":"o-ufmrk5furrrxgsp5tdngefzt5rxdcn",
                     "name":"Epic Dev Test Account"
                  },
                  "productSlug":"[]",
                  "urlSlug":"mysterygame-17",
                  "url":"None",
                  "items":[
                     {
                        "id":"8341d7c7e4534db7848cc428aa4cbe5a",
                        "namespace":"d5241c76f178492ea1540fce45616757"
                     }
                  ],
                  "customAttributes":[
                     {
                        "key":"com.epicgames.app.freegames.vault.close",
                        "value":"[]"
                     },
                     {
                        "key":"com.epicgames.app.blacklist",
                        "value":"[]"
                     },
                     {
                        "key":"com.epicgames.app.freegames.vault.slug",
                        "value":"sales-and-specials/holiday-sale"
                     },
                     {
                        "key":"com.epicgames.app.freegames.vault.open",
                        "value":"[]"
                     },
                     {
                        "key":"com.epicgames.app.productSlug",
                        "value":"[]"
                     }
                  ],
                  "categories":[
                     {
                        "path":"freegames/vaulted"
                     },
                     {
                        "path":"freegames"
                     },
                     {
                        "path":"games"
                     },
                     {
                        "path":"applications"
                     }
                  ],
                  "tags":[
                     
                  ],
                  "catalogNs":{
                     "mappings":"None"
                  },
                  "offerMappings":[
                     
                  ],
                  "price":{
                     "totalPrice":{
                        "discountPrice":0,
                        "originalPrice":0,
                        "voucherDiscount":0,
                        "discount":0,
                        "currencyCode":"USD",
                        "currencyInfo":{
                           "decimals":2
                        },
                        "fmtPrice":{
                           "originalPrice":"0",
                           "discountPrice":"0",
                           "intermediatePrice":"0"
                        }
                     },
                     "lineOffers":[
                        {
                           "appliedRules":[
                              
                           ]
                        }
                     ]
                  },
                  "promotions":{
                     "promotionalOffers":[
                        
                     ],
                     "upcomingPromotionalOffers":[
                        {
                           "promotionalOffers":[
                              {
                                 "startDate":"2024-01-04T16:00:00.000Z",
                                 "endDate":"2024-01-11T16:00:00.000Z",
                                 "discountSetting":{
                                    "discountType":"PERCENTAGE",
                                    "discountPercentage":0
                                 }
                              }
                           ]
                        }
                     ]
                  }
               }
            ],
            "paging":{
               "count":1000,
               "total":2
            }
         }
      }
   },
   "extensions":{
      
   }
}


# Charger le JSON
parsed_json = json.loads(json_data)

# Accéder à la clé "keyImages" pour chaque élément dans "elements"
for element in parsed_json["data"]["Catalog"]["searchStore"]["elements"]:
    key_images = element.get("keyImages", [])
    for key_image in key_images:
        # Accéder aux valeurs dans la clé "keyImages"
        image_type = key_image.get("type")
        image_url = key_image.get("url")

        # Utilisez image_type et image_url comme nécessaire
        print(f"Type d'image : {image_type}, URL de l'image : {image_url}")
