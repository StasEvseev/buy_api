
var app = angular.module('MailApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule', 'ngTable']);

app.factory("MailItems", function($resource, Base64) {
  return $resource("/api/mail", {}, {
    query: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }},
        query_check: {method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
});

app.controller("MailMainCtrl", function($scope, MailItems, ngTableParams) {
    $scope.model = {};

    $scope.model.idSelected = null;

    $scope.setSelected = function (selected) {
       $scope.model.idSelected = selected.id;
       $scope.model.selected = selected;
    };

    $scope.goToPrice = function() {
        location.href = path_to_invoice + $scope.model.selected.invoice_id;
    };

    var loadData = function() {
        MailItems.query({}, function(data) {
            $scope.model.items = data.items;
        });
    };

    $scope.checkPost = function(event) {
        var btn = $(event.target);
        btn.button('loading');
        MailItems.query_check({}, function(data) {
            btn.button('reset');
            loadData();
        })
    };

    loadData();

    $scope.tableParams = new ngTableParams({
        page: 1,            // show first page
        count: 10,          // count per page
        sorting: {
            name: 'asc'     // initial sorting
        }
    }, {
        total: 0,           // length of data
        getData: function($defer, params) {
        }
    });

//    MailItems.query({}, function(data) {
//        $scope.model.items = data.items;
//
////        $scope.model.is_change = Boolean(_.find($scope.model.items, function(el) { return el['is_change'] }));
//    });
});

