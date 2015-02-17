var app = angular.module('AcceptanceApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule', 'ngTable', 'RestApp']);

app.controller("MainCtrl", function($scope, AcceptanceItems, ngTableParams) {
    $scope.model = {};

    $scope.model.idSelected = null;

    $scope.setSelected = function (selected) {
       $scope.model.idSelected = selected.id;
       $scope.model.selected = selected;
    };

    $scope.tableParams = new ngTableParams({
        page: 1,            // show first page
        count: 10,
        sorting: {
            date: 'desc'     // initial sorting
        }
    }, {
        total: 0,           // length of data
        getData: function($defer, params) {

            $scope.model.count = params.count();

            $scope.model.page = params.page();
            var filter = params.filter();
            var sort = params.sorting();

            $scope.model.filter_field = _.keys(filter)[0];
            $scope.model.filter_text = filter[$scope.model.filter_field];
            $scope.model.sort_field = _.keys(sort)[0];
            $scope.model.sort_course = sort[$scope.model.sort_field];

            AcceptanceItems.query({}, function(data) {
                $scope.model.items = data.items;
            });
        }
    });

    $scope.nextStep = function() {

        console.log("NEXTSTEP");
        console.log($scope.model.selected);
        location.href = path_to_acceptance + $scope.model.selected.id;
    };

});