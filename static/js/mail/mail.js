var app = angular.module('myApp', ['ngRoute', 'ng-breadcrumbs', 'ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule', 'ngTable',
    'RestApp', 'TableHelper', 'FilterApp', 'Params', 'ModalApp', 'NumberApp', 'ngAnimate', 'GoodModule', 'ElemsModule']);

app.controller("MainCtrl", function($scope, $route, $location, $routeParams, breadcrumbs) {
    $scope.$route = $route;
    $scope.$location = $location;
    $scope.$routeParams = $routeParams;
    $scope.breadcrumbs = breadcrumbs;
})

    .controller('MailMainCtrl', function($scope, MailItems, $location, breadcrumbs) {
        $scope.breadcrumbs = breadcrumbs;
        $scope.resource = MailItems.query;

        $scope.setSelected = function(item) {
            $location.path("/admin/mailview/" + item.id + "/edit");
        };

        $scope.checkPost = function(event) {
            var btn = $(event.target);
            btn.button('loading');
            MailItems.query_check({}, function(data) {
                btn.button('reset');
                $scope.rel();
            })
        };

        $scope.reload = function(text) {
            $scope.rel(text);
        };
    })

    .controller("EditCtrl", function($scope, $routeParams, breadcrumbs, InvoicePriceItems, PriceItems) {
        $scope.breadcrumbs = breadcrumbs;
        $scope.model = {};

        $scope.model.invoice_id = $routeParams.id;

        $scope.savePrice = function(event) {
            var btn = $(event.target);
            btn.button('loading');
            PriceItems.query({
                'data': {
                    'items': _.filter($scope.model.items, function(el) { return el['price_retail'] || el['price_gross'] }),
                    'invoice_id': $scope.model.invoice_id
                }
            }, function(resp) {
                $scope.model.is_success = true;
                $scope.model.is_error = false;
                btn.button('reset');

            }, function(resp) {
                $scope.model.is_success = false;
                $scope.model.is_error = true;
                btn.button('reset');
            });
        };

        InvoicePriceItems.query({ id: $scope.model.invoice_id }, function(data) {
            $scope.model.items = data.items;

            $scope.model.is_change = Boolean(_.find($scope.model.items, function(el) { return el['is_change'] }));
        });
    })

    .config(function($routeProvider, $locationProvider) {
        $routeProvider
            .when('/admin/mailview', {
                templateUrl: '/static/template/mail/main.html',
                controller: 'MailMainCtrl',
                label: 'Письма'
            })
            .when('/admin/mailview/:id/edit', {
                templateUrl: '/static/template/mail/edit.html',
                controller: 'EditCtrl',
                label: 'Редактирование'
            })
            .otherwise({
                redirectTo: '/admin/mailview'
            });

        // configure html5 to get links working on jsfiddle
        $locationProvider.html5Mode(true);
    });