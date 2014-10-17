
var app = angular.module('myApp', ['ngResource', 'ui.bootstrap'])
.factory("RetailItems", function($resource) {
  return $resource("/api/retailitems/:id", {}, {
    query: { method: "GET", isArray: false },
    query_approve: {method: "GET", isArray:false, params: {approve: true}},
    query_not_approve: {method: "GET", isArray:false, params: {approve: false}}
  });
});


app.controller('MainCtrl', function($scope, $modal, RetailItems) {

    $scope.open = function () {

        var modalInstance = $modal.open({
            templateUrl: 'myModalContent.html',
            //      controller: 'ModalInstanceCtrl',
            resolve: {
                items: function () {
                  return $scope.items;
                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.model = {};

    RetailItems.query({ id: INVOICE_ID }, function(data) {
        $scope.model.items = data.items;
    });

    $scope.removeFromInvoice = function(item) {
        item.is_approve = false;
    };
    $scope.addToInvoice = function(item) {
        if(!item.price_retail) {

        } else {
            item.is_approve = true;
        }

    };

    $scope.btnClick = function() {
        console.log($scope.items);
    }
});