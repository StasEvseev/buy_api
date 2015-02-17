var app = angular.module('myApp', ['ngRoute', 'ng-breadcrumbs', 'ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule', 'ngTable',
    'RestApp', 'TableHelper', 'FilterApp', 'Params', 'ModalApp', 'NumberApp', 'ngAnimate', 'GoodModule', 'ElemsModule']);

app.factory('stateService', function() {
    var GOOD = 'good';

    var state = {
        GOOD: undefined
//        MAIL: undefined,
//        INVOICE: undefined
    };
    return {
            GOOD: GOOD,
            setState: function(st) {
                state = st;
            },

            getState: function() {
                return state;
            },

            setStateAttr: function (attr, value) {
                state[attr] = value;
            },

            getStateAttr: function(attr) {
                return state[attr];
            }
    }
});

app.controller("MainCtrl", function($scope, $route, $location, $routeParams, breadcrumbs) {
    $scope.$route = $route;
    $scope.$location = $location;
    $scope.$routeParams = $routeParams;
    $scope.breadcrumbs = breadcrumbs;
})

.controller('GoodMainCtrl', function($scope, GoodItems, stateService, breadcrumbs, CommodityId) {

        $scope.breadcrumbs = breadcrumbs;
        $scope.attr = {};

        stateService.setStateAttr(stateService.GOOD, undefined);

        $scope.model = {};

        $scope.resource = GoodItems.query;

        $scope.setSelected = function (selected) {
            $scope.model.idSelected = selected.id;
            $scope.model.selected = selected;

            CommodityId.query({id:$scope.model.selected.commodity_id}, function (data) {
                $scope.model.selected.commodity = data;
                stateService.setStateAttr(stateService.GOOD, $scope.model.selected);
                $scope.$location.path("/admin/goodviewpoint/"+ $scope.model.idSelected +"/edit");
            });
        };

        $scope.reload = function(text) {
            $scope.rel(text);
        };
})

    .controller('CreateCtrl', function($scope, $location, stateService, CommodityId) {
        toEditMode(true);

        $scope.discard = function() {
            $location.path("/admin/goodviewpoint");
        };

        $scope.save = function() {
            $scope.savefnc();
        };

        $scope.successclbk = function(data) {
            console.log("SUCCESS", data);

            CommodityId.query({id:data.commodity_id}, function (commodity) {
                data.commodity = commodity;
                stateService.setStateAttr(stateService.GOOD, data);
                $scope.$location.path("/admin/goodviewpoint/"+ data.id +"/edit");
            });
        };

        function toEditMode(edit) {
            $scope.disabled = !edit;
            $scope.editMode = edit;
        }
    })

    .controller('EditCtrl', function($scope, breadcrumbs, stateService, $location, CommodityId, GoodPriceParish, ngTableParams,
        load) {
        var good = stateService.getStateAttr(stateService.GOOD);

        if(!good) {
            $location.path("/admin/goodviewpoint");
            return;
        }
        breadcrumbs.options = {'Редактирование': good.full_name};

        $scope.model = {};

        var last = undefined;
        $scope.object = good;
        $scope.pricesShow = true;

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

                    params.total(data.max);
                    $defer.resolve(data.items);
                }, GoodPriceParish.query, {id: good.id}, $scope);
            }
        });

        toEditMode(false);

        $scope.edit = function() {
            toEditMode(true);
            last = $scope.object;
            $scope.object = _.clone($scope.object);
        };

        $scope.discard = function() {
            toEditMode(false);

            $scope.object = last;
        };

        $scope.save = function() {
            $scope.savefnc();
        };

        $scope.create = function() {
            $location.path("/admin/goodviewpoint/create");
        };

        $scope.successclbk = function(data) {
            console.log("SUCCESS", data);
            toEditMode(false);

            if(data.commodity_id != $scope.object.commodity.id) {
                CommodityId.query({id:data.commodity_id}, function (commodity) {
                    $scope.object = data;
                    $scope.object.commodity = commodity;
                });
            } else {
                var commodity = $scope.object.commodity;
                $scope.object = data;
                $scope.object.commodity = commodity;
            }
        };

        function toEditMode(edit) {
            $scope.disabled = !edit;
            $scope.editMode = edit;
        }
    })

    .config(function($routeProvider, $locationProvider) {
        $routeProvider
            .when('/admin/goodviewpoint', {
                templateUrl: '/static/template/good/main.html',
                controller: 'GoodMainCtrl',
                label: 'Список товаров'
            })
            .when('/admin/goodviewpoint/:id/edit', {
                templateUrl: '/static/template/good/edit.html',
                controller: 'EditCtrl',
                label: 'Редактирование'
            })
            .when('/admin/goodviewpoint/create', {
                templateUrl: '/static/template/good/edit.html',
                controller: 'CreateCtrl',
                label: 'Создание'
            })
            .otherwise({
                redirectTo: '/admin/goodvviewpoint'
            });

        // configure html5 to get links working on jsfiddle
        $locationProvider.html5Mode(true);
    });