
var app = angular.module('myApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select'])
.factory("RetailItems", function($resource) {
  return $resource("/api/retailitems/:id", {}, {
    query: { method: "GET", isArray: false },
    query_approve: {method: "GET", isArray:false, params: {approve: true}},
    query_not_approve: {method: "GET", isArray:false, params: {approve: false}}
  });
})

.factory("CommodityItems", function($resource) {
    return $resource("/api/commodity/:id", {}, {
        query: { method: "GET", isArray: false }
//        query_approve: {method: "GET", isArray:false, params: {approve: true}},
//        query_not_approve: {method: "GET", isArray:false, params: {approve: false}}
    });

});


app.controller('MainCtrl', function($scope, $modal, RetailItems) {

    $scope.openToAdd = function () {

        var modalInstance = $modal.open({
            templateUrl: 'myModalContent.html',
            controller: 'AddToController',
            resolve: {
                items: function () {
                  return $scope.items;
                }
            }
        });

        modalInstance.result.then(function (selected) {
            console.log(selected);
            $scope.model.items.push({
                'full_name': selected.name,
                'price_retail': selected.price_retail,
                'id_price': selected.id_price,
                'id_commodity': selected.id_commodity,
                'is_approve': true
            });
            console.log("THEN1");
        }, function () {
            console.log("THEN2");
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
            bootbox.alert("Ошибка!");
        } else {
            item.is_approve = true;
        }

    };

    $scope.btnClick = function() {
        console.log($scope.items);
    };

});

app.controller('AddToController', function($scope, $modalInstance, CommodityItems) {

    $scope.model = {};

    $scope.model.selected = undefined;

    $scope.ok = function () {
        $modalInstance.close($scope.model.selected);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    CommodityItems.query({}, function(data) {
        $scope.model.commodity_items = data.items;
    });

    $scope.commodity_item = {};
});

app.filter('propsFilter', function() {
  return function(items, props) {
    var out = [];

    if (angular.isArray(items)) {
      items.forEach(function(item) {
        var itemMatches = false;

        var keys = Object.keys(props);
        for (var i = 0; i < keys.length; i++) {
          var prop = keys[i];
          var text = props[prop].toLowerCase();
          if (item[prop].toString().toLowerCase().indexOf(text) !== -1) {
            itemMatches = true;
            break;
          }
        }

        if (itemMatches) {
          out.push(item);
        }
      });
    } else {
      // Let the output be the input untouched
      out = items;
    }

    return out;
  }
});