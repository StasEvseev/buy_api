//
//var app = angular.module('MailApp', ['ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule',
//    'ngTable', 'RestApp']);
//
//app.controller("MailMainCtrl", function($scope, MailItems, ngTableParams) {
//    $scope.model = {};
//
//    $scope.model.idSelected = null;
//
//    $scope.setSelected = function (selected) {
//       $scope.model.idSelected = selected.id;
//       $scope.model.selected = selected;
//    };
//
//    $scope.goToPrice = function() {
//        location.href = path_to_invoice + $scope.model.selected.id;
//    };
//
//    var loadData = function(func_success) {
//
//        var filter_field = $scope.model.filter_field;
//        var filter_text = $scope.model.filter_text;
//        var sort_field = $scope.model.sort_field;
//        var sort_course = $scope.model.sort_course;
//        var page = $scope.model.page;
//        var count = $scope.model.count;
//
//        var attrIfDef = function(attr_name, attr, obj) {
//            if(attr) {
//                obj[attr_name] = attr;
//            }
//        };
//
//        var params = {};
//
//        attrIfDef('filter_field', filter_field, params);
//        attrIfDef('filter_text', filter_text, params);
//        attrIfDef('sort_field', sort_field, params);
//        attrIfDef('sort_course', sort_course, params);
//        attrIfDef('page', page, params);
//        attrIfDef('count', count, params);
//
//        MailItems.query(params, function(data) {
//            $scope.model.items = data.items;
//            if (func_success) {
//                func_success(data);
//            }
//        });
//    };
//
//    $scope.checkPost = function(event) {
//        var btn = $(event.target);
//        btn.button('loading');
//        MailItems.query_check({}, function(data) {
//            btn.button('reset');
//            $scope.tableParams.reload();
//        })
//    };
//
//    $scope.tableParams = new ngTableParams({
//        page: 1,            // show first page
//        count: 10,
//        sorting: {
//            date: 'desc'     // initial sorting
//        }
//    }, {
//        total: 0,           // length of data
//        getData: function($defer, params) {
//
//            $scope.model.count = params.count();
//
//            $scope.model.page = params.page();
//            var filter = params.filter();
//            var sort = params.sorting();
//
//            $scope.model.filter_field = _.keys(filter)[0];
//            $scope.model.filter_text = filter[$scope.model.filter_field];
//            $scope.model.sort_field = _.keys(sort)[0];
//            $scope.model.sort_course = sort[$scope.model.sort_field];
//
//            loadData(function(data) {
//                params.total(data.count);
//            });
//        }
//    });
//});
//
