//
//var app = angular.module('PriceApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule',
//    'NumberApp', 'RestApp']);
//
//app.controller("PriceController", function($scope, InvoicePriceItems, PriceItems) {
//    $scope.model = {};
//
//    $scope.model.invoice_id = INVOICE_ID;
//
//    $scope.savePrice = function(event) {
//        var btn = $(event.target);
//        btn.button('loading');
//        PriceItems.query({
//            'data': {
//                'items': _.filter($scope.model.items, function(el) { return el['price_retail'] || el['price_gross'] }),
//                'invoice_id': $scope.model.invoice_id
//            }
//        }, function(resp) {
//            $scope.model.is_success = true;
//            $scope.model.is_error = false;
//            btn.button('reset');
//
//        }, function(resp) {
//            $scope.model.is_success = false;
//            $scope.model.is_error = true;
//            btn.button('reset');
//        });
//    };
//
//    InvoicePriceItems.query({ id: $scope.model.invoice_id }, function(data) {
//        $scope.model.items = data.items;
//
//        $scope.model.is_change = Boolean(_.find($scope.model.items, function(el) { return el['is_change'] }));
//    });
//});