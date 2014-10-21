
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

})

.factory("RetailInvoice", function($resource) {
    return $resource("/api/retail-invoice", {}, {
        query: { method: "POST", isArray: false },
        query_confirm: {method: "POST", isArray: false, params: {confirm: true}}
//        query_approve: {method: "GET", isArray:false, params: {approve: true}},
//        query_not_approve: {method: "GET", isArray:false, params: {approve: false}}
    });

});


app.controller('MainCtrl', function($scope, $modal, RetailItems, RetailInvoice) {

    $scope.model = {};

    $scope.model.invoice_id = INVOICE_ID;

    $scope.model.is_save = false;

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

    RetailItems.query({ id: $scope.model.invoice_id }, function(data) {
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

    function saveRetailInvoice(force) {
        var res = _.filter($scope.model.items, function(elem){ return elem.is_approve; });

        var method = force?'query_confirm':'query';

        RetailInvoice[method]({
            'data': {
                'invoice_id': $scope.model.invoice_id,
                'items': res
            }
        }, function(resp) {
            var path = resp['path'];
            var status = resp['status'];

            if (status == "ok") {
                $scope.model.is_save = true;
                $scope.model.url_to_download = path;
                $scope.model.is_error = false;
            } else if (status == "confirm") {
                bootbox.confirm("Внимание! Розничная накладная уже сформирована, вы хотите ее перезаписать?", function(result) {
                    if (result) {
                        saveRetailInvoice(true);
                    }
                });
            }
        }, function(resp) {
            console.log(resp);
            $scope.model.is_save = false;
            $scope.model.is_error = true;
        });
    }

    $scope.saveAndPrint = function() {
        saveRetailInvoice(false);
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