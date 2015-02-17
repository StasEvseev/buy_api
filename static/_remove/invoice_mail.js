var app = angular.module('InvoiceMailApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule',
    'ngTable', 'RestApp', 'TableHelper']);

app.controller("MainCtrl", function($scope, MailItems, ngTableParams, load) {
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

            load.loadData(function(data) {
               $scope.model.items = data.items;
                params.total(data.count);
            }, MailItems.query, {}, $scope);
        }
    });

    $scope.model.validate = {};

    $scope.nextStep = function() {

        console.log("NEXTSTEP");

        $scope.model.validate.is_error = !$scope.model.selected ? true : false;

        if($scope.model.validate.is_error) {
            return;
        }
        console.log($scope.model.selected);
        location.href = path_to_acceptance_from_mail.replace("%3C%3E", $scope.model.selected.id);
    };


});