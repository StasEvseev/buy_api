
var app = angular.module('myApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule', 'NumberApp', 'RestApp']);

app.controller("MainCtrl", function($scope, PointSaleItems) {
    $scope.model = {};

    PointSaleItems.query({}, function(data) {
        $scope.model.pointsale_items = data.items;
    });

    $scope.nextStep = function() {
        location.href = PATH_TO_MENU.replace("%3C%3E", $scope.model.selected_pointsale.id);
    };
//
//    $scope.saveAcceptance = function() {
////        AcceptanceInvoiceItem.query({id: INVOICE_ID, point_id: POINTSALE_ID}, function() {
//
////        })
//    };

});

