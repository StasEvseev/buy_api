var app = angular.module('myApp', ['ngRoute', 'ng-breadcrumbs', 'ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule', 'ngTable',
    'RestApp', 'TableHelper', 'FilterApp', 'Params', 'ModalApp', 'NumberApp', 'ngAnimate', 'GoodModule', "ElemsModule"]);

app.controller("MainCtrl", function($scope, $route, $location, $routeParams, breadcrumbs) {
        $scope.$route = $route;
        $scope.$location = $location;
        $scope.$routeParams = $routeParams;
        $scope.breadcrumbs = breadcrumbs;
        console.log(breadcrumbs);
    })

    .controller('AcceptanceMainCtrl', function($scope, $location, AcceptanceItems, breadcrumbs) {
        $scope.breadcrumbs = breadcrumbs;
        $scope.model = {};

        $scope.resource = AcceptanceItems.query;

        $scope.select = function (selected) {
            $location.path("/admin/acceptanceview/"+selected.id+"/edit");
        };
    })

    .controller('AcceptanceEditCtrl', function($scope, $routeParams, DateWidgetScope, AcceptanceIdItems,
                                               AcceptanceId, breadcrumbs, ProviderResource) {

        $scope.breadcrumbs = breadcrumbs;
        $scope.model = {};
        $scope.model.date = {};
        $scope.model.validate = {};
        var lastdate = undefined;
        var lastprov = undefined;
        var lstitems = undefined;

        toEditMode(false);

        $scope.acceptance_id = $routeParams.id;

        $scope.resource = ProviderResource.query;

        AcceptanceId.get({id: $scope.acceptance_id}, function(data) {
            $scope.model.selected_provider = {'id': data.provider_id, 'name': data.provider_name};
            $scope.model.date.dt = data.date;
            breadcrumbs.options = {'Редактирование': data.invoice_str};
        });

        AcceptanceIdItems.query({id: $scope.acceptance_id}, function(data) {
            $scope.model.items = data.items;
        });

        $scope.edit = function() {
            toEditMode(true);
            lastdate = $scope.model.date.dt;
            lastprov = $scope.model.selected_provider;
            lstitems = _.map($scope.model.items, _.clone);

            $scope.model.date.dt = _.clone($scope.model.date.dt);
            $scope.model.selected_provider = _.clone($scope.model.selected_provider);

        };

        $scope.discard = function() {
            toEditMode(false);
            $scope.model.date.dt = lastdate;
            $scope.model.selected_provider = lastprov;
            $scope.model.items = lstitems;
        };

        $scope.saveAcceptance = function() {
//            console.log($scope.model.selected_provider);
//            return;
            AcceptanceId.query({id: $scope.acceptance_id, data: {
                'date': $scope.model.date.dt,
                'provider_id': $scope.model.selected_provider.id,
                'items': $scope.model.items
            }}, function(data) {
                $scope.model.validate.is_error = false;
                $scope.model.validate.is_success = true;
            }, function(data) {
                $scope.model.validate.is_error = true;
                $scope.model.validate.error = data.data.message;
                $scope.model.validate.is_success = false;
            });
        };

        function toEditMode(edit) {
            $scope.disabled = !edit;
            $scope.editMode = edit;
        }
    })

    .controller('AcceptanceCreateNewCtrl', function($scope, $modal, $location, stateService, ProviderResource,
                                                    breadcrumbs, Invoice, InvoiceId) {
        $scope.breadcrumbs = breadcrumbs;
        var pointsale = stateService.getStateAttr(stateService.POINTSALE);
        var is_save = false;
        var model = undefined;

        if (!pointsale) {
            $location.path("/admin/acceptanceview/new");
            return;
        }

        console.log(pointsale);
        breadcrumbs.options = {'Создание новой приемки': 'Создание новой приемки в ' + pointsale.name};
        $scope.model = {};
        $scope.model.validate = {};
        $scope.model.date = {};
        $scope.model.items = [];

        $scope.saveInvoice = function() {

            if (is_save) {
                InvoiceId.edit({id: model.id, data: {
                    items:$scope.model.items,
                    date: $scope.model.date.dt,
                    pointsale_id: pointsale.id
                }}, function(data) {
                    $scope.model.validate.is_success = true;
                    $scope.model.validate.is_error = false;
                }, function(data) {
                    $scope.model.validate.is_success = false;
                    $scope.model.validate.is_error = true;
                    $scope.model.validate.error = data.message;
                });
            } else {
                Invoice.save({
                    data: {
                        provider_id: $scope.model.selected_provider.id,
                        items:$scope.model.items,
                        date: $scope.model.date.dt,
                        pointsale_id: pointsale.id
                    }
                }, function(data) {
                    is_save = true;
                    model = data.data;
                    console.log(data);
                    $scope.model.validate.is_success = true;
                    $scope.model.validate.is_error = false;
                }, function (data) {
                    $scope.model.validate.is_success = false;
                    $scope.model.validate.is_error = true;
                    $scope.model.validate.error = data.message;
                });
            }
        };

        /*
        * Функция удаления записи из списка (нажатие кнопки с изображение мусорки справа).
        * */
        $scope.deleteItem = function(item) {
            var index = $scope.model.items.indexOf(item);
            $scope.model.items.splice(index, 1);
        };

        $scope.editItem = function(item) {
            $scope.openToAdd(item);
        };

        /*
        * Функция нажатия кнопки "Добавить" или Щелчком на записи для редактирования.
        * */
        $scope.openToAdd = function (item) {

            var obj = item;

            var modalInstance = $modal.open({
                templateUrl: '/static/template/modalSelectGood.html',
                controller: 'AddGoodCtrl',
                size: 'lg',
                resolve: {
                    object: function() {
                        return obj;
                    }
                }
            });

            modalInstance.result.then(function (selected) {
                console.log("SELECTED", selected);
                if(obj) {
                    obj['good_id'] = selected.good.id;
                    obj['full_name'] = selected.good.full_name;
                    obj['NDS'] = selected.NDS;
                    obj['price_pre'] = selected.price_pre;
                    obj['price_post'] = selected.price_post;
                    obj['price_retail'] = selected.price_retail;
                    obj['price_gross'] = selected.price_gross;
                } else {
                    var el = selected;
                    el['good_id'] = selected.good.id;
                    el['full_name'] = selected.good.full_name;
                    el['NDS'] = selected.NDS;
                    el['price_pre'] = selected.price_pre;
                    el['price_post'] = selected.price_post;
                    el['price_retail'] = selected.price_retail;
                    el['price_gross'] = selected.price_gross;
                    $scope.model.items.push(el);
                }
            }, function () {
                console.log("THEN2");
            });
        };

        $scope.resource = ProviderResource.query;
    })
    
    .controller('AcceptanceFromMailCtrl', function ($scope, $location, $routeParams, stateService, InvoiceItems,
                                                    AcceptanceInvoiceItem, breadcrumbs) {
//        debugger
        $scope.disabled_provider = true;
        $scope.breadcrumbs = breadcrumbs;

        $scope.invoice = stateService.getStateAttr(stateService.INVOICE);
        $scope.pointsale = stateService.getStateAttr(stateService.POINTSALE);

        if (!$scope.invoice || !$scope.pointsale) {
            $location.path("/admin/acceptanceview/new");
            return
        }
        breadcrumbs.options['Оформление прихода по накладной'] = 'Оформление прихода по накладной ' + $scope.invoice.number + " в " + $scope.pointsale.name;

        $scope.model = {};
        $scope.model.errors = {};
        $scope.model.validate = {};
        $scope.model.date = {};

        $scope.invoice_id = $routeParams.id;

        $scope.model.date.dt = $scope.invoice.date;
        $scope.model.selected_provider = {'id': $scope.invoice.provider_id, 'name': $scope.invoice.provider_name};

        InvoiceItems.query({id: $scope.invoice_id}, function(data) {
            $scope.model.items = data.items;
        });

        $scope.discard = function() {
            $location.path("/admin/acceptanceview/new/select_invoice");
        };

        $scope.saveAcceptance = function() {

            $scope.model.errors.date = $scope.model.date.dt ? false : true;

            if($scope.model.errors.date) {
                return;
            }

            AcceptanceInvoiceItem.query({point_id: $scope.pointsale.id, id: $scope.invoice_id, 'data': {
                'items': $scope.model.items,
                'date': $scope.model.date.dt
            }}, function(data) {
    //            console.log(data);
                $scope.model.validate.is_error = false;
                $scope.model.validate.is_success = true;
            }, function(data) {
    //            console.log(data.data.message);
                $scope.model.validate.is_error = true;
                $scope.model.validate.error = data.data.message;
                $scope.model.validate.is_success = false;
            })
        };
        toEditMode(true);

        function toEditMode(edit) {
            $scope.disabled = !edit;
            $scope.editMode = edit;
        }
    })
    
    .controller('AcceptanceMenuCtrl', function($scope, $location, stateService, PointSaleItems, breadcrumbs) {

        $scope.breadcrumbs = breadcrumbs;

        $scope.model = {};

        $scope.resource = PointSaleItems.query;

//        PointSaleItems.query({ }, function(data) {
//            $scope.model.pointsale_items = data.items;
//        });
        $scope.next = function(point) {
            console.log($scope.model.selected_pointsale);

            stateService.setStateAttr(stateService.POINTSALE, $scope.model.selected_pointsale);
            if(point == "mail") {
                $location.path('/admin/acceptanceview/new/select_invoice');
            } else if (point == "new") {
                $location.path('/admin/acceptanceview/new/create_new');
            }

        }
    })
    .controller('AcceptanceMailCtrl', function($scope, $rootScope, $location, load, ngTableParams, stateService, Invoice, breadcrumbs) {
        $scope.breadcrumbs = breadcrumbs;

        $scope.pointsale = stateService.getStateAttr(stateService.POINTSALE);

        if (!$scope.pointsale) {
            $location.path("/admin/acceptanceview/new");
            return
        }
        breadcrumbs.options = {'Приемка из почтовой накладной': 'Приемка из почтовой накладной в ' + $scope.pointsale.name};

        $scope.model = {};

        $scope.selected = {};

        $scope.resource = Invoice.query;

        $scope.nextStep = function () {
            if ($scope.selected.is_acceptance) {
                bootbox.dialog({
                    message: "Выбранная накладная уже имеет приход. Вы можете перейти к ее редактированию или выбрать другую накладную",
                    title: "Внимание!",
                    buttons: {
                        success: {
                            label: "Выбрать другую!",
                            className: "btn-success",
                            callback: function() {
                                console.log("SUCCESS");
                            }
                        },
                        main: {
                            label: "Редактировать!",
                            className: "btn-primary",
                            callback: function() {
                                console.log("MAIN");
                                $rootScope.$apply(function() {
                                    $location.path("/admin/acceptanceview/" + $scope.selected.acceptance_id + "/edit");
                                });
                            }
                        }
                    }
                });
            } else {
                stateService.setStateAttr(stateService.INVOICE, $scope.selected);
                $location.path("/admin/acceptanceview/new/select_invoice/invoice/" + $scope.selected.id + "/acceptance");
            }
        }
    })

.factory('stateService', function() {

        var POINTSALE = 'pointsale',
            INVOICE = "invoice",
            MAIL = 'mail';

        var state = {
            POINTSALE: undefined,
            MAIL: undefined,
            INVOICE: undefined
        };
        return {
            POINTSALE: POINTSALE,
            MAIL: MAIL,
            INVOICE: INVOICE,
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
    })

.config(function($routeProvider, $locationProvider) {
  $routeProvider
      .when('/admin/acceptanceview', {
          templateUrl: '/static/template/acceptance_main.html',
          controller: 'AcceptanceMainCtrl',
          label: 'Список приемок'
      })
      .when('/admin/acceptanceview/:id/edit', {
          templateUrl: '/static/template/acceptance_edit.html',
          controller: 'AcceptanceEditCtrl',
          label: "Редактирование"
      })

      .when('/admin/acceptanceview/new/select_invoice/invoice/:id/acceptance', {
          templateUrl: '/static/template/acceptance_edit.html',
          controller: 'AcceptanceFromMailCtrl',
          label: 'Оформление прихода по накладной'
      })

      .when('/admin/acceptanceview/new', {
          templateUrl: '/static/template/acceptance_menu.html',
          controller: 'AcceptanceMenuCtrl',
          label: "Выбор точки и действия"
      })
//
      .when('/admin/acceptanceview/new/select_invoice', {
          templateUrl: '/static/template/acceptance_mail.html',
          controller: 'AcceptanceMailCtrl',
          label: 'Приемка из почтовой накладной'
      })
      .when('/admin/acceptanceview/select_waybill', {
          templateUrl: '/static/template/acceptance_waybill.html',
          controller: 'AcceptanceWaybillCtrl',
          label: 'Выбор накладной собственной'
      })

      .when('/admin/acceptanceview/new/create_new', {
          templateUrl: '/static/template/acceptance_create_new.html',
          controller: 'AcceptanceCreateNewCtrl',
          label: 'Создание новой приемки'
      })
      .otherwise({
        redirectTo: '/admin/acceptanceview'
      });


  // configure html5 to get links working on jsfiddle
  $locationProvider.html5Mode(true);
});