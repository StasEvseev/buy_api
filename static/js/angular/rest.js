angular.module('RestApp', [])

.factory("Invoice", function($resource, Base64) {
  return $resource("/api/invoice", {}, {
    query: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') } },
    save: { method: "PUT", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') } }
  });
})

.factory("InvoiceId", function($resource, Base64) {
  return $resource("/api/invoice/:id", {id: "@id"}, {
    edit: { method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') } }
  });
})

.factory("InvoiceItems", function($resource, Base64) {
  return $resource("/api/invoice/:id/items", {}, {
    query: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') } }
  });
})

.factory("InvoiceItemsFromMail", function($resource, Base64) {
  return $resource("/api/mail/:id/items", {}, {
    query: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') } }
  });
})

.factory("AcceptanceItems", function($resource, Base64) {
  return $resource("/api/acceptance", {}, {
    query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
//    query_check: {method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("AcceptanceRemainItems", function($resource, Base64) {
  return $resource("/api/acceptance/remain/:id/items", {}, {
    query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
//    query_check: {method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("AcceptanceIdItems", function($resource, Base64) {
  return $resource("/api/acceptance/:id/items", {}, {
    query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
//    query_check: {method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("AcceptanceId", function($resource, Base64) {
  return $resource("/api/acceptance/:id", {id: "@id"}, {
      get: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
    query: { method: "POST", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
//    query_check: {method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("AcceptanceInvoiceItem", function($resource, Base64) {
  return $resource("/api/acceptance/pointsale/:point_id/invoice/:id", {id: "@id", point_id: "@point_id"}, {
    query: { method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') } }
  });
})

.factory("AcceptanceInvoiceInvoiceItem", function($resource, Base64) {
  return $resource("/api/acceptance/:acc_id/invoice/:id/items", {id: "@id", acc_id: "@acc_id"}, {
    query: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') } }
  });
})

.factory("CommodityId", function($resource, Base64) {
    return $resource("/api/commodity/:id", {id: "@id"}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
        update: { method: "POST", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("CommodityItems", function($resource, Base64) {
    return $resource("/api/commodity", {}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
        save: {method: "PUT", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("GoodItems", function($resource, Base64) {
    return $resource("/api/good", {}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
        save: { method: "PUT", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("GoodItem", function($resource, Base64) {
    return $resource("/api/good/:id", {id: "@id"}, {
        get: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
        update: { method: "POST", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("GoodPriceParish", function($resource, Base64) {
    return $resource("/api/good/:id/priceparish", {id: "@id"}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
//        update: { method: "POST", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("PointSaleItems", function($resource, Base64) {
    return $resource("/api/pointsale", {}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
        save: {method: "PUT", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("PointSaleItem", function($resource, Base64) {
    return $resource("/api/pointsale/:id", {id: "@id"}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
        update: { method: "POST", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("PointSaleItemItems", function($resource, Base64) {
    return $resource("/api/pointsale/:id/items", {}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("ReceiverItems", function($resource, Base64) {
    return $resource("/api/receiver", {}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("WayBill", function($resource, Base64) {
    return $resource("/api/waybill", {}, {
        query: { method: "PUT", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
        query_confirm: {method: "PUT", isArray: false, params: {confirm: true}, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("WayBillItems", function($resource, Base64) {
    return $resource("/api/waybill", {}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("WayBillItem", function($resource, Base64) {
    return $resource("/api/waybill/:id", {id: "@id"}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
        save: { method: "POST", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("WayBillItemItems", function($resource, Base64) {
    return $resource("/api/waybill/:id/items", {}, {
        query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("WayBillHelper", function ($resource, Base64) {
    return $resource("/api/waybill/check_exists", {}, {
        check: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
    });
})

.factory("MailItems", function($resource, Base64) {
  return $resource("/api/mail", {}, {
    query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
    query_check: {method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("InvoicePriceItems", function($resource, Base64) {
  return $resource("/api/invoicepriceitems/:id", {}, {
    query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("ProviderResource", function($resource, Base64) {
  return $resource("/api/provider", {}, {
    query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("PriceHelper", function($resource, Base64) {
  return $resource("/api/price/getprice", {}, {
    get: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("PriceItems", function($resource, Base64) {
  return $resource("/api/pricebulk", {}, {
    query: { method: "POST", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
});