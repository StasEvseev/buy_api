
var app = angular.module('myApp', ['ngResource']);
app.controller('MainCtrl', function($scope) {
    $scope.bla = 'WORK!!!!';

    $scope.items = [
        {full_name: 'Первый товар', count: '155', price_retail: '250.0'}
    ];

    console.log($scope.items)

    $scope.btnClick = function() {
        console.log($scope.items);
    }
});