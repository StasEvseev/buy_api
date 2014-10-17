
var app = angular.module('myApp', ['ngResource'])
.factory("RetailItems", function($resource) {
  return $resource("/api/retailitems/:id", {}, {
    query: { method: "GET", isArray: false }
  });
});


app.controller('MainCtrl', function($scope, RetailItems) {
    $scope.bla = 'WORK!!!!';

//    $scope.items = [
//        {full_name: 'Первый товар', count: '155', price_retail: '250.0'}
//    ];

//    RetailItems.query(function(data) {
//        $scope.items = data.items;
//    });

    RetailItems.get({ id: INVOICE_ID }, function(data) {
        $scope.items = data.items;
//        console.log(data);
    });

    $scope.btnClick = function() {
        console.log($scope.items);
    }
});