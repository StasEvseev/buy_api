
var app = angular.module('PriceApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule']);

app.factory("InvoicePriceItems", function($resource, Base64) {
  return $resource("/api/invoicepriceitems/:id", {}, {
    query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
});

app.factory("PriceItems", function($resource, Base64) {
  return $resource("/api/pricebulk", {}, {
    query: { method: "POST", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
});

app.controller("PriceController", function($scope, InvoicePriceItems, PriceItems) {
    $scope.model = {};

    $scope.model.invoice_id = INVOICE_ID;

    $scope.savePrice = function(event) {
        var btn = $(event.target);
        btn.button('loading');
        PriceItems.query({
            'data': {
                'items': _.filter($scope.model.items, function(el) { return el['price_retail'] || el['price_gross'] }),
                'invoice_id': $scope.model.invoice_id
            }
        }, function(resp) {
            $scope.model.is_success = true;
            $scope.model.is_error = false;
            btn.button('reset');

        }, function(resp) {
            $scope.model.is_success = false;
            $scope.model.is_error = true;
            btn.button('reset');
        });
    };

    InvoicePriceItems.query({ id: $scope.model.invoice_id }, function(data) {
        $scope.model.items = data.items;

        $scope.model.is_change = Boolean(_.find($scope.model.items, function(el) { return el['is_change'] }));
    });
});

//OLD CODE!!!

//function idToRow(index) {
//    return "#row-item-" + index;
//}
//
//function idToInput(index) {
//    return "#price-pay-item-" + index;
//}
//
//function idToIconRemove(index) {
//    return "#icon-remove-" + index;
//}
//
//function idToIconPlus(index) {
//    return "#icon-plus-" + index;
//}
//
//function disableRow(index) {
////    if (confirm("Вы подтверждаете удаление?")) {
//
//        yesDisableConfirm(index);
//
////    }
//}
//
//function enableRow(index) {
////    if (confirm("Вы подтверждаете добавление?")) {
//
//        yesEnableConfirm(index);
//
////    }
//}
//
//function yesDisableConfirm(index) {
//    console.log(index);
//    $(idToRow(index)).addClass('warning');
//    $(idToInput(index)).attr('readonly', 'readonly');
//    $(idToIconPlus(index)).removeClass('hidden');
//    $(idToIconRemove(index)).addClass('hidden');
//}
//
//function yesEnableConfirm(index) {
//    console.log(index);
//    $(idToRow(index)).removeClass('warning');
//    $(idToInput(index)).removeAttr('readonly');
//    $(idToIconPlus(index)).addClass('hidden');
//    $(idToIconRemove(index)).removeClass('hidden');
//}
//
//function idToCommodityId(index) {
//    return "#commodity_id-item-" + index;
//}
//
//function idToNumberLocal(index) {
//    return "#number_local-item-" + index;
//}
//
//function idToNumberGlobal(index) {
//    return "#number_global-item-" + index;
//}
//
//function idToNDS(index) {
//    return "#NDS-item-" + index;
//}
//
//function idToPricePrev(index) {
//    return "#price_prev-item-" + index;
//}
//
//function idToPricePost(index) {
//    return "#price_post-item-" + index;
//}
//
//function idToPriceRetail(index) {
//    return "#price_retail-item-" + index;
//}
//
//function idToPriceGross(index) {
//    return "#price_gross-item-" + index;
//}
//
//
//function submitPrices(count) {
//
//    var res = [];
//
//    for(var i = 0; i < count; i++) {
//        var index = i + 1;
//        res.push({
//            'id': $(idToCommodityId(index)).val(),
//            'number_local': $(idToNumberLocal(index)).val(),
//            'number_global': $(idToNumberGlobal(index)).val(),
//            'NDS': $(idToNDS(index)).val(),
//            'price_prev': $(idToPricePrev(index)).val(),
//            'price_post': $(idToPricePost(index)).val(),
//            'price_retail': $(idToPriceRetail(index)).val(),
//            'price_gross': $(idToPriceGross(index)).val()
//        });
//    }
//
//
//
//    $.ajax({
//        url: '/api/pricebulk',
//        type: 'POST',
//        data: {data: JSON.stringify(res)},
//        success: function(res) {
//            if(res == 'ok') {
//                $("#alert-success").removeClass("hidden");
//                $("#alert-error").addClass("hidden");
//            }
//            console.log("SUCCESS")
//        },
//        error: function() {
//            $("#alert-success").addClass("hidden");
//            $("#alert-error").removeClass("hidden");
//            console.log("ERROR")
//        }
//    });
//
////    $.post('/api/pricebulk', res).success(function() {
////        console.log("SUCCESS")
////    }).error(function() {
////        console.log("ERROR")
////    });
//
//}